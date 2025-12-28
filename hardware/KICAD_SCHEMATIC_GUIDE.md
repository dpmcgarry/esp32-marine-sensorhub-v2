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

### 5a. Add Dual Power OR-ing Diode

**Add the diode:**

1. Press `A`
2. Search for: `D_Schottky`
3. Place after U1 output
4. Reference: `D_BUCK`
5. Value: `B5819W`

**This diode allows dual power from either 12V or USB without conflict.**

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

```text
J1 Pin 1 (+) → +12V power symbol → D1 anode
D1 cathode → C1+ → U1 VIN
J1 Pin 2 (-) → GND → C1- → U1 GND
U1 VOUT → C2+ → C3+ → D_BUCK cathode
D_BUCK anode → C4+ → +3V3 symbol
C2-, C3-, C4- → GND
```

**Note:** The D_BUCK diode prevents backfeeding when USB power is connected.

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

```text
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

```text
+3V3 → R_BOOT → ESP32 GPIO9 pin (BOOT)
ESP32 GPIO9 → SW_BOOT → GND
```

**How it works:** Hold BOOT while pressing RESET to enter download mode for programming.

### 4. Connect Power to ESP32

```text
+3V3 → ESP32 3V3 pin
GND → ESP32 GND pin
```

### 5. Add Power Indicator LED

**Components:**

- `D_PWR`: Green LED
- `R_PWR`: 1kΩ resistor (current limiting)

**Wire it:**

```text
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

- `USB_D-` on GPIO12
- `USB_D+` on GPIO13
- `I2C_SDA` on GPIO6
- `I2C_SCL` on GPIO7
- `ADC_CH0` on GPIO0 (ADC1_CH0) - Current Clamp 1
- `ADC_CH1` on GPIO1 (ADC1_CH1) - Current Clamp 2
- `ADC_CH2` on GPIO2 (ADC1_CH2) - Current Clamp 3
- `ADC_CH3` on GPIO3 (ADC1_CH3) - Current Clamp 4
- `ADC_CH4` on GPIO4 (ADC1_CH4) - Current Clamp 5
- `RGB_LED` on GPIO8 (WS2812B, matches DevKitC)
- `1WIRE_1` on GPIO10
- `SPI_SCK` on GPIO19 (shared by all MAX31855)
- `SPI_MISO` on GPIO18 (shared by all MAX31855)
- `SPI_CS_TC1` on GPIO20 (MAX31855 #1)
- `SPI_CS_TC2` on GPIO21 (MAX31855 #2)
- `SPI_CS_TC3` on GPIO22 (MAX31855 #3)
- `STATUS_LED` on GPIO23

**Note:** GPIO5 (ADC1_CH5) is available for future expansion (6th current clamp).

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

```text
J_USB D+ (pin A6) → Label "USB_D+"
J_USB D- (pin A7) → Label "USB_D-"
```

**Note:** The ESP32-C6 has built-in USB, no bridge chip needed!

### 3. Add CC (Configuration Channel) Resistors

**Components needed:**

- `R_CC1`: 5.1kΩ resistor
- `R_CC2`: 5.1kΩ resistor

**Wire them:**

```text
J_USB CC1 (pin A5) → R_CC1 → GND
J_USB CC2 (pin B5) → R_CC2 → GND
```

**Why:** These resistors tell the USB-C power supply to provide 5V.

### 4. Add ESD Protection (Optional but Recommended)

**Component:**

- `U_ESD`: USBLC6-2SC6 (TVS diode array)

**Connections:**

```text
J_USB VBUS → U_ESD pin 4 (VCC)
J_USB D- → U_ESD pin 1 (I/O1)
J_USB D+ → U_ESD pin 3 (I/O2)
U_ESD pin 2 (GND) → GND
U_ESD pin 5 (I/O1') → Label "USB_D-"
U_ESD pin 6 (I/O2') → Label "USB_D+"
```

**Why:** Protects against static discharge on USB port.

### 5. Add USB Power Path (Dual Power Support)

**This section creates a second power path from USB for programming/development.**

**Components needed:**

- `U_USB_REG`: AMS1117-3.3 (LDO regulator, SOT-223)
- `C_USB_IN`: 10uF ceramic capacitor (input)
- `C_USB_OUT`: 10uF ceramic capacitor (output)
- `D_USB`: B5819W Schottky diode (OR-ing diode)

**Add LDO regulator:**

1. Press `A`
2. Search for: `AMS1117-3.3`
3. Place near USB connector
4. Reference: `U_USB_REG`

**Wire the USB power path:**

```text
J_USB VBUS → C_USB_IN+ → U_USB_REG VIN
C_USB_IN- → GND
U_USB_REG VOUT → C_USB_OUT+ → D_USB cathode
C_USB_OUT- → GND
D_USB anode → +3V3 symbol (meets D_BUCK here)
U_USB_REG GND → GND
J_USB GND → GND
```

**How it works:**

- USB VBUS (5V) → AMS1117 → 3.3V → D_USB → +3V3 rail
- 12V path → LM2596S → 3.3V → D_BUCK → +3V3 rail
- Whichever voltage is higher (after diode drop) powers the board
- Typical: 12V path = 3.0V, USB path = 3.0V (both can power independently)

### 6. Add USB Shield Connection

```text
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

```text
+3V3 → D_RGB VDD pin
D_RGB GND pin → GND
+3V3 → C_RGB → GND (place near LED)
```

### 3. Connect Data Line

**Wire it:**

```text
ESP32 GPIO8 → (optional 330Ω resistor) → D_RGB DIN pin
```

**Or use label:**

```text
ESP32 GPIO8 → Label "RGB_LED"
Label "RGB_LED" → D_RGB DIN pin
```

**Optional:** Add 330Ω series resistor for signal protection.

**Note:** GPIO8 matches the ESP32-C6-DevKitC-1 RGB LED pin for consistency.

### 4. Add Status LED (Optional)

**Simple green LED on GPIO23:**

- `D_STATUS`: Green LED
- `R_STATUS`: 330Ω resistor

```text
ESP32 GPIO23 → R_STATUS → LED anode
LED cathode → GND
```

---

## Part 3: Current Clamp Signal Conditioning (45 minutes)

### Build Channels 1-5 with Op-Amp Buffers

We'll use **two MCP6004 ICs** for buffering all 5 current clamp channels:

- **U5** (MCP6004): Clamps 1-4 (all 4 op-amps used)
- **U6** (MCP6004): Clamps 5-6 (U6A for clamp 5, U6B reserved for clamp 6)

### 1. Add Input Connector (Clamp 1)

1. Press `A`
2. Search: `Screw_Terminal_01x02`
3. Place on left side
4. Reference: `J2`
5. Value: `CLAMP_1`

### 2. Add Signal Conditioning Components (Clamp 1)

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
- Reference: `U5A` (unit A of first MCP6004)

### 3. Wire the Signal Chain (Clamp 1)

```text
J2 Pin 1 → R_SER_1 → R_DIV1_1 → [midpoint junction]
[midpoint] → R_DIV2_1 → GND
[midpoint] → R_FILT_1 → C_FILT_1 → GND
[after R_FILT_1] → U5A Pin 3 (+ input)
U5A Pin 2 (- input) → U5A Pin 1 (output) [unity gain buffer]
U5A Pin 1 → Label "ADC_CH0"
J2 Pin 2 → GND
```

### 4. Add Op-Amp Power - First IC (U5E)

**Important: MCP6004 needs power pins!**

1. Press `A`
2. Search: `MCP6004`
3. When placing, change Unit to `E` (power unit)
4. Reference: `U5E`
5. Place near op-amp circuits
6. Connect:
   - V+ → +3V3
   - V- → GND
   - Add 0.1uF decoupling capacitor between V+ and GND

### 5. Add Remaining Channels 2-4 (U5B, U5C, U5D)

Repeat the same circuit for channels 2-4:

**Channel 2:**

- Connector: `J3` (CLAMP_2)
- Components: `R_SER_2`, `R_DIV1_2`, `R_DIV2_2`, `R_FILT_2`, `C_FILT_2`
- Op-amp: `U5B` → Label "ADC_CH1"

**Channel 3:**

- Connector: `J4` (CLAMP_3)
- Components: `R_SER_3`, `R_DIV1_3`, `R_DIV2_3`, `R_FILT_3`, `C_FILT_3`
- Op-amp: `U5C` → Label "ADC_CH2"

**Channel 4:**

- Connector: `J5` (CLAMP_4)
- Components: `R_SER_4`, `R_DIV1_4`, `R_DIV2_4`, `R_FILT_4`, `C_FILT_4`
- Op-amp: `U5D` → Label "ADC_CH3"

### 6. Add Second MCP6004 for Channel 5

**Add U6 (second MCP6004):**

1. Add all components for channel 5 (same as channels 1-4)
2. Connector: `J6` (CLAMP_5)
3. Components: `R_SER_5`, `R_DIV1_5`, `R_DIV2_5`, `R_FILT_5`, `C_FILT_5`
4. Op-amp: `U6A` → Label "ADC_CH4"

**Add power for second IC (U6E):**

1. Press `A`
2. Search: `MCP6004`
3. Change Unit to `E`
4. Reference: `U6E`
5. Connect:
   - V+ → +3V3
   - V- → GND
   - Add 0.1uF decoupling capacitor between V+ and GND

**Note:** U6B is reserved for future 6th clamp expansion (GPIO5/ADC1_CH5).
U6C and U6D remain unused.

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

```text
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

## Part 4.5: MAX31855 Thermocouple Amplifiers (20 minutes)

### Overview

We'll add **3× MAX31855** thermocouple amplifiers for high-temperature sensing.
All three share the SPI bus (SCK and MISO), but each has its own CS (chip select) pin.

### 1. Add First MAX31855 (U4)

1. Press `A`
2. Search: `MAX31855`
3. Place on schematic
4. Reference: `U4`

### 2. Wire First MAX31855

```text
U4 VCC → +3V3
U4 GND → GND
U4 SCK → Label "SPI_SCK"
U4 SO → Label "SPI_MISO"
U4 CS → Label "SPI_CS_TC1"
U4 T+ → J_TC1 Pin 1 (thermocouple + terminal)
U4 T- → J_TC1 Pin 2 (thermocouple - terminal)
```

### 3. Add Decoupling Capacitor

- `C_TC1`: 0.1uF ceramic
- Connect between VCC and GND (place close to MAX31855)

### 4. Add Thermocouple Connector

1. Press `A`
2. Search: `Screw_Terminal_01x02`
3. Reference: `J_TC1`
4. Value: `K_TYPE_1`

```text
J_TC1 Pin 1 → U4 T+
J_TC1 Pin 2 → U4 T-
```

### 5. Add Second MAX31855 (U7)

Repeat the same circuit for the second thermocouple:

1. Add MAX31855, Reference: `U7`
2. Add connector `J_TC2` (K_TYPE_2)
3. Add decoupling cap `C_TC2`
4. Wire:

```text
U7 VCC → +3V3
U7 GND → GND
U7 SCK → Label "SPI_SCK" (shared)
U7 SO → Label "SPI_MISO" (shared)
U7 CS → Label "SPI_CS_TC2" (GPIO21)
U7 T+ → J_TC2 Pin 1
U7 T- → J_TC2 Pin 2
```

### 6. Add Third MAX31855 (U8)

Repeat for the third thermocouple:

1. Add MAX31855, Reference: `U8`
2. Add connector `J_TC3` (K_TYPE_3)
3. Add decoupling cap `C_TC3`
4. Wire:

```text
U8 VCC → +3V3
U8 GND → GND
U8 SCK → Label "SPI_SCK" (shared)
U8 SO → Label "SPI_MISO" (shared)
U8 CS → Label "SPI_CS_TC3" (GPIO22)
U8 T+ → J_TC3 Pin 1
U8 T- → J_TC3 Pin 2
```

### Notes

- **Shared SPI bus:** SCK and MISO are shared between all MAX31855 ICs
- **Individual CS pins:** Each MAX31855 has its own chip select
- **PCB layout:** Keep thermocouple traces short and away from noisy signals
- **Thermocouple polarity:** Yellow wire = T+, Red wire = T- (standard K-type)

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

**Follow the parts in order:**

1. ✅ **COMPLETED:** Part 1 - Setup & Power Supply (J1, D1, U1, capacitors, D_BUCK, power symbols)
2. ✅ **COMPLETED:** Part 2 - ESP32-C6 Core (U2, RESET/BOOT buttons, power LED, GPIO labels)
3. ✅ **COMPLETED:** Part 2.5 - USB-C Connector (J_USB, CC resistors, ESD protection, USB power path with AMS1117 & D_USB)
4. ✅ **COMPLETED:** Part 2.6 - RGB LED (WS2812B & optional status LED)
5. ✅ **COMPLETED:** Part 3 - Current Clamp Signal Conditioning (5 channels with dual MCP6004)
6. ⏭️ **NEXT:** Part 4 - SHT40 I2C Sensor
7. ⏭️ Part 4.5 - MAX31855 Thermocouple Amplifiers (3× for high-temp sensing)
8. ⏭️ Part 5 - Finishing Up (annotate, ERC, assign footprints)
9. ⏭️ Future expansion: Add DS18B20 sensors on 1-Wire bus, 6th current clamp

---

## Need Help?

If you get stuck:

1. Take a screenshot and describe the issue
2. Check the ERC report for specific errors
3. Verify all pins are connected
4. Make sure power symbols are correct (+3V3, GND)

Let me know when you complete each section and I can help with the next one!
