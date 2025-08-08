from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

#Configuration of the test
APP_URL = "file:///d:/ITLA/7mo%20cuatrimestre/Programaci%C3%B3n%203/T3%20CRUD/game-library-app/src/index.html"
USERNAME = "IchibanKasuga"
PASSWORD = "ichiban12345"

def wait_for_element(driver, by, value, timeout=5):
    for _ in range(timeout * 10):
        try:
            el = driver.find_element(by, value)
            if el.is_displayed():
                return el
        except:
            pass
        time.sleep(0.1)
    raise Exception(f"Element not found: {value}")

chrome_options = Options()
#Chrome driver configuration (You need to install google chrome in order to use this by the way, because I couldn't do it on OperaGX).
driver = webdriver.Chrome(options=chrome_options)
driver.get(APP_URL)

try:
    #Test Steps taking into account the user stories:

    #1. Log in to the application.
    wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
    wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
    wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
    time.sleep(2)

    #2. View list of video games (check if the list is present).
    table = wait_for_element(driver, By.ID, "game-table")
    print("Game list is visible.")
    time.sleep(1)

    #This part is optional, it just toggles the game list visibility to check if the button works.
    toggle_btn = wait_for_element(driver, By.ID, "toggle-list-btn")
    toggle_btn.click()
    print("Game list hidden.")
    time.sleep(2)
    toggle_btn = wait_for_element(driver, By.ID, "toggle-list-btn")
    toggle_btn.click()
    print("Game list shown again.")
    time.sleep(2)

    #3. Add a new game to the list (Sonic Adventure).
    wait_for_element(driver, By.ID, "game-title").send_keys("Sonic Adventure")
    wait_for_element(driver, By.ID, "game-genre").send_keys("Platformer")
    wait_for_element(driver, By.ID, "game-release").send_keys("1998")
    wait_for_element(driver, By.ID, "game-description").send_keys("A classic 3D Sonic game.")
    wait_for_element(driver, By.ID, "game-photo").send_keys("https://static.wikia.nocookie.net/sonic/images/6/67/Sonic_Adventure_main_art.png/revision/latest?cb=20210819015445")
    wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
    time.sleep(2)
    print("Added new game.")

    #4. Edit the game details (It just edits the first row).
    edit_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[1]")
    edit_btn.click()
    time.sleep(1)
    title_input = wait_for_element(driver, By.ID, "game-title")
    title_input.clear()
    time.sleep(1)
    title_input.send_keys("Sonic Adventure DX")
    wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
    time.sleep(2)
    print("Edited first game.")

    #5. Delete video game (It only deletes the first row, which is the one we just edited).
    delete_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[2]")
    delete_btn.click()
    time.sleep(2)
    print("Deleted first game.")

finally:
    driver.quit()