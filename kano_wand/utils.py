from kano_wand.constants import *

async def start_notify(client, notification_handler):
    for char in CHARACTERISTIC_UUIDS.keys():
        await client.start_notify(char, notification_handler)


async def stop_notify(client):
    for char in CHARACTERISTIC_UUIDS.keys():
        await client.stop_notify(char)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
