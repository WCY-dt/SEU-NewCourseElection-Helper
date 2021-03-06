# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import datetime
import os
import sys
import msvcrt
from PIL import Image

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

def pwd_input(): # 密码输入
    chars = []   
    while True:  
        newChar = msvcrt.getch().decode(encoding="utf-8")
        if newChar in '\r\n':             
             break   
        elif newChar == '\b':
             if chars:    
                 del chars[-1]   
                 msvcrt.putch('\b'.encode(encoding='utf-8'))
                 msvcrt.putch( ' '.encode(encoding='utf-8'))
                 msvcrt.putch('\b'.encode(encoding='utf-8'))                
        else:  
            chars.append(newChar)  
            msvcrt.putch('*'.encode(encoding='utf-8'))
    return (''.join(chars) )


def Login(): # 登录
    global t
    global msg
    global error
    global username
    global password
    global teacher
    global driver

    try:
        # 启动浏览器
        driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
        driver.maximize_window()
        driver.set_window_size(500, 10000)
        url = "http://newxk.urp.seu.edu.cn/xsxk/profile/index.html"
        driver.get(url)
        os.system('cls')
        print("开始登录\n")

        username = input("用户名：")
        print("密  码：",end="")
        password = pwd_input()
        print()

        # 截取验证码
        # verifycodepic = driver.find_element_by_xpath('//*[@id="vcodeImg"]')
        # location = verifycodepic.location
        # size = verifycodepic.size
        # print(location, size)
        screenshot = driver.get_screenshot_as_file('verficode.png')
        imgOrigin = Image.open('verficode.png')
        img=imgOrigin.crop((315,332,315+129,332+42))
        img.show()

        verifycode = input("验证码：")
        os.remove('verficode.png')

        # 模拟输入与点击
        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').send_keys(username)
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').send_keys(password)
        driver.find_element_by_xpath(
            '//*[@id="verifyCode"]').click()
        driver.find_element_by_xpath(
            '//*[@id="verifyCode"]').send_keys(verifycode)

        print("\n登陆中，请稍后.", end="")

        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="loginDiv"]/button').click()
        print(".", end="")

        time.sleep(2)
        elecTurn=input("\n\n选课轮次：")
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div[4]/div/div[2]/div/table/tbody/tr['+str(elecTurn)+']/td/div/div/div[6]/div[2]/label/span[1]/span').click()
        print(".", end="")

        time.sleep(1)
        driver.find_element_by_xpath(
           '//*[@id="xsxkapp"]/div[4]/div/div[3]/span/button[1]').click()
        print(".", end="")

        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="stundentinfoDiv"]/button').click()
        print(".", end="")

        time.sleep(2)
        print(".\n\n")

        checkUrl = driver.current_url
        print("\n"+checkUrl+"\n")
        if not checkUrl.startswith("http://newxk.urp.seu.edu.cn/xsxk/elective/"):
            print(username + '\t' + password + '\t登录失败')
            msg += username + '\t' + password + '\t登录失败\n\n'
            error = True
            # driver.quit()
            return
        
        os.system('cls')

        print("成功登录!\n")
        return

    except Exception as e:
        msg += '登录失败' + '\n\n' + str(e) + '\n\n'
        print('\t登录失败' + '\n' + str(e))
        error = True
        # driver.quit()
        return


def main():

    try:
        class_wanted = input("输入课程号：")

        finded = False
        # screenshot = driver.get_screenshot_as_file('a.png')
        # img = Image.open('a.png')
        # img.show()
        print("查找中.", end="")

        # 系统推荐课程

        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[2]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element_by_class_name('number.active').text
        # print("查找第"+pages+"页\n")

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            # print("classlist:")
            # print(class_list)
            # print("\n")
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                # print("即将查找"+class_wanted[0:-6]+"课程\n")
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    # print("查找到"+class_wanted[0:-6]+"课程\n")
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_elements_by_xpath(
                        './/*[@class="card-list course-jxb el-row"]/div')
                    # print("即将查找课程号"+class_wanted[-3:-1])
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element_by_xpath(
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        # print("正在查找课程号"+teacher_num[1:3])
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\n已找到\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("第"+str(Turn)+"次尝试")
                                Turn=Turn+1
                                tl.find_element_by_xpath(
                                    './/*[@class="el-row"]/button[2]').click()
                                try:
                                    driver.find_element_by_xpath(
                                        '/html/body/div[3]/div/div[3]/button[2]').click()
                                except Exception as eEle:
                                    elected=True
                                time.sleep(2)
                                os.system('cls')
                            os.system('cls')
                            print("\n已成功选上！\n")
                            break
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element_by_class_name('number.active').text
                # print("查找第"+pages+"页\n")

        # 体育项目

        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[5]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element_by_class_name('number.active').text
        # print("查找第"+pages+"页\n")

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            # print("classlist:")
            # print(class_list)
            # print("\n")
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                # print("即将查找"+class_wanted[0:-6]+"课程\n")
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    # print("查找到"+class_wanted[0:-6]+"课程\n")
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_elements_by_xpath(
                        './/*[@class="card-list course-jxb el-row"]/div')
                    # print("即将查找课程号"+class_wanted[-3:-1])
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element_by_xpath(
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        # print("正在查找课程号"+teacher_num[1:3])
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\n已找到\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("第"+str(Turn)+"次尝试")
                                Turn=Turn+1
                                tl.find_element_by_xpath(
                                    './/*[@class="el-row"]/button[2]').click()
                                try:
                                    driver.find_element_by_xpath(
                                        '/html/body/div[3]/div/div[3]/button[2]').click()
                                except Exception as eEle:
                                    elected=True
                                time.sleep(2)
                                os.system('cls')
                            os.system('cls')
                            print("\n已成功选上！\n")
                            break
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element_by_class_name('number.active').text
                # print("查找第"+pages+"页\n")
        
        # 通选课

        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[6]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element_by_xpath(
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element_by_class_name('number.active').text
        # print("查找第"+pages+"页\n")

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            # print("classlist:")
            # print(class_list)
            # print("\n")
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[1]').text\
                    + " "\
                    + cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[2]').text
                # print("查找到"+class_num+"课程\n")
                print(".", end="")
                if class_wanted == class_num:
                    print("\n\n已找到\n")
                    finded = True
                    Turn=1
                    elected=False
                    while not elected:
                        print("第"+str(Turn)+"次尝试")
                        Turn=Turn+1
                        tl.find_element_by_xpath(
                            './/*[@class="el-row"]/button[3]').click()
                        try:
                            driver.find_element_by_xpath(
                                '/html/body/div[3]/div/div[3]/button[2]').click()
                        except Exception as eEle:
                            elected=True
                        time.sleep(2)
                        os.system('cls')
                    os.system('cls')
                    print("\n已成功选上！\n")
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element_by_class_name('number.active').text
                # print("查找第"+pages+"页\n")

        if not finded:
            print("\n\n没找到!\n")

        return

    except Exception as e:
        print('\t选课中止' + '\n' + str(e))
        error = True
        # driver.quit()
        return


if __name__ == '__main__':
    error = False
    Login()
    if not error:
        main()
