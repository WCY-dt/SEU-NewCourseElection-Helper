# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import datetime
import os
import sys
import msvcrt

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


def Login():
    global t
    global error
    global username
    global password
    global teacher
    global driver
    global class_wanted
    global elecTurn

    try:
        driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
        driver.maximize_window()
        driver.set_window_size(500, 10000)
        url = "http://newxk.urp.seu.edu.cn/xsxk/profile/index.html"
        driver.get(url)
        
        print("start to login\n")

        print("\nplease wait.", end="")
        successLogin=False
        LoginTurn=1

        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').send_keys(username)
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').send_keys(password)

        while not successLogin:
            driver.find_element_by_xpath(
                '//*[@id="verifyCode"]').click()
            driver.find_element_by_xpath(
                '//*[@id="verifyCode"]').send_keys(str(0))
            driver.find_element_by_xpath('//*[@id="loginDiv"]/button').click()
            print(".", end="")
            time.sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div[4]/div/div[2]/div/table/tbody/tr['+str(elecTurn)+']/td/div/div/div[6]/div[2]/label/span[1]/span').click()
                successLogin=True
            except Exception as eLogin:
                successLogin=False
                print(".", end="")
                LoginTurn=LoginTurn+1
                time.sleep(1)

        time.sleep(1)
        
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
            print(username + '\t' + password + '\tlogin fail')
            error = True
            return
        
        

        print("login successfully!\n")
        return

    except Exception as e:
        print('\tlogin fail')
        error = True
        return


def main():

    try:
        finded = False
        print("finding.", end="")


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

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_elements_by_xpath(
                        './/*[@class="card-list course-jxb el-row"]/div')
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element_by_xpath(
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\nfinded\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("the "+str(Turn)+" trail")
                                Turn=Turn+1
                                tl.find_element_by_xpath(
                                    './/*[@class="el-row"]/button[2]').click()
                                if not (driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                                    elected=True
                                    break
                                driver.find_element_by_xpath(
                                    '/html/body/div[3]/div/div[3]/button[2]').click()
                                time.sleep(5)
                                
                            
                            print("\nelected!\n")
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

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_elements_by_xpath(
                        './/*[@class="card-list course-jxb el-row"]/div')
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element_by_xpath(
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\nfinded\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("the "+str(Turn)+" trail")
                                Turn=Turn+1
                                tl.find_element_by_xpath(
                                    './/*[@class="el-row"]/button[2]').click()
                                if not (driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                                    elected=True
                                    break
                                driver.find_element_by_xpath(
                                    '/html/body/div[3]/div/div[3]/button[2]').click()
                                time.sleep(5)
                                
                            
                            print("\nelected!\n")
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

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements_by_xpath(
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[1]').text\
                    + " "\
                    + cl.find_element_by_xpath(
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[2]').text
                print(".", end="")
                if class_wanted == class_num:
                    print("\n\nfinded\n")
                    finded = True
                    Turn=1
                    elected=False
                    while not elected:
                        print("the "+str(Turn)+" trail")
                        Turn=Turn+1
                        tl.find_element_by_xpath(
                            './/*[@class="el-row"]/button[3]').click()
                        if not (driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                            elected=True
                            break
                        driver.find_element_by_xpath(
                            '/html/body/div[3]/div/div[3]/button[2]').click()
                        time.sleep(5)
                                
                        
                    
                    print("\nelected!\n")
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

        if not finded:
            print("\n\nnot finded!\n")

        return

    except Exception as e:
        print('\tterminated')
        error = True
        return


if __name__ == '__main__':
    if "NAME" in os.environ:
        username = os.environ["NAME"]
    else:
        sys.exit()

    if "PASSWORD" in os.environ:
        password = os.environ["PASSWORD"]
    else:
        sys.exit() 

    if "TURN" in os.environ:
        elecTurn = os.environ["TURN"]
    else:
        elecTurn = "1"

    if "CLASS" in os.environ:
        class_wanted = os.environ["CLASS"]
    else:
        sys.exit()

    error = False
    Login()
    if not error:
        main()
