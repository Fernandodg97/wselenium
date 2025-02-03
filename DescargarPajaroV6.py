import os
import requests
import mysql.connector
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
    bird_data_list_b = []
    bird_data_list_c = []
    
    for bird_name in bird_data_url:
        bird_url = f"https://www.rspb.org.uk/birds-and-wildlife/{bird_name.replace(' ', '-').lower()}"
        driver.get(bird_url)

        #---------------- Extraer los datos de todos los pajaros ------------------#

        # Extraer los datos del pájaro
        bird_data = {}
        bird_data_b = {}
        bird_data_c = []

        # Extraer y guardar el nombre del pájaro
        nombrePajaro = driver.find_element(By.TAG_NAME, 'h1').text
        nombreP = driver.find_elements(By.TAG_NAME, 'h1')
        if nombreP:
            bird_data['nombre'] = nombreP[0].text
        else:
            bird_data['nombre'] = "No se encontro nombre"
            print("No se encontro nombre")

        # Establece el nombre del parajaro como nombre de la imagen
        nombre_archivo_jpg = f"{nombrePajaro.replace(' ', '').replace("'", '').replace('-','').replace('/','')}.jpg"
        # Establece el nombre del parajaro como nombre del archivo de audio
        nombre_archivo_mp3 = f"{nombrePajaro.replace(' ', '').replace("'", '').replace('-','').replace('/','')}.mp3"

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

        # Inicializar la clave 'canto_url' con un valor predeterminado
        bird_data['canto_url'] = "audioNoExiste"

        # Extraer y guardar el enlace del canto del pájaro
        try:
            enlace = driver.find_element(By.CSS_SELECTOR, 'a[_ngcontent-rspb-frontend-app-c63]')
            canto_url = enlace.get_attribute('href')
            bird_data['canto_url'] = "/audio/" + nombre_archivo_mp3
            # Descargar el audio solo si no existe
            descargar_archivo(canto_url + "/download", nombre_archivo_mp3)
        except Exception as e:
            print("No se encontro archivo de canto")

        # Extraer y guardar el estado_conservacion del pájaro
        datos = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c286].value')
        if datos:
             # Solo asignar los valores si existen
            if len(datos) > 0:
                bird_data_b['estado_conservacion'] = datos[0].text if datos[0].text else None
            if len(datos) > 1:
                bird_data_b['dieta'] = datos[1].text if datos[1].text else None
            if len(datos) > 2:
                bird_data_b['poblacion_europea'] = datos[2].text if datos[2].text else None
            if len(datos) > 3:
                bird_data_b['pluma'] = datos[3].text if datos[3].text else None
            if len(datos) > 4:
                bird_data_b['longitud'] = datos[4].text if datos[4].text else None
            if len(datos) > 5:
                bird_data_b['peso'] = datos[5].text if datos[5].text else None
            if len(datos) > 6:
                bird_data_b['envergadura'] = datos[6].text if datos[6].text else None
            if len(datos) > 7:
                bird_data_b['habitats'] = datos[7].text if datos[7].text else None
        else:
            print("No se encontro datos")

        # Extraer y guardar lugares de observación del pájaro

        # Extraer los nombres
        nombreL = driver.find_elements(By.CSS_SELECTOR, 'span.custom-title')
        nombres = [nombre.text for nombre in nombreL] if nombreL else []

        # Extraer las ubicaciones
        ubicacionL = driver.find_elements(By.CSS_SELECTOR, 'span.custom-subtitle')
        ubicaciones = [ubicacion.text for ubicacion in ubicacionL] if ubicacionL else []

        # Iterar sobre los nombres y asignar ubicaciones
        for i, nombre in enumerate(nombres):
            if i < len(ubicaciones):
                ubicacion = ubicaciones[i]
            else:
                ubicacion = "ubicación desconocida"
            bird_data_c.append({
                'nombre': nombre,
                'ubicacion': ubicacion
            })
    
        brid_data_list.append(bird_data)
        bird_data_list_b.append(bird_data_b)
        bird_data_list_c.append(bird_data_c)

        

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

    cursor = conexion.cursor()

    # Consulta SQL Pajaro
    sql_pajaro = "INSERT INTO Pajaro (nombre, nombre_cientifico, grupo, imagen, como_identificar, canto_audio) VALUES (%s, %s, %s, %s, %s, %s)"

     # Consulta SQL Datos
    sql_datos = "INSERT INTO Datos (id_pajaro, estado_conservacion, dieta, poblacion_europea, pluma, longitud, peso, envergadura, habitats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Consulta SQL para Observacion
    sql_observacion = "INSERT INTO Lugares (nombre, ubicacion) VALUES (%s, %s)"
    sql_avistamientos = "INSERT INTO Avistamientos (id_pajaro, id_lugar) VALUES (%s, %s)"
    sql_obtener_lugar = "SELECT id_lugar FROM Lugares WHERE nombre = %s AND ubicacion = %s"

    # Insertar datos
    for bird_data, bird_data_b, bird_data_c in zip(brid_data_list, bird_data_list_b, bird_data_list_c):
        # Insertar en la tabla Pajaro
        cursor.execute(sql_pajaro, (
            bird_data['nombre'],
            bird_data['nombre_cientifico'],
            bird_data['grupo'],
            bird_data['foto_url'],
            bird_data['identificacion'],
            bird_data['canto_url']
        ))
        
        # Obtener el ID autogenerado
        id_pajaro = cursor.lastrowid

        # Insertar en la tabla Datos usando el ID del pájaro
        cursor.execute(sql_datos, (
            id_pajaro,
            bird_data_b['estado_conservacion'],
            bird_data_b['dieta'],
            bird_data_b['poblacion_europea'],
            bird_data_b['pluma'],
            bird_data_b['longitud'],
            bird_data_b['peso'],
            bird_data_b['envergadura'],
            bird_data_b['habitats']
        ))

        # Insertar en la tabla Observacion y Avistamientos
        for observacion in bird_data_c:
            # Verificar si el lugar ya existe
            cursor.execute(sql_obtener_lugar, (observacion['nombre'], observacion['ubicacion']))
            lugar = cursor.fetchone()

            if lugar:
                id_lugar = lugar[0]
            else:
                # Insertar nuevo lugar
                cursor.execute(sql_observacion, (
                    observacion['nombre'],
                    observacion['ubicacion']
                ))
                id_lugar = cursor.lastrowid
            
            # Insertar en Avistamientos
            # Comprobar si ya existe una entrada en la tabla Avistamientos
            cursor.execute("SELECT 1 FROM Avistamientos WHERE id_pajaro = %s AND id_lugar = %s", (id_pajaro, id_lugar))
            if cursor.fetchone() is None:
                # Si no existe, insertar en la tabla Avistamientos
                cursor.execute(sql_avistamientos, (id_pajaro, id_lugar))

        
    
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
