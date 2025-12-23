# KiCad Schematic Requirements - ESP32-C6 Marine Sensor Board

## Project Overview

Create a KiCad 7.x schematic and PCB layout for an ESP32-C6 based
multi-sensor board for marine applications.

## Schematic Requirements

### Main Components

1. **ESP32-C6-WROOM-1-N8** (U2)
   - Use ESP32-C6 symbol from espressif library
   - Footprint: ESP32-C6-WROOM-1
   - **8MB Flash variant** (N8 = 8MB)
   - Built-in USB on GPIO12/GPIO13

2. **USB-C Connector** (J_USB)
   - USB Type-C receptacle (16-pin)
   - Connected to ESP32-C6 native USB (GPIO12/GPIO13)
   - 5.1kΩ resistors on CC pins
   - ESD protection recommended (USBLC6-2SC6 or similar)
   - Used for programming and UART debugging

3. **SHT40** (U3) - Temperature/Humidity Sensor
   - I2C interface
   - Address: 0x44

4. **MAX31855** (U4) - Thermocouple Amplifier
   - SPI interface
   - K-type thermocouple input

5. **MCP6004** (U5, U6) - Quad Op-Amp (2 ICs)
   - Used for current clamp signal buffering
   - SOIC-14 or TSSOP-14 package

6. **LM2596** (U1) - Buck Converter
   - 12V → 3.3V
   - Can use module footprint or discrete IC

### Power Section

- Input: 12V screw terminal (J_PWR)
- MBRS340 Schottky diode (D1) for reverse polarity protection
- SMBJ15A TVS diode (TVS1) for spike protection
- Capacitors: 100µF/25V, 100µF/10V, 10µF, multiple 0.1µF

### GPIO Pin Assignments

**I2C (SHT40):**

- GPIO6: SDA (4.7kΩ pullup)
- GPIO7: SCL (4.7kΩ pullup)

**1-Wire (DS18B20):**

- GPIO8: DS18B20_1 (4.7kΩ pullup)
- GPIO10: DS18B20_2 (4.7kΩ pullup)
- GPIO11: DS18B20_3 (4.7kΩ pullup)

**SPI (MAX31855):**

- GPIO19: SCK
- GPIO18: MISO
- GPIO20: CS

**ADC (Current Clamps):**

- GPIO0-5: ADC1_CH0 through ADC1_CH5 (6 channels)

**USB (Native ESP32-C6 USB):**

- GPIO12: USB D+ (to USB-C connector)
- GPIO13: USB D- (to USB-C connector)

**User Interface:**

- GPIO15: WS2812B RGB LED (addressable, like ESP32-C6-DevKitC)
- GPIO23: Status LED (green, 330Ω resistor)
- GPIO9: BOOT button (momentary, 10kΩ pullup to +3V3)
- EN: RESET button (momentary, 10kΩ pullup, 0.1µF cap to GND)

**Power Indication:**

- D_PWR: Green LED for power indicator (1kΩ resistor from +3V3)

### Current Clamp Signal Conditioning (6x identical circuits)

Each channel:

```text
Input (0-5V from QNHCK2-16) 
  → 1kΩ series resistor
  → Voltage divider (10kΩ / 20kΩ) 
  → RC filter (1kΩ / 0.1µF)
  → MCP6004 buffer (unity gain)
  → ESP32 ADC
```

### Connectors

| Designator | Type | Purpose | Pins |
| ---------- | ---- | ------- | ---- |
| J_PWR | Screw terminal 5mm | 12V power input | 2 |
| J_USB | USB Type-C | Programming & UART debug | 16 (USB 2.0) |
| J1-J3 | RJ45 or JST-XH | DS18B20 sensors | 3 each |
| J4 | Screw terminal | K-type thermocouple | 2 |
| J5-J10 | Screw terminal | Current clamps | 2 each |

### Passives Summary

- Resistors: 4.7kΩ (5x), 10kΩ (~10x), 20kΩ (6x), 1kΩ (~13x), 5.1kΩ
  (2x for USB CC), 330Ω (1x)
- Capacitors: 0.1µF (~15x), 10µF (1x), 100µF 25V (1x), 100µF 10V (1x)
- LEDs: 3x (1x green power LED, 1x green status LED, 1x WS2812B RGB LED)
- Buttons: 2x momentary tactile (RESET, BOOT)
- USB-C connector: 1x (16-pin receptacle)
- ESD protection: 1x USBLC6-2SC6 (optional but recommended)

## PCB Layout Requirements

### Board Specifications

- 2-layer PCB
- Dimensions: ~80mm × 60mm
- Mounting holes: 4× M3

### Layout Guidelines

1. **Component Placement:**
   - Power section (buck converter) on left edge
   - ESP32-C6 center-left
   - SHT40 near ESP32
   - MAX31855 away from buck converter
   - Op-amps in analog section (right side)
   - All connectors on board edges

2. **Trace Width:**
   - 12V input: ≥20 mil (0.5mm)
   - 3.3V power: ≥15 mil (0.4mm)
   - Signal traces: 8-10 mil (0.2-0.25mm)

3. **Ground Plane:**
   - Star ground configuration
   - Separate analog and digital ground zones
   - Single connection point near power supply
   - Ground plane around MAX31855

4. **Thermal Management:**
   - Thermal vias under buck converter
   - Consider heatsinking provision for U1

5. **Design Rules:**
   - Minimum trace: 8 mil
   - Minimum clearance: 8 mil
   - Via size: 12 mil drill, 24 mil pad

6. **Keep-Out Zones:**
   - ESP32 antenna area (mark on silkscreen)
   - High-voltage/high-current traces

### Silkscreen

- Component values for all passives
- Polarity markings on all connectors
- Pin 1 indicators
- Board revision number
- "CONFORMAL COATING SAFE" designation
- Warning: "12V INPUT - CHECK POLARITY"

## Files to Generate

1. **Schematic:**
   - `marine-sensor-board.kicad_sch`
   - Hierarchical sheets optional (could separate: power, MCU, sensors, analog)

2. **PCB Layout:**
   - `marine-sensor-board.kicad_pcb`

3. **Symbol Library:**
   - Create custom symbols if needed (or use standard KiCad libs)

4. **Footprint Library:**
   - Verify all footprints are available or create custom

5. **Bill of Materials:**
   - Export BOM with designators, values, footprints, quantities

6. **Manufacturing Files:**
   - Gerbers (plot to `/gerbers` folder)
   - Drill files
   - Assembly drawings
   - Pick-and-place file (if SMT assembly)

## KiCad Libraries Needed

- ESP32 library (from espressif or snapeda)
- Standard KiCad device library
- Standard KiCad connector library
- May need custom symbols for:
  - SHT40 (or use generic I2C sensor symbol)
  - QNHCK2-16 connector representation

## Design for Manufacturing (DFM)

- All SMD components on top side preferred
- Through-hole connectors on top
- Maintain clearance from board edge: ≥3mm
- Fiducials for assembly: 3× on corners
- Tooling holes if needed for panel
- Lead-free compatible (ROHS)

## Testing Points

Add test points for:

- 12V input
- 3.3V rail
- GND (multiple points)
- Each ADC channel (after op-amp)
- I2C SDA/SCL
- SPI signals
- 1-Wire data lines

## Notes for Claude Code

- Use KiCad 7.x format
- Follow KLC (KiCad Library Convention) for symbols/footprints
- Annotate all components before generating netlist
- Run ERC (Electrical Rule Check) and fix all errors
- Run DRC (Design Rule Check) on PCB
- Generate 3D view for verification
- Export schematic PDF for documentation

## Reference Documents

See `HARDWARE.md` for complete circuit details, component specifications,
and design rationale.

---

**Target Cost:** ~$23-25 per board (components only, qty 1-10)
**Application:** Marine environment - requires conformal coating
**Safety Critical:** Engine monitoring application - implement watchdog and
fault detection
