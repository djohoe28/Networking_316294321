from typing import Optional

from cryptography.fernet import Fernet


class Crypter:
    """
    Responsible for encrypting/decrypting strings using a :class:`Fernet` :class:`bytes` key.

    :ivar bytes key: The key :class:`bytes` used for encryption/decryption; Generated with :class:`Fernet` if not given.
    :ivar Fernet fernet: The underlying :class:`Fernet` instance used for encryption/decryption.
    """
    key: bytes
    fernet: Fernet

    def __init__(self, key: Optional[bytes] = None):
        """
        Constructs a new :class:`Crypter` instance using the given key, or generates a new key if none given.

        :param bytes key: The key used for :class:`Fernet` encryption/decryption; Generate one if none given.
        """
        self.key = key if key is not None else Fernet.generate_key()
        self.fernet = Fernet(self.key)

    @classmethod
    def load(cls, path: str):
        """
        Returns a new instance loaded from the file at the given path.

        :param path: Path to key-file to read from.
        :return: The newly-constructed instance.
        """
        with open(path, "rb") as fp:
            return cls(key=fp.read())

    def save(self, path: str):
        """
        Saves :py:attr:`key` as a file to the given path. Overwrites if exists.

        :param path: Path to save to.
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

    def encrypt_to_file(self, data: bytes, path: str):
        """
        Encrypts the given data and saves it to the given path.

        :param data: Data to save.
        :param path: Path to save to.
        :return: None
        """
        with open(path, "wb") as fp:
            fp.write(self.encrypt(data))

    def decrypt_from_file(self, path: str):
        """
        Loads the data at the given path, and decrypts it.

        :param path: Path to load from.
        :return: Loaded data (decrypted).
        """
        with open(path, "rb") as fp:
            return self.decrypt(fp.read())
