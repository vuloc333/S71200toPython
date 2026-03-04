import xml.etree.ElementTree as ET
import os

class PLCConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.connection = {}
        # Phân tách rõ ràng Read và Write theo chuẩn SOLID
        self.read_map = {"bits": {}, "ints": {}}
        self.write_map = {"bits": {}, "ints": {}}
        
    def load(self):
        if not os.path.exists(self.file_path):
            print(f"Error: {self.file_path} not found.")
            return False

        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            # Connection
            conn = root.find("Connection")
            if conn is not None:
                self.connection = {
                    "IP": conn.find("IP").text,
                    "Rack": int(conn.find("Rack").text),
                    "Slot": int(conn.find("Slot").text),
                    "DB_Number": int(conn.find("DB_Number").text)
                }

            # Parse Read Regions
            for var in root.findall(".//readbits/Var"):
                self.read_map["bits"][var.get("name")] = {"byte": int(var.get("byte")), "bit": int(var.get("bit"))}
            for var in root.findall(".//ReadInts/Var"):
                self.read_map["ints"][var.get("name")] = {"byte": int(var.get("byte"))}

            # Parse Write Regions
            for var in root.findall(".//writebits/Var"):
                self.write_map["bits"][var.get("name")] = {"byte": int(var.get("byte")), "bit": int(var.get("bit"))}
            for var in root.findall(".//WriteInts/Var"):
                self.write_map["ints"][var.get("name")] = {"byte": int(var.get("byte"))}

            return True
        except Exception as e:
            print(f"XML Error: {e}")
            return False