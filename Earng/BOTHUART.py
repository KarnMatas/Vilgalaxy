
import serial
import time
# from marker import *
# from newmain import *
Vilgax = serial.Serial('COM4', 115200, timeout=0.4)  # open serial port default  8N1
Swinggraxia = serial.Serial('COM18', 115200, timeout=0.4)


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


def SetPositionZ(pos, rote, grip):
    posf = pos * 100.00
    posZ = int(posf)
    hbytez = posZ >> 8
    lbytez = posZ % 256
    # print(hex(hbytez), hex(lbytez))
    chk = (hbytez + lbytez + rote + grip + 2) % 256  # calculate checksum
    # print(chk)
    Swinggraxia.write(bytes([255, 255, 2, hbytez, lbytez, int(rote), int(grip),0,0,0, chk]))
    # myrx = Vilgax.read(4)
    # print(myrx)
    # print(".........")
    # if(myrx == hex(0x5350)):

def Capture():
    # cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    # cap.set(3, 1280) # set the resolution
    # cap.set(4, 720)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # for y in range(0,450,50):
    #     # for x in range(10,40,10):
    #     SetPositionXY(20,y)
    #     print("x,y=",[20,y])earำฟea
    #     time.sleep(2)
    #     ret,img = cap.read()
    #     cv2.imshow("raw2",img)
    #     cv2.waitKey(1)
    #     try :
    #         chkpic = img.copy()
    #         test = cropimg(chkpic)
    #         cv2.imshow("test",test)
    #         listofimages.append(img)
    #         print(len(listofimages))
    #         cv2.waitKey(50)
    #     except :
    #         print("recapture")
    #         pass
    #     time.sleep(1)
    print("Misson Complete,Sir!")
    # for img in range(len(listofimages)):
    #     apic = cropimg(listofimages[img])
    #     # listofimages.append(apic)
    #     listofimages[img] = apic
    #     # print(len(listofimages))
    #     # cv2.imshow("photy",listofimages[img])
    #     # print("Karn"+str(img))
    #     # cv2.waitKey(2000)
    #     cv2.destroyAllWindows()
    # norail = forget_that_rail()
    # cv2.imwrite('fieldimages/myfieldgogo.png', norail)
    # print(len(listofimages))
    # print("Analize finish!!!")
    # cv2.imshow("oyi",norail)
    # cv2.waitKey(0)
def gograb():
    SetPositionXY(0,100)

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
    print(".........")
    # if(myrx == hex(0x544A)):
    print("VictoryXY!!!")

def SetHome():
    call = bytes([255,255,0,0,0,0,0,0,0,0,0])
    Swinggraxia.write(call)
    kept = Swinggraxia.read()
    while kept != b'F':
        kept = Swinggraxia.read()
    if kept == b'F':
        kept = Swinggraxia.read()
        if kept == b'0':
            SetPositionZ(400, 70, 0)

    while kept != b'F':
        kept = Swinggraxia.read()
    if kept == b'F':
        kept = Swinggraxia.read()
        if kept == b'4':
            Vilgax.write(call)

    while kept != 'ff':
        kept = Vilgax.read().hex()
        print(kept)
    if kept == 'ff':
        kept = Vilgax.read().hex()
        if kept == 'ff':
            kept = Vilgax.read().hex()
            if kept == '01':
                kept = Vilgax.read().hex()
                if kept == '01':
                    Swinggraxia.write(call)

        # kept = Vilgax.read(4).hex()
        # if kept == 'ff':
        #     kept = Vilgax.read().hex()

    print("Waiting for SetHome ...")
    print(".........")
    print("You are Home,Sir!")
    # if myrx.hex() == "ffff":
    #     myrx = Vilgax.read(2)
    #     print(myrx)
    #     if myrx.hex() == "HM":
    #         print("You are Home,Sir!")

def main():
    # from ctypes import *
    Vilgax.rts = 0
    Vilgax.flush()
    myrx = Vilgax.read(4)  # read to clear buffy
    # print(Vilgax.name)         # check which port was really used
    Swinggraxia.rts = 0
    Swinggraxia.flush()
    myrx2 = Swinggraxia.read(4)  # read to clear buffy
    print("Welcome to Vilgaxia")
    print(".... " + str(Vilgax.name) + " Connected ...")
    print("Hold my Swinggraxia")
    print(".... " + str(Swinggraxia.name) + " Connected ...")
    while (Vilgax.is_open and Swinggraxia.is_open):
        print("Order me, Sir!")
        state = input()
        if state == str(0):  # สั่ง set home (state = 0)
            SetHome()

        elif state == str(1):  # สั่ง ถ่ายรูป (state = 1)
            # Capture()
            func = PathFinder(x)
        elif state == str(2):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            postx = float(input("GO TO X : "))
            posty = float(input("GO TO Y : "))
            SetPositionXY(postx, posty)

        elif state == str(3):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            print("rf",rf_list)
            print("angle",anglespath)
            # rf = float(input("Input Rf : "))
            # degree = float(input("Enter your desire degree: "))
            # TrajectoryXY(rf, degree)
            for t in range(len(rf_list)):
                TrajectoryXY(rf_list[t], anglespath[t])
                time.sleep(7)

        elif state == str(4):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            pos = float(input("GO TO POSITION : "))
            rote = int(input("Rotate degree : "))
            grip = int(input("Grip? open >1 hold = 0 : "))
            SetPositionZ(pos, rote, grip)

        elif state == str(5):  # สั่งย้ายไปที่ตำแหน่งหนึง (state = 10 = 2)
            rf = float(input("Input Rf : "))
            degree = float(input("Enter your desire degree: "))
            TrajectoryZ(rf, degree)
        else:
            print("Forbidden Command, Sorry!")
        # Vilgax.write(call)

main()

