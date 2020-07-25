
import math


def getMean(alist,blist):
    return ((int(alist[0].strip()) + int(blist[0].strip()))/2, (int(alist[1].strip()) + int(blist[1].strip()))/2),((int(alist[2].strip()) + int(blist[2].strip()))/2, (int(alist[3].strip()) + int(blist[3].strip()))/2)

def getFinalListCenter():
    f = open("out.txt", "r")
    Lines = f.readlines()

    ctlist = []
    csrtlist = []
    for line in Lines:
        line = line.strip()
        # print("Line{}: {}".format(count, line))
        if "ct" in line:
            sec = line.split("ct:")
            sec = sec[1].split(") (")
            sec[0] = sec[0].replace('(','')
            sec[1] = sec[1].replace(')', '')
            # print(sec)
            ctlistArr= []
            ctlistArr.append(sec[0].split(",")[0])
            ctlistArr.append(sec[0].split(",")[1])
            ctlistArr.append(sec[1].split(",")[0])
            ctlistArr.append(sec[1].split(",")[1])
            ctlist.append(ctlistArr)

        if "CSRT" in line:
            sec = line.split("CSRT:")
            sec = line.split("CSRT:")
            sec = sec[1].split(") (")
            sec[0] = sec[0].replace('(','')
            sec[1] = sec[1].replace(')', '')
            # print(sec)
            csrtlistArr= []
            csrtlistArr.append(sec[0].split(",")[0])
            csrtlistArr.append(sec[0].split(",")[1])
            csrtlistArr.append(sec[1].split(",")[0])
            csrtlistArr.append(sec[1].split(",")[1])
            csrtlist.append(csrtlistArr)


    # print("ct list",ctlist)
    # print("csrt list",csrtlist)

    finallist = []
    for i in range(len(ctlist)):
        # print(ctlist[i])
        # print(csrtlist[i])
        # print(i)

        if ctlist[i][0] == '-1' and csrtlist[i][0] != '-1':
            # print((int(csrtlist[i][0].strip()),int(csrtlist[i][1].strip())),(int(csrtlist[i][2].strip()),int(csrtlist[i][3].strip())))
            finallist.append([(int(csrtlist[i][0].strip()),int(csrtlist[i][1].strip())),(int(csrtlist[i][2].strip()),int(csrtlist[i][3].strip()))])
        elif csrtlist[i][0] == '-1'  and ctlist[i][0] != '-1':
            # print((int(ctlist[i][0].strip()),int(ctlist[i][1].strip())),(int(ctlist[i][2].strip()),int(ctlist[i][3].strip())))
            finallist.append([(int(ctlist[i][0].strip()),int(ctlist[i][1].strip())),(int(ctlist[i][2].strip()),int(ctlist[i][3].strip()))])

        elif csrtlist[i][0] == '-1'  and ctlist[i][0] == '-1':
            # print("no detection")
            finallist.append([])
        else:
            x,y = getMean(ctlist[i], csrtlist[i])
            finallist.append([x,y])
            # print(x,y)


    # print(finallist)
    finallistCenter = []
    for i in range(len(finallist)):
        if finallist[i] == []:
            finallist[i] = finallist[i-1]

        x = finallist[i][0][0] + finallist[i][1][0]
        y = finallist[i][0][1] + finallist[i][1][1]
        finallistCenter.append((x,y))

    return  finallistCenter




def getFinalListCenterCT():
    f = open("out.txt", "r")
    Lines = f.readlines()

    ctlist = []
    csrtlist = []
    for line in Lines:
        line = line.strip()
        # print("Line{}: {}".format(count, line))
        if "ct" in line:
            sec = line.split("ct:")
            sec = sec[1].split(") (")
            sec[0] = sec[0].replace('(','')
            sec[1] = sec[1].replace(')', '')
            # print(sec)
            ctlistArr= []
            ctlistArr.append(sec[0].split(",")[0])
            ctlistArr.append(sec[0].split(",")[1])
            ctlistArr.append(sec[1].split(",")[0])
            ctlistArr.append(sec[1].split(",")[1])
            ctlist.append(ctlistArr)


    finallist = []
    for i in range(len(ctlist)):
        # print(ctlist[i])
        # print(csrtlist[i])
        # print(i)

        if ctlist[i][0] == '-1':
            # print((int(csrtlist[i][0].strip()),int(csrtlist[i][1].strip())),(int(csrtlist[i][2].strip()),int(csrtlist[i][3].strip())))
            finallist.append([(535 , 777 ),(535 + 34, 777 + 33 )])
        else:
            finallist.append([(int(ctlist[i][0].strip()), int(ctlist[i][1].strip())),
                              (int(ctlist[i][2].strip()), int(ctlist[i][3].strip()))])
            # print(x,y)

    finallistCenter = []
    for i in range(len(finallist)):
        if finallist[i] == []:
            finallist[i] = finallist[i-1]

        x = finallist[i][0][0] + finallist[i][1][0]
        y = finallist[i][0][1] + finallist[i][1][1]
        finallistCenter.append((x,y))

    return  finallistCenter


def printSpeed(finallistCenter):
    for i in range(1,len(finallistCenter)):
        prev = finallistCenter[i-1]
        curr = finallistCenter[i]
        # print("*********gfgfhgf",prev)

        # print(math.sqrt(sum([(a - b) ** 2 for a, b in zip(prev, curr)])))
        d = math.sqrt(sum([(a - b) ** 2 for a, b in zip(prev, curr)]))

        realD = (d * 0.0373)/(35/2)
        # print(realD)

        speed = realD / (1/240)
        print("speed in frame "+str(i) +" :",str(speed) + "m/s")

if __name__ == '__main__':

    print("*****************ball speed using combined of find countour and CSRT method")
    finallistCenter = getFinalListCenter()
    printSpeed(finallistCenter)
    print("*****************ball speed using countour method")
    finallistCenter = getFinalListCenterCT()
    printSpeed(finallistCenter)






