import pyautogui
import random
import time
import threading
import sys
import pystray
from PIL import Image

# -------------------
# 鼠标自动移动逻辑
# -------------------
running = True

def move_mouse():
    global running
    print("程序开始运行，在系统托盘可以退出。")

    last_big_move = time.time()
    big_interval = 60 + random.randint(0, 30)

    while running:
        x, y = pyautogui.position()

        # 检查是否需要大范围移动
        if time.time() - last_big_move >= big_interval:
            screen_width, screen_height = pyautogui.size()
            big_x = random.randint(0, screen_width - 1)
            big_y = random.randint(0, screen_height - 1)
            pyautogui.moveTo(big_x, big_y, duration=0.5)
            print(f"[{time.strftime('%H:%M:%S')}] 执行大范围随机移动，间隔 {big_interval} 秒")
            
            last_big_move = time.time()
            big_interval = 60 + random.randint(0, 30)
        else:
            # 小范围移动
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            pyautogui.moveTo(x + dx, y + dy, duration=0.2)

            # 小范围移动等待：5 秒 + 0~5 秒
            small_interval = 5 + random.randint(0, 5)
            print(f"[{time.strftime('%H:%M:%S')}] 小范围移动，等待 {small_interval} 秒")
            time.sleep(small_interval)

    print("程序已退出。")

# -------------------
# 托盘图标逻辑
# -------------------
def on_exit(icon, item):
    global running
    running = False
    icon.stop()
    sys.exit(0)

def setup_tray():
    image = Image.open("icon.ico")  # 你准备的图标
    menu = pystray.Menu(pystray.MenuItem("退出", on_exit))
    icon = pystray.Icon("摸鱼助手", image, "摸鱼助手", menu)
    icon.run()

# -------------------
# 主入口
# -------------------
if __name__ == "__main__":
    t = threading.Thread(target=move_mouse, daemon=True)
    t.start()
    setup_tray()
