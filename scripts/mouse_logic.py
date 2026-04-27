import hid

class ModelDWireless:
    def __init__(self):
        self.vendor_id = 0x258a
        self.product_id = 0x2012
        self.device = None

    def connect(self):
        try:
            self.device = hid.device()
            self.device.open(self.vendor_id, self.product_id)
            return True
        except:
            return False

    def get_battery(self):
        if not self.device: return "0"
        try:
            self.device.send_feature_report([0x04, 0x02, 0x02, 0x00])
            data = self.device.get_feature_report(0x04, 64)
            return data[9] if data[9] <= 100 else "Charging"
        except:
            return "Err"

    def set_dpi(self, stage):
        if self.device:
            self.device.send_feature_report([0x04, 0x02, 0x01, stage])

    def disconnect(self):
        if self.device:
            self.device.close()
