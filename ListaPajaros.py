import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# URL de la página a scrapear
cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/a-z"

# Función para scrapear con Selenium
def scrape_with_selenium(url):
    options = Options()
    options.headless = False  # Establecer en True para ejecutar en modo headless
    driver = webdriver.Chrome(options=options)

    # Navegar a la página
    driver.get(url)

    # Aceptar cookies
    try:
        # Usar el selector CSS para buscar el botón dentro del div con clase buttons
        accept_button = driver.find_element(By.CSS_SELECTOR, 'rspb-cookie-banner .buttons button.btn-primary')
        accept_button.click()  # Hacer clic en el botón "Accept All"
    except Exception as e:
        print("No se pudo hacer clic en el botón de aceptar cookies:", e)

    # Esperar a que el contenido dinámico cargue
    time.sleep(3)

    # Extraer los nombres de los pájaros
    bird_data_url = []

    # Bucle para hacer scraping mientras haya un botón "Next"
    while True:
        # Extraer todos los <span> con la clase 'text-link-underline text-link-underline--deepsea'
        span_elements = driver.find_elements(By.CSS_SELECTOR, 'span.text-link-underline.text-link-underline--deepsea')

        # Iterar sobre los elementos encontrados y obtener el texto
        for span in span_elements:
            bird_name = span.text
            bird_data_url.append(bird_name)

        # Intentar encontrar el botón "Next" con espera explícita
        try:
            # Esperar hasta que el botón "Next" sea visible
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.next.button'))
            )
            next_button.click()  # Hacer clic en el botón "Next"
            print("Clic en el botón 'Next'")

            # Esperar para que se cargue la siguiente página
            time.sleep(3)
        except Exception as e:
            print("No se encontró el botón 'Next'")
            break  # Terminar el bucle si no se encuentra el botón "Next"

    # Crear la carpeta json si no existe
    if not os.path.exists("json"):
        os.makedirs("json")

    # Guardar los datos en un archivo JSON dentro de la carpeta 'json'
    with open(os.path.join("json", "ListaPajaros.json"), 'w', encoding='utf-8') as json_file:
        json.dump(bird_data_url, json_file, ensure_ascii=False, indent=4)

    # Cerrar el navegador
    driver.quit()

    # Mensaje finalizado
    print("Proceso finalizado.")

# Ejecutar el scraping
scrape_with_selenium(cnn_url)
