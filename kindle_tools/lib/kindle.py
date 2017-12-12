import sys
import os
import usb1

class Kindle:

    documents_dir = ''
    clippings_file = ''
    device_type = ''
    is_kindle = False
    device_detected = False

    def __init__(self, directory):
        if directory:
            self.documents_dir = directory
                       
            files = [f for f in os.scandir(self.documents_dir) if f.name.endswith('.txt')]
            files = [f for f in files if f.name.startswith('My Clippings')]

            if len(files) == 1:
                self.clippings_file = files[0].path
        else:
            with usb1.USBContext() as context:
                for device in context.getDeviceIterator(skip_on_error=True):
                    lab126_device = device.getVendorID() == 0x1949
                    self.device_detected |= lab126_device

                    if lab126_device:
                        device_switcher = {
                            0x0002: 'Amazon Kindle',
                            0x0004: 'Amazon Kindle 3/4/Paperwhite',
                            0x0006: 'Kindle Fire',
                            0x0008: 'Amazon Kindle Fire HD 8.9"',
                            0x000A: 'Amazon Kindle Fire 2nd generation (2012)',
                            0x0222: 'Amazon Kindle Fire 7"',
                            0x0800: 'Fire Phone'
                        }
                        default = hex(device.getVendorID())+":"+hex(device.getProductID())
                        self.device_type = device_switcher.get(device.getProductID(), default)

                        type_switcher = {
                            0x0002: True,
                            0x0004: True,
                            0x0006: False,
                            0x0008: False,
                            0x000A: False,
                            0x0222: False,
                            0x0800: False
                        }
                        self.is_kindle = type_switcher.get(device.getProductID(), False)

                        device_type_str = ('Android', 'Kindle Reader')[self.is_kindle]
                        print("*INFO* Found "+self.device_type+' ('+device_type_str+')\n')

            if self.is_kindle:
                path_switcher = {
                    'linux': '/mnt/parallels/Kindle',
                    'win32': 'F:',
                    'cygwin': 'F:',
                    'darwin': '/Volumes/Kindle'
                }
                self.documents_dir = os.path.join(path_switcher.get(sys.platform, ''), 'documents')

                files = [f for f in os.scandir(self.documents_dir) if f.name.endswith('.txt')]
                files = [f for f in files if f.name.startswith('My Clippings')]

                if len(files) == 1:
                    self.clippings_file = files[0].path
