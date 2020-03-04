class OrderData:
    def __init__(self, data, port_source):
        self.tracking_num = data
        self.source = port_source
        self.shipper = None

        self.determine_shipper()

    def determine_shipper(self):
        if len(self.tracking_num) == 15 and self.tracking_num[:1] == "D":
            self.shipper = 'OnTrac'
        elif len(self.tracking_num) == 18 and self.tracking_num[:2] == "1Z":
            self.shipper = "UPS"
        elif len(self.tracking_num) == 34:
            self.shipper = "FedEX"
            self.tracking_num = self.tracking_num[-12:]
        else:
            self.shipper = "unknown"

    def determine_source(self):
        mapping = {
            '10.51.50.47'
        }

    def __repr__(self):
        return str(self.__dict__)
