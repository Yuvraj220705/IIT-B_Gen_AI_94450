from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com/")
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

search_box = driver.find_element(By.ID, "searchbox_input")

search_box.send_keys("Sunbeam pune")
search_box.send_keys(Keys.ENTER)


link = driver.find_element(By.ID, "r1-0")
link.click()


option = driver.find_element(By.PARTIAL_LINK_TEXT, "INTER")
option.click()


# click_intership=driver.find_element(By.PARTIAL_LINK_TEXT,"Available Internship Programs")
# click_intership.click()

plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
plus_button.click()

Available_internship_row=driver.find_elements(By.TAG_NAME,"tr")


for row in Available_internship_row:
    cols=row.find_elements(By.TAG_NAME,"td")
    

    row_data=[]
    for col in cols:
        row_data.append(col.text)

    for data in row_data:
        print(data)




# Available_internship_row=driver.find_elements(By.TAG_NAME,"tr")
# print("-----  tr ")
# for row in Available_internship_row:
#     print(row.text)



time.sleep(5)
driver.close()