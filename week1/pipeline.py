import numpy as np
import cv2
import math


def set_region_of_interest(img, vertices):
    """

    :param img:       대상 이미지
    :param vertices:  이미지에서 남기고자 하는 영역의 꼭짓점 좌표 리스트
    :return: img 관심 영역만 마스킹 된 이미지
    """

    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)

    return cv2.bitwise_and(img, mask)

def run(img):
    height, width = img.shape[:2]
    vertices = np.array([[(50, height),
                          (width // 2 - 45, height // 2 + 60),
                          (width // 2 + 45, height // 2 + 60),
                          (width - 50, height)]])

    # 1) BGR -> GRAY 영상으로 색 변환
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2) 이미지 내 노이즈를 완화시키기 위해 blur 효과 적용
    blur_img = cv2.GaussianBlur(gray_img, (7, 7), 0)

    # 3) 캐니 엣지 검출을 사용하여 엣지 영상 검출
    edge_img = cv2.Canny(blur_img, threshold1=70, threshold2=140)

    # 4) 관심 영역(ROI; Region Of Interest)을 설정하여 배경 영역 제외
    roi_img = set_region_of_interest(edge_img,vertices)

    # 5) 허프 변환을 사용하여 조건을 만족하는 직선 검출
    #lines = cv2.HoughLinesP(roi_img,1, 1*np.pi/180, 30, np.array([]))
    #Review
    lines = cv2.HoughLinesP(roi_img,
                            rho=1, # 거리 해상도(pixel)
                            theta = np.pi/180, # 각도 해상도(radian)
                            threshold=10, # 변환공간에서 만나야 하는 점의 기준
                            minLineLength=15,# 이 값보다 작으면 직선으로 검출하지 않음
                            maxLineGap=40) # 이 값보다 크면 서로 다른 직선으로 판단

    #result = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    result = np.copy(img)
    # 6) 찾은 직선들을 입력 이미지에 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            #cv2.line(result, (x1, y1), (x2, y2), color=[255,255,255], thickness=2)
            # Review
            cv2.line(result, (x1,y1), (x2,y2), (0,0,255), 5) # B, G,R

    return result

if __name__ == "__main__":

    img = "1.jpg"
    cv2.imshow('img', img)
    result = run(img)
    cv2.imshow('result',result)
    cv2.waitKey(0)

    '''
    cap = cv2.VideoCapture(mp4)

    while True:
        ok, frame = cap.read()
        # 엣지를 비디오 단위로 처리
        edge_img = run(frame)
        cv2.imshow('edge', edge_img)
        #cv2.imshow('frame',frame)
        key = cv2.waitKey(30)
        if key == ord('x'):
            break

    cap.release()
    '''