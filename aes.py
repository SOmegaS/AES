"""Модуль"""

import hashlib
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES


def encrypt(data: bytes, password: str) -> bytes:
    # Создать ключа
    key = hashlib.sha256(password.encode()).digest()

    # Создать конфигурацию криптографа(шифровщика) по ключу
    cryptographer = AES.new(key, AES.MODE_GCM, nonce=key)

    # Зашифровать
    cipher = cryptographer.encrypt(data)
    return b64encode(cipher)


def decrypt(data: bytes, password: str) -> bytes:
    # Создать ключа
    key = hashlib.sha256(password.encode()).digest()

    # Создать конфигурацию криптографа(шифровщика) по ключу
    cryptographer = AES.new(key, AES.MODE_GCM, nonce=key)

    # Расшифровать
    decrypted = cryptographer.decrypt(b64decode(data))
    return decrypted


def encrypt_file(path: str, password: str):
    # Создать ключа
    key = hashlib.sha256(password.encode()).digest()

    # Создать конфигурацию криптографа(шифровщика) по ключу
    cryptographer = AES.new(key, AES.MODE_GCM, nonce=key)

    # Открыть файлы
    input_file = open(path, 'rb')
    output_file = open('encryption' + path[path.rfind('.'):], 'wb')
    # Работа с данными по чанкам
    chunk = input_file.read(512)
    while chunk != b'':
        # Шифрование
        cipher = cryptographer.encrypt(chunk)
        # Запись шифра
        output_file.write(b64encode(cipher))
        # Считывание чанка
        chunk = input_file.read(512)
    input_file.close()
    output_file.close()


def decrypt_file(path: str, password: str):
    # Создать ключа
    key = hashlib.sha256(password.encode()).digest()

    # Создать конфигурацию криптографа(шифровщика) по ключу
    cryptographer = AES.new(key, AES.MODE_GCM, nonce=key)

    # Открыть файлы
    input_file = open(path, 'rb')
    output_file = open('decryption' + path[path.rfind('.'):], 'wb')
    # Работа с данными по чанкам
    chunk = input_file.read(684)
    while chunk != b'':
        # Шифрование
        cipher = cryptographer.decrypt(b64decode(chunk))
        # Запись шифра
        output_file.write(cipher)
        # Считывание чанка
        chunk = input_file.read(684)
    input_file.close()
    output_file.close()


def main():
    """Главная функция"""
    while True:
        print('Шифровальщик файлов')
        mode = input('Выберите режим (e/d/ef/df): ')
        password = input('Введите пароль:\n')
        try:
            if mode == 'e':
                s = input('Введите шифруемую строку:\n')
                print(encrypt(s.encode(), password).decode())
            elif mode == 'd':
                s = input('Введите шифруемую строку:\n')
                print(decrypt(s.encode(), password).decode())
            elif mode == 'ef':
                path = input('Введите путь к файлу:\n')
                encrypt_file(path, password)
            elif mode == 'df':
                path = input('Введите путь к файлу:\n')
                decrypt_file(path, password)
            else:
                print('Введен некорректный режим')
        except FileNotFoundError:
            print('Введен некорректный путь')


if __name__ == '__main__':
    main()
