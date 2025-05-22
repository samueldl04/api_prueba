import json
import os
from pathlib import Path

_manifest = None

def get_manifest():
    """Carga el archivo de manifiesto webpack"""
    global _manifest
    if _manifest is None:
        manifest_path = Path(__file__).parent.parent / "static" / "dist" / "manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                _manifest = json.load(f)
        else:
            _manifest = {}
    return _manifest

def asset_path(path):
    """
    Devuelve la ruta hasheada de un asset desde el manifiesto.
    Si no se encuentra, devuelve la ruta original.
    """
    manifest = get_manifest()
    normalized_path = path.lstrip('/')
    hashed_path = manifest.get(normalized_path)
    
    if hashed_path:
        return hashed_path
    
    return f"/static/{normalized_path}"