
import asyncio
import json
import platform

"""
This is used for reading and decoding values from t he Kano Harry Potter Coding Wand
- Wand sends 25 updates to gyro and accel every second
- Wand sends 3 Dimensional data as 48 bit reverse marshalled integers
- Wand seems to send smaller single dimensional data in 16bit unsigned integers 
"""

SPELLS = json.load("spells.json")
CURR_SPELL = 0

# TODO: RUMBLE
# TODO: RGB

device_address = "D8:9B:12:D1:08:80"



if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        device_address  # <--- Change to your device's address here if you are using Windows or Linux
        if platform.system() != "Darwin"
        else "243E23AE-4A99-406C-B317-18F1BD7B4CBE"  # <--- Change to your device's address here if you are using macOS
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))
