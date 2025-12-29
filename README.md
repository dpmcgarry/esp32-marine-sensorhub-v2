# ESP32-C6 Marine Sensor Hub

A WiFi-enabled multi-sensor board designed for marine applications, featuring
temperature monitoring, humidity sensing, current measurement, and dashboard
I/O capabilities for remote indicators and controls.

![Hardware License](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-blue)
![Software License](https://img.shields.io/badge/software-GPLv3-blue)
![Status](https://img.shields.io/badge/status-In%20Development-yellow)

## Overview

The Marine Sensor Hub is a compact, ruggedized sensor platform built around
the ESP32-C6 microcontroller. It's designed to monitor critical systems on
boats and marine vessels, providing real-time data over WiFi 6 to a central
server via MQTT.

### Key Features

- **ESP32-C6 with WiFi 6** - Low-power RISC-V microcontroller with 8MB flash
- **Multiple Sensor Interfaces:**
  - Onboard SHT40 temperature & humidity sensor (±0.2°C accuracy)
  - Onboard piezo buzzer for audible alarms
  - Multiple DS18B20 1-Wire temperature sensors on shared bus (-67°F to +257°F)
  - 3× K-type thermocouple inputs (up to 2000°F via MAX31855)
  - 5× 30A current clamp inputs (QNHCK2-16 compatible)
- **Dashboard I/O Interface:**
  - 2× 12V LED outputs for remote panel indicators (MOSFET drivers)
  - 3× 12V toggle switch inputs with voltage dividers and protection
  - Supports long wire runs (10+ feet) for dashboard mounting
  - Software-controlled piezo buzzer for alarms
- **Dual Power System:**
  - 12VDC input (automotive/marine standard)
  - USB-C for programming and bench testing
  - Automatic power source selection with OR-ing diodes
- **Marine-Hardened Design:**
  - Reverse polarity protection
  - Voltage spike protection (TVS diode)
  - Conformal coating compatible
  - Wide operating temperature range

## Use Cases

- **Engine Room Monitoring:** Track engine temperature, exhaust temperature,
  and alternator current with dashboard warning LEDs
- **Battery Bank Management:** Monitor charging current across multiple banks
  with visual and audible alarms
- **HVAC Monitoring:** Track refrigerator/freezer performance and cabin
  temperature/humidity
- **Safety Systems:** High-temperature alarms with piezo buzzer and dashboard
  indicators
- **User Controls:** Toggle switches for pump control, alarm acknowledgment,
  or mode selection

## Project Status

Currently in schematic design phase:

- ✅ Hardware requirements defined
- ✅ Component selection complete
- ✅ Dual power system designed (12V + USB-C with OR-ing diodes)
- ✅ Dashboard I/O interface designed (piezo, LEDs, switches)
- 🚧 KiCad schematic starting from beginning (hierarchical sheet approach)
- ⏳ PCB layout pending
- ⏳ Firmware development pending

**Recent Updates:**

- Added dashboard I/O interface with piezo buzzer and 12V LED/switch support
- GPIO5 and GPIO23 repurposed for dashboard I/O (breaking change)
- Updated documentation with detailed circuit designs
- Board cost updated to ~$35.85

## Hardware Specifications

### Microcontroller

- **IC:** ESP32-C6-WROOM-1-N8 (8MB flash)
- **Core:** RISC-V single core @ 160MHz
- **WiFi:** 802.11ax (WiFi 6), 2.4GHz
- **Operating Voltage:** 3.3V

### Power Requirements

- **Input:** 12VDC nominal (9-16V range)
- **Current Draw:** 300-350mA peak @ 3.3V
- **USB-C:** 5V input with 3.3V LDO regulator
- **Power Dissipation:** ~3W maximum

### Sensors & I/O

| Component | Interface | Quantity | Range/Purpose |
| --------- | --------- | -------- | ------------- |
| SHT40 | I2C | 1 (onboard) | -40°C to +125°C, 0-100% RH |
| DS18B20 | 1-Wire | Multiple (shared bus) | -55°C to +125°C |
| MAX31855 | SPI | 3 | -270°C to +1372°C (K-type) |
| QNHCK2-16 | Analog | 5 | 0-30A AC/DC current clamps |
| Piezo Buzzer | GPIO | 1 (onboard) | Audible alarms (85dB @ 10cm) |
| 12V LED Outputs | GPIO | 2 | Dashboard panel indicators |
| 12V Switch Inputs | GPIO | 3 | Toggle switch inputs |

### Connectivity

- **WiFi:** 802.11ax (2.4GHz), WPA3 support
- **Protocol:** MQTT over TCP/IP
- **Programming:** USB-C (native ESP32-C6 USB Serial/JTAG)

## Repository Structure

```text
esp32-marine-sensorhub-v2/
├── README.md                 # This file
├── Hardware.md              # Complete hardware design document
├── Requirements.md          # KiCad schematic requirements
├── hardware/
│   ├── KICAD_SCHEMATIC_GUIDE.md  # Step-by-step build guide
│   └── mshv2/               # KiCad project files
│       ├── mshv2.kicad_pro
│       └── mshv2.kicad_sch
├── firmware/                # (TBD) ESP-IDF firmware
└── docs/                    # Additional documentation
```

## Getting Started

### For Hardware Developers

1. **Review the design:**
   - Read [Hardware.md](Hardware.md) for complete circuit details
   - Check [Requirements.md](Requirements.md) for specifications

2. **Build the schematic:**
   - Follow [hardware/KICAD_SCHEMATIC_GUIDE.md](hardware/KICAD_SCHEMATIC_GUIDE.md)
   - Use KiCad 9.0 or later
   - Open `hardware/mshv2/mshv2.kicad_pro`

3. **Order components:**
   - See BOM in [Hardware.md](Hardware.md#bill-of-materials-bom)
   - Estimated cost: ~$35.85 per board (components only)

### For Firmware Developers

**Coming soon** - firmware development will use ESP-IDF:

- MQTT client implementation
- Sensor polling and calibration
- WiFi connection management
- Watchdog and fault detection

## Technical Highlights

### Dual Power Design

The board features an innovative dual power system that allows operation from
either 12V marine power or USB-C:

```text
12V Path: 12V → LM2596S → 3.3V → D_BUCK → +3V3 rail
USB Path: 5V VBUS → AMS1117 → 3.3V → D_USB → +3V3 rail
```

Schottky diodes (B5819W) automatically select the power source without conflict
or backfeeding.

### Current Clamp Signal Conditioning

Each of the 5 current clamp channels features precision signal conditioning:

- Input protection (1kΩ series resistor)
- Voltage divider (5V → 3.3V range)
- RC low-pass filter (1.6kHz cutoff)
- Unity-gain op-amp buffer (MCP6004) for all channels
- Direct connection to ESP32 ADC (GPIO0-4)

Two MCP6004 quad op-amps provide buffering:

- U5 (channels 1-4)
- U6 (channel 5 only, U6B-D unused)

Note: GPIO5 repurposed for piezo buzzer (6th clamp expansion not available).

### Dashboard I/O Interface

The board provides comprehensive dashboard control capabilities:

**Piezo Buzzer (GPIO5):**

- Murata PKLCS1212E4001-R1 (SMD) or PKM13EPYH4000-A0 (TH)
- NPN transistor driver (2N3904/BC547)
- 85dB @ 10cm, 4kHz operating frequency
- Software-controlled for alarms and alerts

**12V LED Outputs (GPIO11, GPIO15):**

- N-channel MOSFET drivers (2N7002)
- For remote panel-mount indicator LEDs
- Supports long wire runs (10+ feet)
- Suggested colors: Red (alarm), Green (normal)

**12V Toggle Switch Inputs (GPIO16, GPIO17, GPIO23):**

- Voltage dividers (10kΩ/3.3kΩ) for 12V→3.3V level shifting
- Zener diode protection (BZX84C3V3, 3.3V)
- For marine-grade toggle switches (SPST, ON-OFF)
- 3.0V when switch closed (HIGH), 0V when open (LOW)

### Marine Environment Protection

- Reverse polarity protection (MBRS340 Schottky diode)
- Voltage spike protection (SMBJ15A TVS diode)
- Conformal coating compatible PCB design
- Wide trace spacing for moisture resistance
- Mounting holes for secure installation

## Bill of Materials

Estimated component cost: **~$35.85** per board (quantity 1-10)

### Key Components

- ESP32-C6-WROOM-1-N8: $2.50
- SHT40 temperature/humidity sensor: $4.00
- MAX31855 thermocouple amplifier (3×): $15.00
- MCP6004 quad op-amp (2×): $1.00
- LM2596 buck converter module: $2.00
- AMS1117-3.3 LDO regulator: ~$0.50
- Piezo buzzer (Murata): $1.50
- Dashboard I/O components (2× MOSFETs, 3× Zeners, transistor): ~$0.35
- Passive components & connectors: ~$9.00

See [Hardware.md](Hardware.md#bill-of-materials-bom) for complete BOM.

## Design Documents

- **[Hardware.md](Hardware.md)** - Complete hardware design, schematics,
  and specifications
- **[Requirements.md](Requirements.md)** - KiCad schematic requirements and
  PCB guidelines
- **[KICAD_SCHEMATIC_GUIDE.md](hardware/KICAD_SCHEMATIC_GUIDE.md)** -
  Step-by-step schematic creation guide

## MQTT Topic Structure

```text
boat/sensors/{location}/{sensor_type}

Examples:
  boat/sensors/engine_room/temperature
  boat/sensors/engine_room/wet_exhaust_temp
  boat/sensors/galley/fridge_temp
  boat/sensors/salon/humidity
  boat/sensors/battery_bank/current_1
```

## Safety Considerations

### Important Safety Information

⚠️ **Warning:**

- This board is designed for 12V automotive/marine applications
- Ensure proper fusing and circuit protection in your installation
- High-temperature sensors must be installed per manufacturer specifications
- This design has **not** been certified for safety-critical applications
- Implement proper watchdog and fault detection in firmware
- Use conformal coating for marine environments
- Regular inspection and maintenance required

## Contributing

This is an open-source hardware project. Contributions are welcome!

- Report issues or suggest improvements via GitHub Issues
- Submit pull requests for documentation or design improvements
- Share your build photos and experiences

## License

This project uses a dual licensing approach to ensure both hardware and
software remain free and open:

### Hardware (Schematics, PCB, Design Files)

#### CERN Open Hardware Licence Version 2 - Strongly Reciprocal (CERN-OHL-S-2.0)

- All KiCad files, schematics, PCB layouts, and manufacturing files
- Hardware design documentation (Hardware.md, Requirements.md)
- Copyleft license - derivative works must be shared under same terms
- Commercial use permitted
- Full license: <https://ohwr.org/cern_ohl_s_v2.txt>

### Software/Firmware

#### GNU General Public License v3.0 (GPLv3)

- All firmware source code (firmware/ directory)
- Build scripts and automation tools
- Copyleft license ensuring software freedom
- Full license: <https://www.gnu.org/licenses/gpl-3.0.html>

### Documentation

#### Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA-4.0)

- README, guides, and markdown documentation
- Must provide attribution and share-alike
- Full license: <https://creativecommons.org/licenses/by-sa/4.0/>

See the [LICENSE](LICENSE) file for complete terms and conditions.

## Acknowledgments

- ESP32-C6 datasheet and design guidelines from Espressif Systems
- KiCad open-source EDA software
- Marine sensor community feedback and requirements

## Contact & Support

- **GitHub Repository:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2>
- **Issues:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2/issues>
- **Discussions:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2/discussions>

---

Built with ❤️ for the marine community
