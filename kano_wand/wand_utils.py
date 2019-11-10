from kano_wand.constants import *

async def start_notify(client, notification_handler, sensors):
    for char in sensors:
        await client.start_notify(CHARACTERISTIC_UUIDS[char], notification_handler)


async def stop_notify(client, sensors):
    for char in sensors:
        await client.stop_notify(CHARACTERISTIC_UUIDS[char])

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_key(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key

    return "key doesn't exist"