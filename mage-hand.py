import pyautogui
import cv2
from screeninfo import get_monitors
 
fist_cascade = cv2.CascadeClassifier('fist.xml') 
palm_cascade = cv2.CascadeClassifier('palm.xml')

#Gets Monitor info for use later
monitors = get_monitors()
Mwidth = float(monitors[0].width)
Mheight = float(monitors[0].height)

#Main function for detecting our fists and palm
def detect(gray, frame, widthRatio, heightRatio): 
    fists = fist_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x, y, w, h) in fists: 
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2) 
        positionTuple = pyautogui.position()
        yLoc = float(positionTuple[1])

        #Adjusts mouse y offset depenfing on if the position of the mouse is higher or lower than the monitor's height/2
        xPos = ((x+(.5*w)) * widthRatio)
        if(yLoc > Mheight/2):
            yPos = ((y+(h)) * (heightRatio * 1.5))
            pyautogui.moveTo(xPos, yPos)
        else:
            yPos = ((y+(h)) * (heightRatio))
            if yPos < 0:
                pyautogui(xPos, 9)
            else:
                pyautogui.moveTo(xPos, yPos)  
        
    #Palm detection
    palm = palm_cascade.detectMultiScale(gray, 1.3, 5)
    for(px, py, pw, ph) in palm:
        cv2.rectangle(frame, (px,py), ((px +pw), (py + ph)), (0, 0, 255), 2)
        pyautogui.click()

    return frame 


video_capture = cv2.VideoCapture(0) 
clickCount = False

while video_capture.isOpened():
    #Gets Dimensions of Camera 
    camWidth = float(video_capture.get(3))
    camHeight = float(video_capture.get(4))
    widthRatio = Mwidth/camWidth
    heightRatio = Mheight/camHeight

    _, frame = video_capture.read() 
    frame = cv2.flip(frame,1) 
  
    # To capture image in monochrome                     
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
      
    # calls the detect() function     
    canvas = detect(gray, frame, widthRatio, heightRatio)    
  
    # Displays the result on camera feed                      
    cv2.imshow('Video', canvas)  
  
    # The control breaks once q key is pressed                         
    if cv2.waitKey(1) & 0xff == ord('q'):                
        break
  
# Release the capture once all the processing is done. 
video_capture.release()                                  
cv2.destroyAllWindows() 