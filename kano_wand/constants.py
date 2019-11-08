BUTTON = 1
NINE_AXIS = 2
ACCELEROMETER = 3
BATTERY = 4
TEMPERATURE = 5
MAGNETOMETER = 6

CHARACTERISTIC_UUIDS = {
    ("64a7000d-f691-4b93-a6f4-0968f5b648f8"): BUTTON,  # Button
    ("64a7000a-f691-4b93-a6f4-0968f5b648f8"): NINE_AXIS,  # 9 axis
    ("64a7000c-f691-4b93-a6f4-0968f5b648f8"): ACCELEROMETER,  # Accel
    ("64a70007-f691-4b93-a6f4-0968f5b648f8"): BATTERY,
    ("64a70014-f691-4b93-a6f4-0968f5b648f8"): TEMPERATURE,
    ("64a70021-f691-4b93-a6f4-0968f5b648f8"):MAGNETOMETER
}  # <--- Change to the characteristic you want to enable notifications from.