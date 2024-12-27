import serial, sys, struct, time


class PI:
    def __init__(self, com):
        self.ser = serial.Serial(com, 38400, timeout=2)

    def conf(
        self,
    ):

        # init Programming Interface (PI)
        while True:
            try:
                self.ser.write("\x01\x00".encode())
                line = self.ser.read(10000)
                print(line)
                # x = struct.unpack("B", self.ser.read(1))[0]
                # print("x:", hex(x))
                # assert 0x81 == x
                assert "C2 initialized" in line.decode()
            except Exception as e:
                print(e)
                # flush??
                while thing := self.ser.read(1):
                    print(thing)

        print("PI initiated")

    def prog(self, firmware):

        print("Connected")

        # f = open(firmware,'r').readlines()
        f = firmware.splitlines()

        self.conf()

        # erase device
        self.ser.write("\x04\x00".encode())
        assert 0x84 == struct.unpack("B", self.ser.read(1))[0]

        print("Device erased")

        # write hex file
        total = 0
        buf = ""
        buf_size = 0
        for i in f[1:-1]:  # skip first and second lines
            assert i[0] == ":"
            size = int(i[1:3], 16)
            assert size + 4 < 256
            if buf_size == 0:
                addrh = int(i[3:5], 16)
                addrl = int(i[5:7], 16)
            assert i[7:9] == "00"
            data = i[9 : 9 + size * 2]
            assert len(data) == size * 2

            buf += data
            buf_size += size

            if buf_size > 256 - 0x20 or i == f[-2]:
                attempts = 0
                while True:
                    try:
                        print(hex(addrh) + hex(addrl) + " : " + buf)
                        crc = addrh + addrl
                        crc += sum(
                            [struct.unpack("B", x)[0] for x in buf.decode("hex")]
                        )
                        assert len(buf.decode("hex")) == buf_size
                        self.ser.write(
                            bytes([
                                0x3,
                                buf_size + 4 + 1,
                                buf_size,
                                0,
                                addrh,
                                addrl,
                                crc & 0xFF,
                            ])
                        )
                        self.ser.write(buf.decode("hex").encode())
                        ret = struct.unpack("B", self.ser.read(1))[0]
                        if ret == 0x83:
                            pass
                        else:
                            print("error flash write returned " + hex(ret))
                            raise RuntimeError("bad crc")
                        break
                    except Exception as e:
                        attempts += 1
                        self.conf()
                        print(e)
                        print("attempts: " + attempts)
                total += buf_size
                buf_size = 0
                buf = ""
                print("Wrote %d bytes" % total)

        # reset device
        self.ser.write("\x02\x00".encode())
        assert 0x82 == struct.unpack("B", self.ser.read(1))[0]

        # reset device
        self.ser.write("\x02\x00".encode())
        assert 0x82 == struct.unpack("B", self.ser.read(1))[0]

        # reset device
        self.ser.write("\x02\x00".encode())
        assert 0x82 == struct.unpack("B", self.ser.read(1))[0]

        print("Device reset")


programmers = PI("/dev/ttyACM0")
programmers.prog("/home/matt/Downloads/bootloader~hm_trp~915.hex")
