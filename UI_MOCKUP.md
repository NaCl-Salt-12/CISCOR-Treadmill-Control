# CFW-11 Treadmill Controller - UI Mockup

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      CFW-11 Treadmill Controller                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─ Connection Status ──────────────────────────────────────────────────┐ │
│  │  Connection:  [ Connected ✓ ]                                        │ │
│  │               (Green background)                                      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─ Status Monitor ─────────────────────────────────────────────────────┐ │
│  │  Drive Status:  [ Running ]     Current Speed: [ 45.2 RPM ]          │ │
│  │                 (Green bg)                      (Blue border)         │ │
│  │                                                                       │ │
│  │  Target Speed:  [ 45.0 RPM ]    Difference:    [ 0.2 RPM ]           │ │
│  │                 (Gray border)                   (Green border)        │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─ Speed Control ──────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │  Quick Presets:  [ 10 ] [ 20 ] [ 30 ] [ 40 ] [ 50 ]                  │ │
│  │                  (Gray buttons, hover -> blue)                        │ │
│  │                                                                       │ │
│  │  0                    Adjust: 45 RPM                           60     │ │
│  │  ├──────────────────────●──────────────────────────────────────┤      │ │
│  │  │    Slider with tick marks every 10 RPM                     │      │ │
│  │                                                                       │ │
│  │  Fine Adjust: [ 45.0          ] [ + ] [ - ]                          │ │
│  │               (Text input)      (Inc) (Dec)                          │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─ Motor Controls ─────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │  [ Motor Enabled              ] [ ⚠ EMERGENCY STOP ]                 │ │
│  │  (Large green button)            (Large red button, thick border)    │ │
│  │                                                                       │ │
│  │  Keyboard: Space=Enable/Disable | ESC=Emergency Stop | Ctrl++/-=...  │ │
│  │  (Gray italic text)                                                  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

Window Size: 600x550 pixels
```

## Color Scheme

### Status Colors
- **Connection**
  - Connected: Green (#28a745)
  - Disconnected: Red (#dc3545)

- **Drive Status**
  - Ready: Light Green (#90EE90)
  - Running: Green (#28a745)
  - Undervoltage: Yellow (#ffc107)
  - Fault: Red (#dc3545)
  - Self-Tuning: Cyan (#17a2b8)
  - Configuration: Gray (#6c757d)
  - DC-Braking: Orange (#fd7e14)
  - STO: Red (#dc3545)

- **Speed Difference**
  - < 2 RPM: Green (#28a745)
  - 2-5 RPM: Yellow (#ffc107)
  - > 5 RPM: Red (#dc3545)

### Button Colors
- **Enable Motor**
  - Disabled state: Red (#dc3545)
  - Enabled state: Green (#28a745)
  
- **Emergency Stop**: Bright Red (#dc3545) with thick border (#c82333)
- **Preset Buttons**: Light Gray (#e9ecef), hover Blue (#0078d4)
- **Inc/Dec Buttons**: Light Gray (#e9ecef), hover Blue (#0078d4)

## UI Element Sizes
- Main buttons: 50px height
- Preset buttons: 30px height, 50px width
- Inc/Dec buttons: 25px height, 30px width
- Window: 600x550 pixels
- Margins: 20px
- Spacing: 12px between groups

## Interactive Features

### Tooltips (appear on hover)
- Slider: "Drag to adjust speed (auto-applies when motor is enabled)"
- Presets: "Set speed to X RPM"
- Enable: "Start/Stop the motor (Space bar)"
- E-Stop: "Immediately stop the motor (ESC key)"
- Inc/Dec: "Increase/Decrease speed by 1 RPM (Ctrl+±)"
- Fine Adjust: "Enter exact RPM value and press Enter to apply"

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| Space | Toggle motor enable/disable |
| ESC | Emergency stop (with confirmation) |
| Ctrl++ | Increment speed by 1 RPM |
| Ctrl+- | Decrement speed by 1 RPM |
| Enter | Apply manually entered speed |

## User Flow

### Starting the Motor
1. Set desired speed using:
   - Preset button (one click), OR
   - Slider (drag to position), OR
   - Fine Adjust input (type exact value + Enter)
2. Press "Motor Disabled" button (or Space key)
3. Button turns green and shows "Motor Enabled"
4. Motor starts at target speed
5. Watch Current Speed approach Target Speed
6. Difference indicator shows how close you are

### Adjusting Speed While Running
1. Move slider to new position
   - Speed auto-applies (no button needed!)
2. OR click preset button
   - Speed auto-applies
3. OR use +/- buttons for 1 RPM adjustments
   - Each click auto-applies
4. OR type exact value and press Enter

### Stopping the Motor
**Normal Stop:**
- Press "Motor Enabled" button (or Space key)
- Motor stops, button turns red

**Emergency Stop:**
- Press "⚠ EMERGENCY STOP" button (or ESC key)
- Confirmation dialog appears
- Click "Yes" to confirm
- Motor stops immediately and speed resets to 0

## Advantages Over Previous UI

### Before (Old UI)
- Simple slider + manual input
- Separate "Set Speed" button required
- Basic enable toggle
- No presets
- No keyboard shortcuts
- No connection monitoring
- No speed difference display
- Basic status display (white background)

### After (New UI)
- ✅ 5 preset buttons for quick access
- ✅ Auto-apply speed changes (no extra button)
- ✅ Emergency stop with confirmation
- ✅ Full keyboard shortcut support
- ✅ Connection status monitoring
- ✅ Target vs Actual speed comparison
- ✅ Color-coded status displays
- ✅ Inc/Dec buttons for fine control
- ✅ Comprehensive tooltips
- ✅ Help text for shortcuts
- ✅ Better visual hierarchy
- ✅ Larger, clearer buttons
