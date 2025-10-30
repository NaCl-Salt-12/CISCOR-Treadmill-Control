# CFW11 ROS 2 Controller

This is a a ROS 2 RQt plugin GUI for controlling and monitoring a WEG CFW-11 motor controller via Modbus RTU (RS-485).

This plugin provides an intuitive graphical interface for setting RPM, starting/stopping the motor, and monitoring live RPM feedback. It interfaces with a ROS 2 backend node that communicates with the drive using pymodbus over a USB-to-RS485 adapter.

---

## Features

- Interactive slider to control motor RPM
- Start/Stop toggle button with visual status feedback
- ROS 2 integration with real-time topic communication
- Compatible with RQt on ROS 2 Jazzy

---

## Requirements

- ROS 2 (tested with Humble or Jazzy)
- Python 3.10+
- [pymodbus](https://github.com/pymodbus-dev/pymodbus)
- USB-RS485 adapter

## Installation

1. Clone the repository into the src directory of your ROS 2 workspace:

```bash
cd ~/treadmill/src  #change treadmill to your actual ros2ws
git clone https://github.com/wangykev/CISCOR-projects.git
```


## How to Run

## Start the backend ROS 2 node that communicates with the CFW-11 over RS-485:
make sure the RS485 USB is plugged in. 

```bash
cd ~/treadmill #change treadmill to your actual ros2ws
source /opt/ros/jazzy/setup.bash  # or humble
colcon build
source install/setup.bash

ros2 run cfw11_ros2_control treadmill_node
```

If you get "No response received after 3 retries, continue with next request" please check all the wires are plugged in correctly. 

## Starting the GUI

Make sure to open a new terminal then run:
```bash
cd ~/treadmill #change treadmill to your actual ros2ws
colcon build --packages-select rqt_cfw11_gui
source install/setup.bash
rqt
```
In the RQt menu, go to:

Plugins → cfw11_gui → CFW11 Plugin

You should now see the GUI with:
- A horizontal slider for RPM
- A Start/Stop toggle button
- A live RPM display


## How to Use

### User Interface Overview

The improved UI provides intuitive control with the following features:

#### Connection Status
- **Connection Status Indicator**: Shows whether the GUI is connected to the backend node
  - Green: Connected and receiving updates
  - Red: Disconnected (no updates from backend)

#### Status Monitor
- **Drive Status**: Color-coded display showing the current state of the motor drive
  - Green: Ready/Running
  - Yellow: Undervoltage
  - Red: Fault/STO
  - Other colors for Configuration, Self-Tuning, DC-Braking
- **Current Speed**: Live RPM reading from the motor (blue border)
- **Target Speed**: Your desired RPM setting (gray border)
- **Difference**: Shows how far the actual speed is from target
  - Green border: Very close (< 2 RPM difference)
  - Yellow border: Moderate difference (2-5 RPM)
  - Red border: Large difference (> 5 RPM)

#### Speed Control
- **Quick Presets**: One-click buttons to set common speeds (10, 20, 30, 40, 50 RPM)
- **Slider**: Drag to adjust speed smoothly (0-60 RPM with tick marks every 10 RPM)
- **Fine Adjust**: Enter exact RPM values for precise control
- **Increment/Decrement (+/-)**: Fine-tune speed by 1 RPM at a time
- **Auto-Apply**: Speed changes are applied automatically when the motor is enabled (no separate "Set Speed" button needed)

#### Motor Controls
- **Enable Motor Button**: Start/stop the motor
  - Green when enabled
  - Red when disabled
- **Emergency Stop**: Immediately stops the motor with a confirmation dialog
  - Bright red color with warning symbol for high visibility

#### Keyboard Shortcuts
For faster control, use these keyboard shortcuts:
- **Space**: Toggle motor enable/disable
- **ESC**: Emergency stop (with confirmation)
- **Ctrl++**: Increment speed by 1 RPM
- **Ctrl+-**: Decrement speed by 1 RPM
- **Enter**: Apply manually entered speed (when in Fine Adjust field)

### Basic Operation
1. Ensure the backend node is running (connection indicator should be green)
2. Use the slider or preset buttons to set your desired speed
3. Press the "Enable Motor" button (or press Space) to start the motor
4. Speed changes are applied automatically while the motor is running
5. For precise control, use the Fine Adjust input or +/- buttons
6. Press "Motor Disabled" button (or Space) to stop normally
7. In case of emergency, press the red "EMERGENCY STOP" button (or ESC key)


## CFW-11 Drive Parameters (for debugging)
| Parameter |      Value       |        Description            |
| --------- | -----------------| ----------------------------- |
| P0220     | 1 (Always REM)   | Always REM mode               |
| P0222     | 9 (serial/usb)   | Speed ref from serial (P0683) |
| P0227     | 2 (serial/usb)   | Run/Stop from serial (P0682)  |


## Notes

If ros2 run fails, make sure you sourced install/setup.bash

You can also run the node directly:
./install/cfw11_ros2_control/bin/treadmill_node
