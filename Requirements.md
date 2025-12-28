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

4. **MAX31855** (U4, U7, U8) - Thermocouple Amplifiers (3× ICs)
   - SPI interface (shared bus with individual CS lines)
   - K-type thermocouple inputs (3 channels)
   - Temperature range: -270°C to +1372°C
   - 0.25°C resolution with cold junction compensation

5. **MCP6004** (U5, U6) - Quad Op-Amp (2 ICs)
   - Used for current clamp signal buffering (channels 1-5)
   - U5: Channels 1-4, U6: Channel 5 + reserved channel 6
   - SOIC-14 or TSSOP-14 package

6. **LM2596** (U1) - Buck Converter
   - 12V → 3.3V
   - Can use module footprint or discrete IC

7. **Piezo Buzzer** (PIEZO1) - Audible Alarm
   - Murata PKLCS1212E4001-R1 (SMD) or PKM13EPYH4000-A0 (TH)
   - 12mm diameter, 4kHz, 85dB @ 10cm
   - NPN transistor driver (2N3904 or BC547)
   - Always populated, software-controllable

8. **Dashboard I/O Interface**
   - 3× N-channel MOSFETs (2N7002) for 12V LED outputs
   - 3× Zener diodes (BZX84C3V3, 3.3V) for 12V switch input protection
   - Voltage dividers for 12V→3.3V level shifting on switch inputs
   - External: 3× 12V panel-mount LEDs, 3× marine toggle switches (user-supplied)

### Power Section

- Input: 12V from J_MAIN (11-pin consolidated connector, Pins 1-2)
- MBRS340 Schottky diode (D1) for reverse polarity protection
- SMBJ15A TVS diode (TVS1) for spike protection
- Capacitors: 100µF/25V, 100µF/10V, 10µF, multiple 0.1µF

### GPIO Pin Assignments

**I2C (SHT40):**

- GPIO6: SDA (4.7kΩ pullup)
- GPIO7: SCL (4.7kΩ pullup)

**1-Wire (DS18B20):**

- GPIO10: 1-Wire bus (4.7kΩ pullup, multi-drop for all DS18B20 sensors)

**SPI (MAX31855 - 3× ICs):**

- GPIO19: SCK (shared by all 3 MAX31855)
- GPIO18: MISO (shared by all 3 MAX31855)
- GPIO20: CS for MAX31855 #1 (U4)
- GPIO21: CS for MAX31855 #2 (U7)
- GPIO22: CS for MAX31855 #3 (U8)

**ADC (Current Clamps):**

- GPIO0: ADC1_CH0 (Clamp 1)
- GPIO1: ADC1_CH1 (Clamp 2)
- GPIO2: ADC1_CH2 (Clamp 3)
- GPIO3: ADC1_CH3 (Clamp 4)
- GPIO4: ADC1_CH4 (Clamp 5)

**Dashboard I/O:**

- GPIO5: Piezo buzzer (NPN transistor driver, always populated)
- GPIO11: Dashboard LED #1 output (MOSFET → 12V LED)
- GPIO14: Dashboard LED #2 output (MOSFET → 12V LED)
- GPIO15: Dashboard LED #3 output (MOSFET → 12V LED)
- GPIO16: 12V Switch #1 input (voltage divider 12V→3.3V)
- GPIO17: 12V Switch #2 input (voltage divider 12V→3.3V)
- GPIO23: 12V Switch #3 input (voltage divider 12V→3.3V)

**USB (Native ESP32-C6 USB):**

- GPIO12: USB D- (to USB-C connector)
- GPIO13: USB D+ (to USB-C connector)

**User Interface:**

- GPIO8: WS2812B RGB LED (addressable, matches ESP32-C6-DevKitC)
- GPIO9: BOOT button (momentary, 10kΩ pullup to +3V3)
- EN: RESET button (momentary, 10kΩ pullup, 0.1µF cap to GND)

**Power Indication:**

- D_PWR: Green LED for power indicator (1kΩ resistor from +3V3)

### Current Clamp Signal Conditioning (5 channels + 1 reserved)

All channels use identical buffered signal conditioning:

```text
Input (0-5V from QNHCK2-16)
  → 1kΩ series resistor
  → Voltage divider (10kΩ / 20kΩ)
  → RC filter (1kΩ / 0.1µF)
  → MCP6004 buffer (unity gain)
  → ESP32 ADC (GPIO0-4)
```

Op-amp allocation:

- U5A-D: Channels 1-4 → GPIO0-3
- U6A: Channel 5 → GPIO4
- U6B-D: Unused (GPIO5 repurposed for piezo buzzer)

### Connectors

| Designator | Type | Purpose | Pins |
| ---------- | ---- | ------- | ---- |
| J_MAIN | Screw terminal 5mm | Power + DS18B20 sensors | 11 |
| J_TC | Screw terminal 5mm | K-type thermocouples (3×) | 6 |
| J_CLAMP | Screw terminal 5mm | Current clamps (5×) | 10 |
| J_IO | Screw terminal 5mm | Dashboard LEDs + switches | 10 |
| J_USB | USB Type-C | Programming & UART debug | 16 (USB 2.0) |

### Passives Summary

- Resistors: 4.7kΩ (3x), 10kΩ (~15x including gate resistors), 3.3kΩ (3x for
  switch voltage dividers), 20kΩ (5x), 1kΩ (~13x including piezo), 5.1kΩ
  (2x for USB CC), 330Ω (2x for LEDs)
- Capacitors: 0.1µF (~15x including 3x for MAX31855), 10µF (1x), 100µF 25V
  (1x), 100µF 10V (1x)
- LEDs: 2x (1x green power LED, 1x WS2812B RGB LED)
- Transistors: 1x NPN (2N3904/BC547 for piezo), 3x N-ch MOSFET (2N7002
  for LED outputs)
- Diodes: 3x Zener 3.3V (BZX84C3V3 for switch input protection)
- Buttons: 2x momentary tactile (RESET, BOOT)
- Piezo buzzer: 1x Murata PKLCS1212E4001-R1 (SMD) or PKM13EPYH4000-A0 (TH)
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

**Target Cost:** ~$36.00 per board (components only, qty 1-10)
**Application:** Marine environment - requires conformal coating
**Safety Critical:** Engine monitoring application - implement watchdog and
fault detection
**Dashboard I/O:** Supports remote 12V LED indicators and toggle switch inputs
for user interface
