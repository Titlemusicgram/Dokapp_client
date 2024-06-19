import flet as ft


class MyButton(ft.IconButton):
    def __init__(self, icon=None, on_click=None):
        super().__init__()
        self.icon = icon
        self.on_click = on_click
        self.icon_size = 18
        self.icon_color = ft.colors.WHITE60
        self.style = ft.ButtonStyle(
            shape={
                '': ft.RoundedRectangleBorder(radius=7)
            },
            # overlay_color={'': 'transparent'}
        )
