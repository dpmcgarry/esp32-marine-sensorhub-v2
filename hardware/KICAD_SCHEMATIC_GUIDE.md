# KiCad Schematic Creation Guide

## ESP32-C6 Marine Sensor Board

This guide will walk you through creating the schematic from scratch in KiCad 9.0
using **hierarchical sheets** for better organization.

## Connector Design Note

**IMPORTANT:** This design uses consolidated multi-pin screw terminal blocks:

- **J_MAIN** (11-pin): 12V power + 3× DS18B20 sensors
- **J_TC** (6-pin): 3× thermocouples
- **J_CLAMP** (10-pin): 5× current clamps

This consolidated approach saves board space and reduces component count.

See [Hardware.md - Connectors Pinout Reference](../Hardware.md#connectors-pinout-reference)
for detailed pinout diagrams.

---

## Hierarchical Sheet Structure

This schematic uses hierarchical sheets to organize the design into logical,
maintainable sections:

```text
Root Sheet (Overview/Navigation)
├── Power Supply (12V→3.3V conversion, dual power OR-ing)
├── ESP32 Core (MCU, USB-C, buttons, LEDs)
├── Main Connector (J_MAIN 11-pin breakout)
├── Current Sensing (J_CLAMP + signal conditioning)
├── Temperature Sensors (SHT40 + 1-Wire interface)
└── Thermocouples (J_TC + 3× MAX31855)
```

**Benefits:**

- Logical grouping of related circuitry
- Easier navigation of complex schematics
- Cleaner signal flow with hierarchical labels
- Each sheet can be worked on independently

---

## Implementation Progress

| Part | Section                                  | Status         |
| ---- | ---------------------------------------- | -------------- |
| 0    | Setup Hierarchical Sheets                | ✅ Completed   |
| 1    | Power Supply Sheet                       | ✅ Completed   |
| 2    | ESP32 Core Sheet                         | ✅ Completed   |
| 2.5  | USB-C Connector                          | ✅ Completed   |
| 2.6  | RGB LED                                  | ✅ Completed   |
| 3    | Current Sensing Sheet                    | ✅ Completed   |
| 4    | Temperature Sensors Sheet                | ⏳ Not Started |
| 5    | Thermocouples Sheet                      | ⏳ Not Started |
| 6    | Main Connector & I/O Interface Sheet     | ⏳ Not Started |
| 7    | Finishing Up (Annotate, ERC, Footprints) | ⏳ Not Started |

**Legend:** ✅ Completed | 🚧 In Progress | ⏳ Not Started

---

## Part 0: Setup Hierarchical Sheets (20 minutes)

### 1. Open KiCad & Create Project

1. Open KiCad 9.0
2. Open your project: `hardware/mshv2/mshv2.kicad_pro`
3. Open Schematic Editor (click the schematic icon)

### 2. Set Up Root Sheet

The root sheet will contain only hierarchical sheet symbols for navigation.

1. In the schematic editor, you should see a blank sheet
2. Set the page size: File → Page Settings
   - Paper size: A4 or Letter
   - Title: "ESP32-C6 Marine Sensor Hub - Root"
   - Revision: "v1.0"
   - Company: Your name/company

### 3. Create Hierarchical Sheet Symbols

Now we'll add sheet symbols to the root sheet for each functional block.

**Add Power Supply Sheet:**

1. Press `S` or click "Add Hierarchical Sheet" button
2. Click and drag to create a rectangle (about 50mm × 30mm)
3. In the dialog:
   - Sheet name: `Power Supply`
   - Sheet file name: `power.kicad_sch`
4. Click OK

**Position:** Place near top-left of root sheet

**Note:** We'll add sheet pins later using "Import Sheet Pin" after creating
hierarchical labels inside each child sheet. This is covered in Parts 1-6.

**Add ESP32 Core Sheet:**

1. Press `S`
2. Create another rectangle
3. Sheet name: `ESP32 Core`
4. Sheet file name: `esp32.kicad_sch`

**Position:** Place to the right of Power Supply sheet

**Add Main Connector Sheet:**

1. Press `S`
2. Sheet name: `Main Connector`
3. Sheet file name: `main_connector.kicad_sch`

**Position:** Left side, below Power Supply

**Add Current Sensing Sheet:**

1. Press `S`
2. Sheet name: `Current Sensing`
3. Sheet file name: `current_sensing.kicad_sch`

**Position:** Bottom-left

**Add Temperature Sensors Sheet:**

1. Press `S`
2. Sheet name: `Temperature Sensors`
3. Sheet file name: `temperature.kicad_sch`

**Position:** Bottom-center

**Add Thermocouples Sheet:**

1. Press `S`
2. Sheet name: `Thermocouples`
3. Sheet file name: `thermocouples.kicad_sch`

**Position:** Bottom-right

### 4. Save and Continue to Part 1

**Important:** Don't worry about wiring sheet pins yet - we'll add them later
after creating hierarchical labels inside each sheet.

**Next steps:**

1. File → Save to save your root sheet
2. Proceed to **Part 1** to start building the Power Supply sheet
3. As you complete each part (1-6), you'll add hierarchical labels inside each
   child sheet
4. After adding hierarchical labels, return to root and use "Import Sheet Pin"
   to automatically create matching pins
5. Once all sheet pins are imported, you'll wire them together on the root sheet

**Wiring overview (you'll do this later):**

- Use global labels (Press `L`) for signals connecting multiple sheets
- Example: `+3V3` label connects power from Power Supply to all other sheets
- Example: `SPI_SCK` connects ESP32 Core to Thermocouples sheet

### 5. Add Title Block to Root Sheet (Optional)

1. File → Page Settings
2. Fill in title, revision, date, company
3. Add notes about the hierarchical structure if desired

### 6. What You've Accomplished

You now have:

- A root sheet with 6 hierarchical sheet symbols
- Empty child schematic files ready to be populated
- A clean organizational structure for your design

**Next:** Proceed to Part 1 to build the Power Supply sheet!

---

## Part 1: Power Supply Sheet (20 minutes)

### 1. Enter the Power Supply Hierarchical Sheet

From the root sheet:

1. Double-click on the "Power Supply" sheet symbol
2. This opens the `power.kicad_sch` file
3. You should see a blank sheet with hierarchical pins on the edges

**Note:** Hierarchical labels at the sheet boundary correspond to the pins you
defined on the root sheet.

### 2. Add Hierarchical Labels

First, add hierarchical labels that match the sheet pins:

1. Press `H` (or Insert → Hierarchical Label)
2. Add label: `+12V` - set as Input (receives from connector)
3. Add label: `GND` - set as Bidirectional
4. Add label: `+3V3` - set as Output (provides to other sheets)

**Placement tip:** Place labels on the edges where signals enter/exit this sheet.

### 3. Add Reverse Polarity Protection Diode (D1)

**Add the symbol:**

1. Press `A`
2. Search for: `MBRS340` (or `D_Schottky` if not found)
3. Place near the `+12V` hierarchical label
4. If needed, press `R` while placing to rotate

**Configure it:**

1. Press `E` on the diode
2. Reference: `D1`
3. Value: `MBRS340`

**Note:** This diode protects against reverse polarity from the 12V input, which
comes from J_MAIN via the hierarchical label.

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

### 6. Add Power Symbols (Optional for clarity)

**Note:** With hierarchical labels, power symbols are optional but can help with
readability. The hierarchical labels `+12V`, `GND`, and `+3V3` handle all
connections through the sheet boundary.

**If you want to add local power symbols for clarity:**

**Add GND symbols:**

1. Press `P` (Place Power Port)
2. Search for: `GND`
3. Place near ground connections throughout the circuit
4. Repeat as needed (you'll need several for capacitor negatives, U1 GND, etc.)

**Note:** These GND symbols are connected to the `GND` hierarchical label, which
connects through the root sheet to all other sheets.

### 7. Wire the Power Section

**Basic wiring:**

1. Press `W` (Wire tool)
2. Click on a pin to start
3. Click on destination pin to finish
4. Press `Esc` to exit wire mode

**Wire this section:**

```text
Hierarchical Label "+12V" → D1 anode (receives 12V from Main Connector sheet)
D1 cathode → C1+ → U1 VIN
Hierarchical Label "GND" → C1- → U1 GND
U1 VOUT → C2+ → C3+ → D_BUCK cathode
D_BUCK anode → C4+ → Hierarchical Label "+3V3" (outputs to other sheets)
C2-, C3-, C4- → GND
```

**Notes:**

- The D_BUCK diode prevents backfeeding when USB power is connected
- The +12V comes from the Main Connector sheet via the root sheet
- The +3V3 output goes to all other sheets via the root sheet

**Tips:**

- Wires must connect pin to pin
- Use hierarchical labels (`H`) for signals that cross sheet boundaries
- Use local labels (`L`) for internal nets within the sheet
- Click to create corners in wires

### 8. Navigating Between Hierarchical Sheets

**To return to root sheet:**

- Click the "Up" arrow button in toolbar
- Or: View → Navigate → Up in Hierarchy

**To enter a different sheet:**

- Return to root, then double-click another sheet symbol
- Or: Use the hierarchy navigator (View → Hierarchy Navigator)

### 9. Import Sheet Pins to Root Sheet

Now that you've created hierarchical labels inside the Power Supply sheet,
you can import them as sheet pins on the root sheet:

1. Return to root sheet (click Up arrow)
2. Right-click on the Power Supply sheet border
3. Select "Import Sheet Pin" (or similar option)
4. This will automatically create sheet pins matching your hierarchical labels
   (`+12V`, `GND`, `+3V3`)

**Note:** Repeat this step after completing each part (2-6) to import pins for
each sheet.

**Save your work:** File → Save

---

## Part 2: ESP32 Core Sheet (30 minutes)

### 1. Enter the ESP32 Core Hierarchical Sheet

From the root sheet:

1. Double-click on the "ESP32 Core" sheet symbol
2. This opens the `esp32.kicad_sch` file
3. Add hierarchical labels for all pins defined earlier

### 2. Add ESP32 Core Hierarchical Labels

Add these labels (Press `H` for each):

**Power:**

- `+3V3` (Input)
- `GND` (Bidirectional)

**I2C:**

- `I2C_SDA` (Bidirectional) - connects to GPIO6
- `I2C_SCL` (Output) - connects to GPIO7

**1-Wire:**

- `1WIRE_DATA` (Bidirectional) - connects to GPIO10

**SPI:**

- `SPI_SCK` (Output) - connects to GPIO19
- `SPI_MISO` (Input) - connects to GPIO18
- `SPI_CS_TC1` (Output) - connects to GPIO20
- `SPI_CS_TC2` (Output) - connects to GPIO21
- `SPI_CS_TC3` (Output) - connects to GPIO22

**ADC:**

- `ADC_CH0` (Input) - connects to GPIO0
- `ADC_CH1` (Input) - connects to GPIO1
- `ADC_CH2` (Input) - connects to GPIO2
- `ADC_CH3` (Input) - connects to GPIO3
- `ADC_CH4` (Input) - connects to GPIO4

**Dashboard I/O:**

- `PIEZO` (Output) - connects to GPIO5
- `LED1_OUT` (Output) - connects to GPIO11
- `LED2_OUT` (Output) - connects to GPIO15
- `SWITCH1_IN` (Input) - connects to GPIO16
- `SWITCH2_IN` (Input) - connects to GPIO17
- `SWITCH3_IN` (Input) - connects to GPIO23

### 3. Add ESP32-C6 Module (U2)

**Add the symbol:**

1. Press `A`
2. Search for: `ESP32-C6-WROOM-1`
3. Place in center of schematic
4. Reference: `U2`
5. **Important:** Set value to `ESP32-C6-WROOM-1-N8` (this is the 8MB flash variant)

### 4. Connect Power to ESP32

```text
Hierarchical Label "+3V3" → ESP32 3V3 pin
Hierarchical Label "GND" → ESP32 GND pin
```

### 5. Add RESET Button Circuit

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

### 6. Add BOOT Button Circuit

**Components:**

- `R_BOOT`: 10k resistor (pullup)
- `SW_BOOT`: Momentary push button

**Wire it:**

```text
+3V3 → R_BOOT → ESP32 GPIO9 pin (BOOT)
ESP32 GPIO9 → SW_BOOT → GND
```

**How it works:** Hold BOOT while pressing RESET to enter download mode for programming.

### 7. Add Power Indicator LED

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

### 8. Connect GPIO Pins to Sheet Interface

Now connect ESP32 GPIO pins to the hierarchical labels (sheet interface):

**Method:** Use local labels on GPIO pins, then wire to hierarchical labels

**Internal signals (stay within this sheet):**

1. Press `L` (Local Label) on these pins:

   - `USB_D-` on GPIO12 (connects to USB-C connector within this sheet)
   - `USB_D+` on GPIO13 (connects to USB-C connector within this sheet)
   - `RGB_LED` on GPIO8 (connects to WS2812B within this sheet)

**External signals (connect to hierarchical labels):**

Wire these GPIO pins directly to their corresponding hierarchical labels:

**Sensors:**

- GPIO6 → wire → Hierarchical Label `I2C_SDA`
- GPIO7 → wire → Hierarchical Label `I2C_SCL`
- GPIO10 → wire → Hierarchical Label `1WIRE_DATA`
- GPIO19 → wire → Hierarchical Label `SPI_SCK`
- GPIO18 → wire → Hierarchical Label `SPI_MISO`
- GPIO20 → wire → Hierarchical Label `SPI_CS_TC1`
- GPIO21 → wire → Hierarchical Label `SPI_CS_TC2`
- GPIO22 → wire → Hierarchical Label `SPI_CS_TC3`
- GPIO0 → wire → Hierarchical Label `ADC_CH0`
- GPIO1 → wire → Hierarchical Label `ADC_CH1`
- GPIO2 → wire → Hierarchical Label `ADC_CH2`
- GPIO3 → wire → Hierarchical Label `ADC_CH3`
- GPIO4 → wire → Hierarchical Label `ADC_CH4`

**Dashboard I/O:**

- GPIO5 → wire → Hierarchical Label `PIEZO`
- GPIO11 → wire → Hierarchical Label `LED1_OUT`
- GPIO15 → wire → Hierarchical Label `LED2_OUT`
- GPIO16 → wire → Hierarchical Label `SWITCH1_IN`
- GPIO17 → wire → Hierarchical Label `SWITCH2_IN`
- GPIO23 → wire → Hierarchical Label `SWITCH3_IN`

---

## Part 2.5: USB-C Connector (Still on ESP32 Core Sheet) (20 minutes)

**Note:** The USB-C connector stays on the ESP32 Core sheet since the ESP32-C6
has native USB (no bridge chip needed).

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
The RGB LED can be used for status indication instead of a dedicated status LED.

---

## Part 3: Current Sensing Sheet (45 minutes)

### 1. Enter the Current Sensing Hierarchical Sheet

From the root sheet:

1. Navigate back to root (click Up arrow)
2. Double-click on the "Current Sensing" sheet symbol
3. This opens the `current_sensing.kicad_sch` file

### 2. Add Current Sensing Hierarchical Labels

Add these labels (Press `H` for each):

**Power:**

- `+3V3` (Input)
- `GND` (Bidirectional)

**ADC Outputs:**

- `ADC_CH0` (Output) - connects to signal conditioning output
- `ADC_CH1` (Output)
- `ADC_CH2` (Output)
- `ADC_CH3` (Output)
- `ADC_CH4` (Output)

### 3. Build Channels 1-5 with Op-Amp Buffers

We'll use **two MCP6004 ICs** for buffering all 5 current clamp channels:

- **U5** (MCP6004): Clamps 1-4 (all 4 op-amps used)
- **U6** (MCP6004): Clamps 5-6 (U6A for clamp 5, U6B reserved for clamp 6)

### 4. Add Consolidated Current Clamp Connector (J_CLAMP - 10-pin)

**Add the connector:**

1. Press `A`
2. Search: `Screw_Terminal_01x10`
3. Place on left side
4. Reference: `J_CLAMP`
5. Value: `CURRENT_CLAMPS`

**Pin assignments:**

- Pin 1: CLAMP1_SIG, Pin 2: CLAMP1_GND
- Pin 3: CLAMP2_SIG, Pin 4: CLAMP2_GND
- Pin 5: CLAMP3_SIG, Pin 6: CLAMP3_GND
- Pin 7: CLAMP4_SIG, Pin 8: CLAMP4_GND
- Pin 9: CLAMP5_SIG, Pin 10: CLAMP5_GND

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

### 5. Wire the Signal Chain (Clamp 1)

```text
J_CLAMP Pin 1 (CLAMP1_SIG) → R_SER_1 → R_DIV1_1 → [midpoint junction]
[midpoint] → R_DIV2_1 → GND
[midpoint] → R_FILT_1 → C_FILT_1 → GND
[after R_FILT_1] → U5A Pin 3 (+ input)
U5A Pin 2 (- input) → U5A Pin 1 (output) [unity gain buffer]
U5A Pin 1 → Hierarchical Label "ADC_CH0" (outputs to ESP32 Core sheet)
J_CLAMP Pin 2 (CLAMP1_GND) → GND
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

Repeat the same circuit for channels 2-4, connecting to the appropriate pins
on J_CLAMP:

**Channel 2:**

- Connector pins: `J_CLAMP Pin 3` (CLAMP2_SIG), `J_CLAMP Pin 4` (CLAMP2_GND)
- Components: `R_SER_2`, `R_DIV1_2`, `R_DIV2_2`, `R_FILT_2`, `C_FILT_2`
- Op-amp: `U5B` → Label "ADC_CH1"

**Channel 3:**

- Connector pins: `J_CLAMP Pin 5` (CLAMP3_SIG), `J_CLAMP Pin 6` (CLAMP3_GND)
- Components: `R_SER_3`, `R_DIV1_3`, `R_DIV2_3`, `R_FILT_3`, `C_FILT_3`
- Op-amp: `U5C` → Label "ADC_CH2"

**Channel 4:**

- Connector pins: `J_CLAMP Pin 7` (CLAMP4_SIG), `J_CLAMP Pin 8` (CLAMP4_GND)
- Components: `R_SER_4`, `R_DIV1_4`, `R_DIV2_4`, `R_FILT_4`, `C_FILT_4`
- Op-amp: `U5D` → Label "ADC_CH3"

### 6. Add Second MCP6004 for Channel 5

**Add U6 (second MCP6004):**

1. Add all components for channel 5 (same as channels 1-4)
2. Connector pins: `J_CLAMP Pin 9` (CLAMP5_SIG), `J_CLAMP Pin 10` (CLAMP5_GND)
3. Components: `R_SER_5`, `R_DIV1_5`, `R_DIV2_5`, `R_FILT_5`, `C_FILT_5`
4. Op-amp: `U6A` → Hierarchical Label "ADC_CH4"

**Important:** For channels 2-5, connect the op-amp outputs to their corresponding
hierarchical labels (`ADC_CH1`, `ADC_CH2`, `ADC_CH3`, `ADC_CH4`) the same way
you did for channel 1.

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

## Part 4: Temperature Sensors Sheet (20 minutes)

### 1. Enter the Temperature Sensors Hierarchical Sheet

From the root sheet:

1. Navigate back to root (click Up arrow)
2. Double-click on the "Temperature Sensors" sheet symbol
3. This opens the `temperature.kicad_sch` file

### 2. Add Temperature Sensors Hierarchical Labels

**Power:**

- `+3V3` (Input)
- `GND` (Bidirectional)

**I2C:**

- `I2C_SDA` (Bidirectional)
- `I2C_SCL` (Input)

**1-Wire:**

- `1WIRE_DATA` (Bidirectional)

### 3. Add SHT40 I2C Sensor

1. Press `A`
2. Search: `SHT4x`
3. Place on schematic
4. Reference: `U3`

### 4. Add I2C Pullup Resistors

**Components:**

- `R_SDA_PU`: 4.7k resistor
- `R_SCL_PU`: 4.7k resistor

### 5. Wire I2C Section

```text
+3V3 → R_SDA_PU → Hierarchical Label "I2C_SDA"
+3V3 → R_SCL_PU → Hierarchical Label "I2C_SCL"
U3 SDA pin → Hierarchical Label "I2C_SDA"
U3 SCL pin → Hierarchical Label "I2C_SCL"
U3 VDD → +3V3
U3 VSS → GND
```

### 6. Add 1-Wire Interface

**1-Wire Pullup:**

- `R_1WIRE_PU`: 4.7k resistor

**Wire it:**

```text
+3V3 → R_1WIRE_PU → Hierarchical Label "1WIRE_DATA"
```

**Note:** The 1-Wire data line connects to DS18B20 sensors via the Main Connector
sheet. All DS18B20 data pins are wired together to this single 1-Wire bus.

### 7. Add Decoupling Capacitor

- `C_SHT40`: 0.1uF between VDD and VSS

---

## Part 5: Thermocouples Sheet (25 minutes)

### 1. Enter the Thermocouples Hierarchical Sheet

From the root sheet:

1. Navigate back to root
2. Double-click on the "Thermocouples" sheet symbol
3. This opens the `thermocouples.kicad_sch` file

### 2. Add Thermocouples Hierarchical Labels

**Power:**

- `+3V3` (Input)
- `GND` (Bidirectional)

**SPI:**

- `SPI_SCK` (Input) - from ESP32
- `SPI_MISO` (Output) - to ESP32
- `SPI_CS_TC1` (Input) - from ESP32
- `SPI_CS_TC2` (Input) - from ESP32
- `SPI_CS_TC3` (Input) - from ESP32

### 3. Build Thermocouple Circuits

Follow Part 4.5 instructions below, but connect SPI signals to hierarchical
labels instead of local labels:

- SCK pins → Hierarchical Label "SPI_SCK"
- MISO pins → Hierarchical Label "SPI_MISO"
- CS pins → Hierarchical Labels "SPI_CS_TC1", "SPI_CS_TC2", "SPI_CS_TC3"

---

## Part 4.5: MAX31855 Details (Reference for Part 5)

### Overview

We'll add **3× MAX31855** thermocouple amplifiers for high-temperature
sensing. All three share the SPI bus (SCK and MISO), but each has its own
CS (chip select) pin. All thermocouples connect to a single consolidated
**J_TC** (6-pin) connector.

### 1. Add Consolidated Thermocouple Connector (J_TC - 6-pin)

**Add the connector:**

1. Press `A`
2. Search: `Screw_Terminal_01x06`
3. Place on left side
4. Reference: `J_TC`
5. Value: `THERMOCOUPLES`

**Pin assignments:**

- Pin 1: TC1_T+ (Thermocouple 1 +)
- Pin 2: TC1_T- (Thermocouple 1 -)
- Pin 3: TC2_T+ (Thermocouple 2 +)
- Pin 4: TC2_T- (Thermocouple 2 -)
- Pin 5: TC3_T+ (Thermocouple 3 +)
- Pin 6: TC3_T- (Thermocouple 3 -)

### 2. Add First MAX31855 (U4)

1. Press `A`
2. Search: `MAX31855`
3. Place on schematic
4. Reference: `U4`

### 3. Wire First MAX31855

```text
U4 VCC → +3V3
U4 GND → GND
U4 SCK → Label "SPI_SCK"
U4 SO → Label "SPI_MISO"
U4 CS → Label "SPI_CS_TC1"
U4 T+ → J_TC Pin 1 (TC1_T+)
U4 T- → J_TC Pin 2 (TC1_T-)
```

### 4. Add Decoupling Capacitor

- `C_TC1`: 0.1uF ceramic
- Connect between VCC and GND (place close to MAX31855)

### 5. Add Second MAX31855 (U7)

Repeat the same circuit for the second thermocouple:

1. Add MAX31855, Reference: `U7`
2. Add decoupling cap `C_TC2`
3. Wire:

```text
U7 VCC → +3V3
U7 GND → GND
U7 SCK → Label "SPI_SCK" (shared)
U7 SO → Label "SPI_MISO" (shared)
U7 CS → Label "SPI_CS_TC2" (GPIO21)
U7 T+ → J_TC Pin 3 (TC2_T+)
U7 T- → J_TC Pin 4 (TC2_T-)
```

### 6. Add Third MAX31855 (U8)

Repeat for the third thermocouple:

1. Add MAX31855, Reference: `U8`
2. Add decoupling cap `C_TC3`
3. Wire:

```text
U8 VCC → +3V3
U8 GND → GND
U8 SCK → Label "SPI_SCK" (shared)
U8 SO → Label "SPI_MISO" (shared)
U8 CS → Label "SPI_CS_TC3" (GPIO22)
U8 T+ → J_TC Pin 5 (TC3_T+)
U8 T- → J_TC Pin 6 (TC3_T-)
```

### Notes

- **Shared SPI bus:** SCK and MISO are shared between all MAX31855 ICs
- **Individual CS pins:** Each MAX31855 has its own chip select
- **PCB layout:** Keep thermocouple traces short and away from noisy signals
- **Thermocouple polarity:** Yellow wire = T+, Red wire = T- (standard K-type)

---

## Part 6: Main Connector & I/O Interface Sheet (45 minutes)

### 1. Enter the Main Connector Hierarchical Sheet

From the root sheet:

1. Navigate back to root
2. Double-click on the "Main Connector" sheet symbol
3. This opens the `main_connector.kicad_sch` file

### 2. Add Main Connector & I/O Hierarchical Labels

**Power:**

- `+12V` (Output) - provides 12V to Power Supply sheet
- `GND` (Bidirectional)
- `DS18B20_VCC` (Input) - receives 3.3V from Power Supply sheet
- `+3V3` (Input) - receives 3.3V for piezo buzzer

**1-Wire:**

- `1WIRE_DATA` (Bidirectional) - connects to Temperature Sensors sheet

**Dashboard I/O (from/to ESP32 Core sheet):**

- `PIEZO` (Input) - piezo buzzer control from GPIO5
- `LED1_OUT` (Input) - LED 1 control from GPIO11
- `LED2_OUT` (Input) - LED 2 control from GPIO15
- `SWITCH1_IN` (Output) - Switch 1 input to GPIO16
- `SWITCH2_IN` (Output) - Switch 2 input to GPIO17
- `SWITCH3_IN` (Output) - Switch 3 input to GPIO23

### 3. Add J_MAIN Connector (11-pin)

**Add the connector:**

1. Press `A`
2. Search for: `Screw_Terminal_01x11`
3. Place on schematic
4. Reference: `J_MAIN`
5. Value: `POWER+SENSORS`

**Pin assignments:**

- Pin 1: +12V → Hierarchical Label "+12V"
- Pin 2: GND → Hierarchical Label "GND"
- Pins 3, 6, 9: +3.3V → Hierarchical Label "DS18B20_VCC" (all wired together)
- Pins 4, 7, 10: DATA → Hierarchical Label "1WIRE_DATA" (all wired together)
- Pins 5, 8, 11: GND → Hierarchical Label "GND" (all wired together)

**Wiring:**

```text
J_MAIN Pin 1 → Hierarchical Label "+12V"
J_MAIN Pin 2 → Hierarchical Label "GND"

J_MAIN Pin 3 (DS18B20_1_VCC) ─┐
J_MAIN Pin 6 (DS18B20_2_VCC) ─┼→ Hierarchical Label "DS18B20_VCC"
J_MAIN Pin 9 (DS18B20_3_VCC) ─┘

J_MAIN Pin 4 (DS18B20_1_DATA) ─┐
J_MAIN Pin 7 (DS18B20_2_DATA) ─┼→ Hierarchical Label "1WIRE_DATA"
J_MAIN Pin 10 (DS18B20_3_DATA) ┘

J_MAIN Pin 5 (DS18B20_1_GND) ─┐
J_MAIN Pin 8 (DS18B20_2_GND) ─┼→ Hierarchical Label "GND"
J_MAIN Pin 11 (DS18B20_3_GND) ┘
```

### 4. Add Piezo Buzzer Circuit

**Components needed:**

- `PIEZO1`: Murata PKLCS1212E4001-R1 (SMD) or PKM13EPYH4000-A0 (TH)
- `Q1`: 2N3904 or BC547 (NPN transistor)
- `R_PIEZO`: 1kΩ resistor

**Add the components:**

1. Press `A` → Search for `Q_NPN_BCE` → Place
2. Reference: `Q1`
3. Add piezo buzzer symbol (search for `Speaker` or `Buzzer`)
4. Reference: `PIEZO1`
5. Add 1kΩ resistor
6. Reference: `R_PIEZO`

**Wire the circuit:**

```text
Hierarchical Label "PIEZO" (from ESP32 GPIO5) → R_PIEZO (1kΩ) → Q1 base
Q1 collector → PIEZO1 positive terminal
PIEZO1 positive terminal → Hierarchical Label "+3V3"
Q1 emitter → Hierarchical Label "GND"
PIEZO1 negative terminal → Hierarchical Label "GND"
```

**How it works:** GPIO5 drives the NPN transistor base through a 1kΩ
current-limiting resistor. When GPIO5 is HIGH, the transistor conducts,
allowing current to flow through the piezo from +3.3V to GND, producing sound.

### 5. Add J_IO Connector (9-pin)

**Add the connector:**

1. Press `A`
2. Search for: `Screw_Terminal_01x09`
3. Place on schematic
4. Reference: `J_IO`
5. Value: `DASHBOARD_IO`

**Pin assignments:**

- Pin 1: +12V (from main 12V bus)
- Pin 2: GND
- Pin 3: LED1_OUT (to 12V LED cathode)
- Pin 4: LED2_OUT (to 12V LED cathode)
- Pin 5: LED_GND (common return for LED cathodes)
- Pin 6: SWITCH1_IN (from 12V toggle switch)
- Pin 7: SWITCH2_IN (from 12V toggle switch)
- Pin 8: SWITCH3_IN (from 12V toggle switch)
- Pin 9: SWITCH_GND (common ground for switches)

### 6. Add LED Output Circuits (2× identical channels)

**Components per channel:**

- `Q_LED1/2`: 2N7002 (N-channel MOSFET, SOT-23)
- `R_LED1/2`: 10kΩ resistor (gate pulldown)

**Add for LED 1:**

1. Press `A` → Search for `Q_NMOS_GSD` or `2N7002` → Place
2. Reference: `Q_LED1`
3. Add 10kΩ resistor
4. Reference: `R_LED1`

**Wire LED 1 circuit:**

```text
Hierarchical Label "LED1_OUT" (from ESP32 GPIO11) → R_LED1 (10kΩ) → Q_LED1 gate
Q_LED1 drain → J_IO Pin 3 (LED1_OUT)
Q_LED1 source → J_IO Pin 6 (LED_GND) → Hierarchical Label "GND"
J_IO Pin 1 (+12V) → Hierarchical Label "+12V"
```

**Repeat for LED 2:**

- LED 2: GPIO15 → R_LED2 → Q_LED2 gate, Q_LED2 drain → J_IO Pin 4

**How it works:** When ESP32 GPIO goes HIGH (3.3V), it turns on the MOSFET,
which connects the 12V LED cathode to GND through the drain-source channel.
The external 12V LED (with built-in current limiting resistor) has its anode
connected to +12V (Pin 1) and cathode to LED_OUT (Pins 3-4), completing the
circuit.

### 7. Add Switch Input Circuits (3× identical channels)

**Components per channel:**

- `R_SW1_DIV1/2/3`: 10kΩ resistor (top of voltage divider)
- `R_SW1_DIV2/2/3`: 3.3kΩ resistor (bottom of voltage divider)
- `D_Z1/2/3`: BZX84C3V3 (3.3V Zener diode, SOT-23)

**Add for Switch 1:**

1. Add two resistors (10kΩ and 3.3kΩ)
   - References: `R_SW1_DIV1`, `R_SW1_DIV2`
2. Press `A` → Search for `D_Zener` → Place
   - Reference: `D_Z1`
   - Value: `BZX84C3V3` (3.3V)

**Wire Switch 1 circuit:**

```text
J_IO Pin 6 (SWITCH1_IN) → R_SW1_DIV1 (10kΩ) → [midpoint junction]
[midpoint] → R_SW1_DIV2 (3.3kΩ) → J_IO Pin 9 (SWITCH_GND) →
              Hierarchical Label "GND"
[midpoint] → D_Z1 cathode
D_Z1 anode → Hierarchical Label "GND"
[midpoint] → Hierarchical Label "SWITCH1_IN" (to ESP32 GPIO16)
```

**Repeat for Switch 2 and Switch 3:**

- Switch 2: J_IO Pin 7 → voltage divider →
  Hierarchical Label "SWITCH2_IN" (GPIO17)
- Switch 3: J_IO Pin 8 → voltage divider →
  Hierarchical Label "SWITCH3_IN" (GPIO23)

**How it works:**

- External 12V switch connects one terminal to +12V (J_IO Pin 1)
  and the other to SWITCH_IN (Pins 6-8)
- When switch is CLOSED: 12V is divided by 10kΩ/(10kΩ+3.3kΩ) = 3.0V →
  GPIO reads HIGH
- When switch is OPEN: 3.3kΩ pulls to GND → GPIO reads LOW
- Zener diode clamps voltage at 3.3V maximum for ESP32 protection

**Voltage divider calculation:**

- Input: 12V
- R1: 10kΩ (top)
- R2: 3.3kΩ (bottom)
- Output: 12V × [3.3k / (10k + 3.3k)] = 12V × 0.248 = **2.98V** ✓
  (safe for 3.3V GPIO)

### 8. Add Decoupling and Notes

**Optional improvements:**

- Add 0.1µF capacitors across each Zener diode for transient suppression
- Add local labels for clarity (e.g., `LED1_GATE`, `SW1_DIV`)

**Silkscreen notes to add:**

- Mark J_IO Pin 1 with "+12V WARNING"
- Label LED outputs as "TO LED CATHODE" on silkscreen
- Label switch inputs as "FROM 12V SWITCH" on silkscreen

---

## Part 7: Finishing Up (10 minutes)

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
- `S` - Add hierarchical sheet
- `H` - Add hierarchical label
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

1. **Hierarchical sheets**: Organize complex designs into logical
   functional blocks
2. **Hierarchical labels**: Use `H` for signals that cross sheet
   boundaries
3. **Local labels**: Use `L` for signals within a single sheet
4. **Global labels**: Use `G` sparingly, mainly on root sheet for
   power distribution
5. **Power symbols**: Use for all power connections (cleaner than wires)
6. **Grid**: Keep everything on grid (View → Grid Settings)
7. **Reference designators**: Use logical prefixes (J=connectors,
   R=resistors, C=capacitors, U=ICs)

### Common Issues

- **Wires not connecting**: Make sure endpoints touch pins exactly
- **Missing symbols**: Update library tables (Preferences → Manage Symbol Libraries)
- **ERC errors**: Most common are missing power connections and unconnected pins

---

## Build Order - Hierarchical Sheet Approach

**Recommended build order:**

1. **Part 0** - Setup hierarchical sheets on root (create all sheet symbols)
2. **Part 1** - Power Supply sheet (buck converter, USB LDO, OR-ing diodes)
3. **Part 2** - ESP32 Core sheet (MCU, buttons, RGB LED)
4. **Part 2.5** - USB-C connector (on ESP32 Core sheet)
5. **Part 2.6** - RGB LED (on ESP32 Core sheet)
6. **Part 3** - Current Sensing sheet (J_CLAMP connector + conditioning)
7. **Part 4** - Temperature Sensors sheet (SHT40 + 1-Wire interface)
8. **Part 5** - Thermocouples sheet (J_TC connector + 3× MAX31855)
9. **Part 6** - Main Connector & I/O Interface sheet (J_MAIN + J_IO +
   piezo + LED/switch circuits)
10. **Part 7** - Finishing up (annotate, ERC, footprints)

**Benefits of this approach:**

- Clean, organized schematic that's easy to navigate
- Each functional block is self-contained
- Easier to review and debug
- Better for version control and collaboration
- Scales well for future expansions

---

## Need Help?

If you get stuck:

1. Take a screenshot and describe the issue
2. Check the ERC report for specific errors
3. Verify all pins are connected
4. Make sure power symbols are correct (+3V3, GND)

Let me know when you complete each section and I can help with the next one!
