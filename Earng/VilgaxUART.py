
import serial
import time

Vilgax = serial.Serial('COM4', 115200, timeout=0.4)  # open serial port default  8N1
def SetHome():
    call = bytes([255,255,0,0,0,0,0,0,0,0,0])
    Vilgax.write(call)
    print("Waiting for SetHome ...")
    print(".........")
    # myrx = Vilgax.read(4)
    # print(myrx)
    print("You are Home,Sir!")
    # if myrx.hex() == "ffff":
    #     myrx = Vilgax.read(2)
    #     print(myrx)
    #     if myrx.hex() == "HM":
    #         print("You are Home,Sir!")


def Capture():
    print("Doing Capture ...")
    Vilgax.write(bytes([225,225,1,0,0,0,0,0,0,0,1]))
    myrx = Vilgax.read(4)
    print(myrx)
    print(".........")
    if(myrx == hex(0x4350)):
        print("Misson Complete,Sir!")

def SetPositionXY(X, Y):
    print("Roger That,The war is On.")
    postx = X * 100.00
    posty = Y * 100.00
    postx = int(postx)
    posty = int(posty)
    hbytex = postx >> 8
    hbytey = posty >> 8
    print(hex(hbytex), hex(hbytey))
    lbytex = postx % 256
    lbytey = posty % 256
    print(hex(lbytex), hex(lbytey))
    chk = (hbytex + lbytex + hbytey + lbytey + 2) % 256  # calculate checksum
    # print(chk)
    Vilgax.write(bytes([255, 255, 2, hbytex, lbytex, hbytey, lbytey, 0, 0, 0, chk]))
    # myrx = Vilgax.read(4)
    # print(myrx)
    print(".........")
    # if(myrx == hex(0x5350)):
    print("Victory!!!")

def TrajectoryXY(rf, degree):
    print("Roger That,The war is On.")
    postr = rf * 100.00
    postd = degree * 100.00
    hbyter = int(postr) >> 8
    hbyted = int(postd) >> 8
    print(hex(hbyter), hex(hbyted))
    lbyter = int(postr) % 256
    lbyted = int(postd) % 256
    print(hex(lbyter), hex(lbyted))
    chk = (hbyter + lbyter + hbyted + lbyted + 3) % 256  # calculate checksum
    Vilgax.write(bytes([255, 255, 3, hbyter, lbyter, hbyted, lbyted, 0, 0, 0, chk]))
    # print(myrx)
    print(".........")
    # if(myrx == hex(0x544A)):
    print("Victory!!!")

def main():
    # from ctypes import *
    Vilgax.rts = 0
    Vilgax.flush()
    myrx = Vilgax.read(4)  # read to clear buffy
    # print(Vilgax.name)         # check which port was really used
    print("Welcome to Vilgaxia")
    print(".... " + str(Vilgax.name) + " Connected ...")
    while Vilgax.is_open:
        print("Order me, Sir!")
        state = input()
        if state == str(0):  # สั่ง set home (state = 0)
            SetHome()

        elif state == str(1):  # สั่ง ถ่ายรูป (state = 1)
            Capture()

        elif state == str(2):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            postx = float(input("GO TO X : "))
            posty = float(input("GO TO Y : "))
            SetPositionXY(postx, posty)

        elif state == str(3):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            rf = float(input("Input Rf : "))
            degree = float(input("Enter your desire degree: "))
            TrajectoryXY(rf, degree)
        else:
            print("Forbidden Command, Sorry!")
        # Vilgax.write(call)

main()

