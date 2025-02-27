from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
import random
import call_chatgpt as chatgpt_script
import undetected_chromedriver as uc

# Constante para el número de bucles
BUCLES = 10

def fill_form():
    # Configurar el controlador del navegador (Chrome)
    driver = uc.Chrome()
    driver.get("http://localhost:3000/alta")  # Ajusta la URL

    # Función para esperar a que un elemento esté presente
    def wait_for_element(by, value, timeout=5):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"Elemento {value} no encontrado: {e}")
            return None

    # Función para llenar un campo de texto o textarea
    def fill_text_field(element_id, value):
        field = wait_for_element(By.ID, element_id)
        if field:
            try:
                if field.get_attribute("readonly"):
                    print(f"Campo {element_id} es readOnly, omitiendo llenado.")
                    return
                field.clear()
                field.send_keys(value)
                print(f"Campo {element_id} llenado con: {value}")
            except Exception as e:
                print(f"Error al llenar {element_id}: {e}")

    # Función para seleccionar una opción en un select y devolver su valor
    def select_option(element_id, value):
        field = wait_for_element(By.ID, element_id)
        if field:
            select = Select(field)
            select.select_by_value(value)
            print(f"Opción {value} seleccionada en {element_id}")
            return value
        return None

    # Función para llenar un campo de texto o textarea dentro de un div
    def fill_text_field_in_div(div, index, value):
        inputs = div.find_elements(By.TAG_NAME, "input")
        if len(inputs) > index:
            inputs[index].clear()
            inputs[index].send_keys(value)
            print(f"Input {index} en div llenado con: {value}")

    # Función para seleccionar una opción en un select dentro de un div
    def select_option_in_div(div, index, value):
        selects = div.find_elements(By.TAG_NAME, "select")
        if len(selects) > index:
            select = Select(selects[index])
            select.select_by_value(value)
            print(f"Select {index} en div seleccionado con: {value}")

    # Generar valores de ChatGPT
    def get_chatgpt_values():
        prompts = [
            "Genera un nombre de empresa aleatorio. Contéstame solo con el nombre.",
            "Genera un CIF simulado aleatorio. Contéstame solo con el CIF.",
            "Genera una dirección comercial aleatoria en España. Contéstame solo con la dirección.",
            "Genera un código postal de España. Contéstame solo con el código postal.",
            "Genera una ciudad de España. Contéstame solo con la ciudad.",
            "Genera una provincia de España. Contéstame solo con la provincia.",
            "Genera una referencia de producto. Tipo 2 letras 2 números. Contéstame solo con la referencia.",
            "Genera una descripción corta de producto. Tipo FontBella 2L. Contéstame solo con la descripción.",
            "Genera una referencia de producto. Tipo 2 letras 2 números. Contéstame solo con la referencia.",
            "Genera una descripción corta de producto. Tipo FontBella 2L. Contéstame solo con la descripción.",
            "Genera una observación corta para la factura. Por ejemplo 'Viene roto'. Contéstame solo con las observaciones.",
        ]
        responses = []
        for prompt in prompts:
            response = chatgpt_script.get_chatgpt_response(prompt)
            responses.append(response if response else "Valor por defecto")
        return responses

    # Bucle de 10 iteraciones
    for iteration in range(BUCLES):
        print(f"\n=== Iteración {iteration + 1} de {BUCLES} ===")

        # Obtener valores de ChatGPT para esta iteración
        chatgpt_responses = get_chatgpt_values()
        fecha_hoy = date.today().strftime("%Y-%m-%d")  # Formato YYYY-MM-DD

        # Definir los datos para esta iteración
        data = {
            "numeroFactura": f"24/000/{random.randint(100000, 999999):06d}",
            "claveOperacion": random.choice(["03", "04", "05", "06", "07", "09", "10", "11", "19", "S2"]),
            "fechaEmision": fecha_hoy,
            "fechaOperacion": fecha_hoy,
            "tipoFactura": random.choice(["F1", "F2", "R1"]),
            "emisorNombre": "NEOD TECNOLOGIAS DE LA INFORMACION S.L.",
            "emisorNif": "B93013886",
            "emisorDireccion": "Avenida Ortega y Gasset 124",
            "emisorCP": "29006",
            "emisorCiudad": "Malaga",
            "emisorPais": "España",
            "receptorNombre": "LARA  NAZARET",
            "receptorNif": "54594394F",
            "receptorDireccion": chatgpt_responses[2],
            "receptorCP": chatgpt_responses[3],
            "receptorCiudad": chatgpt_responses[4],
            "receptorProvincia": chatgpt_responses[5],
            "receptorPais": "España",
            "tipoRectificativa": random.choice(["I", "S"]),
            "numeroFacturaRectificativa": f"24/000/{random.randint(100000, 999999):06d}",
            "fechaEmisionRectificativa": fecha_hoy,
            "motivo-rectificacion": random.choice(["01-Número de la factura", "02-Serie de la factura", "03-Fecha de expedición", "04-Nombre y apellidos/Razón social Emisor", "05-Nombre y apellidos/Razón social Receptor", "06-Identificación fiscal Emisor", "07-Identificación fiscla Receptor", "08-Domicilio emisor", "09-Domicilio receptor", "10-Detalle operación", "11-Porcentaje impositivo a aplicar", "12-Cuota tributaria a aplicar", "13-Fecha/Periodo a aplicar", "14-Clase de factura", "15-Literales legales", "16-Base imponible", "80-Cálculo de cuotas repercutidas", "81-Cálculo de cuotas retenidas", "82-Base imponible modificada por devolución de envases/embalajes", "83-Base imponible modificada por descuentos y bonificaciones", "84-Base imponible modificada por resolución firme, judicial o administrativa", "85-Base imponible modificada cuotas repercutidas no satisfechas. Auto de declaración de concurso."]),
    "motivo-correccion": random.choice(['01-Rectificación modelo íntegro', '02-Rectificación modelo por diferencias', '03-Rectificación por descuento por volumen de operaciones durante un período', '04-Autorizadas por la Agencia Tributaria']),
            "lineas": [
                {
                    "referencia": chatgpt_responses[6],
                    "descripcion": chatgpt_responses[7],
                    "cantidad": str(random.randint(1, 10)),
                    "precio": str(round(random.uniform(10, 500), 2)),
                    "impuesto": random.choice(["2", "4", "7.5", "10", "21"]),
                },
                {
                    "referencia": chatgpt_responses[8],
                    "descripcion": chatgpt_responses[9],
                    "cantidad": str(random.randint(1, 10)),
                    "precio": str(round(random.uniform(10, 500), 2)),
                    "impuesto": random.choice(["2", "4", "7.5", "10", "21"]),
                },
            ],
            "observaciones": chatgpt_responses[10],
        }

        print(data)

        # Llenar formulario BasicDataForm
        fill_text_field("numeroFactura", data["numeroFactura"])
        tipo_factura = select_option("tipoFactura", data["tipoFactura"])
        fill_text_field("fechaEmision", data["fechaEmision"])
        fill_text_field("fechaOperacion", data["fechaOperacion"])

        # Llenar formulario EmisorForm
        fill_text_field("emisorNombre", data["emisorNombre"])
        fill_text_field("emisorNif", data["emisorNif"])
        fill_text_field("emisorDireccion", data["emisorDireccion"])
        fill_text_field("emisorCP", data["emisorCP"])
        fill_text_field("emisorCiudad", data["emisorCiudad"])
        fill_text_field("emisorPais", data["emisorPais"])

        # Llenar formulario ReceptorForm si aplica
        if tipo_factura not in ["F2", "R5"]:
            receptor_element = wait_for_element(By.ID, "receptorNombre")
            if receptor_element and receptor_element.is_displayed():
                fill_text_field("receptorNombre", data["receptorNombre"])
                fill_text_field("receptorNif", data["receptorNif"])
                fill_text_field("receptorDireccion", data["receptorDireccion"])
                fill_text_field("receptorCP", data["receptorCP"])
                fill_text_field("receptorCiudad", data["receptorCiudad"])
                fill_text_field("receptorProvincia", data["receptorProvincia"])
                select_option("receptorPais", data["receptorPais"])

        # Llenar formulario RectificativaForm si aplica
        if "R" in tipo_factura:
            rectificativa_element = wait_for_element(By.ID, "tipoRectificativa")
            if rectificativa_element:
                select_option("tipoRectificativa", data["tipoRectificativa"])
                fill_text_field("numeroFacturaRectificativa", data["numeroFacturaRectificativa"])
                fill_text_field("fechaEmisionRectificativa", data["fechaEmisionRectificativa"])
                select_option("motivo-rectificacion", data["motivo-rectificacion"])
                select_option("motivo-correccion", data["motivo-correccion"])

        # Añadir y llenar líneas en DetalleProductosForm
        items_div = wait_for_element(By.ID, "items")
        if items_div:
            for i, linea_data in enumerate(data["lineas"]):
                boton_agregar_linea = wait_for_element(By.ID, "agregarLinea")
                if boton_agregar_linea:
                    boton_agregar_linea.click()
                    print(f"Botón 'Añadir línea' clicado para línea {i}")
                    linea_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[@id='items']/div[{i+1}]"))
                    )
                    fill_text_field_in_div(linea_div, 0, linea_data["referencia"])
                    fill_text_field_in_div(linea_div, 1, linea_data["descripcion"])
                    fill_text_field_in_div(linea_div, 2, linea_data["cantidad"])
                    fill_text_field_in_div(linea_div, 3, linea_data["precio"])
                    select_option_in_div(linea_div, 0, linea_data["impuesto"])

        # Llenar formulario Observaciones
        fill_text_field("observaciones", data["observaciones"])

        # Hacer clic en "Grabar"
        boton_grabar = wait_for_element(By.ID, "generar-factura")
        if boton_grabar:
            boton_grabar.click()
            print("Botón 'Grabar' clicado")

        time.sleep(5)  # Pausa breve para confirmar la acción antes de cerrar esta iteración

    # Cerrar el navegador al final de todas las iteraciones
    driver.quit()

if __name__ == "__main__":
    fill_form()