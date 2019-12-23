Selenium 操控 H5 canvas 元素
===
<video src="https://i.imgur.com/MDk8i0Z.mp4" width="800" height="600"  controls="controls">
</video>

## 使用原因
網頁canvas元素需要點擊裡面的東西時，我們會需要圖型判斷來做元素位置來點擊

因為selenium 無法對這個元素內的東西再做定位

於是使用google map 來當作操作範例

除了輸入框輸入"夜市" 不在此demo測試上

其餘動作都是使用圖型辨識確認x,y位置後點擊或是模擬拖移畫面


###### tags: `selenium` `canvas` `圖型操控`

:::info
- chrome version 79.0

- **pip install:**   
    - selenium==3.141.0
    - requests==2.22.0
    - opencv-python==4.1.2.30
    - Pillow==6.2.1
- 參考來源
    https://www.linkedin.com/pulse/html-canvas-testing-selenium-opencv-maciej-kusz
    
:::


## demo run
```
python main.py
```


## 功能介紹

img_Sliding(img, driver, Rtime=10, J=0.7)
用於模擬滑鼠或手機按住左滑畫面
