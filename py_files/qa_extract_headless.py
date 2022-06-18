"""
Script Name	:    Amazon BVR scrapper
Description	:    A web scrapping script to extract the required data from amazon[dot]com
Author      :    Aashish Saini
Email       :    aashish@shorthillstech.com
Updated on  :    02-May-2022
Version     :    2.10
"""

import os
from pygame import mixer  # Load the popular external library

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['WDM_LOG_LEVEL'] = '0'


import sys,re,platform,webbrowser,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from amazoncaptcha import AmazonCaptcha
from bs4 import BeautifulSoup
# import winreg
from seleniumwire import webdriver

ques_base_url = "https://www.amazon.com/ask/questions/asin/"
base_dir = os.path.join( os.getcwd())

USERNAME = "rshorthillstech"
PASSWORD = "8gfhsYYSra"
ENDPOINT = "us-pr.oxylabs.io:10000"

def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"http://{user}:{password}@{endpoint}",
        }
    }

    return wire_options
def printqaProgressBar(k, max, postText):
    n_bar = 10  # size of progress bar
    j = k / max
    sys.stdout.write('\r')
    sys.stdout.write("Downloading Q&A" + f"|{'█' * int(n_bar * j):{n_bar}s}| {int(100 * j)}%  {postText}")
    sys.stdout.flush()
def captcha_check(driver):
    while "Type the characters you see in this image:" in driver.page_source:
        sys.stdout.write('\r')
        sys.stdout.write("Trying to bypass")
        sys.stdout.flush()
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class = 'a-row a-text-center']")))
            link = driver.find_element(By.XPATH,
                "//div[@class = 'a-row a-text-center']").find_element(By.TAG_NAME,"img").get_attribute(
                "src")
            captcha = AmazonCaptcha.fromlink(link)
            solution = captcha.solve()
            driver.find_element(By.ID,"captchacharacters").send_keys(solution)
            driver.find_element(By.CLASS_NAME,"a-button-text").click()
            sys.stdout.write('\r')
            sys.stdout.write("Bypass Successfully")
            sys.stdout.flush()
        except:
            sys.stdout.write('\r')
            sys.stdout.write("Bypass failed")
            sys.stdout.flush()
            driver.refresh()
def get_chrome_version():
    """Reads current Chrome version from registry."""
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, _ = winreg.QueryValueEx(reg_key, 'version')
    winreg.CloseKey(reg_key)
    return version

def QA(asin_no):
    global a,qa_count
    try:
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=ChromeDriverManager(version=get_chrome_version()).install())
        options.add_argument('--headless')
        proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)
        driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=proxies)
    except:
        chromepath = ""
        driver = ""
        if platform.system() == "Darwin":
            chromepath = os.path.abspath(f"{base_dir}/drivers/chromedriver")
        elif platform.system() == "Windows":
            chromepath = os.path.abspath(f"{base_dir}/drivers/chromedriver.exe")
        elif platform.system() == 'Linux':
            chromepath = os.path.abspath(f"{base_dir}/drivers/chromedriver_linux")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        try:
            proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)
            driver = webdriver.Chrome(executable_path=chromepath, chrome_options=options, seleniumwire_options=proxies)
        except Exception as e:
            if "Message: 'chromedriver.exe' executable needs to be in PATH" in str(e):
                print("Chrome driver path is incorrect, Please check and try again.")
                try:
                    mixer.init()
                    mixer.music.load('audio/incorrect_path.mp3')
                    mixer.music.play()
                    time.sleep(5)
                except:
                    pass
            elif "Message: session not created: This version of ChromeDriver only supports Chrome version" in str(e):
                print(
                    "Chrome driver needs to be updated, Please follow the instructions specified in recently opened PDF file...")
                try:
                    mixer.init()
                    mixer.music.load('audio/driver_update.mp3')
                    mixer.music.play()
                    time.sleep(7)
                except:

                    pass
                webbrowser.open_new(r'Chrome driver update instruction.pdf')
            exit()
    driver.maximize_window()
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": "Object.defineProperty(navigator, 'plugins', {get: () = > [1, 2, 3, 4, 5]});"})
    driver.get(ques_base_url + asin_no )
    captcha_check(driver)
    qa_count = 0
    data = {}
    data['qAndA'] = []
    while True:
        try:
            captcha_check(driver)
            try:
                exp_qa = \
                    str(driver.find_element(By.XPATH,"//div[@class = 'a-section askPaginationHeaderMessage']").text).split(" ")[
                        -2].replace("+", "").strip()
            except:
                exp_qa = 0
            cleaned_response = driver.page_source
            soup = BeautifulSoup(cleaned_response, 'html.parser')
            try:
                WebDriverWait(driver, 0.01).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@class = 'a-section askTeaserQuestions']")))
                main_block = soup.find("div",{"class":"a-section askTeaserQuestions"})
                blocks = main_block.find_all("div",{"class":"a-fixed-left-grid a-spacing-base"})[::2]
            except:
                try:
                    driver.refresh()
                    WebDriverWait(driver, 0.01).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "a-section askTeaserQuestions")))
                    WebDriverWait(driver, 0.01).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@class = 'a-section askTeaserQuestions']")))
                    main_block = soup.find("div", {"class": "a-section askTeaserQuestions"})
                    blocks = main_block.find_all("div", {"class": "a-fixed-left-grid a-spacing-base"})[::2]
                except:
                    return

            for i in blocks:
                question = i.find_all("span")[6].text
                answer_l = []
                answer = "Answer not available"
                vote = str(i.find_all("li")[1].text).replace("\n\nvotes","").replace("\nvote","")
                ans_count = 0

                if "See all" in i.text:
                    url = i.find("a",{"class":"a-link-normal"}).get("href")
                    driver.execute_script("window.open('"+url+"');")
                    driver.switch_to.window(driver.window_handles[-1])
                    cleaned_response = driver.page_source
                    soup = BeautifulSoup(cleaned_response, 'html.parser')
                    while True:
                        captcha_check(driver)
                        try:
                            WebDriverWait(driver, 0.01).until(
                                EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'a-section a-spacing-large askAnswersAndComments askWrapText']")))
                            els = soup.find_all("div",id=re.compile("^answer"))
                            for k in els:
                                try:
                                    WebDriverWait(driver, 0.01).until(
                                        EC.visibility_of_all_elements_located((By.XPATH,
                                                                               "//a[@class = 'a-link-normal askSeeMore']")))
                                    k.find_element(By.XPATH,"//a[@class = 'a-link-normal askSeeMore']").click()
                                    answer = str(k.find("span",{"class":"askLongText"}).text).replace("see less","")
                                    by = k.find("span",{"class":"a-profile-name"}).text
                                    date = k.find("span",{"class":"a-color-tertiary aok-align-center"}).text

                                    pattern = re.compile(r'found this helpful')
                                    try:
                                        helpful = k.find("span", string=pattern).text
                                    except :
                                        helpful = ""

                                except:
                                    by = k.find("span",{"class":"a-profile-name"}).text

                                    date = k.find("span",{"class":"a-color-tertiary aok-align-center"}).text

                                    answer = k.find("span").text
                                    pattern = re.compile(r'found this helpful')
                                    try:
                                        helpful = k.find("span",string = pattern).text
                                    except Exception :
                                        helpful = ""
                                ans_count+=1
                                anser_dic = {
                                    "answer": answer,
                                    "by": str(by).strip(),
                                    "date": str(date).replace("· ", '').strip(),
                                    "helpful": helpful.replace("found this helpful. Do you?","")
                                }
                                answer_l.append(anser_dic)
                                if ans_count >=10:
                                    raise TimeoutException
                            WebDriverWait(driver, 0.01).until(EC.element_to_be_clickable((By.XPATH, "//*[@class ='a-last']")))
                            nxt = driver.find_element(By.XPATH, "//*[@class ='a-last']")
                            nxt.click()
                        except TimeoutException:
                            break
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                else:
                    try:
                        answer_text = i.find_all("span")[8].text

                        if "Answer:" in answer_text:
                            answer = i.find_all("span")[9].text

                        else:
                            answer = i.find_all("span")[8].text

                        by = i.find("span", {"class": "a-profile-name"}).text

                        date = i.find("span", {"class": "a-color-tertiary aok-align-center"}).text
                        anser_dic = {
                            "answer": answer,
                            "by": str(by).strip(),
                            "date": str(date),
                            "helpful": ""
                        }
                        answer_l.append(anser_dic)

                    except:
                        anser_dic = {
                            "answer": answer,
                        }
                        answer_l.append(anser_dic)

                q_and_a = {"question": question.strip(),
                           "answers": answer_l,
                           "vote":vote
                           }
                data['qAndA'].append(q_and_a)
                qa_count = qa_count + 1
                if qa_count >= 100:
                    raise TimeoutException
            if int(exp_qa)>=100:
                prog_range_qa = 100
            else:
                prog_range_qa = int(exp_qa)
            printqaProgressBar(qa_count, round(prog_range_qa), "Done       ")
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class ='a-last']")))

            driver.find_element(By.XPATH, "//*[@class ='a-last']").click()
        except TimeoutException:
            break
    driver.close()
    return data['qAndA']
