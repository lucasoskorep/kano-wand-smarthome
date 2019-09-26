import gatt

manager = gatt.DeviceManager(adapter_name='hci0')

class KanoWand(gatt.Device):
    def services_resolved(self):
        super().services_resolved()
        print("Grabbing services")
        print(self.is_connected())
        print(self.services)

        for service in self.services:
            print("FOUND SERVICE")
            # print(service)
            # print(service.device)
            print(service.uuid)
            print(service.characteristics)
            for char in service.characteristics:
                print("FOUND CHARACTERISTIC")
                print(char.uuid)
                print(char.read_value())
        # device_information_service = next(s     for s in self.services if s.uuid == '0000180a-0000-1000-8000-00805f9b34fb')
        #
        # firmware_version_characteristic = next(
        #     c for c in device_information_service.characteristics
        #     if c.uuid == '00002a26-0000-1000 -8000-00805f9b34fb')
        #
        # firmware_version_characteristic.read_value()

    def characteristic_value_updated(self, characteristic, value):
        print("Firmware version:", value.decode("utf-8"))


device = KanoWand(mac_address='e3:ae:cd:af:28:e2', manager=manager)
device.connect()
manager.run()
manager.stop()