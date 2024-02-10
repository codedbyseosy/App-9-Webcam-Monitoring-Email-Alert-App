import cv2
import time

video = cv2.VideoCapture(0) # start a video using the webcam
time.sleep(1) # give the camera time to wait
                  # this will create one frame per second

first_frame = None
while True:
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # to reduce the complexity of the images by converting them to greyscale
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0) # to make calculations more efficient, we'll use the guassian blur method. Also to remove noise
                                                            # (21, 21) is the amount of blurriness
                                                            # 0 is the standard deviation

    if first_frame is None:
        first_frame = gray_frame_gau # obtain the first frame variable



    delta_frame = cv2.absdiff(first_frame, gray_frame_gau) # store the difference b/w the first frame and any new frames - new differences indicated by white colours
    # cv2.imshow("My Video", delta_frame) # show the difference b/w the first frame and any new frames - new differences indicated by white colours



    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] # classify white pixels with a value of 30 or higher and assign them a value of 255
                                                                             # thresh_frame is a list in which we are extracting the second item from

    
    
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2) # this is to remove the noise. The higher the interation number, the higher the amount of processing done
    cv2.imshow("My Video", dil_frame) # show the difference b/w the first frame and any new frames - new differences indicated by white colours
                                                                     
    
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # to detect contours around white areas

    for contour in contours:
        if cv2.contourArea(contour) < 5000: # if identified white area is smaller than 10000 continue
            continue 
        x, y, w, h = cv2.boundingRect(contour) # extract the sizes of the x & y axis and the sizes of the height and width
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) # draw a rect around the original frame (colour frame)
                                                              # the colour of the rectangle '(0, 255, 0)', '3' is the width of the rectangle

        cv2.imshow("Video", frame)







    key = cv2.waitKey(1) # this creates a keyboard key object

    if key == ord("q"): # if the user presses the key "q", it will break the loop and then it will release the video
        break

video.release()