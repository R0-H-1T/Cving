import flet as ft
from cv_model import model_computation
from .controls import ChatMessage, AnswerMessage


class VQApp(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_img = None
        self.pick_files_dialogue = ft.FilePicker(
            on_result=self.file_picker_result, on_upload=self.show_file_upload_progress
        )

        self.chat_window = ft.ListView(
            expand=9,
            auto_scroll=True,
            spacing=10,
            padding=ft.padding.only(left=250, right=250),
        )
        self.new_message = ft.TextField(
            hint_text="enter message...",
            autofocus=True,
            filled=True,
            expand=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            on_submit=self.send_msg,
        )

        self.attach_file_button = ft.IconButton(
            expand=True,
            icon=ft.icons.ATTACH_FILE,
            on_click=lambda _: self.pick_files_dialogue.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.IMAGE,
                allowed_extensions=["jpeg", "jpg", "png"],
            ),
            visible=True,
        )

        self.save_file_button = ft.IconButton(
            expand=True, icon=ft.icons.SAVE, visible=False, on_click=self.upload_file
        )

        self.controls = [
            ft.Container(content=self.chat_window, padding=10, expand=True),
            ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Card(
                                width=70,
                                height=70,
                                content=ft.Row(
                                    controls=[
                                        self.attach_file_button,
                                        self.save_file_button,
                                    ]
                                ),
                                shape=ft.RoundedRectangleBorder.radius,
                            ),
                            self.new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND,
                                tooltip="send message",
                                on_click=self.send_msg,
                            ),
                        ]
                    )
                ],
            ),
        ]

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        # TODO some control to display the uploaded files
        self.attach_file_button.visible = True if e.files is None else False
        self.save_file_button.visible = True if e.files is not None else False
        # self.attach_file_button.icon = ft.icons.SAVE
        self.update()

    def send_msg(self, e):
        if self.new_message.value:
            query = self.new_message.value
            self.chat_window.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[ChatMessage(message=self.new_message.value)],
                )
            )
            self.new_message.value = ""
            self.update()
            ans = model_computation(img=self.current_img, question=query)
            self.chat_window.controls.append(AnswerMessage(ans))
            self.update()

    def build(self):
        self.expand = True
        self.alignment = ft.MainAxisAlignment.END
        self.page.overlay.append(self.pick_files_dialogue)

    def show_file_upload_progress(self, e: ft.FilePickerUploadEvent):
        self.update()
        if e.progress == 1:
            self.show_image(e.file_name)
        self.update()

    def show_image(self, mf: str = None):
        print(self.current_img)
        self.chat_window.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.Image(
                        src=self.current_img,
                        width=450,
                        height=350,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=ft.border_radius.all(10),
                    )
                ],
            ),
        )
        self.update()

    def upload_file(self, e):
        if (
            self.pick_files_dialogue.result is not None
            and self.pick_files_dialogue.result.files is not None
        ):

            mf = self.pick_files_dialogue.result.files[0]
            self.current_img = mf.path
            self.show_image()

            self.save_file_button.visible = False
            self.attach_file_button.visible = True

            self.update()
