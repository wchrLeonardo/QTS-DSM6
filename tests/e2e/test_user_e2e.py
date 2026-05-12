from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


from selenium.webdriver.chrome.options import Options

def get_headless_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

def test_create_user_e2e():
    driver = get_headless_driver()
    driver.get("http://localhost:5000")

    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Leonardo")

    input_email = driver.find_element(By.ID, "email")
    input_email.send_keys("leo@test.com")

    driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 5)
    wait.until(
        lambda d: any(
            "Leonardo" in el.text for el in d.find_elements(By.TAG_NAME, "li")
        )
    )

    users = driver.find_elements(By.TAG_NAME, "li")
    assert any("Leonardo" in user.text for user in users)
    driver.quit()


def test_exercicio_passo_a_passo_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get("http://localhost:5000")
        assert driver.title == "Users"

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Usuario1")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("usuario1@test.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Usuario1" in d.find_element(By.ID, "users").text)

        assert "Usuario1" in driver.find_element(By.ID, "users").text

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Usuario2")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("usuario2@test.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Usuario2" in d.find_element(By.ID, "users").text)

        users_list = driver.find_elements(By.TAG_NAME, "li")
        users_texts = [user.text for user in users_list]
        assert "Usuario1" in str(users_texts)
        assert "Usuario2" in str(users_texts)

    finally:
        driver.quit()


# --- 2 Novos Testes E2E ---
def test_register_user_with_email_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://localhost:5000")

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("E2E Test")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("e2e@test.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "E2E Test" in d.find_element(By.ID, "users").text)

        # Validate that email is somehow displayed or at least name is displayed
        assert "E2E Test" in driver.find_element(By.ID, "users").text
    finally:
        driver.quit()


def test_validation_error_duplicate_email_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://localhost:5000")

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("E2E Duplicate 1")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("duplicate@test.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "E2E Duplicate 1" in d.find_element(By.ID, "users").text)

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("E2E Duplicate 2")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("duplicate@test.com")

        driver.find_element(By.ID, "submit").click()

        # Should NOT appear since it's a duplicate email
        time.sleep(2)  # just to be sure it doesn't appear
        users_text = driver.find_element(By.ID, "users").text
        assert "E2E Duplicate 2" not in users_text

    finally:
        driver.quit()
