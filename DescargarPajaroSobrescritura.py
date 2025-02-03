#Crea un json para todos los pajaros

import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# URL de la página a scrapear
cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/aquatic-warbler"
#cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/arctic-tern"

# Función para descargar archivos
def descargar_archivo(url, nombre_archivo):
    try:
        # Verificar si el archivo ya existe
        if os.path.exists(os.path.join("descargas", nombre_archivo)):
            print(f"El archivo '{nombre_archivo}' ya existe, no se descargará.")
            return  # Si el archivo ya existe, no lo descargamos

        # Realizar la solicitud HTTP para obtener el archivo
        response = requests.get(url)
        response.raise_for_status()  # Lanzar error si la respuesta no es 200

        # Crear la carpeta si no existe
        if not os.path.exists("descargas"):
            os.makedirs("descargas")

        # Guardar el archivo con el nombre proporcionado
        with open(os.path.join("descargas", nombre_archivo), 'wb') as archivo:
            archivo.write(response.content)
        print(f"Archivo '{nombre_archivo}' descargado correctamente.")
    except Exception as e:
        print(f"No se pudo descargar el archivo {nombre_archivo}: {e}")

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

    # Extraer los datos del pájaro
    bird_data = {}

    # Extraer y guardar el nombre del pájaro
    nombrePajaro = driver.find_element(By.TAG_NAME, 'h1').text
    nombreP = driver.find_elements(By.TAG_NAME, 'h1')
    if nombreP:
        bird_data['nombre'] = nombreP[0].text

    # Establece el nombre del parajaro como nombre de la imagen
    nombre_archivo_jpg = f"{nombrePajaro.replace(' ', '')}.jpg"
    # Establece el nombre del parajaro como nombre del archivo de audio
    nombre_archivo_mp3 = f"{nombrePajaro.replace(' ', '')}.mp3"

    # Extraer y guardar el nombre científico del pájaro
    nombreC = driver.find_elements(By.CSS_SELECTOR, 'span.info.latin')
    if nombreC:
        bird_data['nombre_cientifico'] = nombreC[0].text

    # Extraer y guardar el grupo del pájaro
    grupoP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].info.ng-star-inserted')
    if grupoP:
        grupo_texto = grupoP[0].text
        # Dividir el texto por ":", tomar la segunda parte y eliminar los espacios extra
        bird_data['grupo'] = grupo_texto.split(":")[1].strip()

    # Extraer y guardar la foto del pájaro
    fotoP = driver.find_elements(By.CSS_SELECTOR, 'img[_ngcontent-rspb-frontend-app-c201]')
    if fotoP:
        foto_url = fotoP[0].get_attribute('src')
        bird_data['foto_url'] = "/images/" + nombre_archivo_jpg
        # Descargar la foto solo si no existe
        descargar_archivo(foto_url, nombre_archivo_jpg)

    # Extraer y guardar la identificación del pájaro
    ideP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].intro')
    if ideP:
        bird_data['identificacion'] = ideP[0].text

    # Extraer y guardar el enlace del canto del pájaro
    try:
        enlace = driver.find_element(By.CSS_SELECTOR, 'a[_ngcontent-rspb-frontend-app-c63]')
        canto_url = enlace.get_attribute('href')
        bird_data['canto_url'] = "/audio/" + nombre_archivo_mp3
        # Descargar el audio solo si no existe
        descargar_archivo(canto_url + "/download", nombre_archivo_mp3)
    except Exception as e:
        print("No se pudo extraer el enlace de canto:", e)

    # Leer el archivo JSON si existe
    if os.path.exists('bird_data.json'):
        with open('bird_data.json', 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    # Añadir los nuevos datos al archivo
    existing_data.append(bird_data)

    # Guardar los datos en un archivo JSON (añadiendo, no sobrescribiendo)
    with open('bird_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    # Cerrar el navegador
    driver.quit()

    # Mensaje finalizado
    print("Proceso finalizado.")

# Ejecutar el scraping
scrape_with_selenium(cnn_url)
