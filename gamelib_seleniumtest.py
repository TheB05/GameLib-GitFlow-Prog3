from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

#Configuration of the test
#Make sure to change the APP_URL to the correct path of your game library app.
APP_URL = "file:///d:/ITLA/7mo%20cuatrimestre/Programaci%C3%B3n%203/T3%20CRUD/game-library-app/src/index.html"
USERNAME = "IchibanKasuga"
PASSWORD = "ichiban12345"

REPORT_DIR = "selenium_report"
os.makedirs(REPORT_DIR, exist_ok=True)
results = []

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

def take_screenshot(driver, name):
    path = os.path.join(REPORT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    return path

def record_result(name, status, screenshot, message=""):
    results.append({
        "name": name,
        "status": status,
        "screenshot": screenshot,
        "message": message
    })

chrome_options = Options()
#Chrome driver configuration (You need to install google chrome in order to use this by the way, because I couldn't do it on OperaGX).
#But if you want to use OperaGX, you can change the webdriver.Chrome() to webdriver.Opera() and set the path to your OperaGX executable.
driver = webdriver.Chrome(options=chrome_options)
driver.get(APP_URL)

try:
    #1. Log in to the application.
    try:
        wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
        wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(2)
        screenshot = take_screenshot(driver, "01_login_success")
        record_result("Login with correct credentials", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "01_login_success_fail")
        record_result("Login with correct credentials", "FAIL", screenshot, str(e))

    #2. View list of video games.
    try:
        table = wait_for_element(driver, By.ID, "game-table")
        time.sleep(1)
        screenshot = take_screenshot(driver, "02_view_list")
        record_result("View game list", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "02_view_list_fail")
        record_result("View game list", "FAIL", screenshot, str(e))

    #3. Toggle the game list visibility.
    try:
        toggle_btn = wait_for_element(driver, By.ID, "toggle-list-btn")
        toggle_btn.click()
        time.sleep(1)
        toggle_btn = wait_for_element(driver, By.ID, "toggle-list-btn")
        toggle_btn.click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "03_toggle_list")
        record_result("Toggle game list visibility", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "03_toggle_list_fail")
        record_result("Toggle game list visibility", "FAIL", screenshot, str(e))

    #4. Add a new game.
    try:
        wait_for_element(driver, By.ID, "game-title").send_keys("Sonic Adventure")
        wait_for_element(driver, By.ID, "game-genre").send_keys("Platformer")
        wait_for_element(driver, By.ID, "game-release").send_keys("1998")
        wait_for_element(driver, By.ID, "game-description").send_keys("A classic 3D Sonic game.")
        wait_for_element(driver, By.ID, "game-photo").send_keys("https://static.wikia.nocookie.net/sonic/images/6/67/Sonic_Adventure_main_art.png/revision/latest?cb=20210819015445")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(2)
        screenshot = take_screenshot(driver, "04_add_game")
        record_result("Add new game", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "04_add_game_fail")
        record_result("Add new game", "FAIL", screenshot, str(e))

    #5. Edit the game details.
    try:
        edit_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[1]")
        edit_btn.click()
        time.sleep(1)
        title_input = wait_for_element(driver, By.ID, "game-title")
        title_input.clear()
        time.sleep(1)
        title_input.send_keys("Sonic Adventure DX")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(2)
        screenshot = take_screenshot(driver, "05_edit_game")
        record_result("Edit first game", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "05_edit_game_fail")
        record_result("Edit first game", "FAIL", screenshot, str(e))

    #6. Delete video game.
    try:
        delete_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[2]")
        delete_btn.click()
        time.sleep(2)
        screenshot = take_screenshot(driver, "06_delete_game")
        record_result("Delete first game", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "06_delete_game_fail")
        record_result("Delete first game", "FAIL", screenshot, str(e))

    #7. Login with wrong credentials.
    try:
        driver.get(APP_URL)
        wait_for_element(driver, By.ID, "login-username").send_keys("KasugaIchiban")
        wait_for_element(driver, By.ID, "login-password").send_keys("Ichiban54321")
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        error_msg = wait_for_element(driver, By.ID, "login-error").text
        assert "Invalid" in error_msg
        screenshot = take_screenshot(driver, "07_negative_login")
        record_result("Negative login test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "07_negative_login_fail")
        record_result("Negative login test", "FAIL", screenshot, str(e))

    #8. Login with max length username and password.
    try:
        driver.get(APP_URL)
        long_user = "A" * 100
        long_pass = "B" * 100
        wait_for_element(driver, By.ID, "login-username").send_keys(long_user)
        wait_for_element(driver, By.ID, "login-password").send_keys(long_pass)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        error_msg = wait_for_element(driver, By.ID, "login-error").text
        assert "Invalid" in error_msg
        screenshot = take_screenshot(driver, "08_boundary_login")
        record_result("Boundary login test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "08_boundary_login_fail")
        record_result("Boundary login test", "FAIL", screenshot, str(e))

    #9. Happy path login for further tests.
    try:
        wait_for_element(driver, By.ID, "login-username").clear()
        wait_for_element(driver, By.ID, "login-password").clear()
        wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
        wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "09_login_again")
        record_result("Login again for further tests", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "09_login_again_fail")
        record_result("Login again for further tests", "FAIL", screenshot, str(e))

    #10. Add game with empty fields. (The row count should not change)
    try:
        wait_for_element(driver, By.ID, "game-title").clear()
        wait_for_element(driver, By.ID, "game-genre").clear()
        wait_for_element(driver, By.ID, "game-release").clear()
        wait_for_element(driver, By.ID, "game-description").clear()
        wait_for_element(driver, By.ID, "game-photo").clear()
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "10_negative_add_game")
        record_result("Negative add game test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "10_negative_add_game_fail")
        record_result("Negative add game test", "FAIL", screenshot, str(e))

    #11. Add game with very long values.
    try:
        long_text = "X" * 255
        wait_for_element(driver, By.ID, "game-title").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-genre").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-release").send_keys("9999")
        wait_for_element(driver, By.ID, "game-description").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-photo").send_keys("https://preview.redd.it/kaito-san-v0-70v4wow474sc1.jpeg?width=1080&format=pjpg&auto=webp&s=2d5088e36661cbca154bb4560ba3f2ccd9ef8928")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "11_boundary_add_game")
        record_result("Boundary add game test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "11_boundary_add_game_fail")
        record_result("Boundary add game test", "FAIL", screenshot, str(e))

    #12. Edit game to empty values.
    try:
        edit_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[1]")
        edit_btn.click()
        wait_for_element(driver, By.ID, "game-title").clear()
        wait_for_element(driver, By.ID, "game-genre").clear()
        wait_for_element(driver, By.ID, "game-release").clear()
        wait_for_element(driver, By.ID, "game-description").clear()
        wait_for_element(driver, By.ID, "game-photo").clear()
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "12_negative_edit_game")
        record_result("Negative edit game test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "12_negative_edit_game_fail")
        record_result("Negative edit game test", "FAIL", screenshot, str(e))

    #13. Edit game to max length values.
    try:
        edit_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[1]")
        edit_btn.click()
        long_text = "X" * 255
        wait_for_element(driver, By.ID, "game-title").clear()
        wait_for_element(driver, By.ID, "game-title").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-genre").clear()
        wait_for_element(driver, By.ID, "game-genre").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-release").clear()
        wait_for_element(driver, By.ID, "game-release").send_keys("9999")
        wait_for_element(driver, By.ID, "game-description").clear()
        wait_for_element(driver, By.ID, "game-description").send_keys(long_text)
        wait_for_element(driver, By.ID, "game-photo").clear()
        wait_for_element(driver, By.ID, "game-photo").send_keys("https://preview.redd.it/kaito-san-v0-70v4wow474sc1.jpeg?width=1080&format=pjpg&auto=webp&s=2d5088e36661cbca154bb4560ba3f2ccd9ef8928")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        screenshot = take_screenshot(driver, "13_boundary_edit_game")
        record_result("Boundary edit game test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "13_boundary_edit_game_fail")
        record_result("Boundary edit game test", "FAIL", screenshot, str(e))

    #14. Delete when no games exist.
    try:
        while True:
            try:
                delete_btn = driver.find_element(By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[2]")
                delete_btn.click()
                time.sleep(0.5)
            except:
                break
        screenshot = take_screenshot(driver, "14_negative_delete")
        record_result("Negative delete test", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "14_negative_delete_fail")
        record_result("Negative delete test", "FAIL", screenshot, str(e))

finally:
    driver.quit()

#This part right here will generate an HTML report of the test results (It will show a table with the tests and screenshots).
#You can also customize the report format as needed.
report_path = os.path.join(REPORT_DIR, "report.html")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("<html><head><title>Selenium Test Report</title></head><body>")
    f.write("<h1>Selenium Test Report</h1>")
    f.write("<table border='1' cellpadding='8' style='border-collapse:collapse;'>")
    f.write("<tr><th>Test</th><th>Status</th><th>Screenshot</th><th>Message</th></tr>")
    for res in results:
        color = "#d4edda" if res["status"] == "PASS" else "#f8d7da"
        f.write(f"<tr style='background:{color};'><td>{res['name']}</td><td>{res['status']}</td>")
        f.write(f"<td><a href='{os.path.basename(res['screenshot'])}' target='_blank'><img src='{os.path.basename(res['screenshot'])}' width='200'></a></td>")
        f.write(f"<td>{res['message']}</td></tr>")
    f.write("</table></body></html>")

print(f"\nHTML report generated: {report_path}")