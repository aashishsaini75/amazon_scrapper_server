"""
Script Name	:    Amazon BVR scrapper
Description	:    A web scrapping script to extract the required data from amazon[dot]com
Author      :    Aashish Saini
Email       :    aashish@shorthillstech.com
Updated on  :    02-May-2022
Version     :    2.10
"""

import os
import re

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['WDM_LOG_LEVEL'] = '0'

from pygame import mixer  # Load the popular external library
import json
import sys
import time,socket,pymsgbox,platform,webbrowser
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from datetime import datetime
import os
import requests
from tendo import singleton
from amazoncaptcha import AmazonCaptcha
from threading import Thread
from tkinter import *
import tkinter.messagebox as box
# import winreg
from seleniumwire import webdriver

try:
    me = singleton.SingleInstance()
except:
    time.sleep(5)
    sys.exit(-1)

version = "2.10"
r_date = "02-May-2022"

st_data = {}
up_st_data = {}
time_data = {}
upload_time_data = {}
qa_len_data = {}
rev_len_data = {}
exp_rev_len_data={}
exp_rev = 0
'''Getting Date & Time detail'''
print("Started at " + str(time.ctime()))

scrapper_type = "Headless"
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
def get_chrome_version():
    """Reads current Chrome version from registry."""
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, _ = winreg.QueryValueEx(reg_key, 'version')
    winreg.CloseKey(reg_key)
    return version
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
    proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)

    try:
        driver = webdriver.Chrome(executable_path=chromepath, chrome_options=options,seleniumwire_options=proxies)
    except Exception as e:
        if "Message: 'chromedriver.exe' executable needs to be in PATH" in str(e):
            print("Chrome driver path is incorrect, Please check and try again.")
            try:
                mixer.init()
                mixer.music.load(f'{base_dir}/incorrect_path.mp3')
                mixer.music.play()
                time.sleep(5)
            except:
                pass
        elif "Message: session not created: This version of ChromeDriver only supports Chrome version" in str(e):
            print(
                "Chrome driver needs to be updated, Please follow the instructions specified in recently opened PDF file...")
            try:
                mixer.init()
                mixer.music.load(f'{base_dir}/driver_update.mp3')
                mixer.music.play()
                time.sleep(7)
            except:

                pass
            webbrowser.open_new(r'Chrome driver update instruction.pdf')
        exit()

driver.maximize_window()

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


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False
def login():
    global token

    url = "https://dpl.bestviewsreviews.com/velocity/login"



    d = {
        'username': 'Aashish',
        'password': 'bvr@xy123'
    }
    res = requests.post(url, json=d)

    try:
        data = json.loads(res.text)
        full_name = str(data['first_name']+" "+ data['last_name'])
        email = data['email']
        user_id = data['user_id']
        role = data['role']
        token = data['token']
        user_info = {
            'Login_Name': full_name,
            'email': email,
            'velocity_user_id': user_id,
            'role': role,
            'source': 'Velocity'
            # 'auth_token':token
        }
    except Exception as e:

        user_info = {
            'Login_Name': str(os.getlogin()),
            'email':None,
            'velocity_user_id':None,
            'role':None,
            'source':'Local Machine'
            # 'auth_token':None
        }

    return user_info

user_infomation = login()


def get_date_time_detail():
    sys.stdout.flush()
    sys.stdout.write('\r')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data['time'].append(dt_string)
print("BVR scrapper "+ scrapper_type+ "[version " + str(version) + "]")

sheet = pd.ExcelFile(os.path.abspath('asin_list/asin_list.xlsx'))
sheets = sheet.sheet_names
print("Total", len(sheets), "Categories will be scraped")
start_time_1 = time.time()

for s in sheets:
    df = pd.read_excel(os.path.abspath('asin_list/asin_list.xlsx'),sheet_name = s ,dtype=str)
    print(s)
    asin_list = df['ASIN'].to_list()
    k = str(df.iloc[0]['SLUG']).strip()
    if str(asin_list[0]) =="nan":
        print("Asin List is empty, Please check the asin list")
        time.sleep(5)
        exit()
    if k == "nan":
        print("Slug not found, Please check the asin list")
        time.sleep(5)
        driver.quit()
        exit()

    print("Extraction started for",k)
    print("Total",len(asin_list),"Products will be scraped for",k)
    a=0
    if os.path.isdir(os.path.abspath('output_json')) == False:
        os.mkdir(os.path.abspath('output_json/'))
    if os.path.isdir(os.path.abspath('output_json/results')) == False:
        os.mkdir(os.path.abspath('output_json/results'))
    w = pd.ExcelWriter(os.path.abspath('output_json/results/'+k+'_result.xlsx'))
    for i in asin_list:
        try:
            asin_no = str(i).replace("['","").replace("']",'')
            print(int(len(asin_list)) - int(a), "ASIN Left")
            a = a + 1
            if len(asin_no) != 10:
                sys.stdout.write("\rInvalid ASIN, Please check the ASIN No. and try again")
                sys.stdout.flush()
                try:
                    mixer.init()
                    mixer.music.load(f'{base_dir}/invalid_asin.mp3')
                    mixer.music.play()
                    time.sleep(5)
                except:
                    pass
                raise Exception
            filename = asin_no + ".json"

            data = {}
            time_list = [0, 0]
            data['features'] = []
            data['reviewsAspects'] = []
            data['productInformation'] = []
            data['productDescription'] = []
            data['reviews'] = []
            data['qAndA'] = []
            data['time'] = []
            data['reviewsCountInfo'] = []
            data['scrapperInfo'] = []
            data['breadcrumb'] = []
            base_url = "https://www.amazon.com/gp/product/"
            ques_base_url = "https://www.amazon.com/ask/questions/asin/"
            act_review = 0
            skip_review = 0
            rev_count = 1
            qa_count = 1
            prog_count = 0
            product_title = ""
            manufacturer_name = ""
            current_price = ""
            rating = ""
            total_ratings = ""

            '''Initiating progress bar for reviews extraction process'''


            def upload_to_velocity(file_path, cat_slug,asin):
                start_time_2 = time.time()

                data = {'category_slug': cat_slug}
                res = requests.post(url='https://dpl.bestviewsreviews.com/api/product/add_product_velocity',
                                    headers={'Authorization': 'Token '+token},
                                    files={'file': open(file_path, 'rb')},
                                    data=data)
                time_taken = str(round((time.time() - start_time_2) / 60, 2)) + " Minutes"
                if "ASIN is already present" in str(res.text):
                   pass

                else:
                    dic_upload = {
                        asin: time_taken
                    }
                    upload_time_data.update(dic_upload)

                return res.text

            def replace_to_velocity(file_path, cat_slug, asin):
                start_time_3 = time.time()

                data = {'asin': asin, 'category_slug': cat_slug}
                res = requests.put(url='https://dpl.bestviewsreviews.com/velocity/product/product_update',
                                   headers={'Authorization': 'Token '+token},
                                   files={'file': open(file_path, 'rb')},
                                   data=data)
                time_taken = str(round((time.time() - start_time_3) / 60, 2)) + " Minutes"
                dic_replaced = {
                    asin: time_taken
                }
                upload_time_data.update(dic_replaced)
                return res.text
            def url_request():
                try:
                    driver.get(base_url + asin_no + "/?ref=icp_country_us")
                except Exception as e:
                    print(e)

                driver.execute_script("document.body.style.zoom='-7'")
                while "ERR_INTERNET_DISCONNECTED" in driver.page_source or "This site can’t be reached" in driver.page_source:
                    print("Internet lost")
                    driver.refresh()
                    time.sleep(5)
                captcha_check(driver)

                if "Sorry! We couldn't find that page. Try searching or go to Amazon's home page." in driver.page_source:
                    dic_3 = {
                        i: "Expired"
                    }
                    st_data.update(dic_3)
                    raise Exception


            '''Setting up the location to New York '''


            def set_loc():
                try:
                    loc = str(driver.find_element(By.ID,"glow-ingress-line2").text).strip().replace(" ", "")
                    if loc == "India" in driver.page_source:
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "nav-packard-glow-loc-icon")))
                        driver.find_element(By.ID,"nav-packard-glow-loc-icon").click()
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))
                        driver.find_element(By.ID,"GLUXZipUpdateInput").send_keys(10001)
                        ActionChains(driver).send_keys(Keys.SHIFT, Keys.ENTER).perform()

                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "GLUXConfirmClose")))
                        driver.refresh()
                except:
                    pass

            '''Extracting product detail data'''

            def get_product_detail():
                global product_title,manufacturer_name,current_price,rating,total_ratings
                sys.stdout.write(
                    "\rDownloading detail" + f"|{'' * int(1):{''}s}| {int(100 * 0)}%  {'Done                   '}")
                sys.stdout.flush()
                if driver.current_url == str(base_url + asin_no + "/?ref=icp_country_us"):
                    pass
                else:
                    driver.get(str(base_url + asin_no + "/?ref=icp_country_us").strip())
                    driver.maximize_window()

                captcha_check(driver)

                cleaned_response = driver.page_source
                parser = html.fromstring(cleaned_response)
                soup = BeautifulSoup(cleaned_response, 'html.parser')
                try:
                    driver.find_element(By.XPATH,"//input[@data-action-type = 'DISMISS']").click()
                except:
                    pass
                try:
                    product_title = str(
                        parser.xpath(".//span[contains(@id,'productTitle')]//text()")).strip().replace("[",
                                                                                                       "").replace(
                        "]", "").replace("'", "").replace("\\n", "")

                except:
                    try:
                        product_title = str(
                            parser.xpath(".//div[contains(@class,'feature_Title celwidget')]//text()")).strip().replace("[",
                                                                                                                        "").replace(
                            "]", "").replace("'", "").replace("\\n", "")

                    except:
                        try:
                            driver.get(
                                "https://www.amazon.com/product-reviews/" + asin_no + "/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
                            time.sleep(0.5)
                            cleaned_response = driver.page_source
                            parser = html.fromstring(cleaned_response)
                            soup = BeautifulSoup(cleaned_response, 'html.parser')
                            product_title = str(
                                parser.xpath(".//h1[contains(@class,'a-size-large a-text-ellipsis')]//text()")).strip().replace("[",
                                                                                                                                "").replace(
                                "]", "").replace("'", "").replace("\\n", "")
                            driver.back()
                        except:
                            driver.back()
                            pass
                try:
                    manufacturer_name = str(driver.find_element(By.XPATH,"//th[normalize-space()='Brand']/following-sibling::td[1]").text).strip()
                    if manufacturer_name == "":
                        raise Exception
                except :
                    try:
                        manufacturer_name = str(driver.find_element(By.XPATH,
                            "//th[contains(normalize-space()='Manufacturer')]/following-sibling::td[1]").text).strip()
                        if manufacturer_name == "":
                            raise Exception
                    except:
                        try:
                            manufacturer_name = str(driver.find_element(By.XPATH,
                                "//span[contains(normalize-space()='Manufacturer')]/following-sibling::span[1]").text).strip()
                            if manufacturer_name == "":
                                raise Exception
                        except:
                            try:
                                manufacturer_name = str(
                                    parser.xpath(".//a[contains(@id,'bylineInfo')]//text()")).strip().replace("[",
                                                                                                              "").replace(
                                    "]", "").replace("'", "")
                                if manufacturer_name == "":
                                    raise Exception
                            except:
                                try:
                                    manufacturer_name = str(
                                        parser.xpath(".//a[contains(@class,'a-link-normal contributorNameID')]//text()")).replace(
                                                "[",
                                                "").replace(
                                                "]", "").replace("'", "")
                                    if manufacturer_name == "":
                                        raise Exception
                                except:
                                    try:
                                        manufacturer_name = str(
                                            parser.xpath(".//div[contains(@class,'feature_ByLine celwidget')]//text()")).strip().replace("[",
                                                                                                                                         "").replace(
                                            "]", "").replace("'", "")
                                        if manufacturer_name == "":
                                            raise Exception
                                    except:
                                        try:
                                            driver.get(
                                                "https://www.amazon.com/product-reviews/" + asin_no + "/ref=cm_cr_othr_d_show_all_btm?ie=UTF8"
                                                                                                      "&reviewerType=all_reviews")
                                            time.sleep(0.5)
                                            cleaned_response = driver.page_source
                                            parser = html.fromstring(cleaned_response)
                                            soup = BeautifulSoup(cleaned_response, 'html.parser')
                                            manufacturer_name = str(parser.xpath(".//span[contains(@id,'cr-arp-byline')]//text()")).strip().replace(
                                                "[",
                                                "").replace(
                                                "]", "").replace("'", "").replace('"','')
                                            driver.back()
                                        except:
                                            driver.back()
                                            pass


                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                        "Connection": "close", "Upgrade-Insecure-Requests": "1"}

                    page = requests.get(url=base_url + asin_no + "/?ref=icp_country_us", headers=headers)
                    page_response = page.text
                    parser = html.fromstring(page_response)
                    current_price = parser.xpath(".//span[@id='priceblock_saleprice']//text()")
                    if "$" not in current_price:
                        current_price = parser.xpath(".//span[@id='priceblock_ourprice']//text()")
                        if "$" not in current_price:
                            current_price = parser.xpath(".//span[@class='a-price qa-buybox-price-due-today']//text()")
                except:
                    try:

                        current_price = str(soup.find("span", {"id": "priceblock_saleprice"}).text).strip().replace("[",
                                                                                                                    "").replace(
                            "]", "").replace("'", "")
                    except:

                        try:

                            current_price = str(soup.find("span", {"id": "priceblock_ourprice"}).text).strip().replace("[",
                                                                                                                       "").replace(
                                "]", "").replace("'", "")
                        except:

                            try:

                                current_price = str(
                                    soup.find("span", {"class": "a-price qa-buybox-price-due-today"}).text).strip().replace("[",
                                                                                                                            "").replace(
                                    "]", "").replace("'", "").replace(" ", "")
                            except:
                                current_price = ""

                try:
                    rating = str(soup.find("span", {"id": "acrPopover"})['title']).strip().replace("[", "").replace("]",
                                                                                                                    "").replace("'",
                                                                                                                                "")
                except:
                    try:
                        driver.get(
                            "https://www.amazon.com/product-reviews/" + asin_no + "/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
                        time.sleep(0.5)

                        cleaned_response = driver.page_source
                        parser = html.fromstring(cleaned_response)
                        soup = BeautifulSoup(cleaned_response, 'html.parser')
                        rating = str(parser.xpath(".//span[contains(@data-hook,'rating-out-of-text')]//text()")).strip().replace(
                            " out of 5", "")
                        driver.back()
                    except:
                        driver.back()
                        pass
                try:
                    total_ratings = str(soup.find("span", {"id": "acrCustomerReviewText"}).text).strip().replace("[", "").replace(
                        "]", "").replace("'", "")
                except:
                    try:
                        driver.get(
                            "https://www.amazon.com/product-reviews/" + asin_no + "/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
                        time.sleep(0.5)

                        cleaned_response = driver.page_source
                        parser = html.fromstring(cleaned_response)
                        total_ratings = str(
                            parser.xpath(".//div[contains(@data-hook,'total-review-count')]//text()")).strip().replace(
                            " global ratings", "")
                        driver.back()
                    except:
                        driver.back()
                        pass
                try:
                    WebDriverWait(driver, 0.5).until(EC.visibility_of_all_elements_located((By.ID, "nav-belt")))
                    response = driver.page_source
                    date = driver.find_element(By.XPATH,
                        "//th[normalize-space()='Date First Available']/following-sibling::td[1]").text
                except:
                    try:
                        WebDriverWait(driver, 0.5).until(EC.visibility_of_all_elements_located((By.ID, "nav-belt")))
                        date = driver.find_element(By.XPATH,
                            "//th[normalize-space()='Release date']/following-sibling::td[1]").text
                    except:
                        try:
                            WebDriverWait(driver, 0.5).until(EC.visibility_of_all_elements_located((By.ID, "nav-belt")))
                            date = driver.find_element(By.XPATH,
                                "//span[@class='a-text-bold' and contains(text(), 'Date First Available')]/following-sibling::span[1]").text
                        except:
                            date = None
                try:
                    driver.find_element(By.XPATH,"//i[@class = 'a-icon a-icon-addon p13n-best-seller-badge']")
                    bs = True
                except:
                    bs = False
                try:
                    driver.find_element(By.XPATH,"//span[@class = 'a-size-small aok-float-left ac-badge-rectangle']")
                    ac = True
                except:
                    ac = False
                if "FREE delivery:" in driver.page_source:
                    fd = True
                else:
                    fd = False

                try:
                    el = driver.find_element(By.ID,"wayfinding-breadcrumbs_feature_div").find_elements(By.TAG_NAME, "li")
                    bread = ""
                    for i in el:
                        bread = bread + i.text
                    breadcrumb_val = {
                        "breadcrumb": bread
                    }
                    data['breadcrumb'] = breadcrumb_val
                    sys.stdout.write("\rDownloading detail" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                    sys.stdout.flush()
                except:
                    sys.stdout.write("\rDownloading detail" + f"|{'██████████' * int(1):{''}s}| {int(0 * 1)}%  {'Done'}")
                    sys.stdout.flush()
                    pass
                product_title = (product_title+" ; "+manufacturer_name).replace("\\","'")

                manufacturer_name = str(manufacturer_name).strip().replace("by ", "").replace("Visit the ", "").replace(" Store","").replace("\\n","").replace("Brand: ","").replace(",","").replace("for ",'').replace("'",'').replace('"','').strip()
                # if manufacturer_name not in str(product_title):
                #     product_title = manufacturer_name+" "+product_title
                # else:
                #     pass
                product_detail = {
                    "productURL": base_url + asin_no,
                    "ASIN": asin_no,
                    "title": product_title,
                    'date_first_available':date,
                    "manufacturer": manufacturer_name,
                    "currentPrice": current_price,
                    "rating": str(rating).replace(" out of 5 stars", "").replace("]", "").replace("[", "").replace("'", ""),
                    "totalRatings": str(total_ratings).replace("ratings", "").replace("]", "").replace("[", "").replace("'", ""),
                    'amazon_choice': ac,
                    'best_seller': bs,
                    'free_delivery': fd,
                    'amazon_deleted': False
                }
                data.update(product_detail)
                sys.stdout.write("\rDownloading detail" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                sys.stdout.flush()
                time.sleep(0.3)


            '''Extracting product reviews aspects information'''


            def get_review_Aspects():
                def getNdump():
                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "cr-lighthouse-terms")))
                    review_aspects_el = driver.find_element(By.CLASS_NAME,"cr-lighthouse-terms").find_elements(By.CLASS_NAME,
                        "cr-lighthouse-term ")
                    for i in review_aspects_el:
                        if i.text == "":
                            pass
                        else:
                            data['reviewsAspects'].append(i.text)

                sys.stdout.write(
                    "\rDownloading aspects" + f"|{'' * int(1):{''}s}| {int(100 * 0)}%  {'Done                 '}")
                sys.stdout.flush()
                if driver.current_url == str(base_url + asin_no + "/?ref=icp_country_us"):
                    pass
                else:
                    driver.get(str(base_url + asin_no + "/?ref=icp_country_us").strip())
                    driver.maximize_window()

                captcha_check(driver)

                try:
                    driver.find_element(By.XPATH,"//input[@data-action-type = 'DISMISS']").click()
                except:
                    pass
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "acrCustomerReviewText")))
                    driver.find_element(By.ID,"acrCustomerReviewText").click()
                    getNdump()

                except:
                    try:
                        driver.get(base_url + asin_no + "#customerReviews")
                        getNdump()
                    except:
                        pass
                sys.stdout.write("\rDownloading aspects" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                sys.stdout.flush()


            '''Extracting product information'''


            def get_product_information():
                product_spec = ""
                sys.stdout.write(
                    "\rDownloading information" + f"|{'' * int(1):{''}s}| {int(100 * 0)}%  {'Done              '}")
                sys.stdout.flush()
                if driver.current_url == str(base_url + asin_no + "/?ref=icp_country_us"):
                    pass
                else:
                    driver.get(str(base_url + asin_no + "/?ref=icp_country_us").strip())
                    driver.maximize_window()

                cleaned_response = driver.page_source
                soup = BeautifulSoup(cleaned_response, 'html.parser')

                captcha_check(driver)
                try:
                    driver.find_element(By.XPATH,"//input[@data-action-type = 'DISMISS']").click()
                except:
                    pass
                dict = {}
                try:
                    product_spec = (soup.find_all("table",id=re.compile("productDetails")))
                    for j in product_spec:
                        tr = j.find_all("tr")
                        for i in tr:
                            key = i.find_all("th")[0].text
                            value = i.find_all("td")[0].text
                            dict[key] = value
                    data['productInformation'].append(dict)
                except:
                    pass

                sys.stdout.write("\rDownloading information" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                sys.stdout.flush()
                time.sleep(0.1)


            '''Extracting product description data'''


            def get_product_description():
                sys.stdout.write(
                    "\rDownloading description" + f"|{'' * int(1):{''}s}| {int(100 * 0)}%  {'Done             '}")
                sys.stdout.flush()
                if driver.current_url == str(base_url + asin_no + "/?ref=icp_country_us"):
                    pass
                else:
                    driver.get(str(base_url + asin_no + "/?ref=icp_country_us").strip())
                    driver.maximize_window()

                captcha_check(driver)

                try:
                    driver.find_element(By.XPATH,"//input[@data-action-type = 'DISMISS']").click()
                except:
                    pass

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "productDescription")))
                    product_description = str(driver.find_element(By.ID,"productDescription").find_element(By.TAG_NAME,"p").text)
                    data['productDescription'] = str(product_description).replace("Product Description", "").replace(
                        "Product description", "")
                except :
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.ID, "aplus")))
                        product_description = str(driver.find_element(By.ID,"aplus").text).replace("From the manufacturer", "")
                        data['productDescription'] = str(product_description).replace("Product Description", "").replace(
                            "Product description", "")
                    except:
                        try:
                            WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.ID, "productDescription_feature_div")))
                            product_description = driver.find_element(By.ID,"productDescription_feature_div").text
                            data['productDescription'] = str(product_description).replace("Product Description", "")
                        except:
                            pass
                sys.stdout.write("\rDownloading description" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                sys.stdout.flush()
                time.sleep(0.1)


            '''Extracting product features info..'''


            def get_product_features():
                sys.stdout.write(
                    "\rDownloading features" + f"|{'' * int(1):{''}s}| {int(100 * 0)}%  {'Done                 '}")
                sys.stdout.flush()
                if driver.current_url == str(base_url + asin_no + "/?ref=icp_country_us"):
                    pass
                else:
                    driver.get(str(base_url + asin_no + "/?ref=icp_country_us").strip())
                    driver.maximize_window()

                captcha_check(driver)

                try:
                    driver.find_element(By.XPATH,"//input[@data-action-type = 'DISMISS']").click()
                except:
                    pass

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "feature-bullets")))
                    bullet_features = driver.find_element(By.ID,"feature-bullets").find_elements(By.TAG_NAME, "li")
                    for i in bullet_features:
                        if i.text == "":
                            pass
                        else:
                            data['features'].append(i.text)
                except:
                    pass

                sys.stdout.write("\rDownloading features" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                sys.stdout.flush()
                time.sleep(0.1)

            '''Extracting products Q&A data'''

            def get_product_QA():
                from py_files.qa_extract_headless import QA
                data['qAndA'] = QA(i)

            '''Extracting products reviews data'''

            def get_product_reviews():
                global exp_rev
                from py_files.review_extract_headless import get_rev
                try:
                    data['reviews'], exp_rev = get_rev(i)
                except:
                    data['reviews'] = []
                    exp_rev = 0
            final_data = {}

            '''Removing duplicate reviews(if found) from dict'''

            def remove_dup():
                global final_data
                final_data = {'reviews': [dict(t) for t in {tuple(d.items()) for d in data['reviews']}]}
                data.update(final_data)
                return data

            '''Sorting the reviews from latest to oldest in json'''

            def sort():
                global data
                data1 = sorted(data['reviews'], reverse=True, key=lambda x: datetime.strptime(x['reviewDate'], '%B %d, %Y'))
                data['reviews'].clear()
                data['reviews'] = data1
                return data

            def dump_data():
                reviewInfo = {
                    "expRevCount": exp_rev,
                    "actRevCount": act_review,
                    "nonEnglishRevCount": skip_review
                }
                scInfo = {
                    "ScrapperType":scrapper_type,
                    "Version": version,
                    "Released Date": r_date
                }
                data['reviewsCountInfo'] = reviewInfo
                data['scrapperInfo'] = scInfo
                data['UserInformation'] = user_infomation

                '''Dumping a final JSON to local'''
                if os.path.isdir(os.path.abspath('output_json')) == False:
                    os.mkdir(os.path.abspath('output_json/'))
                if os.path.isdir(os.path.abspath('output_json/' + k)) == False:
                    os.mkdir(os.path.abspath('output_json/' + k.strip()))
                with open(os.path.abspath('output_json/'+k)+"/" + filename, 'w') as json_file:
                    json.dump(data, json_file)
                    sys.stdout.write("\rProduct data extraction" + f"|{'██████████' * int(1):{''}s}| {int(100 * 1)}%  {'Done'}")
                    sys.stdout.flush()

                    sys.stdout.write("\r\nJson dumped successfully for " + str(asin_no))
                    sys.stdout.flush()
                    print(("\nProduct Scrapped in " + str(round((time.time() - start_time) / 60, 2)) + " Minutes,"),"Review Count -",act_review+skip_review,"Q&A's Count -",qa_len)

                    dic_4 = {
                        i: str(round((time.time() - start_time) / 60, 2)) + " Minutes"
                    }
                    time_data.update(dic_4)
                    dic_5 = {
                        i: act_review+skip_review
                    }
                    rev_len_data.update(dic_5)
                    dic_6 = {
                        i:qa_len
                    }
                    qa_len_data.update(dic_6)
                    dic_7 = {
                        i: int(exp_rev)
                    }
                    exp_rev_len_data.update(dic_7)

            start_time = time.time()
            def init_info():
                url_request()
                get_product_information()
                get_product_description()
                get_product_detail()
                get_product_features()
                get_review_Aspects()


            if is_connected() == True:

                t1 = Thread(target=init_info)
                t2 = Thread(target=get_product_QA)
                t3 = Thread(target=get_product_reviews)
                t1.start()
                t2.start()
                t3.start()
                t1.join()
                t2.join()
                t3.join()
                remove_dup()
                sort()
                get_date_time_detail()
            else:
                print("Internet Error : Please check the internet and try again")
                try:
                    mixer.init()
                    mixer.music.load(f'{base_dir}/internet_error.mp3')
                    mixer.music.play()
                    time.sleep(3)
                    pymsgbox.alert('Internet is not connected!', 'Connection Error')

                except:
                    pass
                driver.quit()

                exit()

            dic = {
                i:"Successful"
            }
            st_data.update(dic)
            act_review = len(data['reviews'])
            try:
                qa_len = len(data['qAndA'])
            except:
                qa_len = 0

            '''Initiating reviews count validation check'''

            if act_review > 5000:
                dump_data()
                try:
                    res = upload_to_velocity(os.path.abspath('output_json/' + k) + "/" + filename, k,i)
                    if "ASIN is already present" in str(res):
                        try:
                            replace_to_velocity(os.path.abspath('output_json/' + k) + "/" + filename, k, i)
                            dic_3 = {
                                i: "Product already present,Json file replaced"
                            }
                        except Exception as e:
                            dic_3 = {
                                i: "Error:Product already present,Json file couldn't be uploaded"
                            }
                    elif "successful" in str(res):
                        dic_3 = {
                            i: "Successful"
                        }
                    else:
                        dic_3 = {
                            i: res
                        }
                    up_st_data.update(dic_3)
                except Exception as e:
                    dic_3 = {
                        i: "API wasn't responded "+str(e)
                    }
                    up_st_data.update(dic_3)

            elif int(exp_rev) > act_review:
                print(("Total reviews could not be scraped         "))
                print(("Expected reviews (" + str(exp_rev) + ")" " != " + "Actual scraped reviews(" + str(act_review) + ")"))
                for j in range(1):
                    mixer.init()
                    mixer.music.load(f'{base_dir}/alarm.mp3')
                    mixer.music.play()
                    time.sleep(1)
                dump_data()
                try:
                    res = upload_to_velocity(os.path.abspath('output_json/'+k) + "/" + filename, k,i)
                    if "ASIN is already present" in str(res):
                        try:
                            replace_to_velocity(os.path.abspath('output_json/'+k) + "/" + filename,k,i)
                            dic_3 = {
                                i: "Product already present,Json file replaced"
                            }
                        except Exception as e:
                            dic_3 = {
                                i: "Error:Product already present,Json file couldn't be uploaded"
                            }
                    elif "successful" in str(res):
                        dic_3 = {
                            i: "Successful"
                        }
                    else:
                        dic_3 = {
                            i: res
                        }
                    up_st_data.update(dic_3)
                except Exception as e:
                    dic_3 = {
                        i: "API wasn't responded "+str(e)
                    }
                    up_st_data.update(dic_3)
            else:
                dump_data()
                try:
                    res = upload_to_velocity(os.path.abspath('output_json/'+k) + "/" + filename, k,i)
                    if "ASIN is already present" in str(res):
                        try:
                            replace_to_velocity(os.path.abspath('output_json/' + k) + "/" + filename, k, i)
                            dic_3 = {
                                i: "Product already present,Json file replaced"
                            }
                        except Exception as e:
                            dic_3 = {
                                i: "Error:Product already present,Json file couldn't be uploaded"
                            }
                    elif "successful" in str(res):
                        dic_3 = {
                            i: "Successful"
                        }
                    else:
                        dic_3 = {
                            i: res
                        }
                    up_st_data.update(dic_3)
                except Exception as e:
                    dic_3 = {
                        i: "API wasn't responded " + str(e)
                    }
                    up_st_data.update(dic_3)

        except Exception as E:
            print(E)
            if "raise Exception" in str(E):
                pass
            else:
                dic_2 = {
                    i: "Failed\n"+str(E)
                }
                st_data.update(dic_2)

    df['Extraction Status'] = df['ASIN'].map(st_data)
    df['Upload Status'] = df['ASIN'].map(up_st_data)
    df["Extraction Time Taken"] = df['ASIN'].map(time_data)
    df["Uploading Time Taken"] = df['ASIN'].map(upload_time_data)
    df["QA Count"] = df['ASIN'].map(qa_len_data)
    df['Review Count'] = df['ASIN'].map(rev_len_data)
    df['Expected Review Count'] = df['ASIN'].map(exp_rev_len_data)

    df = df.drop(['SLUG'],axis = 1)

    try:
        df.to_excel(w, index=False)
        w.save()
    except:
        w_1 = pd.ExcelWriter(os.path.abspath('output_json/results/'+k+'_asin_list_result_exp.xlsx'))
        df.to_excel(w_1, index=False)
        w_1.save()

print(("\nAll categories scrapped in " + str(round((time.time() - start_time_1) / 60, 2)) + " Minutes"))

try:
    mixer.init()
    mixer.music.load(f'{base_dir}/completed.mp3')
    mixer.music.play()
    time.sleep(3)
except:
    pass
driver.quit()

print("\nFinished at " + str(time.ctime()))
