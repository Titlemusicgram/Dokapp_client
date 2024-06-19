# Импорт
import flet as ft
from view_settings import set_view
from main_page import main_page
from web_connection import set_the_connection
import os


# Основная программа
async def main(page: ft.Page):

    # Если нет папки dokapp_temp, то создаем ее, чтобы класть туда обработанные временные фотографии для отправки
    temp_folder = os.path.dirname(os.path.abspath(__file__)) + "/dokapp_temp"
    if not os.path.isdir(temp_folder):
        os.mkdir(temp_folder)

    # Задаем общие настройки GUI
    set_view(page)

    # Вызываем функцию для создания соединения с сервером
    session = await set_the_connection()

    # Запускаем код главной страницы приложения
    await main_page(page, temp_folder, session)


# Запуск основной программы
if __name__ == '__main__':
    ft.app(target=main)
