from appium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoAlertPresentException,InvalidElementStateException
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
import time,os
caps = {}
caps["platformName"] = "Android"
caps["platformVersion"] = "8.1"
caps["deviceName"] = "test"
caps["appPackage"] = "com.bbk.launcher2"
caps["appActivity"] = "com.bbk.launcher2.Launcher"
caps["unicodeKeyboard"] = True
caps["resetKeyboard"] = True
caps["noReset"] = True
caps["newCommandTimeout"] = 6000
caps["automationName"] = "Uiautomator2"


def is_exist(d,content):
    try:
        ele = d.find_element_by_android_uiautomator(content)
        ele.click()
        return True
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False


def switch_language(d,content):
    seconds = 120
    os.system("adb shell am start -a android.settings.LOCALE_SETTINGS")
    while True:
        if seconds > 0:
            if is_exist(d,content):
                break
            else:
                start = d.find_element_by_xpath('//*[@resource-id="android:id/list"]/*[last()-1]').location
                h = d.get_window_size()['height']
                d.swipe(0, 0.9 * h, 0, 0.1 * h, 5000)
                time.sleep(1)
                end = d.find_element_by_xpath('//*[@resource-id="android:id/list"]/*[last()-1]').location
                seconds -= 1
                print(f'start:{start}end:{end}')

                if start == end:
                    break
        else:
            print('超时')
            break
    os.system("adb shell am force-stop com.android.settings")


def open_wifi(d):
    os.system("adb shell am start -a android.net.wifi.PICK_WIFI_NETWORK")
    time.sleep(2)
    d.implicitly_wait(3)
    if d.find_elements_by_id('com.android.wifisettings:id/scanning_progress'):
        pass
    else:
        d.find_element_by_id('android:id/checkbox').click()
        time.sleep(1)
    os.system("adb shell am force-stop com.android.wifisettings")
    time.sleep(1)


def close_wifi(d):
    os.system("adb shell am start -a android.net.wifi.PICK_WIFI_NETWORK")
    time.sleep(2)
    d.implicitly_wait(3)
    if d.find_elements_by_id('com.android.wifisettings:id/scanning_progress'):
        d.find_element_by_id('android:id/checkbox').click()
        time.sleep(1)
    os.system("adb shell am force-stop com.android.wifisettings")
    time.sleep(1)


root = 'D:\project\img'
t_lan = ['English']

filename2lan = {'English': 'English','Assamese (India)': 'Assamese (India)','Gujarati (India)': 'Gujarati (India)','Hindi (India)': 'Hindi (India)','Kannada (India)': 'Kannada (India)','Malayalam (India)': 'Malayalam (India)','Marathi (India)': 'Marathi (India)','Odia (India)': 'Odia (India)','Punjabi (India)': 'Punjabi (India)','Sanskrit (India)': 'Sanskrit (India)','Tamil (India)': 'Tamil (India)','Telugu (India)': 'Telugu (India)','Arabic (Egypt)': 'Arabic (Egypt)','Maithili': 'Maithili','Bangla (Bangladesh)': 'Bangla (Bangladesh)','German (Germany)': 'German (Germany)','Spanish (Spain)': 'Spanish (Spain)','Spanish (United States)': 'Spanish (United States)','Filipino (Philippines)': 'Filipino (Philippines)','French (France)': 'French (France)','Indonesian (Indonesia)': 'Indonesian (Indonesia)','Italian (Italy)': 'Italian (Italy)','Japanese (Japan)': 'Japanese (Japan)','Khmer (Cambodia)': 'Khmer (Cambodia)','Korean (South Korea)': 'Korean (South Korea)','Lao (Laos)': 'Lao (Laos)','Malay (Malaysia)': 'Malay (Malaysia)','Burmese (Myanmar (Burma))': 'Burmese (Myanmar (Burma))','Burmese (ZG)': 'Burmese (ZG)','Nepali (Nepal)': 'Nepali (Nepal)','Dutch (Netherlands)': 'Dutch (Netherlands)','Portuguese (Brazil)': 'Portuguese (Brazil)','Portuguese (Portugal)': 'Portuguese (Portugal)','Russian (Russia)': 'Russian (Russia)','Sinhala (Sri Lanka)': 'Sinhala (Sri Lanka)','Thai (Thailand)': 'Thai (Thailand)','Urdu (Pakistan)': 'Urdu (Pakistan)','Vietnamese (Vietnam)': 'Vietnamese (Vietnam)','Chinese Simplified': 'Chinese Simplified','Traditional Chinese (Hong Kong SAR)': 'Traditional Chinese (Hong Kong SAR)','Traditional Chinese (Taiwan)': 'Traditional Chinese (Taiwan)'}

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
for one in t_lan:
    driver.implicitly_wait(0.5)
    switch_language(driver,'new UiSelector().text("English").resourceId("android:id/title")')
    switch_language(driver,f'new UiSelector().text("{filename2lan[one]}").resourceId("com.android.settings:id/summary")')
    driver.implicitly_wait(10)
    time.sleep(2)
    # 相册准备每个月份的照片，今日和昨日的照片,wifi开启并记住,
    # 准备1月份的连拍照(后拍出来的显示在前面),准备一首不能播放的乐曲
    # camera相册准备超过20张照片
    # 第二个相册准备一张格式是手机不支持的图片
    os.system("adb shell am start -n com.vivo.gallery/com.android.gallery3d.vivo.GalleryTabActivity")
    # time.sleep(2)
    # # 初始状态按月份显示
    # # tap photo gallery
    # driver.find_element_by_xpath(
    #     '//*[@resource-id="com.vivo.gallery:id/bottomBar"]//android.widget.FrameLayout[1]').click()
    # # TouchAction(driver).tap(x=190, y=2050).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root,one,'Albums','001_Albums_Camera picture_Month-1.png'))
    # # 滑到下一屏
    # driver.swipe(0,1950,0,260,5000)
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '002_Albums_Camera picture_Month-2.png'))
    # # 点最下方的照片进入显示成xx月xx日
    # TouchAction(driver).tap(x=70, y=1870).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '003_Albums_Camera picture.png'))
    # # 进入某张具体照片
    # TouchAction(driver).tap(x=400, y=1870).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '004_Albums_Camera.png'))
    # driver.press_keycode(4)
    # time.sleep(1)
    # # 选中连拍的照片
    # TouchAction(driver).tap(x=130, y=1870).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '005_Albums_CS.png'))
    # # tap burst photos
    # TouchAction(driver).tap(x=540, y=1890).perform()
    # time.sleep(1)
    # # 选中一项
    # TouchAction(driver).tap(x=500, y=800).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '006_Albums_CS_Select.png'))
    # driver.press_keycode(4)
    # time.sleep(1)
    # # tap delete
    # driver.find_element_by_id('com.vivo.gallery:id/delete').click()
    # # TouchAction(driver).tap(x=670, y=2070).perform()
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '007_Albums_CS_Delete.png'))
    # driver.press_keycode(4)
    # time.sleep(1)
    # driver.press_keycode(4)
    # time.sleep(1)
    # # 恢复成按月份显示
    # driver.find_element_by_xpath(
    #     '//*[@resource-id="com.vivo.gallery:id/vivo_title_view"]/android.widget.LinearLayout[2]').click()
    # # TouchAction(driver).tap(x=140, y=150).perform()
    # time.sleep(1)
    # tap albums
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/bottomBar"]//android.widget.FrameLayout[2]').click()
    # TouchAction(driver).tap(x=540, y=2040).perform()
    time.sleep(1)
    # tap +
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/vivo_title_view"]/android.widget.LinearLayout[3]/android.widget.Button[1]').click()
    # TouchAction(driver).tap(x=620, y=160).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root,one,'Albums','008_Albums_Add.png'))
    # create a photo movie
    driver.find_element_by_xpath(
        '//*[@resource-id="android:id/select_dialog_listview"]/android.widget.LinearLayout[2]').click()
    # TouchAction(driver).tap(x=540, y=2020).perform()
    time.sleep(1)
    # tap camera 分类
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/dreamway_folder_albumset_list"]/android.widget.RelativeLayout[1]').click()
    # TouchAction(driver).tap(x=520, y=320).perform()
    time.sleep(1)
    # 选中1张照片(圆圈区域有效)
    TouchAction(driver).tap(x=220, y=280).perform()
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root,one,'Albums','009_Albums_Movie.png'))
    # tap done
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/vivo_title_view"]/android.widget.LinearLayout[3]').click()
    # TouchAction(driver).tap(x=980, y=160).perform()
    time.sleep(1)
    # 向左滑动一屏
    driver.swipe(1040,1500,30,1500,5000)
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '010_Albums_Movie_Create_Templates.png'))
    # 退出提示
    driver.press_keycode(4)
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '011_Albums_Movie_Create_Cancel.png'))
    # 点击取消
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        pass
    # # tap opening credits
    # driver.find_element_by_id('com.vivo.videoeditor:id/et_input_main_title').send_keys('hello444')
    # TouchAction(driver).tap(x=740, y=2080).perform()
    # time.sleep(3)
    # os.system("adb shell input text 'hello444'")
    # time.sleep(1)
    # # 收起键盘
    # driver.press_keycode(4)
    # time.sleep(1)
    # driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '012_Albums_Movie_Create_Opening_Credits.png'))
    # driver.press_keycode(4)
    # time.sleep(1)
    # tap background music
    driver.find_element_by_id('com.vivo.videoeditor:id/rl_bgm').click()
    # TouchAction(driver).tap(x=540, y=1940).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '013_Albums_Movie_Create_Background music.png'))
    # tap customize background music
    driver.find_element_by_id('com.vivo.videoeditor:id/bgmusic_custome').click()
    # TouchAction(driver).tap(x=540, y=380).perform()
    time.sleep(1)
    # 点第一项(能播放的乐曲)
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.videoeditor:id/container"]//android.widget.TextView[1]').click()
    # TouchAction(driver).tap(x=540, y=300).perform()
    time.sleep(1)
    # 此处还需要准备不能播放的乐曲供选择
    driver.get_screenshot_as_file(
        os.path.join(root, one, 'Albums', '014_Albums_Movie_Create_Background music_Customize.png'))
    driver.press_keycode(4)
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(1)
    # tap photo gallery
    driver.find_element_by_id('com.vivo.videoeditor:id/rl_fix_pic').click()
    # TouchAction(driver).tap(x=540, y=1790).perform()
    time.sleep(1)
    # tap x
    driver.find_element_by_id('com.vivo.videoeditor:id/image_delete_button').click()
    # TouchAction(driver).tap(x=50, y=350).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '015_Albums_Movie_Photo_Gallery_Delete_all.png'))
    # tap +
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.videoeditor:id/title_view"]/android.widget.LinearLayout[3]').click()
    # TouchAction(driver).tap(x=1000, y=170).perform()
    time.sleep(1)
    # tap camera 分类
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/dreamway_folder_albumset_list"]/android.widget.RelativeLayout[1]').click()
    # TouchAction(driver).tap(x=520, y=320).perform()
    time.sleep(1)
    # 选中20张照片(圆圈区域有效)
    j = 0
    while j < 5:
        i = 0
        while i < 4:
            TouchAction(driver).tap(x=220+i*270, y=280+j*270).perform()
            i += 1
        j += 1
    time.sleep(1)
    driver.get_screenshot_as_file(
        os.path.join(root, one, 'Albums', '016_Albums_Movie_Create_Photo gallery_Add_Max photos.png'))
    # 反选
    j = 0
    while j < 5:
        i = 0
        while i < 4:
            TouchAction(driver).tap(x=220+i*270, y=280+j*270).perform()
            i += 1
        j += 1
    # tap done
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.gallery:id/vivo_title_view"]/android.widget.LinearLayout[3]').click()
    # TouchAction(driver).tap(x=970, y=170).perform()
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(1)
    # tap save
    driver.find_element_by_xpath(
        '//*[@resource-id="com.vivo.videoeditor:id/title_view"]/android.widget.LinearLayout[3]/android.widget.Button[2]').click()
    # TouchAction(driver).tap(x=970, y=100).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '017_Albums_Movie_Create_saving.png'))
    time.sleep(10)
    # 考虑保存创建MV对后面动作的影响,可能需要删掉
    # tap MV
    TouchAction(driver).tap(x=550, y=580).perform()
    time.sleep(1)
    # tap edit
    TouchAction(driver).tap(x=990, y=160).perform()
    time.sleep(1)
    # tap select all
    TouchAction(driver).tap(x=140, y=160).perform()
    time.sleep(1)
    # tap delete
    TouchAction(driver).tap(x=800, y=2060).perform()
    time.sleep(1)
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        pass
    except InvalidElementStateException:
        pass
    time.sleep(1)
    # 退出比较麻烦，直接杀掉进程，重新launch
    os.system("adb shell am force-stop com.vivo.gallery")
    time.sleep(1)
    os.system("adb shell am start -n com.vivo.gallery/com.android.gallery3d.vivo.GalleryTabActivity")
    time.sleep(1)
    # tap collage
    TouchAction(driver).tap(x=810, y=170).perform()
    time.sleep(1)
    # tap camera 分类
    TouchAction(driver).tap(x=520, y=320).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '017_Albums_Collage.png'))
    # 选中7张照片
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    TouchAction(driver).tap(x=130, y=350).perform()
    time.sleep(0.5)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '018_Albums_Collage_Select_Max.png'))
    # close wifi
    close_wifi(driver)
    # tap collage
    TouchAction(driver).tap(x=940, y=1810).perform()
    # 此处加载较慢
    time.sleep(2)
    # tap more
    TouchAction(driver).tap(x=120, y=1830).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '019_Albums_Collage_No Network.png'))
    driver.press_keycode(4)
    time.sleep(1)
    # tap puzzles
    TouchAction(driver).tap(x=810, y=2070).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '020_Albums_Collage_No Network_Cancel.png'))
    driver.press_keycode(4)
    time.sleep(1)
    # tap administrative
    TouchAction(driver).tap(x=860, y=150).perform()
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '021_Albums_Collage_No download template.png'))
    driver.press_keycode(4)
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(1)
    # open wifi
    open_wifi(driver)
    # 点击文字部分编辑(可变？)
    time.sleep(1)
    TouchAction(driver).tap(x=800, y=400).perform()
    time.sleep(1)
    driver.press_keycode(4)
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '0022_Albums_Collage_Text_edit.png'))
    driver.press_keycode(4)
    time.sleep(1)
    # tap save
    TouchAction(driver).tap(x=980, y=150).perform()
    time.sleep(0.2)
    driver.get_screenshot_as_file(
        os.path.join(root, one, 'Albums', '023_Albums_Collage_Select picture_Collage_Saving.png'))
    time.sleep(0.3)
    driver.get_screenshot_as_file(
        os.path.join(root, one, 'Albums', '024_Albums_Collage_Select picture_Collage_Save.png'))
    # 打开settings里面的albums
    os.system("adb shell am start -n com.vivo.gallery/com.android.gallery3d.vivo.SettingMenuActivity")
    time.sleep(1)
    driver.get_screenshot_as_file(os.path.join(root, one, 'Albums', '0025_Albums_Settings.png'))


# default_size = {'width': 1080, 'height': 2154}
# current_size = driver.get_window_size()
# width_rate = current_size['width']/default_size['width']
# height_rate = current_size['height']/default_size['height']