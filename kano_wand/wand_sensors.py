import pandas as pd


class ThreeAxisSensor(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        print(self.x, self.y, self.z)


class WandSensors(object):
    def __init__(self, wand_update_callback):
        self.gyro = None
        self.gyro_updates = 0

        self.accel = None
        self.accel_updates = 0

        self.magneto = 0
        self.button = 0
        self.temperature = 0

        self.dataframe = pd.DataFrame(columns=["gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z"])

        self.wand_update_callback = wand_update_callback

    def __str__(self):
        return super().__str__()

    def append_to_dataframe(self):
        if self.gyro_updates == self.accel_updates:
            self.dataframe = self.dataframe.append(
                pd.DataFrame({
                    "gyro_x": self.gyro.x,
                    "gyro_y": self.gyro.y,
                    "gyro_z": self.gyro.z,
                    "accel_x": self.accel.x,
                    "accel_y": self.accel.y,
                    "accel_z": self.accel.z,
                    "magneto": self.magneto,
                    "button": self.button
                }, index=[0])
            )
            self.wand_update_callback(self.dataframe)

    def save_df_to_file(self, filename):
        self.dataframe.to_csv(filename, index=False)

    def set_gyro(self, x, y, z):
        self.gyro = ThreeAxisSensor(x, y, z)
        self.gyro_updates += 1
        self.append_to_dataframe()

    def set_accel(self, x, y, z):
        self.accel = ThreeAxisSensor(x, y, z)
        self.accel_updates += 1
        self.append_to_dataframe()

    def set_temp(self, temp):
        self.temp = temp

    def set_button(self, button):
        self.button = button

    def set_magneto(self, magneto):
        self.magneto = magneto

    def get_dataframe(self):
        return self.dataframe
