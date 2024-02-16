import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread 

video = cv2.VideoCapture(0) # start a video using the webcam
time.sleep(1) # give the camera time to wait
                  # this will create one frame per second

first_frame = None
status_list = []
count = 1

def clean_folder(): # function definition to clean folder
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image) # remove each image from the folder
    print("clean_folder function ended")

while True:
    status = 0
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
        if cv2.contourArea(contour) < 2000: # if identified white area is smaller than 5000, ignore it and continue looking
            continue 
        x, y, w, h = cv2.boundingRect(contour) # extract the sizes of the x & y axis and the sizes of the height and width
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) # draw a rect around the original frame (colour frame)
                                                              # the colour of the rectangle '(0, 255, 0)', '3' is the width of the rectangle
        if rectangle.any():
            status = 1 # if object is detected, status value will be updated to 1
            cv2.imwrite(f"images/{count}.png", frame) # To store images 
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]
    
    status_list.append(status) # save the status of object detection in this list
    status_list = status_list[-2:] # modifies the list tow only the last two items to see if they have changed or not 

    if status_list[0] == 1 and status_list[1] == 0: # this means that the object has exited the frame as [1, 1] means it is still in th frame
        # Threading will help prevent the video from pausing when detecting frames
        send_email_thread = Thread(target=send_email, args=(image_with_object, )) # the target is the function 'send_email', and the arguments are what is going to be passed into the function
        send_email_thread.daemon = True # this allows the send email function to be executed in the background
        #send_email(image_with_object)
        clean_thread = Thread(target=clean_folder) # the target is the function 'clean_folder', and no arguments are passed into the function
        clean_thread.daemon = True # this allows the clean_folder function to be executed in the background
        #clean_folder()

        # Calling the threads
        send_email_thread.start() # this will start this thread and the thread will call the "send_email" function

    print(status_list)


    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) # this creates a keyboard key object

    if key == ord("q"): # if the user presses the key "q", it will break the loop and then it will release the video
        break

video.release()
clean_thread.start() # this will start this thread and the thread will call the "clean_folder" function
                    # this is outside of the while loop because we only want to clean the image folder after the user has pressed the "q" key
