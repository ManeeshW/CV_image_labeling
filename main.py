import cv2
import os
ImgDir = os.getcwd() + '/' 
Test_no = 44
  
# Lists to store the bounding box coordinates
top_left_corner=[]
bottom_right_corner=[]
top_left_corner_scale=[]
bottom_right_corner_scale=[]

maxScaleUp = 100
scaleFactor = 0
#windowName = "Resize Image"
trackbarValue = "Scale"
 
# Mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x,y), radius, (255,0,0), -1)
        cv2.imshow("Window",image)
        
# function which will be called on mouse input
def drawLine(action, x, y, flags, *userdata):
  # Referencing global variables 
  global top_left_corner,top_left_corner_scale, bottom_right_corner,bottom_right_corner_scale, scaledImg, image
  # Mark the top left corner when left mouse button is pressed
  scaleValue = cv2.getTrackbarPos('Scale', 'Window')
  scaleFactor = 1+ scaleValue/100.0
  print(scaleValue)
  cv2.displayOverlay("Window", str(1.34445))
  cv2.displayStatusBar("Window", "FFFFFF"	) 
  #cv2.circle(scaledImg, (x,y), 10, (255,0,0), -1)
  #cv2.imshow("Window",scaledImg)
  #scaledImg = cv2.resize(image, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)
#  scaleImg = scaleImage(radius)
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner = [(x,y)]
    top_left_corner_scale = [(int(x/scaleFactor),int(y/scaleFactor))]
    # When left mouse button is released, mark bottom right corner
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner = [(x,y)]  
    bottom_right_corner_scale = [(int(x/scaleFactor),int(y/scaleFactor))]
    # Draw the rectangle
    cv2.rectangle(image, top_left_corner_scale[0], bottom_right_corner_scale[0], (0,255,0),2, 8)
    cv2.rectangle(scaledImg, top_left_corner[0], bottom_right_corner[0], (0,255,0),2, 8)
    cv2.imshow("Window",scaledImg)

# Create the function for the trackbar since its mandatory but we wont be using it so pass.
def scaleIt(x):
    global scaledImg
    scaledImg = scaleImage(x)
    cv2.imshow("Window",scaledImg)
    pass
   
def scaleImage(value=0):
    global scaledImg
    # Get the scale factor from the trackbar 
    scaleFactor = 1+ value/100.0
    # Resize the image
    scaledImg = cv2.resize(image, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)
    return scaledImg
    


def back(*args):
    pass    
    
    
# Read Images
image = cv2.imread(ImgDir + "input_data/Test_{}/1.png".format(Test_no))

scaledImg= image.copy()
# Make a temporary image, will be useful to clear the drawing
temp = image.copy()
# Create a named window
cv2.namedWindow("Window")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", drawLine)
# Create trackbar and associate a callback function / Attach mouse call back to a window and a method
#cv2.setMouseCallback('Window', draw_circle)
cv2.createButton("Window",back)
# Create trackbar and associate a callback function / create trackbars Named Radius with the range of 150 and starting position of 5.
cv2.createTrackbar('Radius', 'Window', 0, 200, scaleIt) 
# Create trackbar and associate a callback function
#cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scaleImage)

k=0
# Close the window when key q is pressed
while k!=113:
  
  # Display the image
  scaledImg = scaleImage()
#  cv2.imshow(windowName, scaledImage) 
  cv2.imshow("Window",scaledImg)
  k = cv2.waitKey(0)
  # If c is pressed, clear the window, using the dummy image
  if (k == 99):
    print('reset')
    cv2.setTrackbarPos('Radius', 'Window', 0)
    image= temp.copy()
    cv2.imshow("Window", image)
    
c = cv2.waitKey(0)
cv2.destroyAllWindows() 



 

 

 

 
 

 
#while True:
#     
#    cv2.imshow('image',img)
#     
#    # get the updated values from the trackbar
#    radius = cv2.getTrackbarPos('Radius', 'image')
# 
#    if cv2.waitKey(20) & 0xFF == 27:
#        break
#         
#cv2.destroyAllWindows()
