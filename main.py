import cv2
import os
import numpy as np
from lib.plot import *
from lib.esti import *
from lib import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
ImgDir = os.getcwd() + '/' 

Test_no = 44
img_No = 1
Input_ImgDir = ImgDir + "input_data/Test_{}/".format(Test_no)
images = os.listdir(Input_ImgDir)
No_imgs_in_folder = len(images)
curr_img_no = 0
Pc = np.array([])
arry = []
catID = 1

Hws = np.zeros((No_imgs_in_folder,12))
Hcs = np.zeros((No_imgs_in_folder,12))
#camera 
K = np.loadtxt(ImgDir+"input_data/CameraProp/Blender_camera/K.txt")
Hc = np.array([[ 9.43276367e-01,  3.31965180e-01,  5.36798032e-03, -1.65780701e+00],
              [ 2.24966041e-02, -8.00382461e-02,  9.96537898e-01, -3.96238258e-01],
              [ 3.31245526e-01, -9.39889886e-01, -8.29662752e-02, -7.10493833e+00]])


# Make output dir Folders
try:
   out_img = ImgDir+"output_data/imgs/Test_{}".format(Test_no)
   os.mkdir(out_img)
except:
   pass

try:
   out_label = ImgDir+"output_data/output_labels/Test_{}".format(Test_no)
   os.mkdir(out_label)
except:
   pass

try:
   out_label = ImgDir+"output_data/output_labels/Test_{}/Annotations".format(Test_no)
   os.mkdir(out_label)
except:
   pass


# Lists to store the bounding box coordinates
top_left_corner=[]
bottom_right_corner=[]
top_left_corner_scale=[]
bottom_right_corner_scale=[]
Mouse_Move = []




maxScaleUp = 100
scaleFactor = 0
#windowName = "Resize Image"
trackbarValue = "Scale"

        
# function which will be called on mouse input
def drawLine(action, x, y, flags, *userdata):
  # Referencing global variables 
  global top_left_corner,top_left_corner_scale, bottom_right_corner,bottom_right_corner_scale, scaledImg, image, arry, Pc, curr_img_no, scaleFactor
  # Mark the top left corner when left mouse button is pressed
  scaleValue = cv2.getTrackbarPos('Scale', 'Window')
  scaleFactor = 1+ scaleValue/100.0
  
  #cv2.displayOverlay("Window", str(1.34445))
  cv2.displayStatusBar("Window", "Image No : {}      {}|{}".format(img_No,int(x/scaleFactor),int(y/scaleFactor))) 
  #cv2.circle(scaledImg, (x,y), 10, (255,0,0), -1)
  #cv2.imshow("Window",scaledImg)
  #
#  scaleImg = scaleImage(radius)
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner = [(x,y)]
    top_left_corner_scale = [(int(x/scaleFactor),int(y/scaleFactor))]
    
    #print(np.array([x,y]))
    arry.append([x,y])
    Pc = np.array(arry)

    #arr = np.append([arr,], axis=0)
    # When left mouse button is released, mark bottom right corner
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner = [(x,y)]  
    bottom_right_corner_scale = [(int(x/scaleFactor),int(y/scaleFactor))]
    # Draw the rectangle
    cv2.circle(scaledImg, top_left_corner[0], 1, (2,255,0), -1)
    cv2.circle(image, top_left_corner_scale[0], 1, (2,255,0), -1)
    # cv2.rectangle(image, top_left_corner_scale[0], bottom_right_corner_scale[0], (0,255,0),2, 8)
    # cv2.rectangle(scaledImg, top_left_corner[0], bottom_right_corner[0], (0,255,0),2, 8)
    cv2.imshow("Window",scaledImg)

  elif action == cv2.EVENT_MOUSEMOVE:
     cv2.circle(scaledImg, (x,y), 1, (255,20,200), -1)
     cv2.imshow("Window",scaledImg)
     scaledImg = cv2.resize(image, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)

  if curr_img_no != img_No:
     curr_img_no = img_No
     scaleValue = 0
     scaleFactor = 1
     cv2.setTrackbarPos('Scale', 'Window', 0)
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
    

def Next(*args):
    
    global img_No, image, scaledImg, Pc, arry
    img_no = img_No+1
    if img_no <= No_imgs_in_folder:
       img_No = img_no
    else:
       img_No = No_imgs_in_folder
    image = cv2.imread(ImgDir + "input_data/Test_{}/{}.png".format(Test_no, img_No))
    scaledImg= image.copy()
    Pc = np.array([])
    arry = []
    cv2.setTrackbarPos('Scale', 'Window', 0)
    cv2.imshow("Window",scaledImg)

def Refresh(*args):
    global img_No, image, scaledImg, Pc, arry
    image = cv2.imread(ImgDir + "input_data/Test_{}/{}.png".format(Test_no, img_No))
    scaledImg= image.copy()
    Pc = np.array([])
    arry = []
    cv2.imshow("Window",scaledImg)

def Back(*args):
    global img_No, image, scaledImg, Pc, arry
    img_no = img_No-1
    if img_no < 1:
       img_No = 1
    else:
       img_No = img_no
    image = cv2.imread(ImgDir + "input_data/Test_{}/{}.png".format(Test_no, img_No))
    scaledImg = image.copy()
    Pc = np.array([])
    arry = []
    cv2.setTrackbarPos('Scale', 'Window', 0)
    cv2.imshow("Window",scaledImg)
   
    
def Save(*args):
    global img_No, image, Pc, Hws, Hcs
    cv2.imwrite(out_img+'/{}.png'.format(img_No), image)
    np.savetxt(ImgDir+"output_data/output_labels/Test_{}/Annotations/Hc_Test_{}_gt.txt".format(Test_no,Test_no),Hcs)
    np.savetxt(ImgDir+"output_data/output_labels/Test_{}/Annotations/Hw_Test_{}_gt.txt".format(Test_no,Test_no),Hws)   

def Tick(*args):
    print("click")
    
def OpenImgLabel(*args):
    global img_No, Pc, Hws, Hcs
    fig = plt.figure(figsize=(6.4,4.8),dpi = 150)
    Hc, Hw = Epnp2Hc(PW_label, Pc, K, dist = None)
    Hcs[img_No-1,:] = Hc.reshape(1,12)
    Hws[img_No-1,:] = Hw.reshape(1,12)

    np.savetxt(ImgDir+"output_data/output_labels/Test_{}/Annotations/Hc_Test_{}_gt.txt".format(Test_no,Test_no),Hcs)
    np.savetxt(ImgDir+"output_data/output_labels/Test_{}/Annotations/Hw_Test_{}_gt.txt".format(Test_no,Test_no),Hws)

    global catID
    if catID == 11:
       catID = 1
    im = cv2.imread(ImgDir + "input_data/Test_{}/{}.png".format(Test_no, img_No))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
    pc = est_pc(Hc, K, cat_id = catID)
    catID = catID+1
    #plot_box(pc, clr_lines = "green", clr_corners = "red", clr_int_corners = "blue")
    plot_box(pc, clr_lines = "orange", corners = False, int_corners = False, linewidth=1.3,  label = 'TNN-PnP Est. for Real imgs')
    imshow(im)
    plt.savefig(ImgDir+"output_data/output_labels/Test_{}/{}.png".format(Test_no, img_No))
    im = cv2.imread(ImgDir+"output_data/output_labels/Test_{}/{}.png".format(Test_no, img_No))
    cv2.imshow("Label",im)
    cv2.waitKey(5000)  
    cv2.destroyWindow("Label") 
    fig.canvas.draw()
    fig.canvas.flush_events()
    catID = 1



# Read Images
image = cv2.imread(ImgDir + "input_data/Test_{}/{}.png".format(Test_no, img_No))

scaledImg= image.copy()
# Make a temporary image, will be useful to clear the drawing
temp = image.copy()
# Create a named window
cv2.namedWindow("Window")
cv2.namedWindow("Label")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", drawLine)
# Create trackbar and associate a callback function / Attach mouse call back to a window and a method
#cv2.setMouseCallback('Window', draw_circle)
# cv2.createButton("Window",back)
cv2.createButton("Back",Back,None,cv2.QT_PUSH_BUTTON,1)
cv2.createButton("Refresh",Refresh,None,cv2.QT_PUSH_BUTTON,1)
cv2.createButton("Next",Next,None,cv2.QT_PUSH_BUTTON,1)
cv2.createButton("Img-Label",OpenImgLabel,None,cv2.QT_PUSH_BUTTON,1)
cv2.createButton("Save",Save,None,cv2.QT_PUSH_BUTTON,1)

cv2.createButton("D1",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("D2",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("D3",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("D4",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("W1",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("W2",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("W3",Tick,None,cv2.QT_CHECKBOX,1)
cv2.createButton("W4",Tick,None,cv2.QT_CHECKBOX,1)

# Create trackbar and associate a callback function / create trackbars Named Radius with the range of 150 and starting position of 5.
cv2.createTrackbar('Scale', 'Window', 0, 200, scaleIt) 
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
    cv2.setTrackbarPos('Scale', 'Window', 0)
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
