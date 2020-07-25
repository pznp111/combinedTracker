# combinedTracker

this is for tracking baseball movement, without using DL approach. tracked images are in savedImage folder <br />
Adopting 2 methods: CSRT and find Contour.


To run the Trackers: <br />
1. run combinedTracker2.py to perform object tracking, it perform the following 2 trackers: <br />

1.1. CSRT methond:  <br />
need to label the initial positon bbox = (535, 777, 33, 34), able to track first few frames(except frame2)but tracking failed half way through <br />

1.2. findContours: <br />

firstly, image processing to remove background using cv2.createBackgroundSubtractorMOG2 <br />
secondly, apply patch to remove all content  <br />

                    fgmask[550:730, 290:400] = 0
                    fgmask[850:1000, 190:400] = 0
                to cover the player body and legs because those 2 areas doesnt contain ball
thirdly, filter by rectangle size. <br />
This method cannot detect the first few frames because of the fact that stick and ball overlapped in those frames. <br />

combinedTracker2.py will generate out.txt file of tracking result <br />


2.run  computeSpeed.py to compute speed using the result in the out.txt <br />

Technically, it is not possible to get the very accurate ball speed because there is only 1 camera targetting the player(unless using lastest DL methond which might somehow get depth information from a single image or a single angle of images). <br />
Thus, I just estimate the speed based on radius of baseball is 0.0373m, in the detections, most of the bounding box has width of 33-35 pixals, which means <br />
35/2 pixal represent  0.0373m. Of course this is not accurate without using camera models but on the other hand, using 1 camera technically cannot estimate accurate speed  because of the missing depth information. <br />

Here is the result:  <br />

*****************ball speed using combined of find countour and CSRT method <br />
speed in frame 1 : 0.0m/s <br />
speed in frame 2 : 18.47937508617405m/s <br />
speed in frame 3 : 26.560849973121982m/s <br />
speed in frame 4 : 32.208925430909325m/s <br />
speed in frame 5 : 32.76371101474861m/s <br />
speed in frame 6 : 34.30485121469032m/s <br />
speed in frame 7 : 37.924960836959315m/s <br />
speed in frame 8 : 39.49992043804955m/s <br />
speed in frame 9 : 52.059382562075115m/s <br />
speed in frame 10 : 48.90520939022796m/s <br />
speed in frame 11 : 50.1312m/s <br />
speed in frame 12 : 55.485306650260746m/s <br />
speed in frame 13 : 60.20144443043044m/s <br />
speed in frame 14 : 65.81232953917572m/s <br />



If CSRT is consider ML method, not a conventional solution, then just consider findContours method: <br />
*****************ball speed using countour method <br />
speed in frame 1 : 0.0m/s <br />
speed in frame 2 : 0.0m/s <br />
speed in frame 3 : 0.0m/s <br />
speed in frame 4 : 71.61782691547332m/s <br />
speed in frame 5 : 32.90616476958786m/s <br />
speed in frame 6 : 35.621164820519446m/s <br />
speed in frame 7 : 39.22903405508087m/s <br />
speed in frame 8 : 34.7322155431924m/s <br />
speed in frame 9 : 52.059382562075115m/s <br />
speed in frame 10 : 48.90520939022796m/s <br />
speed in frame 11 : 50.1312m/s <br />
speed in frame 12 : 55.485306650260746m/s <br />
speed in frame 13 : 60.20144443043044m/s <br />
speed in frame 14 : 65.81232953917572m/s <br />
