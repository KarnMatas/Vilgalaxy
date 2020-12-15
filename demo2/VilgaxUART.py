import serial
import time
from marker import *
from newmain import *

Vilgax = serial.Serial('COM11', 115200, timeout=0.6)  # open serial port default  8N1
Swinggraxia = serial.Serial('COM3', 115200, timeout=0.6)
# print("Welcome to Vilgaxia")
# print(".... " + str(Vilgax.name) + " Connected ...")
# print("Hold my Swinggraxia")
# print(".... " + str(Swinggraxia.name) + " Connected ...")

Vilgax.rts = 0
Vilgax.flush()
myrx = Vilgax.read(8)  # read to clear buffy
# print(Vilgax.name)         # check which port was really used
Swinggraxia.rts = 0
Swinggraxia.flush()
myrx2 = Swinggraxia.read(8)  # read to clear buffy


def SetHome():
    call = bytes([255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # Swinggraxia.write(call)
    # while kept != b'F':
    #     kept = Swinggraxia.read()
    # if kept == b'F':
    #     kept = Swinggraxia.read()
    #     if kept == b'0':
    SetPositionZ(25, 70, 1)
    kept = Swinggraxia.read()

    while kept != b'F':
        kept = Swinggraxia.read()
        # print(kept)
    if kept == b'F':
        kept = Swinggraxia.read()
        # print(kept)
        if kept == b'4':
            # print(kept)
            Vilgax.write(call)

    while kept != 'ff':
        kept = Vilgax.read().hex()
        # print(kept)
    if kept == 'ff':
        kept = Vilgax.read().hex()
        if kept == 'ff':
            kept = Vilgax.read().hex()
            if kept == '01':
                kept = Vilgax.read().hex()
                if kept == '01':
                    Swinggraxia.write(call)
    # print("Waiting for SetHome ...")
    # print("You are Home,Sir!")
    # print(".........")


def SetPositionXY(X, Y):
    print("SetXY")
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
    # if(myrx == hex(0x5350)):
    print("Victory!!!")
    print(".........")


def Capture():
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    cap.set(3, 1280)  # set the resolution
    cap.set(4, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    for y in range(0, 450, 50):
        for x in range(0, 100, 20):
            SetPositionXY(x, y)
            print("x,y=", [x, y])
            time.sleep(2)
            ret, img = cap.read()
            cv2.imshow("raw2", img)
            cv2.waitKey(1)
            try:
                chkpic = img.copy()
                test = cropimg(chkpic)
                cv2.imshow("test", test)
                listofimages.append(img)
                print(len(listofimages))
                cv2.waitKey(50)
            except:
                print("recapture")
                pass
            time.sleep(1)
    print("Misson Complete,Sir!")
    for img in range(len(listofimages)):
        try:
            apic = cropimg(listofimages[img])
            # listofimages.append(apic)
            listofimages[img] = apic
            # print(len(listofimages))
            # cv2.imshow("photy",listofimages[img])
            # print("Karn"+str(img))
            # cv2.waitKey(2000)
        except:
            print("What the hell which this picture")
            pass
        cv2.destroyAllWindows()

    norail = forget_that_rail()
    cv2.imwrite('fieldimages/myfielddemo.png', norail)
    print(len(listofimages))
    print("Analize finish!!!")
    print(".........")
    cv2.imshow("oyi", norail)
    cv2.waitKey(0)


def SetPositionZ(pos, rote, grip):
    print("SetZ")
    posf = pos * 1000.00
    posZ = int(posf)
    hbytez = posZ >> 8
    lbytez = posZ % 256
    # print(hex(hbytez), hex(lbytez))
    chk = (hbytez + lbytez + rote + grip + 2) % 256  # calculate checksum
    # print(chk)
    Swinggraxia.write(bytes([255, 255, 2, hbytez, lbytez, int(rote), int(grip), 0, 0, 0, chk]))
    print(".........")


def TrajectoryZ(rf, degree):
    print("Roger That,The war is On.Z")
    postr = rf * 1000.00
    postd = degree
    hbyter = int(postr) >> 8
    lbyter = int(postr) % 256
    print(hex(hbyter), hex(lbyter))
    byted = int(postd)
    print(hex(byted))
    chk = (hbyter + lbyter + byted + 3) % 256  # calculate checksum
    Swinggraxia.write(bytes([255, 255, 3, hbyter, lbyter, byted, 0, 0, 0, 0, chk]))
    # myrx2 = Swinggraxia.read(4)
    # print(myrx2)
    # if(myrx == hex(0x544A)):
    print("Victory!!!")
    print(".........")


def TrajectoryXY(rf, degree):
    print("Roger That,XY The war is On.")
    postr = rf * 100.00
    postd = degree
    hbyter = int(postr) >> 8
    hbyted = int(postd) >> 8
    print(hex(hbyter), hex(hbyted))
    lbyter = int(postr) % 256
    lbyted = int(postd) % 256
    print(hex(lbyter), hex(lbyted))
    chk = (hbyter + lbyter + hbyted + lbyted + 3) % 256  # calculate checksum
    Vilgax.write(bytes([255, 255, 3, hbyter, lbyter, hbyted, lbyted, 0, 0, 0, chk]))
    # print(myrx)
    # if(myrx == hex(0x544A)):
    print("VictoryXY!!!")
    print(".........")


# positionZ =[]

def GripTheRod():
    SetPositionZ(10, 150, 1)
    time.sleep(4)
    SetPositionZ(10, 150, 0)

def Run():
    # Capture()
    positionZ, anglesZ = PathFinder(x)
    print('ang', anglespath)
    print('rf', rf_list)
    print("angleZ", anglesZ)
    print('sortpointZ fuck =', positionZ)

def Start():
    SetPositionZ(40, 70, 1)
    Capture()

def main():
    # global positionZ
    # from ctypes import *
    print("Welcome to Vilgaxia")
    print(".... " + str(Vilgax.name) + " Connected ...")
    print("Hold my Swinggraxia")
    print(".... " + str(Swinggraxia.name) + " Connected ...")
    while (Vilgax.is_open):  # and Swinggrasia.is_open
        Vilgax.rts = 0
        Vilgax.flush()
        myrx = Vilgax.read(8)  # read to clear buffy
        # print(Vilgax.name)         # check which port was really used
        Swinggraxia.rts = 0
        Swinggraxia.flush()
        myrx2 = Swinggraxia.read(8)  # read to clear buffy
        print("Order me, Sir!")
        state = input()
        if state == str(0):  # สั่ง set home (state = 0)
            SetHome()

        elif state == str(1):  # สั่ง ถ่ายรูป (state = 1)
            # Capture()
            positionZ, anglesZ = PathFinder(x)
            print('ang', anglespath)
            print('rf', rf_list)
            print("angleZ", anglesZ)
            print('sortpointZ  =', positionZ)
        elif state == str(2):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            postx = float(input("GO TO X : "))
            posty = float(input("GO TO Y : "))
            SetPositionXY(postx, posty)

        elif state == str(3):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            print("rf", rf_list)
            print("angle", anglespath)
            # rf = float(input("Input Rf : "))
            # degree = float(input("Enter your desire degree: "))
            # TrajectoryXY(rf, degree)
            print("angleZ", anglesZ)
            print('sortpointZ=', positionZ)
            SetPositionXY(world_position[0][0], world_position[0][1])
            SetPositionZ(positionZ[0], 70, 0)
            time.sleep(3)
            for t in range(len(rf_list)):
                print('pos', positionZ[t + 1])
                TrajectoryXY(rf_list[t], anglespath[t])
                TrajectoryZ(positionZ[t + 1], int(anglesZ[t]))  # +1
                # TrajectoryXY(rf_list[t], anglespath[t])
                time.sleep(7)
        elif state == str(4):
            SetPositionZ(40, 70, 1)
            time.sleep(4)
            Capture()
        elif state == str(5):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            pos = float(input("GO TO POSITION : "))
            rote = int(input("Rotate degree : "))
            grip = int(input("Grip? open >1 hold = 0 : "))
            SetPositionZ(pos, rote, grip)

        elif state == str(6):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            rf = float(input("Input Rf : "))
            degree = float(input("Enter your desire degree: "))
            TrajectoryZ(rf, degree)

        elif state == str(7):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            GripTheRod()
        else:
            print("Forbidden Command, Sorry!")
        # Vilgax.write(call)

main()