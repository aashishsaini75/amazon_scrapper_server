import requestsimport base64import timeimport shutilimport osfrom datetime import datetimeimport globos.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"from pygame import mixer  # Load the popular external librarynow = datetime.now()dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")def main_update():    token = str(base64.b64decode("OGZiNDVkOGMzZGJhODc5NTUyN2NmYjRjNDM3NjAyMWQxZWYwZDcxMA==").decode("utf-8"))    headers = {'Authorization': 'token ' + token}    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/amazon_scrapper_server.py",headers = headers)    if res.status_code ==200:        with open("amazon_scrapper_server.py",'w',encoding="utf-8") as file:            file.write(res.text)            file.close()        print("Non Headless Scrapper updated successfully")            else:        print(str(res.status_code)+" Error, Non Headless Scrapper not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/product_upload.py",headers = headers)    if res.status_code ==200:        with open("product_upload.py",'w',encoding="utf-8") as file:            file.write(res.text)            file.close()        print("Product Upload updated successfully")    else:        print(str(res.status_code)+" Error, Product Upload not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/py_files/qa_extract.py",                       headers=headers)    if res.status_code == 200:        with open("py_files/qa_extract.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("QA Extract  updated successfully")    else:        print(            str(res.status_code) + " Error, QA Extract not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/py_files/qa_extract_headless.py",                       headers=headers)    if res.status_code == 200:        with open("py_files/qa_extract_headless.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("QA Extract headless updated successfully")    else:        print(            str(res.status_code) + " Error, QA Extract headless not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get(        "https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/py_files/review_extract.py",        headers=headers)    if res.status_code == 200:        with open("py_files/review_extract.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("Review extract updated successfully")    else:        print(            str(res.status_code) + " Error, Review Extract not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get(        "https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/py_files/review_extract_headless.py",        headers=headers)    if res.status_code == 200:        with open("py_files/review_extract_headless.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("Review extract headless updated successfully")    else:        print(            str(res.status_code) + " Error, Review Extract headless not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/amazon_scrapper_server_headless.py",                       headers=headers)    if res.status_code == 200:        with open("amazon_scrapper_server_headless.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("Headless Scrapper updated successfully")    else:        print(            str(res.status_code) + " Error,Headless Scrapper not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/user_agents/user_agents.txt",                       headers=headers)    if res.status_code == 200:        with open("user_agents/user_agents.txt", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("user agents updated successfully")    else:        print(            str(res.status_code) + " Error, User Agents not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/requirements.txt",headers=headers)    if res.status_code == 200:        with open("requirements.txt", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("requirements.txt updated successfully")    else:        print(str(res.status_code) + " Error, requirements not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)    res = requests.get("https://raw.githubusercontent.com/aashishsaini75/amazon_scrapper_server/main/update.py",                       headers=headers)    if res.status_code == 200:        with open("update.py", 'w', encoding="utf-8") as file:            file.write(res.text)            file.close()        print("update.py updated successfully")    else:        print(str(res.status_code) + " Error, update.py not updated, Please contact to aashish@shorthillstech.com")        time.sleep(10)def essential_ops():    if os.path.isdir('user_agents') == False:        os.mkdir('user_agents')    if os.path.isdir('py_files') == False:        os.mkdir('py_files')    if os.path.isfile('qa_extract.py') == True:        os.remove('qa_extract.py')    if os.path.isfile('qa_extract_headless.py') == True:        os.remove('qa_extract_headless.py')    if os.path.isfile('review_extract_headless.py') == True:        os.remove('review_extract_headless.py')    if os.path.isfile('review_extract.py') == True:        os.remove('review_extract.py')def folder_clean():    files = glob.glob('../amazon_scraper/old_scraper/*')    for f in files:        os.remove(f)def completed_alert():    mixer.init()    mixer.music.load('audio/updated.mp3')    mixer.music.play()try:    folder_clean()except:    print("old_scraper couldn't be cleaned")    passtry:    essential_ops()except:    print("Essential ops wasn't performed")    passessential_ops()main_update()completed_alert()