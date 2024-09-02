import cv2
import matplotlib.pyplot as plt
img = cv2.imread("im3.jpeg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_hsv_equalized = img_hsv
img_hsv_equalized[:,:,2] = cv2.equalizeHist(img_hsv[:,:,2])
equalized_img = cv2.cvtColor(img_hsv_equalized, cv2.COLOR_HSV2BGR)
cv2.imshow("original image", img)
cv2.imshow("equalized image", equalized_img)
fig, ax = plt.subplots(1, 2, figsize=(11,5))
hist = cv2.calcHist([img],[2], None, [256], [0, 256])
ax[0].plot(hist)
ax[0].set_title("Histogram of the original image, Value Channel")
equalized_hist = cv2.calcHist([img_hsv_equalized], [2], None, [256], [0, 256])
ax[1].plot(equalized_hist)
ax[1].set_title("Equalized histogram, Value Channel")
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()