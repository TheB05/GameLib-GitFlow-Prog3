from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

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
driver = webdriver.Chrome(options=chrome_options)
driver.get(APP_URL)

try:
    #Login tests.
    #Rejects incorrect credentials.
    try:
        wait_for_element(driver, By.ID, "login-username").clear()
        wait_for_element(driver, By.ID, "login-password").clear()
        wait_for_element(driver, By.ID, "login-username").send_keys("KasugaIchiban")
        wait_for_element(driver, By.ID, "login-password").send_keys("1234Ichiban")
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        error_msg = wait_for_element(driver, By.ID, "login-error").text
        assert "Invalid" in error_msg
        screenshot = take_screenshot(driver, "auth_reject_wrong_credentials")
        record_result("Rejects incorrect credentials", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_reject_wrong_credentials_fail")
        record_result("Rejects incorrect credentials", "FAIL", screenshot, str(e))

    #Validates empty fields.
    try:
        driver.get(APP_URL)
        wait_for_element(driver, By.ID, "login-username").clear()
        wait_for_element(driver, By.ID, "login-password").clear()
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        error_msg = wait_for_element(driver, By.ID, "login-error").text
        assert error_msg.strip() != ""
        screenshot = take_screenshot(driver, "auth_empty_fields")
        record_result("Validates empty fields", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_empty_fields_fail")
        record_result("Validates empty fields", "FAIL", screenshot, str(e))

    #Accepts correct credentials and redirects to game form.
    try:
        driver.get(APP_URL)
        wait_for_element(driver, By.ID, "login-username").clear()
        wait_for_element(driver, By.ID, "login-password").clear()
        wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
        wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(2)
        wait_for_element(driver, By.ID, "game-form")
        screenshot = take_screenshot(driver, "auth_accept_correct_credentials")
        record_result("Accepts correct credentials and redirects", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_accept_correct_credentials_fail")
        record_result("Accepts correct credentials and redirects", "FAIL", screenshot, str(e))

    #Keeps session active until logout.
    try:
        driver.refresh()
        wait_for_element(driver, By.ID, "game-form")
        screenshot = take_screenshot(driver, "auth_session_persists")
        record_result("Session persists after reload", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_session_persists_fail")
        record_result("Session persists after reload", "FAIL", screenshot, str(e))

    #Logout clears session and redirects to login.
    try:
        wait_for_element(driver, By.ID, "logout-btn").click()
        time.sleep(1)
        wait_for_element(driver, By.ID, "login-form")
        screenshot = take_screenshot(driver, "auth_logout_clears_session")
        record_result("Logout clears session and redirects", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_logout_clears_session_fail")
        record_result("Logout clears session and redirects", "FAIL", screenshot, str(e))

    #Character limit in login fields.
    try:
        driver.get(APP_URL)
        long_user = "Ichiban" * 30
        long_pass = "Kasuga" * 30
        wait_for_element(driver, By.ID, "login-username").send_keys(long_user)
        wait_for_element(driver, By.ID, "login-password").send_keys(long_pass)
        username_value = wait_for_element(driver, By.ID, "login-username").get_attribute("value")
        password_value = wait_for_element(driver, By.ID, "login-password").get_attribute("value")
        assert len(username_value) <= 25 and len(password_value) <= 25
        screenshot = take_screenshot(driver, "auth_login_char_limit")
        record_result("Login fields enforce 25-char limit", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "auth_login_char_limit_fail")
        record_result("Login fields enforce 25-char limit", "FAIL", screenshot, str(e))

    #CRUD tests.
    #Create: Validates required fields and numeric types.
    try:
        #Login first before testing CRUD, just to be sure it works.
        wait_for_element(driver, By.ID, "login-username").clear()
        wait_for_element(driver, By.ID, "login-password").clear()
        wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
        wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        #Try to submit empty form fields and check for validation.
        wait_for_element(driver, By.ID, "game-title").clear()
        wait_for_element(driver, By.ID, "game-genre").clear()
        wait_for_element(driver, By.ID, "game-release").clear()
        wait_for_element(driver, By.ID, "game-description").clear()
        wait_for_element(driver, By.ID, "game-achievements").clear()
        wait_for_element(driver, By.ID, "game-playtime").clear()
        wait_for_element(driver, By.ID, "game-photo").clear()
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        # Should not add a new row, because fields are required for the form.
        rows = driver.find_elements(By.XPATH, "//tbody[@id='game-table-body']/tr")
        assert len(rows) == 0
        screenshot = take_screenshot(driver, "crud_create_required_fields")
        record_result("Create validates required fields", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_create_required_fields_fail")
        record_result("Create validates required fields", "FAIL", screenshot, str(e))

    #Create: Validates numeric types.
    try:
        wait_for_element(driver, By.ID, "game-title").send_keys("Sonic Adventure")
        wait_for_element(driver, By.ID, "game-genre").send_keys("Platformer")
        wait_for_element(driver, By.ID, "game-release").send_keys("1998-23-12")
        wait_for_element(driver, By.ID, "game-description").send_keys("Sonic!")
        wait_for_element(driver, By.ID, "game-achievements").send_keys("abc")  #Check numeric validation.
        wait_for_element(driver, By.ID, "game-playtime").send_keys("xyz")      #Check numeric validation, again.
        wait_for_element(driver, By.ID, "game-photo").send_keys("https://static.wikia.nocookie.net/sonic/images/6/67/Sonic_Adventure_main_art.png/revision/latest?cb=20210819015445")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        #Should not add a new row again, because achievements and playtime are not numeric.
        rows = driver.find_elements(By.XPATH, "//tbody[@id='game-table-body']/tr")
        assert len(rows) == 0
        screenshot = take_screenshot(driver, "crud_create_numeric_validation")
        record_result("Create validates numeric types", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_create_numeric_validation_fail")
        record_result("Create validates numeric types", "FAIL", screenshot, str(e))

    #Create: Add valid game.
    try:
        wait_for_element(driver, By.ID, "game-achievements").clear()
        wait_for_element(driver, By.ID, "game-playtime").clear()
        wait_for_element(driver, By.ID, "game-achievements").send_keys("10")
        wait_for_element(driver, By.ID, "game-playtime").send_keys("100")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        rows = driver.find_elements(By.XPATH, "//tbody[@id='game-table-body']/tr")
        assert len(rows) == 1
        screenshot = take_screenshot(driver, "crud_create_valid_game")
        record_result("Create valid game", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_create_valid_game_fail")
        record_result("Create valid game", "FAIL", screenshot, str(e))

    #Read: Displays all stored games.
    try:
        row = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]")
        cells = row.find_elements(By.TAG_NAME, "td")
        assert all(cell.text.strip() != "" for cell in cells[:-1]) 
        screenshot = take_screenshot(driver, "crud_read_display_games")
        record_result("Read displays all stored games", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_read_display_games_fail")
        record_result("Read displays all stored games", "FAIL", screenshot, str(e))

    #Update: Changes are reflected and persist.
    try:
        edit_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[1]")
        edit_btn.click()
        title_input = wait_for_element(driver, By.ID, "game-title")
        title_input.clear()
        title_input.send_keys("Test Game Updated")
        wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
        time.sleep(1)
        updated_row = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[2]")
        assert updated_row.text == "Test Game Updated"
        screenshot = take_screenshot(driver, "crud_update_reflects")
        record_result("Update reflects immediately and persists", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_update_reflects_fail")
        record_result("Update reflects immediately and persists", "FAIL", screenshot, str(e))

    #Delete: Deletion is permanent and persists.
    try:
        delete_btn = wait_for_element(driver, By.XPATH, "//tbody[@id='game-table-body']/tr[1]/td[last()]/button[2]")
        delete_btn.click()
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        rows = driver.find_elements(By.XPATH, "//tbody[@id='game-table-body']/tr")
        assert len(rows) == 0
        screenshot = take_screenshot(driver, "crud_delete_persists")
        record_result("Delete is permanent and persists", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "crud_delete_persists_fail")
        record_result("Delete is permanent and persists", "FAIL", screenshot, str(e))

    #List display tests.
    try:
        driver.get(APP_URL)
        wait_for_element(driver, By.ID, "login-username").send_keys(USERNAME)
        wait_for_element(driver, By.ID, "login-password").send_keys(PASSWORD)
        wait_for_element(driver, By.CSS_SELECTOR, "#login-form button[type='submit']").click()
        time.sleep(1)
        table_body = wait_for_element(driver, By.ID, "game-table-body")
        assert "No games" in driver.page_source or len(table_body.text.strip()) == 0
        screenshot = take_screenshot(driver, "list_empty_message")
        record_result("List loads and shows empty message", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "list_empty_message_fail")
        record_result("List loads and shows empty message", "FAIL", screenshot, str(e))

    #Dashboard tests.
    try:
        for i, (title, genre, playtime) in enumerate([
            ("Yakuza 4", "Action", "50"),
            ("Yakuza 3", "Action", "100"),
            ("Sonic Lost Worlds", "Platformer", "150"),
            ("Yakuza 7", "RPG", "20"),
        ]):
            wait_for_element(driver, By.ID, "game-title").clear()
            wait_for_element(driver, By.ID, "game-genre").clear()
            wait_for_element(driver, By.ID, "game-release").clear()
            wait_for_element(driver, By.ID, "game-description").clear()
            wait_for_element(driver, By.ID, "game-achievements").clear()
            wait_for_element(driver, By.ID, "game-playtime").clear()
            wait_for_element(driver, By.ID, "game-photo").clear()
            wait_for_element(driver, By.ID, "game-title").send_keys(title)
            wait_for_element(driver, By.ID, "game-genre").send_keys(genre)
            wait_for_element(driver, By.ID, "game-release").send_keys("2025-15-8")
            wait_for_element(driver, By.ID, "game-description").send_keys("Juego de prueba")
            wait_for_element(driver, By.ID, "game-achievements").send_keys("5")
            wait_for_element(driver, By.ID, "game-playtime").send_keys(playtime)
            wait_for_element(driver, By.ID, "game-photo").send_keys("https://static.wikia.nocookie.net/yakuza/images/e/e6/Yakuza_4_Remastered_-_Cover_-_PS4_WW.jpeg/revision/latest/thumbnail/width/360/height/360?cb=20210609074200")
            wait_for_element(driver, By.CSS_SELECTOR, "#game-form button[type='submit']").click()
            time.sleep(0.5)
        dashboard = wait_for_element(driver, By.ID, "dashboard")
        assert "RPG" in dashboard.text and "Action" in dashboard.text and "Puzzle" in dashboard.text
        screenshot = take_screenshot(driver, "dashboard_top_genres")
        record_result("Dashboard updates and calculates top 3 genres", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "dashboard_top_genres_fail")
        record_result("Dashboard updates and calculates top 3 genres", "FAIL", screenshot, str(e))

    #Data Persistence tests.
    try:
        driver.refresh()
        time.sleep(1)
        rows = driver.find_elements(By.XPATH, "//tbody[@id='game-table-body']/tr")
        assert len(rows) >= 3
        screenshot = take_screenshot(driver, "persistence_after_reload")
        record_result("Data persists after reload", "PASS", screenshot)
    except Exception as e:
        screenshot = take_screenshot(driver, "persistence_after_reload_fail")
        record_result("Data persists after reload", "FAIL", screenshot, str(e))

finally:
    driver.quit()

#HTML report
report_path = os.path.join(REPORT_DIR, "report.html")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("<html><head><title>Selenium Test Report</title></head><body>")
    f.write("<h1>Selenium Test Report</h1>")
    f.write("<table border='1' cellpadding='8' style='border-collapse:collapse;'>")
    f.write("<tr><th>Test</th><th>Status</th><th>Screenshot</th></tr>")
    for res in results:
        color = "#d4edda" if res["status"] == "PASS" else "#f8d7da"
        f.write(f"<tr style='background:{color};'><td>{res['name']}</td><td>{res['status']}</td>")
        f.write(f"<td><a href='{os.path.basename(res['screenshot'])}' target='_blank'><img src='{os.path.basename(res['screenshot'])}' width='200'></a></td></tr>")
    f.write("</table></body></html>")

print(f"\nHTML report generated: {report_path}")