import flet as ft
from style import (chat_text_clr, hint_text_clr, chat_bg_clr, fields_bg_color, chat_text_size,
                   writing_message_height, shdw)
from MyButton import MyButton
from PIL import Image

list_of_selected_control_images = []
list_of_images_to_send = []


async def main_page(page, temp_folder, session=None):
    # Progress ring
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    # Функции, выполняемые на главной странице
    async def send_text_to_server(json_text_to_send):
        # Пока что GET-запрос для проверки
        async with session.post('/', json=json_text_to_send) as resp:
            print(resp.status)
            json_content = await resp.json()
            print(json_content)

    async def send_photo_to_server(file):
        with open(file, 'rb') as f:
            async with session.post('/post_photo', data={"file": f}) as resp:
                print(resp.status)
                print(await resp.text())

    async def upload_files():
        if file_picker.result is not None and file_picker.result.files is not None:
            pr.visible = True
            page.update()
            global list_of_images_to_send
            local_list_of_control_photo_to_send = []
            for file in list_of_images_to_send:

                # Здесь отправляем фото на сервер, если подключение существует
                if session is not None:
                    # Вызываем функцию отправки фотографии на сервер
                    await send_photo_to_server(file)

                local_list_of_control_photo_to_send.append(ft.Image(src=file, width=112,
                                                                    border_radius=10, fit=ft.ImageFit.SCALE_DOWN))
            row_of_photos = ft.Row(controls=local_list_of_control_photo_to_send, wrap=True, spacing=5)
            container_with_photos = ft.Container(
                content=row_of_photos,
                expand=True,
                expand_loose=True,
                padding=ft.padding.only(top=5, bottom=5, left=20, right=20),
                bgcolor=fields_bg_color,
                border_radius=15)
            if (len(file_picker.result.files)) != 0:
                chat.controls.append(ft.Row(
                    controls=[container_with_photos],
                    expand=True,
                    expand_loose=True
                ))
                pr.visible = False
                page.update()
            list_of_images_to_send = []
            file_picker.result.files = []

    async def pick_photos(e):
        file_picker.pick_files(allow_multiple=True, allowed_extensions=['jpg', 'JPG', 'jpeg', 'JPEG'])

    async def send_message_click(e):
        if write_message_field.value != '':
            text = ft.Text(f"{write_message_field.value}", color=chat_text_clr, size=chat_text_size)

            # Здесь отправляем текст на сервер, если подключение существует
            if session is not None:
                json_text_to_send = {"text": f"{write_message_field.value}"}
                # Вызываем функцию отправки текста на сервер
                await send_text_to_server(json_text_to_send)

            text_row = ft.Container(
                content=text,
                expand=True,
                expand_loose=True,
                padding=ft.padding.only(top=5, bottom=5, left=20, right=20),
                bgcolor=fields_bg_color,
                border_radius=15
            )
            chat.controls.append(ft.Row(
                controls=[text_row],
                expand=True,
                expand_loose=True,
                )
            )
            write_message_field.value = ""
            page.update()
        await upload_files()
        upload_photo_container.visible = False
        page.update()

    async def dismiss_selected_photos(e):
        global list_of_images_to_send
        file_picker.result.files = []
        list_of_images_to_send = []
        upload_photo_container.visible = False
        page.update()

    dismiss_icon = MyButton(icon=ft.icons.CLOSE, on_click=dismiss_selected_photos)

    async def pick_files_result(e: ft.FilePickerResultEvent):
        global list_of_selected_control_images
        global list_of_images_to_send
        list_of_selected_control_images = []
        list_of_images_to_send = []
        if e is not None and e.files is not None:
            for f in e.files:
                small_photo_path = f'{temp_folder}/{f.name}'
                with Image.open(f.path) as im:
                    if 'exif' in im.info.keys():
                        exif = im.info['exif']
                        im = im.resize((1600, 1200))
                        im.save(small_photo_path, exif=exif)
                    else:
                        im = im.resize((1600, 1200))
                        im.save(small_photo_path)
                list_of_images_to_send.append(small_photo_path)
                photo = ft.Image(src=small_photo_path, fit=ft.ImageFit.SCALE_DOWN, border_radius=10)
                list_of_selected_control_images.append(photo)
            selected_photos = ft.Row(
                controls=list_of_selected_control_images,
                height=100,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=False,
                vertical_alignment=ft.alignment.center,
                alignment=ft.alignment.center,
                spacing=5
            )
            upload_photo_container.content = ft.Column(
                controls=[ft.Container(dismiss_icon, alignment=ft.Alignment(1, 0)),
                          ft.Container(selected_photos, alignment=ft.Alignment(0, 0))],
                height=140,
                expand=False,
                horizontal_alignment=ft.alignment.center,
                alignment=ft.alignment.center,
                spacing=5
            )
            upload_photo_container.visible = True
        page.update()

    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.extend([file_picker])

    # Задаем элементы, отображаемые на экране

    send_button = MyButton(icon=ft.icons.SEND, on_click=send_message_click)
    upload_photo_button = MyButton(icon=ft.icons.PHOTO, on_click=pick_photos)

    write_message_field = ft.TextField(
        hint_text="Message...",
        hint_style=ft.TextStyle(color=hint_text_clr),
        text_size=14,
        height=writing_message_height-20,
        shift_enter=True,
        min_lines=1,
        max_lines=4,
        filled=True,
        bgcolor=fields_bg_color,
        expand=True,
        opacity=1,
        focused_border_color=ft.colors.WHITE30,
        focused_border_width=1,
        focused_bgcolor=ft.colors.BLACK54,
        content_padding=ft.padding.only(top=1, bottom=1, left=15, right=15),
        border_radius=20,
        autofocus=False,
        on_submit=send_message_click
    )

    upload_photo_container = ft.Container(
        alignment=ft.Alignment(0, 0),
        bgcolor=fields_bg_color,
        height=160,
        expand=False,
        shadow=shdw,
        opacity=1,
        visible=False
    )

    chat = ft.ListView([
    ],
        spacing=10,
        padding=20,
        expand=True,
        expand_loose=True,
        auto_scroll=True
        )

    divider = ft.Divider(height=5, color='transparent')

    writing_message_row = ft.Row([upload_photo_button, write_message_field, send_button])

    # Задаем зоны, в которых размещены элементы
    chat_zone = ft.Container(content=chat,
                             expand=True,
                             expand_loose=True,
                             alignment=ft.alignment.center,
                             on_click=page.update(),
                             bgcolor=chat_bg_clr)

    writing_message_zone = ft.Container(content=writing_message_row,
                                        bgcolor=chat_bg_clr,
                                        height=writing_message_height,
                                        padding=ft.padding.only(left=10, right=10))

    progress_ring_zone = ft.Container(pr, alignment=ft.alignment.center)

    page.add(ft.SafeArea(content=chat_zone, expand=True, expand_loose=True))
    page.add(ft.SafeArea(content=ft.Column([progress_ring_zone,
                                            upload_photo_container,
                                            divider,
                                            writing_message_zone],
                                           spacing=0)))
