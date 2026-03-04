import snap7
from snap7.util import get_bool, get_int, set_bool, set_int

class PLC_Connect:
    def __init__(self, config_loader):
        self.config = config_loader
        self.client = snap7.client.Client()
        self.data_buffer = bytearray() # Bộ nhớ đệm chứa dữ liệu DB

    def connect(self):
        conn = self.config.connection
        try:
            self.client.connect(conn['IP'], conn['Rack'], conn['Slot'])
            return self.client.get_connected()
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def read_all(self):
        """Đọc toàn bộ DB một lần để tối ưu tốc độ"""
        db_num = self.config.connection['DB_Number']
        # Đọc 32 bytes (khớp với file config của bạn đến iSpare11)
        self.data_buffer = self.client.db_read(db_num, 0, 32)

    def get_bit(self, name):
        addr = self.config.bit_map.get(name)
        if addr:
            return get_bool(self.data_buffer, addr['byte'], addr['bit'])
        return None

    def get_int(self, name):
        addr = self.config.int_map.get(name)
        if addr:
            return get_int(self.data_buffer, addr['byte'])
        return None