from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import sys
#cap = DesiredCapabilities().FIREFOX
#cap["marionette"] = False
start = time.time()
display = Display(visible=0, size=(800, 400))
display.start()
print("Before driver")
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
try:
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
    driver.set_window_size(800,400)
except Exception as e:
    print(f"Driver Failed: {e}")
page = driver.get('https://www.student.ladok.se/student/loggain')
link = driver.find_element_by_link_text('Välj lärosäte / Choose university').click()
try:
    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/form/div[2]/div[5]")))
    search.click()
except Exception as e:
    print(e)
try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='proceed']")))
    element.click()
except Exception as e:
    print(e)

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/form/div/div/div[1]/div/input")))
    element.send_keys(str(sys.argv[1]))
    passwordField = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div[2]/div/input")
    passwordField.send_keys(str(sys.argv[2]))
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div[3]/button").click()
except Exception as e:
    print(e)
try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[1]/ladok-pagaende-kurser/div[3]/ladok-pagaende-kurser-i-struktur/div/ladok-pagaende-kurslista/div[1]/div/h4/ladok-kurslink/div[2]/a")))
except Exception as e:
    print(e)
current = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[1]/ladok-pagaende-kurser/div[3]/ladok-pagaende-kurser-i-struktur/div/ladok-pagaende-kurslista/div")
print("--------Kurser Ladok--------")
print("Aktuella kurser:")
for element in current:
    course = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
    print(course.get_attribute('textContent'))
old = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[3]/ladok-oavslutade-kurser/div[3]/ladok-oavslutade-kurser-i-struktur/div/ladok-kommande-kurslista/div")
print("\nOavslutade kurser:")
for element in old:
    course = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
    print(course.get_attribute('textContent'))
fri = driver.find_elements_by_xpath("/html/body/ladok-applikation/div/main/div/ng-component/ladok-aktuell/div[2]/div[3]/ladok-oavslutade-kurser/div[4]/ladok-kommande-kurslista/div")
print("\nFristående kurser:")
for element in fri:
    course = element.find_element_by_xpath("./div/h4/ladok-kurslink/div[2]/a")
    print(course.get_attribute('textContent'))
driver.quit()
display.stop()
end = time.time()
print(end - start)