
import serial
import time

Vilgax = serial.Serial('COM18', 115200, timeout=0.4)  # open serial port default  8N1

def Capture():
    print("Doing Capture ...")
    call = bytes([255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 1])
    Vilgax.write(call)
    myrx = Vilgax.read(4)
    print(myrx)
    print(".........")
    if(myrx == hex(0x4350)):
        print("Misson Complete,Sir!")

def SetPosition(pos, rote, grip):
    print("Roger That,The war is On.")
    posf = pos * 100.00
    posZ = int(posf)
    hbytez = posZ >> 8
    lbytez = posZ % 256
    print(hex(hbytez), hex(lbytez))
    chk = (hbytez + lbytez + rote + grip + 2) % 256  # calculate checksum
    # print(chk)
    Vilgax.write(bytes([255, 255, 2, hbytez, lbytez, int(rote), int(grip),0,0,0, chk]))
    myrx = Vilgax.read(4)
    print(myrx)
    print(".........")
    # if(myrx == hex(0x5350)):
    print("Victory!!!")

def TrajectoryZ(rf, degree):
    print("Roger That,The war is On.")
    postr = rf * 100.00
    postd = degree
    hbyter = int(postr) >> 8
    lbyter = int(postr) % 256
    byted = int(postd)
    chk = (hbyter + lbyter + byted + 3) % 256  # calculate checksum
    Vilgax.write(bytes([255, 255, 3, hbyter, lbyter, byted,0,0,0,0,chk]))
    myrx = Vilgax.read(4)
    print(myrx)
    print(".........")
    # if(myrx == hex(0x544A)):
    print("Victory!!!")

def SetHome():
    call = bytes([255,255,0,0,0,0,0,0,0,0,0])
    Vilgax.write(call)
    print("Waiting for SetHome ...")
    print(".........")
    kept = ""
    while kept != b'\r':
        kept = Vilgax.read()
        # SetPosition(150.00, rote, grip)
        print(kept)
        if kept == b'F':
            print("SetXY")
    # print("You are Home,Sir!")
    # if myrx.hex() == "ffff":
    # myrx = Vilgax.read(4)
    # print(myrx)
    #     if myrx.hex() == "HM":
    #         print("You are Home,Sir!")

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
            pos = float(input("GO TO POSITION : "))
            rote = int(input("Rotate degree : "))
            grip = int(input("Grip? open >1 hold = 0 : "))
            SetPosition(pos, rote, grip)

        elif state == str(3):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            rf = float(input("Input Rf : "))
            degree = float(input("Enter your desire degree: "))
            TrajectoryZ(rf, degree)
        else:
            print("Forbidden Command, Sorry!")
        # Vilgax.write(call)

main()

