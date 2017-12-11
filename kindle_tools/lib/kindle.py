import sys
import os
import usb1

class Kindle:

    documents_dir = ''
    clippings_file = ''
    device_type = ''
    is_kindle = False

    def __init__(self):
        with usb1.USBContext() as context:
            for device in context.getDeviceIterator(skip_on_error=True):
                if device.getVendorID() == 0x1949:
                    device_switcher = {
                        0x0002: 'Amazon Kindle',
                        0x0004: 'Amazon Kindle 3/4/Paperwhite',
                        0x0006: 'Kindle Fire',
                        0x0008: 'Amazon Kindle Fire HD 8.9"',
                        0x000A: 'Amazon Kindle Fire 2nd generation (2012)',
                        0x0222: 'Amazon Kindle Fire 7"',
                        0x0800: 'Fire Phone'
                    }
                    self.device_type = device_switcher.get(device.getProductID(), hex(device.getProductID()))

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
                    
                    print("*INFO* Found "+self.device_type+' ('+('Android','Kindle Reader')[self.is_kindle]+')\n')

        if self.is_kindle:
            path_switcher = {
                'linux': '/mnt/parallels/Kindle',
                'win32': 'F:',
            	'cygwin': 'F:',
            	'darwin': '/Volumes/Kindle'
            }
            self.documents_dir = os.path.join(path_switcher.get(sys.platform, ''), 'documents')

            file_witcher = {
                'linux': 'My%20Clipplings.txt',
                'win32': 'My Clipplings.txt',
            	'cygwin': 'My Clipplings.txt',
            	'darwin': 'My%20Clipplings.txt'
            }
            self.clippings_file = os.path.join(self.documents_dir, file_witcher.get(sys.platform, 'My Clipplings.txt'))
