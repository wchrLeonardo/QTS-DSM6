from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


#Teste de modo incorreto com time.sleep
def test_create_user_e2e():
    driver = webdriver.Chrome()

    driver.get("http://localhost:5000")
    
    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Leonardo")

    driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 5)

    wait.until(
        lambda d: any("Leonardo" in el.text for el in d.find_elements(By.TAG_NAME, "li"))
    )
    
    users = driver.find_elements(By.TAG_NAME, "li")

    assert any("Leonardo" in user.text for user in users)

    driver.quit()


def test_register_two_users_e2e():
    driver = webdriver.Chrome()
    
    try:
        driver.get("http://localhost:5000")
        wait = WebDriverWait(driver, 5)

        # Cadastro do primeiro usuário
        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Usuario1")
        driver.find_element(By.ID, "submit").click()

        # Garantir que o sistema atualizou a interface após o primeiro cadastro
        wait.until(
            lambda d: "Usuario1" in d.find_element(By.ID, "users").text
        )

        # Cadastro do segundo usuário
        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Usuario2")
        driver.find_element(By.ID, "submit").click()

        # Garantir que o sistema atualizou a interface após o segundo cadastro
        wait.until(
            lambda d: "Usuario2" in d.find_element(By.ID, "users").text
        )

        # Validar se os dois usuários aparecem na lista exibida na tela
        users_text = driver.find_element(By.ID, "users").text
        assert "Usuario1" in users_text
        assert "Usuario2" in users_text

    finally:
        driver.quit()