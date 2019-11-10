import pandas as pd
import datetime

class ThreeAxisSensor(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, +{self.y}, +{self.z}"


class WandSensors(object):
    def __init__(self, wand_update_callback, data_folder = "./", dataframe_handler = None):

        self.accel = None
        self.accel_updates = 0

        self.button = 0

        self.gyro = None
        self.gyro_updates = 0

        self.magneto = 0
        self.temperature = 0

        self.df = pd.DataFrame()

        self.wand_update_callback = wand_update_callback
        self.data_folder = data_folder
        self.dataframe_handler = dataframe_handler

    def __str__(self):
        return f"Button " \
            f"{self.button} " \
            f"Accel " \
            f"{self.accel} " \
            f"Gyro " \
            f"{self.gyro} " \
            f"Mag {self.magneto} | Temp {self.temperature}"

    def append_to_dataframe(self):
        if self.gyro_updates == self.accel_updates:
            self.df = self.df.append(
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
            self.send_data_back()

    def send_data_back(self):
        self.wand_update_callback(self)

    def save_df_to_file(self):
        filename = self.data_folder +  datetime.datetime.now().strftime("%I%M%S-%B%d%Y.csv")
        import os
        try:
            os.makedirs(self.data_folder)
        except FileExistsError:
            # directory already exists
            pass
        try:
            self.df.to_csv(filename, index=False)
        except Exception as e:
            print(e)

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
        self.send_data_back()
        if not button:
            self.save_df_to_file()
        else:
            self.df = pd.DataFrame()
    def set_magneto(self, magneto):
        self.magneto = magneto

    def get_dataframe(self):
        return self.df
