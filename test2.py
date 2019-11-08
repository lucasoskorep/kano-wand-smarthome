import asyncio
from bleak import discover

from pprint import pprint


async def run():
    devices = await discover()
    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

# import asyncio
# from bleak import BleakClient
#
# address = "e3:ae:cd:af:28:e2"
# MODEL_NBR_UUID = "64a7000f-f691-4b93-a6f4-0968f5b648f8"
#
# async def run(address, loop):
#     async with BleakClient(address, loop=loop) as client:
#         # await client.connect()
#         print(await client.is_connected())
#         print(await client.get_services())
#         services = await client.get_services()
#         pprint(services.descriptors)
#         pprint(services.characteristics)
#         pprint(services.services)
#         # print(services.descriptors)
#         # for key, val in services.descriptors.items():
#         #     print(f"{key} + {val}")
#         #
#         # print(services.characteristics)
#         # for key, val in services.characteristics.items():
#         #     print(f"{key} + {val}")
#
#         print(services)
#         for x in services:
#             print(x)
#             for characteristic in x.characteristics:
#                 print("")
#                 print(characteristic)
#                 print(characteristic.properties)
#                 for descriptor in characteristic.descriptors:
#                     print(descriptor)
#             print(x.description)
#         # for i in range(10):
#         #     x = await client.read_gatt_descriptor(i)
#         #     print(x)
#
#         # model_number = await client.read_gatt_char()
#         # print(model_number)
#         # print("Model Number: {0}".format("".join(map(chr, model_number))))
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run(address, loop))