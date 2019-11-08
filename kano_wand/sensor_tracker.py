import pandas as pd

class Gyro(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        print(self.x, self.y, self.z)


class Accel(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        print(self.x, self.y, self.z)


class SensorTracker(object):
    def __init__(self):
        self.gyro = None
        self.gyro_updates = 0

        self.accel = None
        self.accel_updates = 0
        self.dataframe = pd.DataFrame(columns=["gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z"])

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
                }, index=[0])
            )

    def save_df_to_file(self, filename):
        self.dataframe.to_csv(filename, index=False)

    def set_gyro(self, gyro):
        self.gyro = gyro
        self.gyro_updates += 1

    def set_accel(self, accel):
        self.accel = accel
        self.accel_updates += 1
