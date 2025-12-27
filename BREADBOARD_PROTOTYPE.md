# Breadboard Prototype Guide - ESP32-C6 Marine Sensor Hub

This guide walks you through building a soldered breadboard prototype of the
Marine Sensor Hub to validate the design before ordering custom PCBs.

## Why Prototype First?

- **Validate the design** before spending money on custom PCBs
- **Test sensor interfacing** and signal conditioning circuits
- **Develop firmware** in parallel with hardware refinement
- **Identify issues** early in the design process
- **Prove the concept** to stakeholders or for yourself

## Recommended Development Board

### Option 1: ESP32-C6-DevKitC-1-N8 (Recommended)

**Why this board:**

- Official Espressif board with excellent documentation
- Exposes all GPIO pins needed for your design
- Has USB-C (native ESP32-C6 USB) for programming
- Includes reset and boot buttons
- Available from Adafruit, Mouser, DigiKey (~$7-10)
- Compatible pinout with other ESP32-C6 boards

**Key Features:**

- ESP32-C6-WROOM-1-N8 module (8MB flash)
- USB-C connector (native USB Serial/JTAG)
- All GPIO broken out to headers
- 3.3V and GND pins accessible
- Built-in RGB LED (GPIO8)

### Option 2: ESP32-C6 Super Mini

**Pros:** Very compact, cheap (~$3-5)
**Cons:** Fewer broken-out pins, harder to work with on breadboard

### Option 3: SparkFun Qwiic Pocket Dev Board

**Pros:** Qwiic connector for I2C, compact, good documentation
**Cons:** More expensive (~$18), not all pins broken out

## Prototyping Strategy

### Phase 1: Core System (Start Here)

Build and test the minimal system first:

1. ✅ ESP32-C6 dev board (power from USB-C)
2. ✅ SHT40 I2C sensor
3. ✅ Basic firmware (WiFi, MQTT, sensor reading)

**Goal:** Prove WiFi connectivity and I2C communication work

### Phase 2: Current Clamp Channels (1-2 channels)

Add signal conditioning for testing:

1. Build ONE current clamp channel on breadboard
2. Test ADC reading and voltage divider
3. Add op-amp buffer if needed
4. Validate with actual current clamp sensor

**Goal:** Prove current sensing circuit works correctly

### Phase 3: Temperature Sensors

Add external temperature sensing:

1. DS18B20 1-Wire sensor (1 channel to test)
2. MAX31855 thermocouple interface (if needed for your application)

**Goal:** Validate 1-Wire and SPI sensor interfaces

### Phase 4: Full Integration

Only after testing individual subsystems:

1. Add remaining current clamp channels
2. Add remaining DS18B20 sensors
3. Test all sensors simultaneously
4. Load test (measure power consumption)

## Bill of Materials - Prototype

### Development Board

| Item | Part | Source | Price |
| ---- | ---- | ------ | ----- |
| ESP32-C6 Dev Board | ESP32-C6-DevKitC-1-N8 | Adafruit #5672 | $9.95 |

### Prototyping Supplies

| Item | Quantity | Notes |
| ---- | -------- | ----- |
| Solderable breadboard | 1-2 | 830 tie-point or similar |
| 22AWG solid wire | 1 spool | For breadboard jumpers |
| Pin headers (male) | 2×20 pins | For dev board |
| Screw terminals | 6-8 | 2-pin, 2.54mm pitch (or use jumper wires) |

### Phase 1: Core Components

| Item | Part Number | Quantity | Source |
| ---- | ----------- | -------- | ------ |
| SHT40 sensor | SHT40 breakout | 1 | Adafruit/SparkFun |
| Pullup resistors | 4.7kΩ | 2 | Any supplier |

**Note:** Most ESP32-C6 dev boards have I2C pullups already, so you may not
need external ones.

### Phase 2: Current Clamp Circuit (Per Channel)

| Component | Value | Quantity (per channel) | Notes |
| --------- | ----- | ---------------------- | ----- |
| Series resistor | 1kΩ | 1 | Protection |
| Voltage divider R1 | 10kΩ | 1 | Top of divider |
| Voltage divider R2 | 20kΩ | 1 | Bottom to GND |
| Filter resistor | 1kΩ | 1 | RC filter |
| Filter capacitor | 0.1µF ceramic | 1 | RC filter |
| Op-amp | MCP6004 | 1 (for 4 channels) | Quad op-amp |
| Decoupling cap | 0.1µF | 1 | For op-amp |
| Current clamp | QNHCK2-16 | 1 | 30A, 0-5V output |

Start with 1-2 channels, then expand.

### Phase 3 Components: Temperature Sensors

| Item | Quantity | Notes |
| ---- | -------- | ----- |
| DS18B20 waterproof probe | 1 | Test with one first |
| 4.7kΩ pullup resistor | 1 | 1-Wire bus |
| MAX31855 breakout | 1 | If testing thermocouples |
| K-type thermocouple | 1 | Optional |

### Tools Needed

- Soldering iron (temperature controlled)
- Solder (lead-free recommended)
- Wire strippers
- Multimeter
- Helping hands/PCB holder
- Flush cutters
- USB-C cable (for programming)

## Breadboard Layout

### Power Distribution Strategy

**DO NOT use 12V on the breadboard** - too dangerous and unnecessary for
prototype. Instead:

- Power everything from the dev board's **3.3V** pin
- Dev board powered from **USB-C**
- This is safe and sufficient for testing

**Power Rails:**

```text
Top rail:    +3V3 (from dev board 3.3V pin)
Bottom rail: GND (from dev board GND pin)
```

### Section Layout (Left to Right)

```text
[ESP32-C6 Dev Board] | [SHT40] | [Current Clamp Circuits] | [1-Wire] | [SPI]
```

## Wiring Guide

### Phase 1: Core System

#### ESP32-C6 Dev Board Setup

1. **Mount dev board:**
   - Solder male pin headers to dev board (if not pre-installed)
   - Insert into breadboard or use female jumper wires

2. **Power distribution:**
   - Connect dev board **3V3 pin** → breadboard **+3V3 rail**
   - Connect dev board **GND pin** → breadboard **GND rail**

3. **USB connection:**
   - Connect USB-C cable to dev board
   - This provides power and programming interface

#### SHT40 I2C Sensor

**Connections:**

```text
SHT40 VDD → +3V3 rail
SHT40 GND → GND rail
SHT40 SDA → ESP32-C6 GPIO6
SHT40 SCL → ESP32-C6 GPIO7
```

**I2C Pullups:**

Most dev boards and SHT40 breakouts have pullups already. If not:

```text
+3V3 → 4.7kΩ → GPIO6 (SDA)
+3V3 → 4.7kΩ → GPIO7 (SCL)
```

### Phase 2: Current Clamp Signal Conditioning

Build ONE channel first to test:

#### Channel 1 Wiring

```text
Current Clamp Input (screw terminal)
  Pin 1 (Signal) → 1kΩ (R_SER) → Junction A
  Pin 2 (GND)    → GND rail

Junction A:
  → 10kΩ (R_DIV1) → Junction B

Junction B:
  → 20kΩ (R_DIV2) → GND rail
  → 1kΩ (R_FILT)  → Junction C

Junction C:
  → 0.1µF cap → GND
  → MCP6004 Pin 3 (IN+)

MCP6004 Unity Gain Buffer:
  Pin 3 (IN+) ← from Junction C
  Pin 2 (IN-) ← connect to Pin 1 (OUT)
  Pin 1 (OUT) → ESP32-C6 GPIO0 (ADC1_CH0)
  Pin 4 (V-)  → GND rail
  Pin 11 (V+) → +3V3 rail

Add 0.1µF decoupling cap between Pin 11 and Pin 4
```

**Testing without op-amp (simplified):**

If you want to test without the MCP6004 first:

```text
Current Clamp → 1kΩ → Voltage Divider (10kΩ/20kΩ) → RC Filter → ESP32 GPIO0
```

This will work but may have loading issues with high-impedance sensors.

### Phase 3A: DS18B20 1-Wire Sensor

```text
DS18B20 (3 wires in cable):
  Red    → +3V3 rail
  Black  → GND rail
  Yellow → 4.7kΩ → +3V3 (pullup)
  Yellow → ESP32-C6 GPIO8 (1-Wire data)
```

**Multiple Sensors:**

You can add up to 3 DS18B20 on separate GPIO pins, or use them all on one
1-Wire bus (all yellow wires together to same GPIO).

### Phase 3B: MAX31855 Thermocouple (SPI)

If using a MAX31855 breakout board:

```text
MAX31855 Breakout:
  VCC  → +3V3 rail
  GND  → GND rail
  SCK  → ESP32-C6 GPIO19 (SPI_SCK)
  SO   → ESP32-C6 GPIO18 (SPI_MISO)
  CS   → ESP32-C6 GPIO20 (SPI_CS)
  T+   → Thermocouple + (yellow wire)
  T-   → Thermocouple - (red wire)
```

## Assembly Steps

### Step 1: Power Rails

1. **Strip and tin wires** for power distribution
2. **Solder +3V3 rail** across top of breadboard
3. **Solder GND rail** across bottom of breadboard
4. **Test continuity** with multimeter

### Step 2: Mount Dev Board

1. **Solder pin headers** to dev board (if needed)
2. **Position dev board** on left side of breadboard
3. **Solder or use socket** to secure it
4. **Connect power:**
   - Dev board 3V3 → breadboard +3V3 rail
   - Dev board GND → breadboard GND rail

### Step 3: SHT40 Sensor

1. **Position SHT40** breakout near dev board
2. **Solder power connections** (VDD, GND)
3. **Solder I2C lines** (SDA to GPIO6, SCL to GPIO7)
4. **Test with multimeter:**
   - Verify 3.3V on VDD
   - Verify continuity on I2C lines

### Step 4: Current Clamp Circuit (Start with 1)

1. **Mount components** for one channel:
   - Resistors (1kΩ, 10kΩ, 20kΩ, 1kΩ)
   - Capacitor (0.1µF)
   - MCP6004 (if using)
   - Screw terminal for input

2. **Solder signal chain** following the wiring diagram above

3. **Add decoupling cap** for MCP6004 (0.1µF between V+ and GND)

4. **Connect to ESP32-C6:**
   - Op-amp output → GPIO0 (ADC1_CH0)

5. **Test without current clamp:**
   - Apply 0V to input: should read ~0V on ADC
   - Apply 3.3V to input: should read ~3.3V on ADC

### Step 5: Test Each Subsystem

Before adding more:

1. **Flash firmware** to test I2C (SHT40)
2. **Flash firmware** to test ADC (current clamp)
3. **Verify readings** make sense
4. **Debug issues** before proceeding

### Step 6: Expand (Only After Testing)

1. Add 2nd current clamp channel (same circuit, GPIO1)
2. Add 3rd current clamp channel (GPIO2), etc.
3. Add DS18B20 sensors (GPIO8, 10, 11)
4. Add MAX31855 if needed (SPI interface)

## Testing Procedures

### Test 1: Power and Basic Operation

1. **Connect USB-C** to dev board
2. **Verify power LED** on dev board lights up
3. **Measure voltages:**
   - Dev board 3V3 pin: 3.3V ±0.1V
   - Breadboard +3V3 rail: 3.3V ±0.1V
   - SHT40 VDD: 3.3V ±0.1V

### Test 2: I2C Communication (SHT40)

1. **Flash I2C scanner** firmware
2. **Verify SHT40 detected** at address 0x44
3. **Read temperature and humidity**
4. **Compare with reference** thermometer

### Test 3: ADC / Current Clamp

1. **Without current clamp connected:**
   - Input floating: should read ~mid-range (noise)
   - Input to GND: should read ~0V
   - Input to 3.3V: should read ~3.3V (or max ADC)

2. **With current clamp (no load):**
   - Should read ~1.65V (mid-scale, 0A)

3. **With current clamp (known load):**
   - Use resistive load and measure actual current with multimeter
   - Compare ADC reading to expected value
   - Calibrate if needed

### Test 4: 1-Wire (DS18B20)

1. **Flash 1-Wire test firmware**
2. **Read sensor ROM ID**
3. **Read temperature**
4. **Verify with ice bath** (0°C) or boiling water (100°C)

### Test 5: SPI (MAX31855)

1. **Flash SPI test firmware**
2. **Read thermocouple temperature**
3. **Verify cold junction compensation** works
4. **Test with ice bath** for accuracy

## Common Issues and Troubleshooting

### I2C Not Working

- **Check pullups:** Make sure 4.7kΩ resistors present (or on breakout)
- **Check wiring:** SDA and SCL not swapped?
- **Check voltage:** Is SHT40 getting 3.3V?
- **Check address:** Run I2C scanner, verify 0x44

### ADC Readings Wrong

- **Check voltage divider:** Measure voltage at op-amp input
- **Check op-amp power:** MCP6004 getting 3.3V?
- **Check feedback:** Op-amp output connected to IN-?
- **Calibrate:** Use known voltages to create calibration curve

### Current Clamp Reads Zero

- **Check clamp orientation:** Arrow should point to load
- **Check clamp power:** Some clamps need external power
- **Check AC vs DC:** QNHCK2-16 works for both, but verify mode
- **Check input protection:** 1kΩ series resistor might be wrong value

### 1-Wire Not Detecting Sensor

- **Check pullup:** 4.7kΩ required on data line
- **Check wiring:** Data, power, ground correct?
- **Check parasitic power mode:** DS18B20 might need VDD connected
- **Try another sensor:** Could be defective

## Next Steps After Prototype

Once your breadboard prototype is working:

1. **Document what works** and what doesn't
2. **Update schematic** based on findings
3. **Measure actual current draw** of full system
4. **Test power consumption** in different modes
5. **Develop firmware** fully before ordering PCBs
6. **Consider changes** to component values if needed

## Transitioning to PCB

After successful breadboard prototype:

- ✅ You've proven the design works
- ✅ Firmware is mostly complete
- ✅ You know actual power requirements
- ✅ Component values are verified
- 🚀 Ready to order custom PCBs!

**Update your KiCad schematic** with any changes discovered during
prototyping, then proceed with PCB layout.

## Cost Estimate - Breadboard Prototype

### Minimal Prototype (Phase 1)

- ESP32-C6 dev board: $10
- SHT40 breakout: $7
- Breadboard: $5
- Wire/headers: $5
- **Total: ~$27**

### Full Prototype (All Phases)

- ESP32-C6 dev board: $10
- SHT40 breakout: $7
- MCP6004 + passives: $5
- DS18B20 sensors (3): $12
- MAX31855 + thermocouple: $20
- Current clamps (2 for testing): $20
- Breadboard + supplies: $10
- **Total: ~$84**

**Recommendation:** Start with Phase 1 (~$27) to validate the concept before
investing in all sensors.

## Resources

- [ESP32-C6-DevKitC-1 User Guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/user_guide.html)
- [ESP32-C6 Super Mini Pinout](https://www.espboards.dev/esp32/esp32-c6-super-mini/)
- [SparkFun Qwiic Pocket Dev Board](https://www.sparkfun.com/sparkfun-qwiic-pocket-development-board-esp32-c6.html)
- [Adafruit ESP32-C6-DevKitC-1](https://www.adafruit.com/product/5672)

---

**Good luck with your prototype! Test incrementally and document everything.**
