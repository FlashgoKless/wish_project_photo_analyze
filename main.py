import face_recognition as fr
import cv2

image_fr = fr.load_image_file('1.jpg')
image_cv = cv2.imread('1.jpg')
landmarks = fr.face_landmarks(image_fr)[0]
keys = ['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip']

def landmarks_out(landmarks = landmarks, keys = keys):
    '''
        постепенный вывод всех точек словаря landmarks
    '''
    for key in keys:
        ch = landmarks[key]
        flag = False
        for point in ch:
            cv2.circle(image_cv, point, 1, (0, 0, 255), 5)
            if flag == True:
                cv2.line(image_cv, point, last_p, (0, 0, 255), 1)
            flag = True
            last_p = point
            cv2.imshow('kkk', image_cv)
            cv2.waitKey(0)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)

def chin(key = keys[0], landmarks = landmarks):
    '''
    return: возвращает следующий список:
     1 элемент - ширина челючсти
     2 элемент - высота челюсти
    '''

    lst = []
    left_point_chin, right_point_chin = landmarks[key][0], landmarks[key][-1]

    a = abs(left_point_chin[0] - right_point_chin[0])
    b = abs(left_point_chin[1] - right_point_chin[1])
    res_1 = (a**2 + b**2) ** 0.5

    median_y_up = int((left_point_chin[1] + right_point_chin[1]) / 2) #среднее расстояние по оси y верхней части челюсти
    median_x_up = int((left_point_chin[0] + right_point_chin[0]) / 2) #среднее расстояние по оси x верхней части челюсти
    median_y_down = int((landmarks[key][7][1] + landmarks[key][8][1] + landmarks[key][9][1]) / 3) #среднее расстояние по оси y нижней части челюсти
    median_x_down = int((landmarks[key][7][0] + landmarks[key][8][0] + landmarks[key][9][0]) / 3) #среднее расстояние по оси x верхней части челюсти

    a =  abs(median_x_down - median_x_up)
    b = abs(median_y_up - median_y_down)
    res_2 = (a**2 + b**2) ** 0.5

    lst.append(res_1)
    lst.append(res_2)
    '''
    #вывод сравниваемых точек
    
    cv2.circle(image_cv, (left_point_chin), 1, (0, 0, 255), 5)
    cv2.circle(image_cv, (right_point_chin), 1, (0, 0, 255), 5)
    cv2.line(image_cv, left_point_chin, right_point_chin, (0, 0, 255), 1)

    cv2.circle(image_cv, (median_x_up, median_y_up), 1, (0, 0, 255), 5)
    cv2.circle(image_cv, (median_x_down, median_y_down), 1, (0, 0, 255), 5)
    cv2.line(image_cv, (median_x_up, median_y_up), (median_x_down, median_y_down), (0, 0, 255), 1)

    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''
    return lst

def eyebrows(key_eyebrow_left = keys[1], key_eyebrow_right = keys[2], landmarks = landmarks):
    '''
        return: возвращает следующий списокЖ
        1 элемент - средняя длина брови
        2 элемент - средняя высота брови
        3 элемент - кратчайшее расстояние между бровями
        4 элемент - широчайшее расстояние между бровями
    '''

    lst = []

    for eyebrows in (key_eyebrow_left, key_eyebrow_right):
        last_point = eyebrows[0]
        res = 0
        for index_point in range(1, len(eyebrows)):
            a = abs(last_point[0] - eyebrows[index_point][0])
            b = abs(last_point[1] - eyebrows[index_point][1])
            res += (a ** 2 + b ** 2) ** 0.5
            last_point = eyebrows[index_point]
        lst.append(res)

    average_length = (lst[0] + lst[1]) / 2

    average_height = (abs(key_eyebrow_left[0][1] - key_eyebrow_left[-1][1]) + abs(
        key_eyebrow_right[0][1] - key_eyebrow_right[-1][1])) / 2

#landmarks_out()