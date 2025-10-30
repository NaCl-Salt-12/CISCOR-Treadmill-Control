from python_qt_binding.QtWidgets import QDialog
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

        # Slider setup (already configured in UI file)
        self.horizontalSlider.valueChanged.connect(self.on_slider_change)

        # Button connections
        self.pushButton.setCheckable(True)
        self.pushButton.toggled.connect(self.on_enable_toggle)
        self.pushButton_2.clicked.connect(self.on_set_speed)

        # Manual input ↔ slider sync
        self.lineEdit_manual_rpm.textChanged.connect(self.on_manual_rpm_changed)
        self.lineEdit_manual_rpm.returnPressed.connect(self.on_set_speed)

        # Init enable button state
        self.pushButton.setText("Disabled")
        self.pushButton.setStyleSheet("background-color: red; color: white; border-radius: 5px;")

        # Track last status
        self.last_status_code = None

        # Initialize slider value label
        self.sliderValueLabel.setText(f"Target: {self.horizontalSlider.value()} RPM")


    def on_slider_change(self, value):
        self.lineEdit_manual_rpm.setText(str(value))
        self.sliderValueLabel.setText(f"Target: {value} RPM")

    def on_manual_rpm_changed(self):
        text = self.lineEdit_manual_rpm.text().strip()
        try:
            rpm = int(float(text))
            rpm = max(0, min(60, rpm))
            self.horizontalSlider.blockSignals(True)
            self.horizontalSlider.setValue(rpm)
            self.horizontalSlider.blockSignals(False)
            self.sliderValueLabel.setText(f"Target: {rpm} RPM")
        except ValueError:
            pass

    def on_set_speed(self):
        manual_text = self.lineEdit_manual_rpm.text().strip()
        rpm = None

        if manual_text:
            try:
                rpm = float(manual_text)
                rpm = max(0, min(60, rpm))
            except ValueError:
                return

        if rpm is None:
            rpm = float(self.horizontalSlider.value())

        self.rpm_pub.publish(Float32(data=rpm))
        self.sliderValueLabel.setText(f"Target: {int(rpm)} RPM")

    def on_enable_toggle(self, checked):
        self.run_pub.publish(Bool(data=checked))
        if checked:
            self.pushButton.setText("Enabled")
            self.pushButton.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
        else:
            self.pushButton.setText("Disabled")
            self.pushButton.setStyleSheet("background-color: red; color: white; border-radius: 5px;")

    def update_actual_rpm(self, msg):
        self.rpmMonitor.setText(f"{msg.data:.1f} RPM")


    def update_status(self, msg):
        status_code = int(msg.data)
        description = self.decode_status_word(status_code)
        self.statusMonitor.setText(f"{description}")


    def decode_status_word(self, code):
        status_map = {
            0: "Ready",
            1: "Run",
            2: "Undervoltage",
            3: "Fault",
            4: "Self-Tuning",
            5: "Configuration",
            6: "DC-Braking",
            7: "STO"
        }
        return status_map.get(code, f"Unknown ({code})")
