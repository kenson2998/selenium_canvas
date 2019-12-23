from chrome_data.chrome_setting import *
from pic_function.selenium_img_find import *
from pic_function.img_process import save_pic
import requests, sys

# pip install Pillow
# pip install selenium
# pip install requests
# pip install pytesseract
# pip install opencv-python
# time.sleep(5)
# 滾動滑鼠往左滑
# for _ in range(5):
#     script_Sliding(d)
#     time.sleep(5)

if __name__ == '__main__':
    d = openchrome('https://www.google.com.tw/maps')
    img_list = ['師大夜市.png', '樂華夜市.png', '通化夜市.png', '饒河街觀光夜市.png', '公館夜市.png', '南機場夜市.png']
    if os.name == 'nt':
        pic_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pic')
    else:
        pic_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mac_pic')
    # 跳轉當判斷用
    if img_wait(os.path.join(pic_dir, 'search0.png'), d, Rtime=5) == 0:
        print('已找到search0.png')
    d.find_element_by_css_selector('#searchboxinput').send_keys('夜市')
    d.find_element_by_css_selector('#searchboxinput').send_keys(Keys.RETURN)
    time.sleep(3)

    # 找夜市列表
    for img in img_list:
        img_dir = os.path.join(pic_dir, img)
        back_img_dir = os.path.join(pic_dir, '返回結果.png')
        if img_wait(img_dir, d, Rtime=5) == 0:
            print(f'已找到{img}')
            img_single(img_dir, d, Rtime=5)
            img_single(back_img_dir, d, Rtime=5, J=0.5)
            time.sleep(2)
        else:
            print(f'未找到{img}')

    d.quit()
