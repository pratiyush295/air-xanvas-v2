import numpy as np
import cv2

paint=True
er=False
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
status="draw"
f=open("mode.txt","w+")
f.write("clean")
f.close()


video=cv2.VideoCapture(0)
video.set(10,1000)

#############################################################
while True:
    check,img=video.read()
    if check==True:
        break
canvas=np.ones_like(img)*255
##############################################################
def nothing(x):
    pass

##############################################################

cv2.namedWindow("Setter")
cv2.createTrackbar("LH","Setter",0,179,nothing)
cv2.createTrackbar("LS","Setter",0,255,nothing)
cv2.createTrackbar("LV","Setter",0,255,nothing)
cv2.createTrackbar("UH","Setter",179,179,nothing)
cv2.createTrackbar("US","Setter",255,255,nothing)
cv2.createTrackbar("UV","Setter",255,255,nothing)
###############################################################
def blur(img):
    blur_img=cv2.GaussianBlur(img,(11,11),0)
    return blur_img
###############################################################
def hsv(blur_img):
    hsv_img=cv2.cvtColor(blur_img,cv2.COLOR_BGR2HSV)
    return hsv_img
################################################################

def track():
    lh=cv2.getTrackbarPos("LH","Setter")
    ls=cv2.getTrackbarPos("LS","Setter")
    lv=cv2.getTrackbarPos("LV","Setter")
    uh=cv2.getTrackbarPos("UH","Setter")
    us=cv2.getTrackbarPos("US","Setter")
    uv=cv2.getTrackbarPos("UV","Setter")

    return lh,ls,lv,uh,us,uv

################################################################

def mask_generator(lh,ls,lv,uh,us,uv,hsv_img):
    l_value=np.array([79,76,68])
    u_value=np.array([128,255,255])
    
    
    mask=cv2.inRange(hsv_img,l_value,u_value)
    kernel=np.ones((7,7),np.uint8)
    cv2.erode(mask,kernel,iterations=1)
    cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    cv2.dilate(mask,kernel,iterations=1)

    return mask
####################################################################
def contour_operation(mask,img):

 
    contour,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contour:
        area=cv2.contourArea(cnt)
        if area>170:
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
            cv2.circle(img,(x+10,y+5),8,(0,255,0),cv2.FILLED)
            #if x!=0 or y!=0:
    return x,y
######################################################################

def draw_rect(img):
    cv2.rectangle(img,(20,5),(100,60),(0,0,0),cv2.FILLED)
    cv2.putText(img,"ERASE ALL",(30,35),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),1)


    cv2.rectangle(img,(130,5),(210,60),(0,0,0),cv2.FILLED)
    cv2.putText(img,"ERASER",(140,35),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),1)

    cv2.rectangle(img,(240,5),(320,60),(0,255,0),cv2.FILLED)
    cv2.putText(img,"GREEN",(250,35),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)

    cv2.rectangle(img,(350,5),(430,60),(0,0,255),cv2.FILLED)
    cv2.putText(img,"RED",(360,35),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)

    cv2.rectangle(img,(470,5),(550,60),(255,0,0),cv2.FILLED)
    cv2.putText(img,"BLUE",(480,35),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)
    
    return img
#######################################################################
def write_file(a):
    f=open("mode.txt","w+")
    f.write(a)
    f.close()


######################################################################
def read_file():
    f=open("mode.txt","r+")
    a=f.read()
    f.close()
    return a



#######################################################################
def check_rect(x,y):
    #global past
    #print(past)
    if((x>20 and x<100) and (y>5 and y<60)):
        #print("CAUGHT")
        #past="erase"
        #return "clean"
        write_file("clean")
    if((x>130 and x<210) and (y>5 and y<60)):
        #print("HEUYU")
        #past="draw"
        #return "eraser"
        print("hiitt")
        write_file("eraser")
    if((x>240 and x<320) and (y>5 and y<60)):
        
        write_file("green")
    if((x>350 and x<430) and (y>5 and y<60)):
        write_file("red")

    if((x>470 and x<550) and (y>5 and y<60)):
        write_file("blue")
        
    else:
        pass
########################################################################
def clean(img,x,y):
    #for i in range(x,x+2):
    
    #cv2.circle(canvas,(x+10,y+5),12,(255,255,255),cv2.FILLED)
    canvas=np.ones_like(img)*255
    return canvas
########################################################################
def eraser(canvas,x,y):
    cv2.circle(canvas,(x+10,y+5),24,(255,255,255),cv2.FILLED)
    return canvas


#######################################################################
def pointer(x,y):
    cv2.circle(img,(x-5,y),3,(0,0,255),cv2.FILLED)
#######################################################################
def green(canvas,x,y):
    #for i in range(x,x+2):
        
    cv2.circle(canvas,(x+10,y+5),8,(0,255,0),cv2.FILLED)
    #cv2.circle(canvas,(x+15,y+10),8,(0,255,0),cv2.FILLED)
    return canvas
#######################################################################

def red(canvas,x,y):
    #for i in range(x,x+2):
        
    cv2.circle(canvas,(x+10,y+5),8,(0,0,255),cv2.FILLED)
    #cv2.circle(canvas,(x+15,y+10),8,(0,255,0),cv2.FILLED)
    return canvas
#########################################################################
def blue(canvas,x,y):
    #for i in range(x,x+2):
        
    cv2.circle(canvas,(x+10,y+5),8,(255,0,0),cv2.FILLED)
    #cv2.circle(canvas,(x+15,y+10),8,(0,255,0),cv2.FILLED)
    return canvas
#########################################################################
def face_blur(img):
    
    faces=face_cascade.detectMultiScale(img,1.05,5)
    for (x,y,w,h) in faces:
        cut=img[y:y+h,x:x+w]
        blur=cv2.GaussianBlur(cut,(91,91),100)
        img[y:y+h,x:x+w]=blur
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img,"DETECTED",(x,y-10),cv2.FONT_HERSHEY_COMPLEX,0.3,(0,255,0),1)
    return img



###########################################################################



while True:
    _,img=video.read()
    img=cv2.flip(img,1)
    
    blur_img=blur(img)
    hsv_img=hsv(blur_img)
    
    lh,ls,lv,uh,us,uv=track()
    
    mask=mask_generator(lh,ls,lv,uh,us,uv,hsv_img)

    img=draw_rect(img)
    
    x,y=contour_operation(mask,img)
    
    
    check_rect(x,y)
    status=read_file()
    
    if status=="clean":
        canvas=clean(canvas,x,y)
        pointer(x,y)
    if status=="green":
        canvas=green(canvas,x,y)
    if status=="eraser":
        canvas=eraser(canvas,x,y)
    if status=="red":
        canvas=red(canvas,x,y)
    if status=="blue":
        canvas=blue(canvas,x,y)

    #img=face_blur(img)  
    #cv2.imshow("MASK",mask)
    cv2.imshow("Recorder",img)
    cv2.imshow("Canvas",canvas)

    
    key=cv2.waitKey(1)
    if key==ord("q"):
        break
        
        
video.release()
cv2.destroyAllWindows()







    
    
