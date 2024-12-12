import flet as ft
from typing import List
from yolo_obj_detection import organize


class ChatMessage(ft.Row):
    def __init__(self, message: str):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            # ft.CircleAvatar(
            #     content=ft.Text(value='Y'),
            # ),
            # ft.Column(
            #     controls=[
            #         ft.Text(value=message, weight="bold", selectable=True)
            #     ]
            # ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(value=message, weight="bold", selectable=True, overflow=ft.TextOverflow.VISIBLE)
                        ],
                        wrap=True
                    ),
                    padding=10
                ),
                color=ft.colors.SURFACE_VARIANT
            )
        ]




class AnswerMessage(ft.Row):
    def __init__(self, ans: List[str]):
        super().__init__()
        self.ans = ans
        self.my_row = ft.Row()
        self.controls.append(
            ft.CircleAvatar(
                content=ft.Text(value='CV'),
            )
        )

        for a in ans:
            self.my_row.controls.append(
                ft.OutlinedButton(text=a)
            )
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
        
        self.actions=[
            IconThemeChange()
        ]

    def build(self):
        if self.page.route == '/vqa':
            self.title=ft.Text("Visual Question Answering")
            self.center_title=True,
        elif self.page.route == '/image_class':
            self.title=ft.Text('Image Organization')
            self.center_title=True,
        else:
            self.title=ft.Text('Cving')
            self.center_title=True,




class ImgOrg(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_picker = ft.FilePicker(on_result=self.dir_picker_event)
        self.alert_dialogue = ft.AlertDialog()
        self.button_dir_path = ft.Button(
            text='Select directory',
            on_click=lambda _:self.dir_picker.get_directory_path()
        )
        self.dir_path = ft.Text(visible=False)
        self.organize_button = ft.Button(
            text='Organize Photos',
            visible=False,
            on_click=self.organize_photos
        )
        self.cancel_button = ft.OutlinedButton(
            text='Cancel',
            visible=False,
            on_click=self.handle_cancel_event
        )
        self.img_listview = ft.ListView(
            expand=1,
            spacing=10,
        )
        self.row_img = ft.Row(wrap=True)
        self.controls = [   
            self.button_dir_path,
            self.dir_path,
            ft.Row(controls=[self.organize_button, self.cancel_button]),
            self.row_img
        ]

    def build(self):
        self.page.overlay.append(self.dir_picker)
        self.expand = True

    def dir_picker_event(self, e: ft.FilePickerResultEvent):
        self.dir_path.value = e.path if e.path else 'Cancelled'

        self.cancel_button.visible = True
        self.button_dir_path.visible = False
        self.organize_button.visible = True
        self.dir_path.visible = True
        import os
        files = [file for file in os.listdir(e.path) if file.endswith(('png', 'jpeg', 'jpg'))]
        for file in files:
            print(f'{e.path}/{file}')
            self.row_img.controls.append(
                ft.Image(
                    src=f'{e.path}/{file}',
                    height=200,
                    width=200
                )
            )
            self.row_img.update()
        self.update()

    def handle_cancel_event(self, e):
        self.dir_path.visible = False,
        self.cancel_button.visible = False,
        self.organize_button.visible = False
        self.organize_button.visible = True
        self.row_img.clean()
        self.update()

    def organize_photos(self, e):
        try:
            organize(self.dir_path.value)
            self.alert_dialogue.title = ft.Text(value='Successfully organized!')
            self.page.open(self.alert_dialogue)
        except Exception:
            self.alert_dialogue.title = ft.Text(value='Something went wrong.')