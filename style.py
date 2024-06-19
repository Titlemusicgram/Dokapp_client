import flet as ft

wdw_width = 450
wdw_height = 800
writing_message_height = 70
chat_height = wdw_height - writing_message_height

chat_text_clr = ft.colors.WHITE60
hint_text_clr = ft.colors.WHITE30
chat_text_size = 16
chat_bg_clr = ft.colors.BLACK
fields_bg_color = ft.colors.WHITE12

# gradient = ft.RadialGradient(
#     center=ft.Alignment(2, -5),
#     radius=4,
#     colors=[ft.colors.GREY, ft.colors.BLACK]
# )

shdw = ft.BoxShadow(
        spread_radius=1,
        blur_radius=15,
        color=ft.colors.BLUE_GREY_300,
        offset=ft.Offset(0, 0),
        blur_style=ft.ShadowBlurStyle.OUTER,
    )
