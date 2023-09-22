import sys
from time import wait
# Selenium #
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Mouse #
import pyautogui
from time import sleep

from bs4 import BeautifulSoup

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def main():
    global driver
    print('Welcome to ShopeeScraper!!! \n')
    search_item = str(input('What item would you like to scrape from Shopee?: '))
    runs = int(input('How many runs allowed?: '))
    print(f'Searching {search_item} on Shopee now...')
    # Set Up Browser #
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    #options.add_experimental_option("detach",True) 
    driver = webdriver.Chrome(executable_path=r'C:\Users\School\Desktop\Python Projects\WebScrapers\chromedriver.exe',chrome_options=options)
    driver.get('https://shopee.sg/')
    driver.maximize_window()
    sleep(3)
    btn = pyautogui.locateCenterOnScreen("popupbtn.PNG",confidence=.9)
    pyautogui.doubleClick(btn)
    search_bar = driver.find_element_by_class_name('shopee-searchbar-input__input')
    search_bar.send_keys(search_item)
    search_bar.send_keys(Keys.RETURN)
    sleep(3)
    #runs = 3
    collections = []
    while runs > 0:
        print(f'Scanning... {runs - 1} runs left')
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 5):
            driver.execute_script("window.scrollTo(0, {});".format(i))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div',{'data-sqe':'item'})
        for i in range(len(results)):
            item = results[i].find('a',{'data-sqe':'link'})
            if item:       
                url = 'https://shopee.sg' + item.get('href').translate(non_bmp_map)
                title = item.find('div',{'data-sqe':'name'}).text.translate(non_bmp_map)
                price = item.find('div',{'data-sqe':'name'}).next_sibling.findChild()
                if price:
                    price = price.text
                else:
                    price = ''
                discount = item.find('span',{'class':'percent'})
                if discount:
                    discount = discount.text + ' OFF'
                else:
                    discount = ''
                amount_sold = item.find('div',{'data-sqe':'rating'}).next_sibling
                if amount_sold:
                    amount_sold = amount_sold.text
                else:
                    amount_sold = 0
                dataset = [url,title,price,discount,amount_sold]
                collections.append(dataset)
                #print(f'Success Item {i}')
            else:
                #print(f'Error Item {i}')
                pass
        btn = pyautogui.locateCenterOnScreen("shpnextbtn.PNG",confidence=.9)
        pyautogui.doubleClick(btn)
        sleep(3)
        runs -= 1
    print('')
    print('Number of items found: ' + str(len(collections)) + '\n')
    for collection in collections:
        [url,title,price,discount,amount_sold] = collection
        print('Title: ',title)
        print('Price: ' + price)
        print('Discount: ' + discount)
        print('Amount Sold: ',str(amount_sold))
        print('URL: ' + url)
        print('\n')
    driver.quit()


def AutoDocs():
    # Set Up Browser #
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(chrome_options=options)
    ### Open Selenium Documentation ##
    driver.get('https://selenium-python.readthedocs.io/')
    driver.execute_script("window.open('about:blank', 'tab2');")
    driver.switch_to.window("tab2")
    driver.get('https://www.selenium.dev/documentation/en/')
    ### Open PyAutoGui ###
    driver.execute_script("window.open('about:blank', 'tab3');")
    driver.switch_to.window("tab3")
    driver.get('https://pyautogui.readthedocs.io/en/latest/quickstart.html')
    driver.maximize_window()
    print("Program completed.")

if __name__ == "__main__":  #runs the function main() automatically
    main()  

### Basic Driver ###
##driver.back()
##driver.forward()
##driver.current_url
##driver.refresh()
##driver.title
##driver.current_window_handle
##driver.quit()
##driver.set_window_size(1024, 768)
##driver.minimize_window()
##driver.fullscreen_window()
##driver.save_screenshot('./image.png') take screenshot

### Opens a new tab and switches to new tab
##driver.switch_to.new_window('tab')

### Opens a new window and switches to new window
##driver.switch_to.new_window('window')

### Close the tab or window
##driver.close()

### Switch back to the old tab or window
##driver.switch_to.window(original_window)

### Access each dimension individually
#width = driver.get_window_size().get("width")
#height = driver.get_window_size().get("height")

### store the dimensions and query them later
#size = driver.get_window_size()
#width1 = size.get("width")
#height1 = size.get("height")



#### MISC ####
def CheckWindowChange(driver_instance):
    driver = driver_instance
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    # Click the link which opens in a new window
    driver.find_element(By.LINK_TEXT, "new window").click()
    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    # Wait for the new tab to finish loading content
    wait.until(EC.title_is(""))
