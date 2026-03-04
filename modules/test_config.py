from config_loader import PLCConfigLoader

# Initialize loader
loader = PLCConfigLoader("config/io_map.xml") # Đường dẫn đến file của bạn

if loader.load():
    # Test connection info
    print(f"PLC IP: {loader.get_connection()['IP']}")
    
    # Test bit address lookup
    name = "bJOgFw01"
    addr = loader.get_bit_address(name)
    print(f"Address of {name}: Byte {addr[0]}, Bit {addr[1]}")