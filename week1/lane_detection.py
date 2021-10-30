import cv2


data_path = './data/'
img = cv2.imread(data_path + 'test_images/solidWhiteRight.jpg')

'''
result = week6_pipeline.run(img)

cv2.imshow('result', result)
cv2.waitKey(0)

cv2.destroyAllWindows()

'''
# 강의 코드
def pipeline(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# convert color to gray
    blurred_img = cv2.GaussianBlur(gray_img, (15,15), 0.0) # for remove noise : sigmoid=0.0

    t_high = 140  # threshold1
    t_low = 70 # threshold2
    edge_img = cv2.Canny(blurred_img, t_low, t_high)
    return edge_img

# # 동영상 테스트
mp4 = '/Users/anjimin/Desktop/SMU/2021_fall/Pattern_Recognition/AssignmentCode/data/test_videos/solidWhiteRight.mp4'
cap = cv2.VideoCapture(mp4)
#cap = cv2.VideoCapture(data_path + 'test_videos/solidWhiteRight.mp4')
'''
line detection for video image(.mp4)
while True:
     ok, frame = cap.read()
     if not ok:
         break

     result = pipeline.run(frame)

     cv2.imshow('result', result)
     key = cv2.waitKey(1)  # -1
     if key == ord('x'):
         break

cap.release()
cv2.destroyAllWindows()
'''
# 강의 코드
while True:
    ok, frame = cap.read()
    # 엣지를 비디오 단위로 처리
    edge_img = pipeline(frame)
    #cv2.imshow('frame', frame)
    cv2.imshow('edge', edge_img)
    # delay 30m/sec
    key = cv2.waitKey(30)
    if key == ord('x'):
        break

cap.release()