import cv2

big_image=cv2.imread('000003.jpg')
small_image=cv2.resize(big_image,(612,512))
y,x,_=big_image.shape

scale_y=y/512
scale_x=x/612

cv2.rectangle(small_image, (100,100), (300,300),(0,0,0),3)
cv2.imshow('small',small_image)

cv2.rectangle(big_image,(int(100*scale_y),int(100*scale_x)),(int(300*scale_y),int(300*scale_x)),(0,0,0),3)
cv2.imshow('big',big_image)

cv2.waitKey(0)
