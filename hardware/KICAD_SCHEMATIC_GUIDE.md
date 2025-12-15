# KiCad Schematic Creation Guide
## ESP32-C6 Marine Sensor Board

This guide will walk you through creating the schematic from scratch in KiCad 9.0.

---

## Part 1: Setup & Power Supply (15 minutes)

### 1. Open KiCad & Create New Schematic

1. Open KiCad 9.0
2. Open your project: `hardware/mshv2/mshv2.kicad_pro`
3. Open Schematic Editor (click the schematic icon)
4. If there's an existing schematic, you can either:
   - Start fresh: File → New → Schematic
   - Or clear the current one and start over

### 2. Add Power Input Connector (J1)

**Add the symbol:**
1. Press `A` (Add Symbol) or click the "Place Symbol" button
2. Search for: `Screw_Terminal_01x02`
3. Click to place it at a comfortable position (left side, near top)
4. Press `Esc` when done

**Configure it:**
1. Hover over the symbol and press `E` (Edit)
2. Set Reference: `J1`
3. Set Value: `12V_INPUT`
4. Click OK

### 3. Add Reverse Polarity Protection Diode (D1)

**Add the symbol:**
1. Press `A`
2. Search for: `MBRS340` (or `D_Schottky` if not found)
3. Place to the right of J1
4. If needed, press `R` while placing to rotate

**Configure it:**
1. Press `E` on the diode
2. Reference: `D1`
3. Value: `MBRS340`

### 4. Add Buck Converter (U1)

**Add the symbol:**
1. Press `A`
2. Search for: `LM2596S-3.3`
3. Place to the right of D1

**Configure it:**
1. Press `E`
2. Reference: `U1`
3. Value: `LM2596S-3.3`

### 5. Add Capacitors

**For each capacitor:**
1. Press `A`
2. Search for: `C_Polarized` (for electrolytics) or `C` (for ceramic)
3. Place appropriately

**You need:**
- `C1`: 100uF/25V (input, after D1)
- `C2`: 100uF/10V (output, after U1)
- `C3`: 10uF ceramic (output)
- `C4`: 0.1uF ceramic (decoupling)

### 6. Add Power Symbols

**Add +12V symbol:**
1. Press `P` (Place Power Port)
2. Search for: `+12V`
3. Click to place at J1 pin 1
4. Press `Esc`

**Add GND symbols:**
1. Press `P`
2. Search for: `GND`
3. Place near J1 pin 2 and other ground connections
4. Repeat as needed (you'll need several)

**Add +3V3 symbol:**
1. Press `P`
2. Search for: `+3V3`
3. Place at U1 output

### 7. Wire the Power Section

**Basic wiring:**
1. Press `W` (Wire tool)
2. Click on a pin to start
3. Click on destination pin to finish
4. Press `Esc` to exit wire mode

**Wire this section:**
```
J1 Pin 1 (+) → +12V power symbol → D1 anode
D1 cathode → C1+ → U1 VIN
J1 Pin 2 (-) → GND → C1- → U1 GND
U1 VOUT → C2+ → C3+ → C4+ → +3V3 symbol
C2-, C3-, C4- → GND
```

**Tips:**
- Wires must connect pin to pin
- Use labels for nets that span long distances (we'll do this later)
- Click to create corners in wires

---

## Part 2: ESP32-C6 Core (20 minutes)

### 1. Add ESP32-C6 Module (U2)

**Add the symbol:**
1. Press `A`
2. Search for: `ESP32-C6-WROOM-1`
3. Place in center of schematic
4. Reference: `U2`
5. **Important:** Set value to `ESP32-C6-WROOM-1-N8` (this is the 8MB flash variant)

### 2. Add RESET Button Circuit

**Components needed:**
- `R_EN`: 10k resistor (pullup to EN)
- `C_EN`: 0.1uF capacitor (EN filter)
- `SW_RESET`: Momentary push button

**Add each:**
1. Press `A` → search for `SW_Push` → place
2. Reference: `SW_RESET`
3. Add resistor and capacitor

**Wire it:**
```
+3V3 → R_EN → ESP32 EN pin
ESP32 EN pin → C_EN → GND
ESP32 EN pin → SW_RESET → GND
```

**How it works:** Pressing RESET pulls EN to GND, resetting the ESP32.

### 3. Add BOOT Button Circuit

**Components:**
- `R_BOOT`: 10k resistor (pullup)
- `SW_BOOT`: Momentary push button

**Wire it:**
```
+3V3 → R_BOOT → ESP32 GPIO9 pin (BOOT)
ESP32 GPIO9 → SW_BOOT → GND
```

**How it works:** Hold BOOT while pressing RESET to enter download mode for programming.

### 4. Connect Power to ESP32

```
+3V3 → ESP32 3V3 pin
GND → ESP32 GND pin
```

### 5. Add Power Indicator LED

**Components:**
- `D_PWR`: Green LED
- `R_PWR`: 1kΩ resistor (current limiting)

**Wire it:**
```
+3V3 → R_PWR → LED anode
LED cathode → GND
```

**Tips:**
- LED symbol has anode (pin 1, triangle) and cathode (pin 2, bar)
- Rotate with `R` if needed

### 6. Add GPIO Labels (for peripherals)

**Use labels instead of long wires:**
1. Press `L` (Local Label)
2. Type label name
3. Place on ESP32 GPIO pin

**Add these labels:**
- `USB_D+` on GPIO12
- `USB_D-` on GPIO13
- `I2C_SDA` on GPIO6
- `I2C_SCL` on GPIO7
- `ADC_CH0` on GPIO0 (ADC1_CH0)
- `ADC_CH1` on GPIO1 (ADC1_CH1)
- `1WIRE_1` on GPIO2
- `RGB_LED` on GPIO15
- `STATUS_LED` on GPIO23
- `SPI_SCK` on GPIO19
- `SPI_MISO` on GPIO18
- `SPI_CS_TC` on GPIO20

---

## Part 2.5: USB-C Connector (20 minutes)

### 1. Add USB-C Connector (J_USB)

**Add the symbol:**
1. Press `A`
2. Search for: `USB_C_Receptacle_USB2.0`
3. Place near ESP32
4. Reference: `J_USB`

### 2. Add USB Data Lines

**Wire USB data to ESP32:**
```
J_USB D+ (pin A6) → Label "USB_D+"
J_USB D- (pin A7) → Label "USB_D-"
```

**Note:** The ESP32-C6 has built-in USB, no bridge chip needed!

### 3. Add CC (Configuration Channel) Resistors

**Components needed:**
- `R_CC1`: 5.1kΩ resistor
- `R_CC2`: 5.1kΩ resistor

**Wire them:**
```
J_USB CC1 (pin A5) → R_CC1 → GND
J_USB CC2 (pin B5) → R_CC2 → GND
```

**Why:** These resistors tell the USB-C power supply to provide 5V.

### 4. Add ESD Protection (Optional but Recommended)

**Component:**
- `U_ESD`: USBLC6-2SC6 (TVS diode array)

**Connections:**
```
J_USB VBUS → U_ESD pin 4 (VCC)
J_USB D- → U_ESD pin 1 (I/O1)
J_USB D+ → U_ESD pin 3 (I/O2)
U_ESD pin 2 (GND) → GND
U_ESD pin 5 (I/O1') → Label "USB_D-"
U_ESD pin 6 (I/O2') → Label "USB_D+"
```

**Why:** Protects against static discharge on USB port.

### 5. Connect USB Power

**Simple approach:**
```
J_USB VBUS → (optional diode) → +3V3 (if powering from USB)
J_USB GND → GND
```

**OR for dual power:**
- Add a diode from USB VBUS to +3V3
- Add a diode from 12V buck output to +3V3
- This allows powering from either USB or 12V input

### 6. Add USB Shield Connection

```
J_USB Shield (pin S1) → (100nF capacitor) → GND
```

**Why:** Connects shield to ground through capacitor for noise immunity.

---

## Part 2.6: RGB LED (10 minutes)

### 1. Add WS2812B RGB LED (D_RGB)

**Add the symbol:**
1. Press `A`
2. Search for: `WS2812B` or `LED_ARGB`
3. Place near ESP32
4. Reference: `D_RGB`

### 2. Add Decoupling Capacitor

**Component:**
- `C_RGB`: 0.1uF capacitor

**Wire it:**
```
+3V3 → D_RGB VDD pin
D_RGB GND pin → GND
+3V3 → C_RGB → GND (place near LED)
```

### 3. Connect Data Line

**Wire it:**
```
ESP32 GPIO15 → (optional 330Ω resistor) → D_RGB DIN pin
```

**Or use label:**
```
ESP32 GPIO15 → Label "RGB_LED"
Label "RGB_LED" → D_RGB DIN pin
```

**Optional:** Add 330Ω series resistor for signal protection.

### 4. Add Status LED (Optional)

**Simple green LED on GPIO23:**
- `D_STATUS`: Green LED
- `R_STATUS`: 330Ω resistor

```
ESP32 GPIO23 → R_STATUS → LED anode
LED cathode → GND
```

---

## Part 3: Current Clamp Signal Conditioning (30 minutes)

### For ONE Current Clamp Channel:

### 1. Add Input Connector

1. Press `A`
2. Search: `Screw_Terminal_01x02`
3. Place on left side
4. Reference: `J2`
5. Value: `CLAMP_1`

### 2. Add Signal Conditioning Components

**Components (in order):**

**Series Resistor:**
- `R_SER_1`: 1k resistor (protection)

**Voltage Divider:**
- `R_DIV1_1`: 10k resistor (top)
- `R_DIV2_1`: 20k resistor (bottom to GND)

**RC Filter:**
- `R_FILT_1`: 1k resistor
- `C_FILT_1`: 0.1uF capacitor to GND

**Op-Amp Buffer:**
- Use `MCP6004` (quad op-amp)
- Reference: `U5A` (unit A)

### 3. Wire the Signal Chain

```
J2 Pin 1 → R_SER_1 → R_DIV1_1 → [midpoint junction]
[midpoint] → R_DIV2_1 → GND
[midpoint] → R_FILT_1 → C_FILT_1 → GND
[after R_FILT_1] → U5A Pin 3 (+ input)
U5A Pin 2 (- input) → U5A Pin 1 (output) [unity gain buffer]
U5A Pin 1 → Label "ADC_CH0"
```

### 4. Add Op-Amp Power (Unit E)

**Important: MCP6004 needs power pins!**

1. Press `A`
2. Search: `MCP6004`
3. When placing, change Unit to `E` (power unit)
4. Place near op-amp circuits
5. Connect:
   - V+ → +3V3
   - V- → GND
   - Add 0.1uF decoupling capacitor between V+ and GND

---

## Part 4: SHT40 I2C Sensor (15 minutes)

### 1. Add SHT40 Sensor

1. Press `A`
2. Search: `SHT4x`
3. Place on right side
4. Reference: `U3`

### 2. Add I2C Pullup Resistors

**Components:**
- `R_SDA_PU`: 4.7k resistor
- `R_SCL_PU`: 4.7k resistor

### 3. Wire I2C Section

```
+3V3 → R_SDA_PU → Label "I2C_SDA"
+3V3 → R_SCL_PU → Label "I2C_SCL"
U3 SDA pin → Label "I2C_SDA"
U3 SCL pin → Label "I2C_SCL"
U3 VDD → +3V3
U3 VSS → GND
```

### 4. Add Decoupling Capacitor

- `C_SHT40`: 0.1uF between VDD and VSS

---

## Part 5: Finishing Up (10 minutes)

### 1. Annotate Components

1. Tools → Annotate Schematic
2. Click "Annotate"
3. This assigns final reference designators

### 2. Run Electrical Rules Check (ERC)

1. Inspect → Electrical Rules Checker
2. Click "Run ERC"
3. Fix any errors:
   - **Pin not connected**: Add wire or "No Connect" flag (`X` key)
   - **Power pin not driven**: Add PWR_FLAG (`A` → search "PWR_FLAG")
   - **Missing power pins**: Make sure all IC power pins are connected

### 3. Assign Footprints

1. Tools → Assign Footprints
2. For each component, select appropriate footprint
3. Common footprints:
   - Screw terminals: `TerminalBlock_Phoenix`
   - SMD resistors: `Resistor_SMD:R_0805`
   - SMD capacitors: `Capacitor_SMD:C_0805`
   - ESP32-C6: Should auto-assign
   - ICs: SOIC or QFN packages

### 4. Save Everything

1. File → Save (Ctrl+S)
2. Generate netlist if needed: File → Netlist

---

## Tips & Tricks

### Keyboard Shortcuts
- `A` - Add symbol
- `P` - Add power port
- `W` - Wire tool
- `L` - Local label
- `G` - Global label
- `E` - Edit properties
- `R` - Rotate (while placing)
- `M` - Move
- `C` - Copy
- `Del` - Delete
- `X` - Add no-connect flag
- `Esc` - Cancel current action

### Best Practices
1. **Use labels**: For nets that span long distances
2. **Power symbols**: Use for all power connections (cleaner than wires)
3. **Grid**: Keep everything on grid (View → Grid Settings)
4. **Organize**: Group related circuits together
5. **Reference designators**: Use logical prefixes (J=connectors, R=resistors, C=capacitors, U=ICs)

### Common Issues
- **Wires not connecting**: Make sure endpoints touch pins exactly
- **Missing symbols**: Update library tables (Preferences → Manage Symbol Libraries)
- **ERC errors**: Most common are missing power connections and unconnected pins

---

## What to Build First

**Recommended order:**
1. ✅ Power supply section (most critical)
2. ✅ ESP32-C6 core with RESET/BOOT buttons
3. ✅ Power indicator LED (green)
4. ✅ USB-C connector for programming
5. ✅ RGB LED (WS2812B)
6. ✅ Status LED (optional)
7. ✅ One current clamp channel (test the concept)
8. ✅ SHT40 I2C sensor
9. ⏭️ Add more current clamp channels (copy/paste first one)
10. ⏭️ Add DS18B20 1-Wire sensors
11. ⏭️ Add MAX31855 thermocouple interface

---

## Need Help?

If you get stuck:
1. Take a screenshot and describe the issue
2. Check the ERC report for specific errors
3. Verify all pins are connected
4. Make sure power symbols are correct (+3V3, GND)

Let me know when you complete each section and I can help with the next one!
