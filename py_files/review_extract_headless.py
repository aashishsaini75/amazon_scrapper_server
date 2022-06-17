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

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from amazoncaptcha import AmazonCaptcha
from lxml import html
import platform,time
import random,webbrowser

user_agent_path = "/home/ubuntu/aashish/amazon_scrapper_server/user_agents/user_agents.txt"

with open(user_agent_path,"r") as file:
    ua_list=list(str(file.read()).split("\n"))


options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--hide-scrollbars')
# options.add_argument('--v=99')
# options.add_argument('--aggressive-cache-discard')
options.add_argument('--headless')
# options.add_argument('--no-proxy-server')
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--disable-infobars")
# options.add_argument("start-maximized")
# options.add_argument("--disable-extensions")
# options.add_experimental_option("prefs", {
#     "profile.default_content_setting_values.notifications": 1
# })
# options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

options.add_argument(f'user-agent={random.choice(ua_list)}')

def get_chrome_version():
    """Reads current Chrome version from registry."""
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, _ = winreg.QueryValueEx(reg_key, 'version')
    winreg.CloseKey(reg_key)
    return version

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
    if "captcha" not in driver.current_url and "a-section a-spacing-top-large a-text-center review-filter-error aok-hidden" not in driver.page_source and "Sorry! Something went wrong!" not in driver.title:
        driver.execute_script("location.reload(true);")
        if "Type the characters you see in this image:" in driver.page_source:
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


def printrevProgressBar(k, max, postText):
    n_bar = 10  # size of progress bar
    try:
        j = k / max
    except ZeroDivisionError:
        j = 0
    sys.stdout.write('\r')
    sys.stdout.write("Downloading Reviews" + f"|{'█' * int(n_bar * j):{n_bar}s}| {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def dog_resolver(driver):
    if "Sorry! Something went wrong!" in driver.title:
        sys.stdout.write('\r')
        sys.stdout.write("Dog - Sorry! Something went wrong! Major Block")
        sys.stdout.flush()
        attempt = 0
        while attempt <= 10:
            try:
                time.sleep(310)
                driver.execute_script("location.reload(true);")
                if "Sorry! Something went wrong!" not in driver.title:
                    sys.stdout.write("Dog - Major block resolved")
                    break
                else:
                    raise Exception
            except:
                attempt+=1
            print("attempt count",attempt)
exp_rev = 0

def get_rev(asin_no):
    global cr_url,options
    try:
        service = ChromeService(executable_path=ChromeDriverManager(version=get_chrome_version()).install())

        driver = webdriver.Chrome(service=service, options=options)
    except:
        chromepath = ""
        driver = ""
        if platform.system() == "Darwin":
            chromepath = os.path.abspath("drivers/chromedriver")
        elif platform.system() == "Windows":
            chromepath = os.path.abspath("drivers/chromedriver.exe")
        elif platform.system() == 'Linux':
            chromepath = os.path.abspath("/home/ubuntu/aashish/amazon_scrapper_server/drivers/chromedriver_linux")
        try:
            driver = webdriver.Chrome(executable_path=chromepath, chrome_options=options)
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

    rev_url = "https://www.amazon.com/product-reviews/" + asin_no + "/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    driver.get(rev_url)
    dog_resolver(driver)
    # driver.get("https://www.amazon.com/product-reviews/B07K2HBB1H/ref=cm_cr_getr_d_paging_btm_next_490?ie=UTF8&reviewerType=all_reviews&pageNumber=490")
    data = {}
    data['reviews'] = []
    skip_review = 0
    rev_count = 1
    prog_count = 0

    server_attempt = 0
    while "This site can’t be reached" in driver.page_source and server_attempt <= 10:
        print("Amazon Server, Exception ignored, Waiting for the expected response")
        driver.refresh()
        time.sleep(5)
        server_attempt+=1

    captcha_check(driver)
    dog_resolver(driver)

    driver.execute_script("scroll(0, -1000);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-hook='cr-filter-info-review-rating-count']")))
    gl_rev_el = driver.find_element(By.XPATH,"//div[@data-hook='cr-filter-info-review-rating-count']").text
    gl_rev_el = str(gl_rev_el).replace(",","")
    # if "global reviews" in gl_rev_el:
    #     exp_rev = str(gl_rev_el).split("|")[-1].split(" ")[1].replace(",", "")
    # elif "total ratings" in gl_rev_el:
    #     exp_rev = str(gl_rev_el).split("total ratings")[-1].replace(",", "").replace(" ", "")
    #     exp_rev = int(re.search(r'\d+', exp_rev).group())
    # elif "with reviews" in gl_rev_el:
    #     exp_rev = str(gl_rev_el).split(",")[-1]
    #     exp_rev = int(re.search(r'\d+', exp_rev).group())
    # else:
    '''Getting total review count'''
    numbers = []
    for word in str(gl_rev_el).split():
        if word.isdigit():
            numbers.append(int(word))
    exp_rev = int(numbers[-1])


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-hook='cr-filter-info-review-rating-count']")))
    gl_rev_el_1 = driver.find_element(By.XPATH,"//div[@data-hook='cr-filter-info-review-rating-count']").text
    if "global reviews" in gl_rev_el_1:
        exp_rev_1 = str(gl_rev_el_1).split("|")[-1].split(" ")[1].replace(",", "")
    else:
        exp_rev_1 = str(gl_rev_el_1).split("total ratings")[-1].replace(",","").replace(" ","")
        exp_rev_1 = int(re.search(r'\d+', exp_rev_1).group())
    if int(exp_rev) > 5010:
        exp_rev = 5000
    else:
        pass
    while True:
        try:
            captcha_check(driver)
            dog_resolver(driver)

            ref_count = 0
            while exp_rev_1 == '0':
                time.sleep(2)
                driver.refresh()
                ref_count = ref_count + 1
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@data-hook='cr-filter-info-review-rating-count']")))
                gl_rev_el_1 = driver.find_element(By.XPATH,
                    "//div[@data-hook='cr-filter-info-review-rating-count']").text
                if "global reviews" in gl_rev_el_1:
                    exp_rev_1 = str(gl_rev_el_1).split("|")[-1].split(" ")[1].replace(",", "")
                else:
                    exp_rev_1 = str(gl_rev_el_1).split("total ratings")[-1].replace(",", "").replace(" ", "")
                    exp_rev_1 = int(re.search(r'\d+', exp_rev_1).group())
                if ref_count == 2 and exp_rev_1 != "0":
                    break
                if ref_count == 2 and exp_rev_1 == '0':
                    return
            cleaned_response = driver.page_source
            parser = html.fromstring(cleaned_response)
            review_blocks = parser.xpath("//div[@data-hook='review']")
            if "Sorry, no reviews match your current selections." in driver.page_source and len(
                    review_blocks) < 1:
                print("Sorry, no reviews match your current selections")
                return
            elif "No customer reviews" in driver.page_source and len(review_blocks) < 1:
                print("No customer reviews")
                return
            else:
                for i in review_blocks:
                    attempts = 0
                    while attempts <= 3:
                        try:
                            sc = str(html.tostring(i))

                            if "Translate review to English" in sc and 'cr-translate-this-review-link' in sc:
                                exp_rev = int(exp_rev) - 1
                                skip_review = skip_review + 1
                                pass
                            else:
                                prog_count = prog_count + 1
                                rev_count = rev_count + 1
                                helpful = ""
                                reviewer_name = str(
                                    i.xpath(".//span[contains(@class,'profile-name')]//text()")).strip().replace(
                                    "[", "").replace("]", "").replace("'", "")
                                ratings = str(i.xpath(".//i[@data-hook='review-star-rating']//text()")).strip().replace(
                                    "[",
                                    "").replace(
                                    "]", "").replace("'", "")
                                if ratings == "":
                                    try:
                                        ratings = str(
                                            i.xpath(
                                                ".//i[@data-hook='cmps-review-star-rating']//span//text()")).strip().replace(
                                            "[",
                                            "").replace(
                                            "]", "").replace("'", "")
                                    except:

                                        pass
                                else:
                                    pass

                                review_title = str(
                                    i.xpath(".//a[@data-hook='review-title']//span//text()")).strip().replace(
                                    "[",
                                    "").replace(
                                    "]", "").replace("'", "").replace("\\n", "").rstrip()
                                if review_title == "":
                                    try:
                                        review_title = str(
                                            i.xpath(".//span[@data-hook='review-title']//text()")).strip().replace(
                                            "[", "").replace("]", "").replace("'", "").replace("\\n", "")
                                    except:
                                        pass
                                else:
                                    pass

                                review_date1 = str(
                                    i.xpath(".//span[@data-hook='review-date']//text()")).strip().replace("[",
                                                                                                          "").replace(
                                    "]", "").replace("'", "")
                                review_date2 = review_date1.split(" ")[-3:]
                                review_date = str(review_date2[0] + " " + review_date2[1] + " " + review_date2[2])
                                review_text = str(
                                    i.xpath(".//span[@data-hook='review-body']//span//text()")).strip().replace(
                                    "[",
                                    "").replace(
                                    "]", "").replace("'", "").replace("\\n", "")
                                rev_prof_url = "https://www.amazon.com" + str(
                                    i.xpath(".//a[contains(@class,'a-profile')]/@href")).strip().replace("[",
                                                                                                         "").replace(
                                    "]",
                                    "").replace(
                                    "'", "")
                                if rev_prof_url == "https://www.amazon.com":
                                    rev_prof_url = "N/A"
                                else:
                                    pass
                                try:
                                    helpful = str(
                                        i.xpath(
                                            ".//span[@data-hook='helpful-vote-statement']//text()")).strip().replace(
                                        "[", "").replace("]", "").replace("'", "")
                                except:
                                    pass
                                product_reviews = {"reviewerName": reviewer_name,
                                                   "reviewerUrl": rev_prof_url,
                                                   "rating": ratings.replace("\n", ""),
                                                   "reviewTitle": review_title,
                                                   "reviewDate": review_date,
                                                   "reviewText": (review_text).replace("\\","'"),
                                                   "is_Helpful": helpful}
                                data['reviews'].append(product_reviews)
                            break
                        except:
                            attempts += 1

                if int(exp_rev) > 5010:
                    prog_range = 5010
                else:
                    prog_range = int(exp_rev)

                printrevProgressBar(prog_count, round(prog_range), "Done   ")
                cr_url = driver.current_url
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//li[@class = 'a-last']")))
                driver.find_element(By.XPATH,"//li[@class = 'a-last']").click()
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, "//div[@class='a-section cr-list-loading reviews-loading']")))
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located(
                        (By.XPATH,
                         "//div[@class='a-spinner-wrapper reviews-load-progess a-spacing-top-large']")))

        except TimeoutException:
            break

    driver.close()
    return data["reviews"], exp_rev
