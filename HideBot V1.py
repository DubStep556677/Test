import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import time
import cv2
import numpy as np
import keyboard
import json
import ssl
import urllib.request
def create_window():
    # Создаем главное окно
    window = tk.Tk()
    window.title("Автоматические Скриншоты")
    return window

url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
def find_contours(img):
    with urllib.request.urlopen(url, context=ssl_context) as response:
        data = json.load(response)
    range = data["activePlayer"]["championStats"]["attackRange"]
    range2 = int(range*0.85)
    # Конвертируем изображение в формат HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Задаем цветовой диапазон для поиска контура
    lower_color = np.array([38, 52, 171])
    upper_color = np.array([49, 60, 173])
    lower_color2 = np.array([5, 52, 60])
    upper_color2 = np.array([5, 52, 61])
    lower_color3 = np.array([2, 7, 63])
    upper_color3 = np.array([2, 7, 64])
    # Создаем маску для выделения контура по цвету
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
    mask3 = cv2.inRange(hsv, lower_color3, upper_color3)
    # Применяем пороговую обработку к маске
    _, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    _, thresh2 = cv2.threshold(mask2, 127, 255, cv2.THRESH_BINARY)
    _, thresh3 = cv2.threshold(mask3, 127, 255, cv2.THRESH_BINARY)
    kernel = np.array([[0, 1, 1, 1, 0],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [0, 1, 1, 1, 0],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1]], dtype=np.uint8)
    # Применение морфологического преобразования
    morphed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Находим контуры на пороговом изображении
    #contours, _ = cv2.findContours(morphed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours22 = sorted(contours2, key=cv2.contourArea, reverse=True)[:1]
    for contour2 in sorted_contours22:
        x, y, w, h = cv2.boundingRect(contour2)
        mask_around_contour = np.zeros_like(morphed_img)  # Создаем пустую маску
        cv2.rectangle(mask_around_contour, (x + range2, y - range2), (x - range2, y + range2), (255, 255, 255), -1)  # Заполняем область вокруг контура

        # Применение маски к исходному изображению
        masked_image = cv2.bitwise_and(mask, mask_around_contour)

        # Поиск контуров внутри маски
        contours, _ = cv2.findContours(masked_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Сортируем контуры по убыванию площади
        sorted_contours3 = sorted(contours, key=len, reverse=True)[0:8]
        #sorted_contours3 = sorted(sorted_contours, key=len, reverse=False)[0:1]
        def distance_to_top_contour(contour):
            cx, cy, _, _ = cv2.boundingRect(contour)
            return np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        sorted_contours4 = sorted(sorted_contours3, key=distance_to_top_contour, reverse=False)[0:1]
        for contour3 in sorted_contours4:
            x3, y3, w3, h3 = cv2.boundingRect(contour3)
            mask_around_contour = np.zeros_like(thresh3)  # Создаем пустую маску
            cv2.rectangle(mask_around_contour, (x3 + 110, y3 - 15), (x3 - 110, y3 + 15), (255, 255, 255),
                          -1)  # Заполняем область вокруг контура
            # Применение маски к исходному изображению
            masked_image2 = cv2.bitwise_and(mask3, mask_around_contour)

            # Поиск контуров внутри маски
            contours3, _ = cv2.findContours(masked_image2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # Сортируем контуры по убыванию площади
            sorted_contours3 = sorted(contours3, key=len, reverse=True)[0:1]
    #sorted_contours2 = sorted(sorted_contours, key=len, reverse=True)[0:1]
    # Возвращаем первые восемь контуров или меньше, если их количество меньше восьми
            return sorted_contours3#[:min(len(sorted_contours3), 1)]

def update_screenshot(window):
    with urllib.request.urlopen(url, context=ssl_context) as response:
        data = json.load(response)
    # Делаем скриншот и сохраняем его в переменную
    screenshot = pyautogui.screenshot()

    # Конвертируем скриншот в формат, подходящий для OpenCV
    frame = np.array(screenshot)

    # Ищем контуры
    contours = find_contours(frame)

    def s(ats):
        a = 0.74 / ats * 0.40
        m = 1 / ats * 0.61
        return a, m

    if keyboard.is_pressed('space'):
    # Если контуры найдены, выводим координаты самого большого контура
     if contours:
        # Итерируем по всем контурам и получаем ограничивающие прямоугольники
        for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                keyboard.press('p')
                keyboard.press('o')
                attack_speed = data["activePlayer"]["championStats"]["attackSpeed"]
                attack, move = s(attack_speed)
                start_x, start_y = pyautogui.position()
                pyautogui.PAUSE = 0.01
                pyautogui.moveTo(x+60, y+110, _pause=True)
                # keyboard.press('e')
                pyautogui.mouseDown(button='right')
                pyautogui.mouseUp(button='right')
                # keyboard.release('e')
                time.sleep(0.0000001)
                pyautogui.moveTo(start_x, start_y, _pause=False)
                pyautogui.moveTo(start_x, start_y, _pause=False)
                time.sleep(attack)
                start_time = time.time()
                while time.time() - start_time <= move:
                    pyautogui.mouseDown(button='right')
                    pyautogui.mouseUp(button='right')
                    time.sleep(0.025)
                    if time.time() - start_time >= move:
                        keyboard.send('space', do_press=False, do_release=True)
                        break
     else:
        keyboard.press('p')
        keyboard.press('o')
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(0.03)
    else:
        keyboard.release('p')
        keyboard.release('o')

    #else:
        # Если контуры не найдены, выводим сообщение
        #print("Контуры не найдены.")

    # Конвертируем изображение обратно в формат, подходящий для Tkinter
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    # Если label уже содержит изображение, обновляем его
    if hasattr(update_screenshot, 'image_label'):
        update_screenshot.image_label.config(image=imgtk)
        update_screenshot.image_label.image = imgtk
    else:
        # Иначе создаем новый label с изображением
        update_screenshot.image_label = tk.Label(window, image=imgtk)
        update_screenshot.image_label.image = imgtk
        update_screenshot.image_label.pack()

    # Устанавливаем таймер на следующий скриншот
    window.after(10, lambda: update_screenshot(window))  # 16 миллисекунд между скриншотами

root = create_window()
update_screenshot(root)  # Запускаем первый скриншот и обновление окна
root.mainloop()
