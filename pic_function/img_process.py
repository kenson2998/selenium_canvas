from PIL import Image # pip install Pillow
from pytesseract import image_to_string
import pytesseract, os, requests, shutil
import cv2
import numpy as np


def save_pic(pic_url, pic_name):
    '''
    :param pic_url: 'https://xxx.xxxxx.jpg'
    :param pic_name: 'picture.jpg'
    :return pic_name
    '''
    headers = {
        'user-agent': 'Mozilla/6.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3359.181 Safari/537.36'}
    html = requests.get(pic_url, headers=headers)
    with open(pic_name, 'wb') as file:
        file.write(html.content)
    return pic_name


def OCR_Procs(picname, driver=None, img_ele=None):
    app_path = os.path.dirname(os.path.abspath(__file__))
    '''
    :param driver: selenium 浏览器
    :param img_ele: 验证马 css ".validate-img"
    :param picname: 图片档名
    :return ocr_text: 图转文字的内容
    '''
    if driver:  # 有driver就執行class搜索img_ele 元素
        codeimage = driver.find_element_by_css_selector(img_ele)
        left = codeimage.location['x']
        top = codeimage.location['y']
        elementWidth = codeimage.location['x'] + codeimage.size['width']
        elementHeight = codeimage.location['y'] + codeimage.size['height']
        print(f"X:{elementWidth},Y:{elementHeight}")
        driver.save_screenshot(os.path.join(app_path, picname))
        driver.save_screenshot(os.path.join(app_path, picname))
        pic = Image.open(os.path.join(app_path, picname))
        pic = pic.crop((left, top, elementWidth, elementHeight))
        pic.save(os.path.join(app_path, picname))

    image = Image.open(os.path.join(app_path, picname))
    imgry = image.convert("L")
    threshold = 150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    out.save(os.path.join(app_path, picname))
    ocr_text = OCR_judge(imgry)
    return ocr_text


def OCR_judge(img):
    '''
    :param img: "pic.jpg" or image
    :return: 回传文字
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ORC_PATH = os.path.join(BASE_DIR, 'Tesseract-OCR')
    if os.path.exists(ORC_PATH) is True:
        pass
    else:
        shutil.copytree(os.path.join(BASE_DIR, 'Tesseract-OCR'), ORC_PATH)
    pytesseract.pytesseract.tesseract_cmd = ORC_PATH + r'\tesseract.exe'
    # ocr_text = image_to_string(img, config='-psm 7', lang='chi_sim')
    ocr_text = image_to_string(img, config='-psm 7')
    print(f"result: {ocr_text} ({img})")
    return ocr_text


def Opencv_noise(picname, level=7):
    image = cv2.imread(picname)
    # remove_noise
    image_mid_blur = np.hstack(
        [cv2.medianBlur(image, level)])  # 邻域越大，过滤椒盐噪声效果越好，但是图像质量也会下降明显。除非非常密集椒盐噪声，否则不推荐Ksize=7这么大的卷积核
    cv2.imwrite(picname, image_mid_blur)
    cv2.imwrite('noise.png', image_mid_blur)
    return OCR_judge(picname)


def Opencv_Gray(picname):
    image = cv2.imread(picname)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将输入转换为灰度图片
    cv2.imwrite(picname, img_hsv)
    cv2.imwrite('gray.png', img_hsv)
    OCR_judge(picname)


def Opencv_Black(picname):
    image = cv2.imread(picname)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # 执行边缘检测
    edged1 = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite(picname, edged1)
    cv2.imwrite('black.png', edged1)
    ocr_text = OCR_judge(picname)
    return ocr_text









if __name__ == "__main__":
    PIC_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png'
    # PIC_name = 'google.png'
    PIC_name1 = 'nice4.png'
    PIC_name = 'money2.png'
    with open(PIC_name1, 'rb') as f1, open(PIC_name, 'wb') as f2:
        f2.write(f1.read())
    # save_pic(PIC_url, PIC_name)  # 下载存图
    OCR_judge(PIC_name)  # 直接判断图片回传结果
    OCR_Procs(picname=PIC_name)  # 处理图片回传结果
    Opencv_noise(picname=PIC_name)  # opencv 辨识
    Opencv_Gray(picname=PIC_name)  # opencv 辨识
    Opencv_Black(picname=PIC_name)  # opencv 辨识
