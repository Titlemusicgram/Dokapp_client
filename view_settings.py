import flet as ft
from style import wdw_width, wdw_height, chat_bg_clr


def set_view(page: ft.Page):
    page.title = 'DOK'
    page.theme_mode = "dark"
    page.bgcolor = chat_bg_clr

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    page.window_height = wdw_height
    page.window_width = wdw_width
    page.padding = 0
    page.spacing = 0
