import flet as ft
from typing import List
from yolo_obj_detection import organize
from cv_model import model_computation


class ChatMessage(ft.Row):
    def __init__(self, message: str):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                value=message,
                                weight="bold",
                                selectable=True,
                                overflow=ft.TextOverflow.VISIBLE,
                            )
                        ],
                        wrap=True,
                    ),
                    padding=10,
                ),
                color=ft.colors.SURFACE_VARIANT,
            )
        ]


class AnswerMessage(ft.Row):
    def __init__(self, ans: List[str]):
        super().__init__()
        self.ans = ans
        self.my_row = ft.Row()
        self.controls.append(
            ft.CircleAvatar(
                content=ft.Text(value="CV"),
            )
        )

        for a in ans:
            self.my_row.controls.append(ft.OutlinedButton(text=a))
            break
            # self.controls.append(
            #     ft.OutlinedButton(text=a)
            # )
        self.controls.append(self.my_row)


class IconThemeChange(ft.IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.icon = ft.Icons.LIGHT_MODE
            case ft.ThemeMode.DARK:
                self.icon = ft.Icons.DARK_MODE
            case _:
                self.icon = ft.Icons.CONTRAST
        self.on_click = self.__on_click

    def __on_click(self, e):
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
            case ft.ThemeMode.DARK:
                self.page.theme_mode = ft.ThemeMode.LIGHT
            case _:
                pass

        self.page.update()


class AppBarControl(ft.AppBar):
    def __init__(self):
        super().__init__()
        self.toggle_theme = ft.Ref[ft.IconButton]()
        # self.title = ft.Text("AppBar Example"),
        # self.title=ft.Text(value='Cving'),

        self.actions = [IconThemeChange()]

    def build(self):
        if self.page.route == "/vqa":
            self.title = ft.Text("Visual Question Answering")
            self.center_title = (True,)
        elif self.page.route == "/image_class":
            self.title = ft.Text("Image Organization")
            self.center_title = (True,)
        else:
            self.title = ft.Text("Cving")
            self.center_title = (True,)
