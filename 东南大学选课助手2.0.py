# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
import datetime
import os
import sys
import msvcrt


# Instruction
# 1. you need to make sure your chrome has been
# linked with python environment(selenium)
# remember to change the path address to ur own(line:54)

# 2. fill in your own info at the end of the code

# 3. RUN!

# 4. this procedure is designed to help you
# keep waiting for one class, instead of picking it up
# at the earliest moment

# 5. IMPORTANT
# This code is ONLY for fun! No malicious usage is allowed based
# on it and the author won't be responsible for
# any possible consequences


# speed optimization
# Actually no options can speedup
# or delay the process o_o ....

chrome_options = webdriver.ChromeOptions()

# close headless to help u debug

# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# anyway its a trial of 0, so no need to load images
chrome_options.add_argument("blink-settings=imagesEnabled=false")

# chrome_options.page_load_strategy = 'eager'

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
        driver = webdriver.Chrome(executable_path=r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver"
                                  , options=chrome_options)
        driver.maximize_window()
        driver.set_window_size(500, 10000)
        url = "http://newxk.urp.seu.edu.cn/xsxk/profile/index.html"
        driver.get(url)
        
        print("start to login\n")

        print("\nplease wait.", end="")
        successLogin=False
        LoginTurn=1

        driver.find_element(by=By.XPATH,value='//*[@id="loginNameDiv"]/div/input').click()
        # username_input = driver.find_element(by = By.ID, value = "loginNameDiv")
        # username_input.send_keys(username)

        driver.find_element(by=By.XPATH,value=
            '//*[@id="loginNameDiv"]/div/input').send_keys(username)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="loginPwdDiv"]/div/input').click()
        driver.find_element(by=By.XPATH,value=
            '//*[@id="loginPwdDiv"]/div/input').send_keys(password)

        while not successLogin:
            driver.find_element(by=By.XPATH,value=
                '//*[@id="verifyCode"]').click()
            driver.find_element(by=By.XPATH,value=
                '//*[@id="verifyCode"]').send_keys(str(0))
            driver.find_element(by=By.XPATH,value='//*[@id="loginDiv"]/button').click()
            print(".", end="")
            time.sleep(1)
            try:
                driver.find_element(by=By.XPATH,value=
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
        driver.find_element(by=By.XPATH,value=
           '//*[@id="xsxkapp"]/div[4]/div/div[3]/span/button[1]').click()
        print(".", end="")

        time.sleep(1)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="stundentinfoDiv"]/button').click()
        print(".", end="")

        time.sleep(2)
        print(".\n\n")

        checkUrl = driver.current_url
        print("\n"+checkUrl+"\n")
        if not checkUrl.startswith("http://newxk.urp.seu.edu.cn/xsxk/elective/"):
            print('Login fail')
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


        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[2]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element(by=By.XPATH,value='//*[@class="number active"]').text

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements(by=By.XPATH,value=
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            # elements instead of element

            for cl in class_list:

                class_num = cl.find_element(by=By.XPATH,value=
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    # elements not element
                    teacher_list=cl.find_elements(by=By.XPATH,value=
                        './/*[@class="card-list course-jxb el-row"]/div')
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element(by=By.XPATH,value=
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\nfound\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("the "+str(Turn)+" trial")
                                Turn=Turn+1

                            # click select
                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        tl.find_element(by=By.XPATH,value='.//*[@class="el-row"]/button[2]').click()
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False
                            # confirm select
                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        msgText=driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False

                                if not (driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                                    elected=True
                                    break
                                driver.find_element(by=By.XPATH,value=
                                    '/html/body/div[3]/div/div[3]/button[2]').click()
                                
                            
                            print("\nelected!\n")
                            break
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element(by=By.XPATH,value='//*[@class="number active"]').text
        
        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[4]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element(by=By.XPATH,value='number.active').text

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements(by=By.XPATH,value=
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element(by=By.XPATH,value=
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_element(by=By.XPATH,value=
                        './/*[@class="card-list course-jxb el-row"]/div')
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element(by=By.XPATH,value=
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\nfinded\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("the "+str(Turn)+" trail")
                                Turn=Turn+1

                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        tl.find_element(by=By.XPATH,value='.//*[@class="el-row"]/button[2]').click()
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False

                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        msgText=driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False

                                if not (driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                                    elected=True
                                    break
                                driver.find_element(by=By.XPATH,value=
                                    '/html/body/div[3]/div/div[3]/button[2]').click()
                                
                            
                            print("\nelected!\n")
                            break
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element(by=By.XPATH,value='number.active').text

        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[5]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element(by=By.XPATH,value='number.active').text

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_element(by=By.XPATH,value=
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element(by=By.XPATH,value=
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                print(".", end="")
                if class_wanted[0:-5] == class_num:
                    cl.click()
                    time.sleep(0.2)
                    print(".", end="")
                    teacher_list=cl.find_elements(by=By.XPATH,value=
                        './/*[@class="card-list course-jxb el-row"]/div')
                    for tl in teacher_list:
                        print(".", end="")
                        teacher_num=tl.find_element(by=By.XPATH,value=
                            './/*[@class="card-item head"]/div[1]/span[1]').text
                        if class_wanted[-3:-1]==teacher_num[1:3]:
                            print("\n\nfinded\n")
                            finded = True
                            Turn=1
                            elected=False
                            while not elected:
                                print("the "+str(Turn)+" trial")
                                Turn=Turn+1
                                
                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        tl.find_element(by=By.XPATH,value='.//*[@class="el-row"]/button[2]').click()
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False

                                tmpErr=False
                                while not tmpErr:
                                    try:
                                        msgText=driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                        tmpErr=True
                                    except Exception as eTmp:
                                        tmpErr=False

                                if not (driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                                    elected=True
                                    break
                                driver.find_element(by=By.XPATH,value=
                                    '/html/body/div[3]/div/div[3]/button[2]').click()
                                
                            
                            print("\nelected!\n")
                            break
                    break
            if not finded:
                curpages = curpages+1
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element(by=By.XPATH,value='number.active').text

        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
        time.sleep(0.5)
        print(".", end="")
        driver.find_element(by=By.XPATH,value='//*[@id="xsxkapp"]/div/div[1]/ul/li[6]').click()
        time.sleep(1)
        print(".", end="")

        curpages = 1

        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
        driver.find_element(by=By.XPATH,value=
            '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
        time.sleep(1)
        print(".", end="")
        pages = driver.find_element(by=By.XPATH,value='number.active').text

        while str(pages) == str(curpages) and not finded:
            class_list = driver.find_elements(by=By.XPATH,value=
                '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
            for cl in class_list:
                class_num = cl.find_element(by=By.XPATH,value=
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[1]').text\
                    + " "\
                    + cl.find_element(by=By.XPATH,value=
                    './/*[@class="el-card__body"]/div[2]/div/div[2]/span[2]').text
                print(".", end="")
                if class_wanted == class_num:
                    print("\n\nfinded\n")
                    finded = True
                    Turn=1
                    elected=False
                    while not elected:
                        print("the "+str(Turn)+" trial")
                        Turn=Turn+1

                        tmpErr=False
                        while not tmpErr:
                            try:
                                tl.find_element(by=By.XPATH,value='.//*[@class="el-row"]/button[3]').click()
                                tmpErr=True
                            except Exception as eTmp:
                                tmpErr=False

                        tmpErr=False
                        while not tmpErr:
                            try:
                                msgText=driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                tmpErr=True
                            except Exception as eTmp:
                                tmpErr=False

                        if not (driver.find_element(by=By.XPATH,value='/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text=="确认选择课程吗？"):
                            elected=True
                            break
                        driver.find_element(by=By.XPATH,value=
                            '/html/body/div[3]/div/div[3]/button[2]').click()
                                
                        
                    
                    print("\nelected!\n")
                    break
            if not finded:
                curpages = curpages+1
                # Backspace twice to ensure all the numbers are gone
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys('%d' %curpages)
                driver.find_element(by=By.XPATH,value=
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="")
                pages = driver.find_element(by=By.XPATH,value='//*[@class="number active"]').text

        if not finded:
            print("\n\nnot finded!\n")

        return

    except Exception as e:
        print('\tterminated')
        error = True
        return


if __name__ == '__main__':
    # if "NAME" in os.environ:
    #     username = os.environ["NAME"]
    # else:
    #     sys.exit()
    #
    # if "PASSWORD" in os.environ:
    #     password = os.environ["PASSWORD"]
    # else:
    #     sys.exit()
    #
    # if "TURN" in os.environ:
    #     elecTurn = os.environ["TURN"]
    # else:
    #     elecTurn = "1"
    #
    # if "CLASS" in os.environ:
    #     class_wanted = os.environ["CLASS"]
    # else:
    #     sys.exit()


    # Fill in ur info before use

    username = "213xxxxxx"
    password = "ur password"
    elecTurn = "x"
    class_wanted = "B0xxxxxx [0x]"


    error = False
    Login()
    if not error:
        main()
