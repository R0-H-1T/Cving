import flet as ft
from controls import ChatMessage, AnswerMessage

# from dotenv import load_dotenv
import base64
from cv_model import model_computation

# load_dotenv()


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_img = None
        self.app = app
        self.page = page
        self.pick_files_dialogue = ft.FilePicker(
            on_result=self.file_picker_result, on_upload=self.show_file_upload_progress
        )
        self.page.overlay.append(self.pick_files_dialogue)
        self.chat_window = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing=10,
            padding=ft.padding.only(left=250, right=250),
        )
        self.new_message = ft.TextField(
            # prefix=self.attach_file_button,
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

        self.page.add(
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
        )

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        # @TODO some control to display the uploaded files
        self.attach_file_button.visible = True if e.files is None else False
        self.save_file_button.visible = True if e.files is not None else False
        # self.attach_file_button.icon = ft.icons.SAVE
        self.page.update()

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
            self.page.update()
            ans = model_computation(img=self.current_img, question=query)
            self.chat_window.controls.append(AnswerMessage(ans))
            self.page.update()

    def show_file_upload_progress(self, e: ft.FilePickerUploadEvent):
        # self.chat_window.controls.append(ft.Text(value=e.progress))
        self.page.update()
        if e.progress == 1:
            self.show_image(e.file_name)
        self.page.update()

    def show_image(self, mf: str = None):
        # @TODO refactor code
        # no need to create a file object, pass path to Image control directly
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
        self.page.update()

    def upload_file(self, e):
        print("Welcome to file upload function")
        if (
            self.pick_files_dialogue.result is not None
            and self.pick_files_dialogue.result.files is not None
        ):

            mf = self.pick_files_dialogue.result.files[0]
            self.current_img = mf.path
            self.show_image()

            # filepicker_upload = ft.FilePickerUploadFile(name=mf.name, upload_url=self.page.get_upload_url(mf.name, 600))
            # self.pick_files_dialogue.upload([filepicker_upload])

            self.save_file_button.visible = False
            self.attach_file_button.visible = True

            self.page.update()


class CvingApp(AppLayout):
    def __init__(self, page: ft.Page):
        self.page = page
        self.toggle_theme = ft.Ref[ft.IconButton]()
        self.page.appbar = ft.AppBar(
            # leading=ft.Icon(name=ft.icons.CAMERA, size=30),
            leading_width=30,
            title=ft.Text(value="CVing"),
            center_title=True,
            elevation=10,
            actions=[
                ft.IconButton(
                    icon=ft.icons.LIGHT_MODE,
                    ref=self.toggle_theme,
                    on_click=self.__change_theme,
                )
            ],
            # bgcolor=ft.colors.BLUE_400
        )
        self.page.update()
        super().__init__(self, self.page)

    def __change_theme(self, e: ft.ControlEvent):
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
                self.toggle_theme = ft.icons.DARK_MODE
            case ft.ThemeMode.DARK:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                self.toggle_theme = ft.icons.LIGHT_MODE
            case ft.ThemeMode.SYSTEM:
                self.toggle_theme = ft.icons.CONTRAST
                pass
                # self.page.theme_mode = ft.ThemeMode.SYSTEM

        self.page.update()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "CVing"
    app = CvingApp(page)
    page.add(app)
    page.update()


if __name__ == "__main__":
    ft.app(target=main, upload_dir="assets/uploads")
