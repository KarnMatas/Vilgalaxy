
import serial
import time
from marker import *
from newmain import *
Vilgax = serial.Serial('COM11', 115200, timeout=0.4)  # open serial port default  8N1
# Swinggraxia = serial.Serial('COM4', 115200, timeout=0.4)
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

def Capture():
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    cap.set(3, 1280) # set the resolution
    cap.set(4, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    for y in range(0,450,50):
        for x in range(0,100,20):
            SetPositionXY(x,y)
            print("x,y=",[x,y])
            time.sleep(2)
            ret,img = cap.read()
            cv2.imshow("raw2",img)
            cv2.waitKey(1)
            try :
                chkpic = img.copy()
                test = cropimg(chkpic)
                cv2.imshow("test",test)
                listofimages.append(img)
                print(len(listofimages))
                cv2.waitKey(50) 
            except :
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
        except :
                print("What the hell which this picture")
                pass
        cv2.destroyAllWindows()

    norail = forget_that_rail()  
    cv2.imwrite('fieldimages/myfieldeiei.png', norail)
    print(len(listofimages))
    print("Analize finish!!!") 
    cv2.imshow("oyi",norail)
    cv2.waitKey(0)
def gograb():
    SetPositionXY(0,100)

def TrajectoryZ(posZ,degree):
    print("Roger That, Z The war is On.")
    newposZ = posZ * 100.00
    sent_ang = degree - 180
    # มุม
    hbyteang = int(sent_ang) >> 8
    hbyteZ   = int(posZ) >> 8
    lbyteang = int(sent_ang) % 256
    lbyteZ = int(posZ) % 256
    print(hex(hbyteZ), hex(hbyteang))
    print(hex(lbyteZ), hex(lbyteang))
    chk = (hbyteZ + lbyteZ + hbyteang + lbyteang + 3) % 256  # calculate checksum
    Swinggraxia.write(bytes([255, 255, 3, hbyteZ, lbyteZ, hbyteang, lbyteang, 0, 0, 0, chk]))
    # print(myrx)
    print(".........")
    # if(myrx == hex(0x544A)):
    print("VictoryZ!!!")

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

def main():
    # from ctypes import *
    Vilgax.rts = 0
    Vilgax.flush()
    myrx = Vilgax.read(4)  # read to clear buffy
    # print(Vilgax.name)         # check which port was really used
    # Swinggraxia.rts = 0
    # Swinggraxia.flush()
    # myrx2 = Swinggraxia.read(4)  # read to clear buffy
    print("Welcome to Vilgaxia")
    print(".... " + str(Vilgax.name) + " Connected ...")
    # print("Hold my Swinggraxia")
    # print(".... " + str(Swinggraxia.name) + " Connected ...")
    while (Vilgax.is_open):#and Swinggrasia.is_open
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
            SetPositionXY(world_position[0][0], world_position[0][1])
            time.sleep(7)
            for t in range(len(rf_list)):
                TrajectoryXY(rf_list[t], anglespath[t])
                time.sleep(7)
        elif state == str(4):
            Capture()
        else:
            print("Forbidden Command, Sorry!")
        # Vilgax.write(call)

main()

