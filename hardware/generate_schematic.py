#!/usr/bin/env python3
"""
KiCad Schematic Generator for ESP32-C6 Marine Sensor Board
Generates mshv2.kicad_sch file programmatically in KiCad 9.0 format (version 20250114)
"""

import uuid
from typing import List, Tuple, Dict

# KiCad 9.0 uses millimeters directly as the coordinate unit
def mm_to_units(mm: float) -> float:
    """Convert millimeters to KiCad units (KiCad 9.0 uses mm directly)"""
    return float(mm)

class KiCadSchematic:
    def __init__(self, project_uuid: str = "71e681ae-2e40-4eed-9bbd-6e93cdfb5938"):
        self.project_uuid = project_uuid
        self.symbols = []
        self.wires = []
        self.labels = []
        self.global_labels = []
        self.junctions = []
        self.no_connects = []
        self.lib_symbols = {}
        self.power_symbols = []
        self.text_annotations = []

    def add_symbol(self, ref: str, value: str, lib_id: str, x: float, y: float,
                   unit: int = 1, properties: Dict = None, mirror_x: bool = False,
                   rotation: int = 0):
        """Add a component symbol to the schematic"""
        sym_uuid = str(uuid.uuid4())

        # Convert position to KiCad units
        x_units = mm_to_units(x)
        y_units = mm_to_units(y)

        # Build property list
        props = {
            "Reference": ref,
            "Value": value,
        }
        if properties:
            props.update(properties)

        symbol = {
            "uuid": sym_uuid,
            "lib_id": lib_id,
            "reference": ref,
            "value": value,
            "unit": unit,
            "x": x_units,
            "y": y_units,
            "mirror_x": mirror_x,
            "rotation": rotation,
            "properties": props
        }

        self.symbols.append(symbol)
        return sym_uuid

    def add_wire(self, x1: float, y1: float, x2: float, y2: float, stroke_width: float = 0):
        """Add a wire connection"""
        self.wires.append({
            "x1": mm_to_units(x1),
            "y1": mm_to_units(y1),
            "x2": mm_to_units(x2),
            "y2": mm_to_units(y2),
            "stroke": stroke_width
        })

    def add_label(self, text: str, x: float, y: float, angle: int = 0):
        """Add a net label"""
        self.labels.append({
            "text": text,
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "uuid": str(uuid.uuid4()),
            "angle": angle
        })

    def add_global_label(self, text: str, x: float, y: float, shape: str = "input", angle: int = 0):
        """Add a global label (for power, etc.)"""
        self.global_labels.append({
            "text": text,
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "uuid": str(uuid.uuid4()),
            "shape": shape,
            "angle": angle
        })

    def add_power_symbol(self, symbol_type: str, x: float, y: float, rotation: int = 0):
        """Add a power symbol (+3V3, GND, etc.)"""
        self.power_symbols.append({
            "type": symbol_type,
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "uuid": str(uuid.uuid4()),
            "rotation": rotation
        })

    def add_junction(self, x: float, y: float):
        """Add a junction (connection point) at coordinates"""
        self.junctions.append({
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "uuid": str(uuid.uuid4())
        })

    def add_no_connect(self, x: float, y: float):
        """Add a no-connect flag"""
        self.no_connects.append({
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "uuid": str(uuid.uuid4())
        })

    def add_text(self, text: str, x: float, y: float, size: float = 1.27):
        """Add text annotation"""
        self.text_annotations.append({
            "text": text,
            "x": mm_to_units(x),
            "y": mm_to_units(y),
            "size": size,
            "uuid": str(uuid.uuid4())
        })

    def generate_sexpr(self) -> str:
        """Generate the complete KiCad S-expression schematic"""

        # Due to the complexity of generating full KiCad S-expressions with proper
        # symbol definitions, pin connections, etc., we'll create a simplified but
        # functional schematic that can be opened and edited in KiCad

        sexpr = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid {self.project_uuid})
\t(paper "A4" portrait)
\t
\t(title_block
\t\t(title "ESP32-C6 Marine Multi-Sensor Board")
\t\t(date "{{}}")
\t\t(rev "v1.0")
\t\t(comment 1 "6x Current Clamp Sensors (30A)")
\t\t(comment 2 "3x DS18B20 Temperature + 1x K-Type Thermocouple")
\t\t(comment 3 "SHT40 Humidity/Temperature Sensor")
\t\t(comment 4 "Marine Environment - 12VDC Input")
\t)
\t
\t(lib_symbols
'''

        # Add symbol library definitions (abbreviated - KiCad will resolve from standard libs)
        lib_symbols_data = self._generate_lib_symbols()
        sexpr += lib_symbols_data

        sexpr += "\t)\n\n"

        # Add all schematic elements
        for sym in self.symbols:
            sexpr += self._format_symbol(sym)

        for wire in self.wires:
            sexpr += self._format_wire(wire)

        for label in self.labels:
            sexpr += self._format_label(label)

        for pwr in self.power_symbols:
            sexpr += self._format_power_symbol(pwr)

        for junc in self.junctions:
            sexpr += self._format_junction(junc)

        for nc in self.no_connects:
            sexpr += self._format_no_connect(nc)

        for text in self.text_annotations:
            sexpr += self._format_text(text)

        # Close the schematic
        sexpr += '''\t
\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
'''

        return sexpr

    def _generate_lib_symbols(self) -> str:
        """Generate lib_symbols section with required component definitions"""
        # Note: KiCad needs actual symbol definitions here for symbols to display properly
        # For now, this returns empty - user must open in KiCad GUI and use
        # "Tools > Update Symbols from Library" or let KiCad auto-rescue symbols
        # A future enhancement would be to read symbols from KiCad's .kicad_sym library files
        # and embed them here
        return ""

    def _format_symbol(self, sym: Dict) -> str:
        """Format a symbol in S-expression format"""
        mirror_str = " (mirror x)" if sym["mirror_x"] else ""

        # Format properties with proper structure
        ref_val = sym["properties"].get("Reference", sym["reference"])
        value_val = sym["properties"].get("Value", sym["value"])

        sexpr = f'''\t(symbol (lib_id "{sym["lib_id"]}") (at {sym["x"]:.4f} {sym["y"]:.4f} {sym["rotation"]}){mirror_str}
\t\t(unit {sym["unit"]})
\t\t(uuid {sym["uuid"]})
\t\t(property "Reference" "{ref_val}"
\t\t\t(at {sym["x"] + 2.54:.4f} {sym["y"] - 1.27:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{value_val}"
\t\t\t(at {sym["x"] + 2.54:.4f} {sym["y"] + 1.27:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {sym["x"]:.4f} {sym["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at {sym["x"]:.4f} {sym["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
'''

        # Add any additional properties (skip Footprint and Datasheet as they're already added)
        for key, val in sym["properties"].items():
            if key not in ["Reference", "Value", "Footprint", "Datasheet"]:
                sexpr += f'''\t\t(property "{key}" "{val}"
\t\t\t(at {sym["x"]:.4f} {sym["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
'''

        # Add pins section (empty for now, KiCad will use library definition)
        sexpr += '\t\t(instances\n'
        sexpr += f'\t\t\t(project "mshv2"\n'
        sexpr += f'\t\t\t\t(path "/"\n'
        sexpr += f'\t\t\t\t\t(reference "{ref_val}") (unit {sym["unit"]})\n'
        sexpr += '\t\t\t\t)\n'
        sexpr += '\t\t\t)\n'
        sexpr += '\t\t)\n'
        sexpr += '\t)\n'

        return sexpr

    def _format_wire(self, wire: Dict) -> str:
        """Format a wire in S-expression format"""
        stroke = wire["stroke"] if wire["stroke"] > 0 else 0
        return f'''\t(wire (pts (xy {wire["x1"]:.4f} {wire["y1"]:.4f}) (xy {wire["x2"]:.4f} {wire["y2"]:.4f}))
\t\t(stroke (width {stroke}) (type default))
\t\t(uuid {str(uuid.uuid4())})
\t)
'''

    def _format_label(self, label: Dict) -> str:
        """Format a label in S-expression format"""
        return f'''\t(label "{label["text"]}" (at {label["x"]:.4f} {label["y"]:.4f} {label["angle"]})
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid {label["uuid"]})
\t)
'''

    def _format_power_symbol(self, pwr: Dict) -> str:
        """Format a power symbol"""
        lib_map = {
            "+3V3": "power:+3V3",
            "GND": "power:GND",
            "+12V": "power:+12V",
            "AGND": "power:GNDA"
        }
        lib_id = lib_map.get(pwr["type"], "power:GND")

        return f'''\t(symbol (lib_id "{lib_id}") (at {pwr["x"]:.4f} {pwr["y"]:.4f} {pwr["rotation"]})
\t\t(unit 1)
\t\t(uuid {pwr["uuid"]})
\t\t(property "Reference" "#PWR?"
\t\t\t(at {pwr["x"]:.4f} {pwr["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Value" "{pwr["type"]}"
\t\t\t(at {pwr["x"]:.4f} {pwr["y"] + 2.54:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {pwr["x"]:.4f} {pwr["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at {pwr["x"]:.4f} {pwr["y"]:.4f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(instances
\t\t\t(project "mshv2"
\t\t\t\t(path "/"
\t\t\t\t\t(reference "#PWR?") (unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
'''

    def _format_junction(self, junc: Dict) -> str:
        """Format a junction"""
        return f'''\t(junction (at {junc["x"]:.4f} {junc["y"]:.4f}) (diameter 0) (color 0 0 0 0)
\t\t(uuid {junc["uuid"]})
\t)
'''

    def _format_no_connect(self, nc: Dict) -> str:
        """Format a no-connect symbol"""
        return f'''\t(no_connect (at {nc["x"]:.4f} {nc["y"]:.4f}) (uuid {nc["uuid"]}))
'''

    def _format_text(self, text: Dict) -> str:
        """Format text annotation"""
        return f'''\t(text "{text["text"]}" (at {text["x"]:.4f} {text["y"]:.4f} 0)
\t\t(effects (font (size {text["size"]:.2f} {text["size"]:.2f})) (justify left bottom))
\t\t(uuid {text["uuid"]})
\t)
'''


def generate_marine_sensor_schematic() -> str:
    """
    Generate the complete ESP32-C6 Marine Sensor Board schematic
    """

    sch = KiCadSchematic()

    # Layout coordinates (in mm from top-left)
    # A4 page is 210mm x 297mm in KiCad 9.0
    # Standard schematic area is roughly 20mm to 180mm horizontal, 20mm to 270mm vertical
    # We'll use a comfortable starting position

    base_x = 40  # Start 40mm from left edge
    base_y = 40  # Start 40mm from top edge

    print("Generating schematic...")
    print("1. Adding power supply section...")

    # ===== POWER SUPPLY SECTION (Top Left) =====
    pwr_x = base_x
    pwr_y = base_y

    # J_PWR - 12V Input
    sch.add_symbol("J_PWR", "Screw_Terminal_01x02", "Connector:Screw_Terminal_01x02",
                   pwr_x, pwr_y, properties={"Datasheet": "~", "Description": "12V Power Input"})

    # D1 - MBRS340 Reverse polarity protection
    sch.add_symbol("D1", "MBRS340", "Diode:MBRS340",
                   pwr_x + 20, pwr_y, properties={"Description": "Reverse Polarity Protection"})

    # TVS1 - SMBJ15A TVS Diode (using generic D_TVS symbol)
    sch.add_symbol("TVS1", "SMBJ15A", "Device:D_TVS",
                   pwr_x + 40, pwr_y + 10, rotation=90,
                   properties={"Description": "Voltage Spike Protection", "Manufacturer_Part_Number": "SMBJ15A"})

    # C1 - 100uF/25V input capacitor
    sch.add_symbol("C1", "100uF", "Device:C_Polarized",
                   pwr_x + 60, pwr_y, properties={"Voltage": "25V", "Description": "Input filter cap"})

    # U1 - LM2596 Buck Converter (using generic regulator symbol)
    sch.add_symbol("U1", "LM2596S-3.3", "Regulator_Switching:LM2596S-3.3",
                   pwr_x + 80, pwr_y + 10, properties={"Description": "12V to 3.3V Buck Converter"})

    # C2 - 100uF/10V output capacitor
    sch.add_symbol("C2", "100uF", "Device:C_Polarized",
                   pwr_x + 100, pwr_y, properties={"Voltage": "10V", "Description": "Output filter cap"})

    # C3 - 10uF ceramic
    sch.add_symbol("C3", "10uF", "Device:C",
                   pwr_x + 110, pwr_y, properties={"Description": "Output filter cap"})

    # C4 - 0.1uF ceramic decoupling
    sch.add_symbol("C4", "0.1uF", "Device:C",
                   pwr_x + 120, pwr_y, properties={"Description": "Decoupling cap"})

    # Power indicator LED
    sch.add_symbol("D_PWR", "LED", "Device:LED",
                   pwr_x + 130, pwr_y, properties={"Description": "Power indicator"})
    sch.add_symbol("R_PWR", "1k", "Device:R",
                   pwr_x + 140, pwr_y, properties={"Description": "LED current limit"})

    # Add power symbols
    sch.add_power_symbol("+12V", pwr_x, pwr_y - 10)
    sch.add_power_symbol("GND", pwr_x, pwr_y + 20)
    sch.add_power_symbol("+3V3", pwr_x + 130, pwr_y - 10)

    # Add labels for power section - labels auto-connect in KiCad
    sch.add_label("VIN_12V", pwr_x + 5, pwr_y)  # J_PWR output
    sch.add_label("VIN_12V", pwr_x + 18, pwr_y)  # D1 input
    sch.add_label("V_PROT", pwr_x + 22, pwr_y)  # D1 output
    sch.add_label("V_PROT", pwr_x + 40, pwr_y)  # TVS1 connection
    sch.add_label("V_PROT", pwr_x + 58, pwr_y)  # C1 input
    sch.add_label("V_PROT", pwr_x + 78, pwr_y + 5)  # Buck input
    sch.add_label("+3V3_OUT", pwr_x + 82, pwr_y + 15)  # Buck output
    sch.add_label("+3V3_OUT", pwr_x + 98, pwr_y)  # C2 connection
    sch.add_label("+3V3_OUT", pwr_x + 108, pwr_y)  # C3 connection
    sch.add_label("+3V3_OUT", pwr_x + 118, pwr_y)  # C4 connection

    print("2. Adding ESP32-C6 core circuit...")

    # ===== ESP32-C6 CORE SECTION (Center) =====
    esp_x = base_x + 50
    esp_y = base_y + 50

    # U2 - ESP32-C6-MINI-1
    sch.add_symbol("U2", "ESP32-C6-MINI-1", "RF_Module:ESP32-C6-MINI-1",
                   esp_x, esp_y, properties={"Description": "ESP32-C6 WiFi 6 Module"})

    # EN circuit
    sch.add_symbol("R_EN", "10k", "Device:R",
                   esp_x - 20, esp_y - 15, properties={"Description": "EN pullup"})
    sch.add_symbol("C_EN", "0.1uF", "Device:C",
                   esp_x - 20, esp_y - 5, properties={"Description": "EN filter cap"})
    sch.add_symbol("SW_RESET", "SW_Push", "Switch:SW_Push",
                   esp_x - 30, esp_y - 10, properties={"Description": "Reset button"})

    # BOOT circuit
    sch.add_symbol("R_BOOT", "10k", "Device:R",
                   esp_x - 20, esp_y + 15, properties={"Description": "BOOT pullup"})
    sch.add_symbol("SW_BOOT", "SW_Push", "Switch:SW_Push",
                   esp_x - 30, esp_y + 20, properties={"Description": "Boot button"})

    # Add power symbols for ESP32
    sch.add_power_symbol("+3V3", esp_x - 10, esp_y - 20)
    sch.add_power_symbol("GND", esp_x - 10, esp_y + 30)

    # GPIO labels (these would connect to ESP32 pins - simplified representation)
    gpio_labels = [
        ("ADC_CH0", esp_x + 30, esp_y),
        ("ADC_CH1", esp_x + 30, esp_y + 3),
        ("ADC_CH2", esp_x + 30, esp_y + 6),
        ("ADC_CH3", esp_x + 30, esp_y + 9),
        ("ADC_CH4", esp_x + 30, esp_y + 12),
        ("ADC_CH5", esp_x + 30, esp_y + 15),
        ("I2C_SDA", esp_x + 30, esp_y + 20),
        ("I2C_SCL", esp_x + 30, esp_y + 23),
        ("1WIRE_1", esp_x + 30, esp_y + 26),
        ("1WIRE_2", esp_x + 30, esp_y + 29),
        ("1WIRE_3", esp_x + 30, esp_y + 32),
        ("SPI_SCK", esp_x + 30, esp_y + 36),
        ("SPI_MISO", esp_x + 30, esp_y + 39),
        ("SPI_CS_TC", esp_x + 30, esp_y + 42),
        ("LED_STATUS", esp_x + 30, esp_y + 46),
    ]

    for label, x, y in gpio_labels:
        sch.add_label(label, x, y)

    print("3. Adding I2C sensor (SHT40)...")

    # ===== SHT40 I2C SENSOR (Top Right) =====
    sht_x = base_x + 140
    sht_y = base_y + 30

    # U3 - SHT40 (using generic I2C sensor symbol)
    sch.add_symbol("U3", "SHT40", "Sensor_Humidity:SHT4x",
                   sht_x, sht_y, properties={"Description": "Temperature/Humidity Sensor", "Address": "0x44"})

    # I2C pullups
    sch.add_symbol("R_SDA_PU", "4.7k", "Device:R",
                   sht_x - 10, sht_y - 10, properties={"Description": "I2C SDA pullup"})
    sch.add_symbol("R_SCL_PU", "4.7k", "Device:R",
                   sht_x - 10, sht_y - 5, properties={"Description": "I2C SCL pullup"})

    # Decoupling cap
    sch.add_symbol("C_SHT40", "0.1uF", "Device:C",
                   sht_x + 10, sht_y + 10, properties={"Description": "Decoupling cap"})

    # Power and labels
    sch.add_power_symbol("+3V3", sht_x, sht_y - 15)
    sch.add_power_symbol("GND", sht_x, sht_y + 15)

    # I2C connection labels - place near sensor and pullup pins
    sch.add_label("I2C_SDA", sht_x - 12, sht_y)
    sch.add_label("I2C_SCL", sht_x - 12, sht_y + 3)
    sch.add_label("I2C_SDA", sht_x - 8, sht_y - 10)  # At pullup
    sch.add_label("I2C_SCL", sht_x - 8, sht_y - 5)   # At pullup

    print("4. Adding 1-Wire temperature sensors (DS18B20 x3)...")

    # ===== DS18B20 1-WIRE SENSORS (Right Edge) =====
    ds_x = base_x + 170
    ds_y_base = base_y + 60

    for i in range(3):
        ds_y = ds_y_base + (i * 20)

        # Connector
        sch.add_symbol(f"J{i+1}", "Conn_01x03", "Connector_Generic:Conn_01x03",
                       ds_x, ds_y, properties={"Description": f"DS18B20 Sensor {i+1}"})

        # Pullup resistor
        sch.add_symbol(f"R_1W{i+1}_PU", "4.7k", "Device:R",
                       ds_x - 10, ds_y, properties={"Description": f"1-Wire pullup {i+1}"})

        # Labels for 1-Wire connections
        sch.add_power_symbol("+3V3", ds_x + 5, ds_y - 5)
        sch.add_power_symbol("GND", ds_x + 5, ds_y + 5)
        sch.add_label(f"1WIRE_{i+1}", ds_x - 12, ds_y)  # At connector
        sch.add_label(f"1WIRE_{i+1}", ds_x - 8, ds_y)   # At pullup

    print("5. Adding MAX31855 thermocouple interface...")

    # ===== MAX31855 THERMOCOUPLE INTERFACE (Bottom Right) =====
    max_x = base_x + 170
    max_y = base_y + 140

    # U4 - MAX31855
    sch.add_symbol("U4", "MAX31855KASA", "Sensor_Temperature:MAX31855KASA",
                   max_x, max_y, properties={"Description": "K-Type Thermocouple Amplifier"})

    # J4 - Thermocouple connector
    sch.add_symbol("J4", "Screw_Terminal_01x02", "Connector:Screw_Terminal_01x02",
                   max_x - 20, max_y, properties={"Description": "K-Type Thermocouple"})

    # Decoupling cap
    sch.add_symbol("C_MAX", "0.1uF", "Device:C",
                   max_x + 10, max_y + 10, properties={"Description": "Decoupling cap"})

    # Power and SPI labels for MAX31855
    sch.add_power_symbol("+3V3", max_x, max_y - 15)
    sch.add_power_symbol("AGND", max_x, max_y + 20)
    sch.add_label("SPI_SCK", max_x - 12, max_y + 5)
    sch.add_label("SPI_MISO", max_x - 12, max_y + 8)
    sch.add_label("SPI_CS_TC", max_x - 12, max_y + 11)

    print("6. Generating current clamp signal conditioning channels (6x)...")

    # ===== CURRENT CLAMP CHANNELS (Bottom Section) =====
    clamp_x_base = base_x
    clamp_y_base = base_y + 170
    clamp_spacing = 35  # Increased spacing between channels

    for ch in range(6):
        clamp_x = clamp_x_base + (ch * clamp_spacing)
        clamp_y = clamp_y_base

        # Connector
        sch.add_symbol(f"J{ch+5}", "Screw_Terminal_01x02", "Connector:Screw_Terminal_01x02",
                       clamp_x, clamp_y, properties={"Description": f"Current Clamp {ch+1}"})

        # Series resistor
        sch.add_symbol(f"R_SER_{ch+1}", "1k", "Device:R",
                       clamp_x, clamp_y + 10, properties={"Description": "Series resistor"})

        # Voltage divider
        sch.add_symbol(f"R_DIV1_{ch+1}", "10k", "Device:R",
                       clamp_x, clamp_y + 20, properties={"Description": "Voltage divider top"})
        sch.add_symbol(f"R_DIV2_{ch+1}", "20k", "Device:R",
                       clamp_x + 5, clamp_y + 25, rotation=90, properties={"Description": "Voltage divider bottom"})

        # RC filter
        sch.add_symbol(f"R_FILT_{ch+1}", "1k", "Device:R",
                       clamp_x, clamp_y + 35, properties={"Description": "Filter resistor"})
        sch.add_symbol(f"C_FILT_{ch+1}", "0.1uF", "Device:C",
                       clamp_x + 5, clamp_y + 40, rotation=90, properties={"Description": "Filter cap"})

        # Op-amp buffer (MCP6004 unit)
        # Channels 1-4 use U5 (units A-D), channels 5-6 use U6 (units A-B)
        if ch < 4:
            unit_letter = chr(ord('A') + ch)
            sch.add_symbol(f"U5{unit_letter}", "MCP6004", "Amplifier_Operational:MCP6004",
                           clamp_x, clamp_y + 50, unit=ch+1,
                           properties={"Description": f"Op-amp buffer {ch+1}"})
        else:
            unit_letter = chr(ord('A') + (ch - 4))
            sch.add_symbol(f"U6{unit_letter}", "MCP6004", "Amplifier_Operational:MCP6004",
                           clamp_x, clamp_y + 50, unit=ch-3,
                           properties={"Description": f"Op-amp buffer {ch+1}"})

        # Labels for current clamp channel
        sch.add_label(f"CLAMP_{ch+1}_RAW", clamp_x - 10, clamp_y + 5)
        sch.add_label(f"ADC_CH{ch}", clamp_x + 10, clamp_y + 55)
        sch.add_power_symbol("GND", clamp_x + 10, clamp_y + 45)

    # Add op-amp power decoupling caps
    sch.add_symbol("C_U5_DEC", "0.1uF", "Device:C",
                   clamp_x_base + 60, clamp_y_base + 65,
                   properties={"Description": "U5 decoupling"})
    sch.add_symbol("C_U6_DEC", "0.1uF", "Device:C",
                   clamp_x_base + 150, clamp_y_base + 65,
                   properties={"Description": "U6 decoupling"})

    # Op-amp power symbols
    sch.add_power_symbol("+3V3", clamp_x_base + 60, clamp_y_base + 60)
    sch.add_power_symbol("GND", clamp_x_base + 60, clamp_y_base + 70)
    sch.add_power_symbol("+3V3", clamp_x_base + 150, clamp_y_base + 60)
    sch.add_power_symbol("GND", clamp_x_base + 150, clamp_y_base + 70)

    print("7. Adding status LED and programming header...")

    # ===== STATUS LED (Bottom Left) =====
    led_x = base_x
    led_y = base_y + 120

    sch.add_symbol("D_STATUS", "LED", "Device:LED",
                   led_x, led_y, properties={"Description": "Status LED"})
    sch.add_symbol("R_STATUS", "330", "Device:R",
                   led_x + 10, led_y, properties={"Description": "LED current limit"})

    sch.add_label("LED_STATUS", led_x - 10, led_y)
    sch.add_power_symbol("GND", led_x + 15, led_y + 5)

    # ===== PROGRAMMING HEADER (Optional) =====
    prog_x = base_x + 20
    prog_y = base_y + 130

    sch.add_symbol("J_PROG", "Conn_02x03_Odd_Even", "Connector_Generic:Conn_02x03_Odd_Even",
                   prog_x, prog_y, properties={"Description": "Programming Header"})

    sch.add_power_symbol("+3V3", prog_x - 5, prog_y - 5)
    sch.add_power_symbol("GND", prog_x + 10, prog_y + 5)

    # Add text annotations
    sch.add_text("Power Supply", pwr_x, pwr_y - 15, size=2.0)
    sch.add_text("ESP32-C6 Core", esp_x - 10, esp_y - 25, size=2.0)
    sch.add_text("Current Clamp Channels (6x 30A)", clamp_x_base, clamp_y_base - 10, size=2.0)
    sch.add_text("I2C Sensor", sht_x - 10, sht_y - 20, size=1.5)
    sch.add_text("1-Wire Sensors", ds_x - 10, ds_y_base - 10, size=1.5)
    sch.add_text("Thermocouple", max_x - 10, max_y - 20, size=1.5)

    print("8. Generating S-expression output...")

    return sch.generate_sexpr()


if __name__ == "__main__":
    print("=" * 60)
    print("ESP32-C6 Marine Sensor Board - Schematic Generator")
    print("=" * 60)
    print()

    schematic_content = generate_marine_sensor_schematic()

    output_file = "mshv2/mshv2.kicad_sch"

    print()
    print(f"Writing schematic to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(schematic_content)

    print()
    print("[OK] Schematic generation complete!")
    print()
    print("Next steps:")
    print("1. Open KiCad 9.0")
    print("2. Open the project: mshv2/mshv2.kicad_pro")
    print("3. Open the schematic: mshv2/mshv2.kicad_sch")
    print("4. Run Electrical Rules Check (ERC)")
    print("5. Assign footprints to components")
    print("6. Refine component placement and wiring as needed")
    print()
    print("=" * 60)
