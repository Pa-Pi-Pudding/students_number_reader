# coding:UTF-8
from binascii import hexlify
from sense_hat import SenseHat
from time import sleep
import sys

sys.path.insert(1, '/home/pi/nfcpy')
import nfc

sense = SenseHat()
roop = 0
TDU = ["NE", "NC", "NM", "EJ", "EK", "EH", "ES", "EF", "EC", "FI""FA", "FR", "AJ", "AD", "JK", "JKM", "RMU", "RMD",
       "RMB", "RMT", "RMG", "RU", "RD", "RB", "RT", "RG"]
system_code = 0xFE00


def check_services(tag, start, n):
    services = [nfc.tag.tt3.ServiceCode(i >> 6, i & 0x3f)
                for i in xrange(start, start + n)]
    versions = tag.request_service(services)
    for i in xrange(n):
        if versions[i] == 0xffff: continue
        print services[i], versions[i]


def check_system(tag, system_code):
    idm, pmm = tag.polling(system_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, system_code
    print tag
    n = 32
    for i in xrange(0, 0x10000, n):
        check_services(tag, i, n)


def on_connect(tag):
    print '\n'.join(tag.dump())

    idm, pmm = tag.polling(system_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, system_code

    sc = nfc.tag.tt3.ServiceCode(106, 0x0b)

    student_number_bc = nfc.tag.tt3.BlockCode(0, service=0)
    student_name_bc = nfc.tag.tt3.BlockCode(1, service=0)

    data1 = tag.read_without_encryption([sc], [student_number_bc])
    data2 = tag.read_without_encryption([sc], [student_name_bc])

    comparison(data1, data2)


def comparison(data1, data2):
    for i in TDU:
        if (i in data1):
            num_locate = data1.decode('UTF-8').find('00', 9)
            name_locate = (hexlify(data2).find('00', 0)) / 2

           sense.show_message(data1.decode('UTF-8')[2:num_locate])
           sense.show_message(data2.decode('UTF-8')[0:name_locate])


def main():
    while roop < 1:
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                clf.connect(rdwr={'on-connect': on_connect})

        except:
            x = [255, 0, 0]
            o = [255,255,255]
            not_mark = [
                x, o, o, o, o, o, o, x,
                o, x, o, o, o, o, x, o,
                o, o, x, o, o, x, o, o,
                o, o, o, x, x, o, o, o,
                o, o, o, x, x, o, o, o,
                o, o, x, o, o, x, o, o,
                o, x, o, o, o, o, x, o,
                x, o, o, o, o, o, o, x,
            ]
            sense.set_pixels(not_mark)
            sleep(1)
            sense.clear()
            print "not_service"


if __name__ == '__main__':
    main()

