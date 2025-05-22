import os
import shutil
import sys

def clean_pycache(start_dir="."):
    """
    Elimina todas las carpetas __pycache__ y archivos .pyc recursivamente
    comenzando desde el directorio especificado.
    """
    count_dirs = 0
    count_files = 0
    
    print(f"Buscando archivos y carpetas para limpiar desde: {os.path.abspath(start_dir)}")
    
    # Recorrer el árbol de directorios
    for root, dirs, files in os.walk(start_dir):
        # Eliminar carpetas __pycache__
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print(f"Eliminando carpeta: {pycache_path}")
            shutil.rmtree(pycache_path)
            count_dirs += 1
            # Importante: evitar que os.walk entre en la carpeta que acabamos de eliminar
            dirs.remove("__pycache__")
        
        # Eliminar archivos .pyc
        for file in files:
            if file.endswith(".pyc") or ".cpython-" in file and file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                print(f"Eliminando archivo: {file_path}")
                os.remove(file_path)
                count_files += 1
    
    print(f"\n¡Limpieza completada!")
    print(f"Carpetas __pycache__ eliminadas: {count_dirs}")
    print(f"Archivos .pyc eliminados: {count_files}")

if __name__ == "__main__":
    # Si se proporciona un directorio como argumento, usarlo como punto de inicio
    start_directory = sys.argv[1] if len(sys.argv) > 1 else "."
    clean_pycache(start_directory)