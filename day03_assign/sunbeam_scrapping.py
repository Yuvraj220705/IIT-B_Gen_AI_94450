from asyncio import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
time.sleep(5)

driver.get("https://www.duckduckgo.com/")
print("Initial Page Title" , driver.title)
time.sleep(5)

search_box = driver.find_element(By.NAME, "q")

for ch in "Sun beam pune":
    search_box.send_keys(ch)
    time.sleep(0.1)

search_box.send_keys(Keys.RETURN)

link = driver.find_element(By.ID, "r1-0")
link.click()

inter = driver.find_element(By.PARTIAL_LINK_TEXT, "INTERNSHIP")
inter.click()

print("later Page Title:", driver.title)


time.sleep(10)

plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
plus_button.click()

Available_internship_row=driver.find_elements(By.TAG_NAME,"tr")

time.sleep(5)
driver.quit()