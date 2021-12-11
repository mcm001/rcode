from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time, pickle

driver = webdriver.Firefox()
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
except Exception:
    pass

driver.get("https://northeastern.bioraft.com/node/2054541/users")

# list = ["veghte.b@northeastern.edu","tortolani.ma@northeastern.edu","wheeler.ky@northeastern.edu","demartino.da@northeastern.edu","dao.t@northeastern.edu","smoragiewicz.t@northeastern.edu","moore.w@northeastern.edu","barnett.c@northeastern.edu","ng.da@northeastern.edu","lefkoff.h@northeastern.edu","benenson.sa@northeastern.edu","barbozahurtado.j@northeastern.edu","rabson.g@northeastern.edu","frieden.t@northeastern.edu","ryan.bre@northeastern.edu","zabib.a@northeastern.edu","rezendebarbosa.g@northeastern.edu","leffers.ch@northeastern.edu","fox.wi@northeastern.edu","logcher.s@northeastern.edu","webster.q@northeastern.edu","gurin.r@northeastern.edu",]
list = ["Aidan Rozes","Zach Safford","Henry Silverstein","Spencer Sweeney","David Wasserman","Owen Welch","Sam Wohlever","Hanye ","David DeRienzo","Sandra Chai","Salmaan Shafqat","Tej Vyas","Ashley Banaszewski","Vanessa Khangi","Thomas Chan","Kellan McCarthy"]

# input("Waiting for input...")
try:
    element = WebDriverWait(driver, 240).until(
        EC.presence_of_element_located((By.ID, "edit-userRole"))
    )
    print("Starting")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

    for e in list:
        try: 
            print(e)
            ele = driver.find_element_by_id("edit-username")
            ele.clear()
            ele.send_keys(str(e))
            ele = Select(driver.find_element_by_id("edit-userRole"))
            ele.select_by_index(2)
            driver.find_element_by_id("edit-lookup").click()
            time.sleep(4)
        except Exception as e:
            print(e)
            pass
finally:
    driver.quit()

