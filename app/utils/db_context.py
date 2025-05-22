import os
import sys

def recorrer_carpeta(ruta):
    archivos_info = []
    for root, dirs, files in os.walk(ruta):
        # Omitir carpetas que comiencen con "__" o "."
        dirs[:] = [d for d in dirs if not (d.startswith("__") or d.startswith("."))]
        # Omitir archivos que comiencen con "__" o "."
        files = [f for f in files if not (f.startswith("__") or f.startswith("."))]
        for archivo in files:
            ruta_archivo = os.path.join(root, archivo)
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
            except Exception as e:
                contenido = f"Error al leer el archivo: {e}"
            archivos_info.append((ruta_archivo, contenido))
    return archivos_info

def main():
    # Directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Ruta por defecto
    ruta_param = sys.argv[1] if len(sys.argv) > 1 else "../models/"
    ruta_completa = os.path.abspath(os.path.join(script_dir, ruta_param))
    
    if not os.path.isdir(ruta_completa):
        print("La ruta proporcionada no es un directorio válido.")
        sys.exit(1)
    
    datos_archivos = recorrer_carpeta(ruta_completa)
    
    # Archivo de salida por defecto en el mismo directorio del script
    archivo_salida = os.path.join(script_dir, "db_context.txt")
    with open(archivo_salida, "w", encoding="utf-8") as salida:
        for nombre_archivo, contenido in datos_archivos:
            salida.write(f"{nombre_archivo}:\n{contenido}\n\n")
    
    print(f"Archivo generado: {archivo_salida}")

if __name__ == "__main__":
    main()
