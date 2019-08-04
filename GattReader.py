import pygatt

adapter = pygatt.BGAPIBackend()

adapter.start()
device = adapter.connect('E3:AE:CD:AF:28:E2')
print(device.char_read("64a70010-f691-4b93-a6f4-0968f5b648f8"))