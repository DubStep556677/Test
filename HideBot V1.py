import pyautogui
import imageio
import numpy as np
import time
import multiprocessing

def capture_screen(queue):
    fps = 25
    duration = 20
    screen_width, screen_height = pyautogui.size()
    writer = imageio.get_writer('screen_record.mp4', fps=fps)

    for _ in range(int(duration * fps)):
        img = pyautogui.screenshot()
        time.sleep(0.25 / fps)
        img_np = np.array(img)
        frame = imageio.core.util.Array(img_np)
        writer.append_data(frame)

    writer.close()
    queue.put("Done")

if __name__ == "__main__":
    process_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=capture_screen, args=(process_queue,))
    process.start()

    # Ждем, пока процесс не закончит запись видео
    while True:
        if not process.is_alive():
            break

    process.join()
    result = process_queue.get()
