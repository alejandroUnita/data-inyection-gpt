# chatgpt_script.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc

def get_chatgpt_response(prompt_text):

    # Configurar el controlador del navegador (Chrome)
    driver = uc.Chrome()

    # Abrir ChatGPT.com
    driver.get("https://chatgpt.com/")
    time.sleep(2)  # Pausa inicial para cargar la página

    # Función para esperar a que un elemento esté presente
    def wait_for_element(by, value, timeout=10):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"Elemento {value} no encontrado tras {timeout} segundos: {e}")
            return None

    # Localizar el div contenteditable
    prompt_div = wait_for_element(By.ID, "prompt-textarea")
    if not prompt_div:
        print("No se encontró el div #prompt-textarea")
        driver.quit()
        return None

    try:
        # Enfocar y llenar el div con el prompt
        prompt_div.click()
        time.sleep(0.5)  # Pausa para simular comportamiento humano
        driver.execute_script(f"document.getElementById('prompt-textarea').innerText = '{prompt_text}'")
        print(f"Div prompt-textarea llenado con: {prompt_text}")
        
        # Simular la pulsación de Enter
        time.sleep(0.5)  # Pausa antes de enviar
        prompt_div.send_keys(Keys.ENTER)
        print("Tecla Enter pulsada para enviar el prompt")
    except Exception as e:
        print(f"Error al llenar o enviar prompt-textarea: {e}")
        driver.quit()
        return None

    time.sleep(2)
    # Esperar la respuesta en el div con clase específica
    try:
        response_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'markdown prose w-full break-words')]"))
        )
        response_text = response_div.text
        print(f"Respuesta obtenida: {response_text}")
    except Exception as e:
        print(f"Error al obtener la respuesta: {e}")
        response_text = None

    # Cerrar el navegador
    driver.quit()
    
    return response_text

if __name__ == "__main__":
    # Prueba directa si se ejecuta este archivo
    prompt = "Tell me a short story about a cat."
    response = get_chatgpt_response(prompt)
    if response:
        print("Respuesta final:", response)
    else:
        print("No se pudo obtener una respuesta")