from python_qt_binding.QtWidgets import QDialog, QMessageBox
from python_qt_binding.QtCore import Qt, QTimer
from python_qt_binding.QtGui import QKeySequence, QShortcut
from python_qt_binding import loadUi
from std_msgs.msg import Float32, Bool
from pathlib import Path
from ament_index_python.packages import get_package_share_directory


class CFW11GUI(QDialog):
    def __init__(self, node):
        super().__init__()
        self.node = node

        ui_file = Path(
            get_package_share_directory('rqt_cfw11_gui')
        ) / 'resource' / 'MyPlugin.ui'
        loadUi(str(ui_file), self)

        # Publishers
        self.rpm_pub = node.create_publisher(Float32, 'cfw11/set_rpm', 10)
        self.run_pub = node.create_publisher(Bool, 'cfw11/run', 10)

        # Subscribers
        node.create_subscription(Float32, 'cfw11/actual_rpm', self.update_actual_rpm, 10)
        node.create_subscription(Float32, 'cfw11/status', self.update_status, 10)

        # Track current and target RPM
        self.current_rpm = 0.0
        self.target_rpm = 0.0
        self.is_enabled = False
        self.last_status_code = None
        self.connection_ok = False

        # Slider setup
        self.horizontalSlider.valueChanged.connect(self.on_slider_change)

        # Button connections
        self.pushButton.setCheckable(True)
        self.pushButton.toggled.connect(self.on_enable_toggle)
        self.emergencyStopButton.clicked.connect(self.on_emergency_stop)

        # Preset buttons
        self.preset10Button.clicked.connect(lambda: self.set_preset_speed(10))
        self.preset20Button.clicked.connect(lambda: self.set_preset_speed(20))
        self.preset30Button.clicked.connect(lambda: self.set_preset_speed(30))
        self.preset40Button.clicked.connect(lambda: self.set_preset_speed(40))
        self.preset50Button.clicked.connect(lambda: self.set_preset_speed(50))

        # Increment/Decrement buttons
        self.incrementButton.clicked.connect(self.increment_speed)
        self.decrementButton.clicked.connect(self.decrement_speed)

        # Manual input ↔ slider sync
        self.lineEdit_manual_rpm.textChanged.connect(self.on_manual_rpm_changed)
        self.lineEdit_manual_rpm.returnPressed.connect(self.apply_manual_speed)

        # Keyboard shortcuts
        self.setup_shortcuts()

        # Initialize button state
        self.pushButton.setText("Motor Disabled")
        self.pushButton.setStyleSheet(
            "QPushButton { background-color: #dc3545; color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: #c82333; }"
        )

        # Initialize displays
        self.sliderValueLabel.setText(f"Adjust: {self.horizontalSlider.value()} RPM")
        self.targetMonitor.setText(f"{self.target_rpm:.1f} RPM")
        self.deltaMonitor.setText("0.0 RPM")

        # Connection status timer
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection_status)
        self.connection_timer.start(2000)  # Check every 2 seconds
        self.last_update_time = node.get_clock().now()

    def setup_shortcuts(self):
        """Set up keyboard shortcuts for better user experience."""
        # Space bar - Enable/Disable
        self.space_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.space_shortcut.activated.connect(self.toggle_motor)

        # ESC - Emergency Stop
        self.esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.esc_shortcut.activated.connect(self.on_emergency_stop)

        # Ctrl++ - Increment
        self.plus_shortcut = QShortcut(QKeySequence("Ctrl++"), self)
        self.plus_shortcut.activated.connect(self.increment_speed)

        # Ctrl+- - Decrement
        self.minus_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
        self.minus_shortcut.activated.connect(self.decrement_speed)

    def toggle_motor(self):
        """Toggle motor enable state."""
        if not self.lineEdit_manual_rpm.hasFocus():
            self.pushButton.setChecked(not self.pushButton.isChecked())

    def check_connection_status(self):
        """Check if we're receiving updates from the backend."""
        time_since_update = (self.node.get_clock().now() - self.last_update_time).nanoseconds / 1e9
        
        if time_since_update > 3.0:  # No update for 3 seconds
            self.connection_ok = False
            self.connectionStatus.setText("Disconnected")
            self.connectionStatus.setStyleSheet(
                "background-color: #dc3545; color: white; padding: 5px; border-radius: 3px;"
            )
        else:
            if not self.connection_ok:
                self.connection_ok = True
                self.connectionStatus.setText("Connected")
                self.connectionStatus.setStyleSheet(
                    "background-color: #28a745; color: white; padding: 5px; border-radius: 3px;"
                )

    def on_slider_change(self, value):
        """Handle slider value changes - auto-apply speed."""
        self.lineEdit_manual_rpm.setText(str(value))
        self.sliderValueLabel.setText(f"Adjust: {value} RPM")
        self.target_rpm = float(value)
        self.targetMonitor.setText(f"{self.target_rpm:.1f} RPM")
        self.update_delta_display()
        
        # Auto-apply if motor is enabled
        if self.is_enabled:
            self.send_rpm_command(float(value))

    def on_manual_rpm_changed(self):
        """Sync manual input with slider."""
        text = self.lineEdit_manual_rpm.text().strip()
        try:
            rpm = int(float(text))
            rpm = max(0, min(60, rpm))
            self.horizontalSlider.blockSignals(True)
            self.horizontalSlider.setValue(rpm)
            self.horizontalSlider.blockSignals(False)
            self.sliderValueLabel.setText(f"Adjust: {rpm} RPM")
        except ValueError:
            pass

    def apply_manual_speed(self):
        """Apply manually entered speed."""
        manual_text = self.lineEdit_manual_rpm.text().strip()
        
        if not manual_text:
            return
            
        try:
            rpm = float(manual_text)
            rpm = max(0, min(60, rpm))
            self.target_rpm = rpm
            self.targetMonitor.setText(f"{self.target_rpm:.1f} RPM")
            self.update_delta_display()
            self.send_rpm_command(rpm)
        except ValueError:
            self.node.get_logger().warn(f"Invalid RPM value: {manual_text}")

    def set_preset_speed(self, rpm):
        """Set a preset speed value."""
        self.horizontalSlider.setValue(rpm)
        self.target_rpm = float(rpm)
        self.targetMonitor.setText(f"{self.target_rpm:.1f} RPM")
        self.update_delta_display()
        
        # Auto-apply if motor is enabled
        if self.is_enabled:
            self.send_rpm_command(float(rpm))

    def increment_speed(self):
        """Increment speed by 1 RPM."""
        current_value = self.horizontalSlider.value()
        new_value = min(60, current_value + 1)
        self.horizontalSlider.setValue(new_value)

    def decrement_speed(self):
        """Decrement speed by 1 RPM."""
        current_value = self.horizontalSlider.value()
        new_value = max(0, current_value - 1)
        self.horizontalSlider.setValue(new_value)

    def send_rpm_command(self, rpm):
        """Send RPM command to backend."""
        self.rpm_pub.publish(Float32(data=rpm))
        self.node.get_logger().info(f"Set target speed to {rpm:.1f} RPM")

    def on_enable_toggle(self, checked):
        """Handle enable/disable toggle."""
        self.is_enabled = checked
        self.run_pub.publish(Bool(data=checked))
        
        if checked:
            self.pushButton.setText("Motor Enabled")
            self.pushButton.setStyleSheet(
                "QPushButton { background-color: #28a745; color: white; border-radius: 5px; }"
                "QPushButton:hover { background-color: #218838; }"
            )
            # Send current target speed when enabling
            self.send_rpm_command(self.target_rpm)
        else:
            self.pushButton.setText("Motor Disabled")
            self.pushButton.setStyleSheet(
                "QPushButton { background-color: #dc3545; color: white; border-radius: 5px; }"
                "QPushButton:hover { background-color: #c82333; }"
            )

    def on_emergency_stop(self):
        """Handle emergency stop - immediately disable motor."""
        reply = QMessageBox.question(
            self,
            'Emergency Stop',
            'Are you sure you want to perform an emergency stop?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            self.pushButton.setChecked(False)
            self.horizontalSlider.setValue(0)
            self.node.get_logger().warn("EMERGENCY STOP activated by user")

    def update_actual_rpm(self, msg):
        """Update actual RPM display."""
        self.current_rpm = msg.data
        self.rpmMonitor.setText(f"{msg.data:.1f} RPM")
        self.update_delta_display()
        self.last_update_time = self.node.get_clock().now()

    def update_delta_display(self):
        """Update the difference between target and actual RPM."""
        delta = abs(self.target_rpm - self.current_rpm)
        self.deltaMonitor.setText(f"{delta:.1f} RPM")
        
        # Color-code the delta based on magnitude
        if delta < 2.0:
            color = "#28a745"  # Green - very close
        elif delta < 5.0:
            color = "#ffc107"  # Yellow - moderate difference
        else:
            color = "#dc3545"  # Red - large difference
            
        self.deltaMonitor.setStyleSheet(
            f"background-color: white; color: {color}; padding: 5px; "
            f"border: 2px solid {color}; border-radius: 3px; font-weight: bold;"
        )

    def update_status(self, msg):
        """Update drive status display."""
        status_code = int(msg.data)
        description = self.decode_status_word(status_code)
        self.statusMonitor.setText(f"{description}")
        self.last_update_time = self.node.get_clock().now()
        
        # Color-code status
        status_colors = {
            0: "#90EE90",  # Ready - light green
            1: "#28a745",  # Run - green
            2: "#ffc107",  # Undervoltage - yellow
            3: "#dc3545",  # Fault - red
            4: "#17a2b8",  # Self-Tuning - cyan
            5: "#6c757d",  # Configuration - gray
            6: "#fd7e14",  # DC-Braking - orange
            7: "#dc3545",  # STO - red
        }
        
        bg_color = status_colors.get(status_code, "#e9ecef")
        text_color = "white" if status_code in [1, 2, 3, 6, 7] else "black"
        
        self.statusMonitor.setStyleSheet(
            f"background-color: {bg_color}; color: {text_color}; "
            f"padding: 5px; border: 1px solid #ccc; border-radius: 3px;"
        )

    def decode_status_word(self, code):
        """Decode drive status code."""
        status_map = {
            0: "Ready",
            1: "Running",
            2: "Undervoltage",
            3: "Fault",
            4: "Self-Tuning",
            5: "Configuration",
            6: "DC-Braking",
            7: "STO"
        }
        return status_map.get(code, f"Unknown ({code})")
