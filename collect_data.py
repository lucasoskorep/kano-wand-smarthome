import asyncio
import json
import os
import platform
import uuid
import pandas as pd
from kano_wand.ble_client import KanoBLEClient
from kano_wand.constants import NINE_AXIS, ACCELEROMETER, BUTTON
from time import sleep
from tkinter import *

"""
This is used for reading and decoding values from t he Kano Harry Potter Coding Wand
- Wand sends 25 updates to gyro and accel every second
- Wand sends 3 Dimensional data as 48 bit reverse marshalled integers
- Wand seems to send smaller single dimensional data in 16bit unsigned integers 
"""

HEIGHT = 2
WIDTH = 35
LOOP = asyncio.get_event_loop()


class SpellCollectionGUI:
    def __init__(self, root, spells, kano_ble_client):
        self.root = root
        self.kano_ble_client = kano_ble_client
        self.data_output_file = f"recording-session-{uuid.uuid4()}.csv"

        self.root = root
        self.root.title("Microphone Recorder")

        self.label = Label(root, text="Select a spell, and then press start to begin recording spell data!")
        self.label.pack()

        self.spell_variable = StringVar(root)
        self.spell_list = OptionMenu(root, self.spell_variable,
                                     *["", *[spell for spell in spells]
                                       ], command=self.select_spell)
        self.spell_list.config(height=HEIGHT, width=WIDTH)
        self.spell_list.pack()

        self.recording_button = Button(root, text="Start Recording", command=self.start_recording, height=HEIGHT,
                                       width=WIDTH)
        self.recording_button.pack()

        self.close_button = Button(root, text="Close", command=root.quit, height=HEIGHT, width=WIDTH)
        self.close_button.pack()

        self.spell = None
        self.root.after(0, self.kano_ble_client.connect, True)

    def select_spell(self, selected_value):
        self.spell = selected_value

    def start_recording(self):
        print("Started Recording")
        self.root.after(0)

        self.kano_ble_client.start_recieving_data()


def select_spell(spells):
    try:
        spell = spells[int(input("Please select a spell.\n " +
                                 "\n".join([f"{s} - {spells[s]}" for s in range(len(spells))]) +
                                 "\nenter -1 to exit\n"))]
        print(f"You have selected {spell}")
        return spell
    except Exception as e:
        print(e)
        print("Selected spell is uncorrect")
    return None
async def main(loop):
    device_address = "D8:9B:12:D1:08:80"

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        device_address  # <--- Change to your device's address here if you are using Windows or Linux
        if platform.system() != "Darwin"
        else "243E23AE-4A99-406C-B317-18F1BD7B4CBE"  # <--- Change to your device's address here if you are using macOS
    )

    # One method for connect
    # One for getting all data
    # One for getting data when button is pressed

    spells = pd.read_csv("spells.csv")["spells"]
    sensors = [NINE_AXIS, ACCELEROMETER, BUTTON]
    kble = KanoBLEClient(address, loop)
    await kble.connect(True)
    await kble.start_recieving_data(sensors)
    x = 1
    while x:
        x = select_spell(spells)
        if x is not None:
            kble.change_spell(x)

    await kble.stop_recieving_data(sensors)
    print("finished main")

df = None



# def display_selections():


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
