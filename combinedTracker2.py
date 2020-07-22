import cv2
import sys
import math
import numpy as np
import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


class Questionaire(object):
    def __init__(self):
        self.pos1 = (535, 777)
        self.pos2 = (535 + 33, 777 + 33)
        self.isFirst = True
        self.isFail = False
        self.fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=30)
        self.tracker = cv2.TrackerCSRT_create()
        self.frame = ''
        self.frameModified = ''
        self.frameTotal = ''
        self.frameNo = 0

    def process(self):
        filepath = "./data/IMG1.bmp"
        # print("*********", filepath)
        ret = True
        # if ret is true than no error with cap.isOpened
        self.frame = cv2.imread(filepath)
        self.frameModified = cv2.imread(filepath)
        self.frameTotal = cv2.imread(filepath)

        # Define an initial bounding box
        bbox = (535, 777, 33, 34)

        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(self.frame, bbox)

        # initial position

        finalp1 = (535, 777)
        finalp2 = (535 + 33, 777 + 33)

        for i in range(1, 16):
            print(str(i) + '\n')
            filepath = "./data/IMG" + str(i) + '.bmp'
            # print("*********", filepath)
            # if ret is true than no error with cap.isOpened
            self.frame = cv2.imread(filepath)
            self.frameModified = cv2.imread(filepath)
            self.frameNo = i

            self.ct()
            self.csrt()

        cv2.imshow("Tracking", self.frameTotal)
        cv2.waitKey()



    def displacement(self, x, y):
        """Find Euclidean displacement between x and y (x,y are tuple)
        """
        return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

    def csrt(self):
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = self.tracker.update(self.frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

            # print("p1",p1)
            # print("p2", p2)
            d = self.displacement(p1, self.pos1)
            # print("displacement",d)
            cp1 = (-1. - 1)
            cp2 = (-1, -1)

            # print("cp1", cp1)
            # print("cp2", cp2)
            if self.isFirst:
                # pos1 = p1
                self.isFirst = False
                cv2.rectangle(self.frameModified, p1, p2, (255, 0, 0), 2, 1)
                cv2.rectangle(self.frameTotal, p1, p2, (255, 0, 0), 2, 1)
                cv2.imshow("Tracking", self.frameModified)
                cv2.waitKey(1000)
                print("CSRT:" + str(p1) + " " + str(p2) + '\n')
            elif d > 13.1 and self.frameNo > 2:
                # print("1")
                self.pos1 = p1
                cv2.rectangle(self.frameModified, p1, p2, (255, 0, 0), 2, 1)
                cv2.rectangle(self.frameTotal, p1, p2, (255, 0, 0), 2, 1)
                cv2.imshow("Tracking", self.frameModified)
                cv2.waitKey(1000)
                print("CSRT:" + str(p1) + " " + str(p2) + '\n')
            elif d < 9 and self.frameNo <= 2:
                # print("2")
                self.pos1 = p1
                cv2.rectangle(self.frameModified, p1, p2, (255, 0, 0), 2, 1)
                cv2.rectangle(self.frameTotal, p1, p2, (255, 0, 0), 2, 1)
                cv2.imshow("Tracking", self.frameModified)
                cv2.waitKey(1000)
                print("CSRT:" + str(p1) + " " + str(p2) + '\n')
            else:
                print("CSRT:(-1, -1) (-1, -1)" + '\n')

        else:
            # Tracking failure
            cv2.putText(self.frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display result
        cv2.imshow("Tracking", self.frameModified)
        cv2.waitKey(1000)

    def ct(self):
        """Track baseball using contours method
            1. apply createBackgroundSubtractorMOG2 to remove net background (createBackgroundSubtractorKNN does not work well in this case)
            2. apply patch
                    fgmask[550:730, 290:400] = 0
                    fgmask[850:1000, 190:400] = 0
                to cover the player body and legs because those 2 areas doesnt contain ball
            3. apply findContours to find the contours list, then using cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, False), False) to find the rounded shape, which is the baseball in this case
            4. filter the rounded shape by applying some filter


            this method is not able to detect the first few frames because in those frames, baseball overlapped  stick
            """
        fgmask = self.fgbg.apply(self.frame)

        fgmask[550:730, 290:400] = 0
        fgmask[850:1000, 190:400] = 0

        (contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:

            if cv2.contourArea(c) < 300:
                continue
            # approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, False), False)
            counter = 0
            # print(len(approx))
            # print("len(approx)", len(approx))
            # print("cv2.contourArea(c)", cv2.contourArea(c))
            # if (len(approx) > 10) and (cv2.contourArea(c) < 2000) and (cv2.contourArea(c) > 300):
            if (True):
                # get bounding box from countour'

                (x, y, w, h) = cv2.boundingRect(c)
                # print("x", x)
                # print("y", y)
                # print("w", w)
                # print("h", h)
                # print("w/2", int(w / 2))
                # print("h/2", int(h / 2))
                w1 = int(w * 0.6)
                h1 = int(h * 0.6)

                counter = 1

                if (w > 50 and w < 300 and h < 50):
                    # cv2.rectangle(frame, ((x+w1), (y+h1)), (x + 34, y + 34), (0, 255, 0), 2)
                    cv2.rectangle(self.frameModified, ((x + w1), (y + h1)), (x + w1 + 34, y + h1 + 34), (0, 255, 0), 2)
                    cv2.rectangle(self.frameTotal, ((x + w1), (y + h1)), (x + w1 + 34, y + h1 + 34), (0, 255, 0), 2)
                    cp1 = ((x + w1), (y + h1))
                    cp2 = (x + w1 + 34, y + h1 + 34)
                    print("ct:" + str(cp1) + " " + str(cp2))
                elif h >= 50:
                    print("ct:(-1, -1) (-1, -1)" + '\n')
                elif (w > 300):
                    print("ct:(-1, -1) (-1, -1)" + '\n')
                else:
                    cv2.rectangle(self.frameModified, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.rectangle(self.frameTotal, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cp1 = (x, y)
                    cp2 = (x + w, y + h)
                    print("ct:" + str(cp1) + " " + str(cp2))
                if (counter == 1):
                    break


if __name__ == '__main__':

    q = Questionaire()
    q.process()






    #
    #
    #
    #
    #
    # fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=30)
    # tracker = cv2.TrackerCSRT_create()
    #
    #
    # pos1 = (535, 777)
    # pos2 = (535 + 33, 777 + 33)
    # isFirst = True
    # isFail = False
    # filepath = "./data/IMG1.bmp"
    # # print("*********", filepath)
    # ret = True
    # # if ret is true than no error with cap.isOpened
    # frame = cv2.imread(filepath)
    #
    # # Define an initial bounding box
    # bbox = (535, 777, 33, 34)
    #
    # # Initialize tracker with first frame and bounding box
    # ok = tracker.init(frame, bbox)
    #
    # #initial position
    #
    #
    #
    # finalp1 = (535,777)
    # finalp2 = (535+33,777+33)
    #
    # for i in range(1, 16):
    #     print(str(i)+'\n')
    #     filepath = "./data/IMG" + str(i) + '.bmp'
    #     # print("*********", filepath)
    #     # if ret is true than no error with cap.isOpened
    #     frame = cv2.imread(filepath)
    #
    #     # Start timer
    #     timer = cv2.getTickCount()
    #
    #     # Update tracker
    #     ok, bbox = tracker.update(frame)
    #
    #     # Calculate Frames per second (FPS)
    #     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    #
    #     # Draw bounding box
    #     if ok:
    #         # Tracking success
    #         p1 = (int(bbox[0]), int(bbox[1]))
    #         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    #
    #         # print("p1",p1)
    #         # print("p2", p2)
    #         d = displacement(p1,pos1)
    #         # print("displacement",d)
    #         cp1 = (-1. - 1)
    #         cp2 = (-1, -1)
    #         ct(frame)
    #         # print("cp1", cp1)
    #         # print("cp2", cp2)
    #         if isFirst:
    #             # pos1 = p1
    #             isFirst = False
    #             cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    #             cv2.imshow("Tracking", frame)
    #             cv2.waitKey(1000)
    #             print("CSRT:"+str(p1) +" "+str(p2) + '\n')
    #         elif d >13.1 and i>2 :
    #             # print("1")
    #             pos1 = p1
    #             cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    #             cv2.imshow("Tracking", frame)
    #             cv2.waitKey(1000)
    #             print("CSRT:" + str(p1) + " " + str(p2) + '\n')
    #         elif d <9 and i <= 2:
    #             # print("2")
    #             pos1 = p1
    #             cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    #             cv2.imshow("Tracking", frame)
    #             cv2.waitKey(1000)
    #             print("CSRT:" + str(p1) + " " + str(p2) + '\n')
    #         else:
    #             print("CSRT:(-1, -1) (-1, -1)" + '\n')
    #             # print("CSRT fail, using other method")
    #             # ct(filepath)
    #     else:
    #         # Tracking failure
    #         cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    #
    #     # Display result
    #     cv2.imshow("Tracking", frame)
    #     cv2.waitKey(1000)


    sys.stdout = orig_stdout
    f.close()
