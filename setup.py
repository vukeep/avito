# setup.py
# Определяет метаданные пакета и зависимости для оптимальной установки
from setuptools import setup, find_packages

setup(
    name="avito_api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # Указываем минимальную версию для совместимости
    ],
    author="vukeep",
    author_email="vukeep@gmail.com",
    description="API клиент для работы с Avito API",
)