#Crea un json por pajaro

import mysql.connector
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL de la página a scrapear
cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/a-z"

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

    #---------------- Extraer los nombres de todos los pajaros ----------------#

    # Mensaje 
    print("////// --- Parte 1: Inicio --- //////")

    # Extraer los nombres de los pájaros
    bird_data_url = []

    # Bucle para hacer scraping mientras haya un botón "Next"
    while True:
        # Extraer todos los <span> con la clase 'text-link-underline text-link-underline--deepsea'
        span_elements = driver.find_elements(By.CSS_SELECTOR, 'span.text-link-underline.text-link-underline--deepsea')

        # Iterar sobre los elementos encontrados y obtener el texto
        for span in span_elements:
            # Convertir a minúsculas, reemplazar espacios y eliminar apóstrofes
            bird_name = span.text.lower().replace(' ', '-').replace("'", '').replace("/", '-')  
            bird_data_url.append(bird_name)

        # Intentar encontrar el botón "Next" con espera explícita
        try:
            # Esperar hasta que el botón "Next" sea visible
            next_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.next.button'))
            )
            next_button.click()  # Hacer clic en el botón "Next"
            print("////// --- Clic en el botón 'Next' --- //////")

            # Esperar para que se cargue la siguiente página
            time.sleep(3)
        except Exception as e:
            print("No se encontró el botón 'Next'")
            break  # Terminar el bucle si no se encuentra el botón "Next"
    
    # Mensaje 
    print("////// --- Parte 1: Completa --- //////")

    #---------------- Dirigirse a la url ------------------#

    # Mensaje 
    print("////// --- Parte 2: Inicio --- //////")

    brid_data_list = []
    
    for bird_name in bird_data_url:
        bird_url = f"{"https://www.rspb.org.uk/birds-and-wildlife"}/{bird_name.replace(' ', '-').lower()}"
        driver.get(bird_url)

        #---------------- Extraer los datos de todos los pajaros ------------------#

        # Extraer los datos del pájaro
        bird_data = {}

        # Extraer y guardar el nombre del pájaro
        nombrePajaro = driver.find_element(By.TAG_NAME, 'h1').text
        nombreP = driver.find_elements(By.TAG_NAME, 'h1')
        if nombreP:
            bird_data['nombre'] = nombreP[0].text
        else:
            bird_data['nombre'] = "No se encontro nombre"
            print("No se encontro nombre")

        # Establece el nombre del parajaro como nombre de la imagen
        nombre_archivo_jpg = f"{nombrePajaro.replace(' ', '').replace("'", '').replace('-','')}.jpg"
        # Establece el nombre del parajaro como nombre del archivo de audio
        nombre_archivo_mp3 = f"{nombrePajaro.replace(' ', '').replace("'", '').replace('-','')}.mp3"

        # Extraer y guardar el nombre científico del pájaro
        nombreC = driver.find_elements(By.CSS_SELECTOR, 'span.info.latin')
        if nombreC:
            bird_data['nombre_cientifico'] = nombreC[0].text
        else:
            bird_data['nombre_cientifico'] = "No se encontro nombre cientifico"
            print("No se encontro nombre cientifico")

        # Extraer y guardar el grupo del pájaro
        grupoP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].info')
        if grupoP:
            grupo_texto = grupoP[1].text
            # Dividir el texto por ":", tomar la segunda parte y eliminar los espacios extra
            if ":" in grupo_texto:
                bird_data['grupo'] = grupo_texto.split(":")[1].strip()
            else:
                bird_data['grupo'] = "Grupo no disponible"
                print("Grupo no disponible")
        else:
            print("Grupo no disponible")

        # Extraer y guardar la foto del pájaro
        fotoP = driver.find_elements(By.CSS_SELECTOR, 'img[_ngcontent-rspb-frontend-app-c201]')
        if fotoP:
            foto_url = fotoP[0].get_attribute('src')
            bird_data['foto_url'] = "/images/" + nombre_archivo_jpg
            # Descargar la foto solo si no existe
            descargar_archivo(foto_url, nombre_archivo_jpg)
        else:
            print("No se encontro archivo imagen")
        

        # Extraer y guardar la identificación del pájaro
        ideP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].intro')
        if ideP:
            bird_data['identificacion'] = ideP[0].text.replace('-','').replace('–','')
        else:
            bird_data['identificacion'] = "No se encontro identificacion"
            print("No se encontro identificacion")

        # Extraer y guardar el enlace del canto del pájaro
        try:
            enlace = driver.find_element(By.CSS_SELECTOR, 'a[_ngcontent-rspb-frontend-app-c63]')
            canto_url = enlace.get_attribute('href')
            bird_data['canto_url'] = "/audio/" + nombre_archivo_mp3
            # Descargar el audio solo si no existe
            descargar_archivo(canto_url + "/download", nombre_archivo_mp3)
        except Exception as e:
            print("No se encontro archivo de canto")
    
        brid_data_list.append(bird_data)

    # ////// Guardado ////////

    # Conexion con la base de datos
        try: 
            conexion = mysql.connector.connect(
            host="localhost",
            user="usuario",
            password="usuario",
            database="wikiagapornis")
            if conexion.is_connected():
                print("Conexión exitosa con la base de datos")
        except Exception as e:
            print("Error al conectar con la base de datos:", e)
            return

        print(conexion)
        
        cursor = conexion.cursor()

        # Consulta SQL
        sql = "INSERT INTO Pajaro (nombre, nombre_cientifico, grupo, imagen, como_identificar, canto_audio) VALUES (%s, %s, %s, %s, %s, %s)"

        # Insertar datos
        for bird_data in brid_data_list:
            cursor.execute(sql, (bird_data['nombre'], bird_data['nombre_cientifico'], bird_data['grupo'], bird_data['foto_url'], bird_data['identificacion'], bird_data['canto_url']))
        
        # Guardar cambios
        conexion.commit()
        conexion.close()

        # Mensaje 
        print("////// --- Parte 2: Completa --- //////")

        # Cerrar el navegador
        driver.quit()

        # Mensaje finalizado
        print("////// --- Proceso finalizado. --- //////")

    # Ejecutar el scraping
    scrape_with_selenium(cnn_url)
