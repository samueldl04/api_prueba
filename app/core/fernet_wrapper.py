from cryptography.fernet import Fernet

class FernetWrapper:
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.fernet.encrypt(data)

    def decrypt(self, token):
        decrypted = self.fernet.decrypt(token)
        return decrypted.decode('utf-8')

    def _update_key(self, key):
        # Actualiza la clave según lo requiere SQLAlchemy-Utils.
        self.fernet = Fernet(key)
