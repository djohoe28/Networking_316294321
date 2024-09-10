import time
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet


class Crypter:
    """
    Responsible for encrypting/decrypting data with :py:attr:`key`.

    :ivar key: The key :class:`bytes` used for encryption/decryption; Generated with :class:`Fernet` if not given.
    :ivar fernet: The underlying :class:`Fernet` instance used for encryption/decryption.
    """
    key: bytes
    fernet: Fernet

    def __init__(self, key: Optional[bytes] = None):
        """
        :class:`Crypter` Constructor.

        :param key: The :class:`bytes` key used for :class:`Fernet` encryption/decryption; Generate if none given.
        """
        self.key = key if key is not None else Fernet.generate_key()
        if key is None:
            # No key has been provided, therefore we need to log the generated key.
            path = f"{time.time()}.key"
            with open(path, "wb") as fp:
                fp.write(self.key)
            print(f"Key has been set to {self.key}; Exported to {path}.")
        self.fernet = Fernet(self.key)

    @classmethod
    def load(cls, path: Path):
        """
        Returns a new instance with a :class:`bytes` :py:attr:`key` loaded from the file at the given :class:`Path`.

        :param path: Path to key-file to read from.
        :return: The newly-constructed instance.
        """
        with open(path, "rb") as fp:
            return cls(key=fp.read())

    def save(self, path: Path):
        """
        Saves :py:attr:`key` to file in the given path. Overwrite if exists.

        :param path: :class:`Path` to save to.
        :return: None
        """
        with open(path, "wb") as fp:
            fp.write(self.key)

    def encrypt(self, data: bytes):
        """
        Encrypts the given data.

        :param data: Data to encrypt.
        :return: Encrypted data.
        """
        return self.fernet.encrypt(data)

    def decrypt(self, data: bytes | str):
        """
        Decrypts the given data.

        :param data: Data to decrypt.
        :return: Decrypted data.
        """
        return self.fernet.decrypt(data)

    def encrypt_to_file(self, data: bytes, path: Path):
        """
        Encrypts the given data and saves it to the given path.

        :param data: Data to save.
        :param path: Path to save to.
        :return: None
        """
        with open(path, "wb") as fp:
            fp.write(self.encrypt(data))

    def decrypt_from_file(self, path: Path):
        """
        Loads the data at the given path, and decrypts it.

        :param path: Path to load from.
        :return: Loaded data (decrypted).
        """
        with open(path, "rb") as fp:
            return self.decrypt(fp.read())
