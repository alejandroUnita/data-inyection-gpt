# executor.py
import alta_neodsif_data_inyection

def ejecutar_script_veces(veces=10):
    for i in range(veces):
        print(f"\nEjecución {i+1} de {veces}")
        try:
            alta_neodsif_data_inyection.fill_form()
            print(f"Ejecución {i+1} completada con éxito")
        except Exception as e:
            print(f"Error en ejecución {i+1}: {e}")

def main():
    # Ejecutar el script 10 veces sin interacción
    ejecutar_script_veces()

    print("\n=== Ejecución Finalizada ===")
    print("Se ejecutó el script 10 veces.")

if __name__ == "__main__":
    main()