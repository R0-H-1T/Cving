import flet as ft
from .controls import ChatMessage, AnswerMessage, Message, MessageControl, ImageControl
from .cv_model import model_computation
from contextvars import ContextVar


class AppThemeToggle(ft.IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("child 0")

    def did_mount(self):
        print("child 2")

    def __on_click(self, e: ft.ControlEvent):
        print("child click()")
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
            case ft.ThemeMode.DARK:
                self.page.theme_mode = ft.ThemeMode.LIGHT
            case _:
                pass
        print(self.page.theme_mode)
        # NOTE
        # Since we changed the Page's attributes
        # We need to call update() on the Page
        # This is not an isloated control
        # So, self (our custom control)
        # will be included in the update() digest
        self.page.update()

    def build(self):
        print("child 1")
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.icon = ft.Icons.LIGHT_MODE
            case ft.ThemeMode.DARK:
                self.icon = ft.Icons.DARK_MODE
            case _:
                self.icon = ft.Icons.CONTRAST
        self.on_click = self.__on_click

    def before_update(self):
        # NOTE
        # We won't call
        # update() either on the Page, or
        # the self
        match self.page.theme_mode:
            case ft.ThemeMode.LIGHT:
                self.icon = ft.Icons.LIGHT_MODE
            case ft.ThemeMode.DARK:
                self.icon = ft.Icons.DARK_MODE
            case _:
                self.icon = ft.Icons.CONTRAST


class MainApplication:
    def __init__(self):
        print("bound 0")
        self.appbar = ft.Ref[ft.AppBar]()
        self.filepicker = ft.Ref[ft.FilePicker]()
        self.fab = ft.Ref[ft.FloatingActionButton]()
        self.textfield = ft.Ref[ft.TextField]()
        self.listview = ft.Ref[ft.ListView]()
        self.dialog = ft.Ref[ft.AlertDialog]()

    def __filepicker_on_result(self, e: ft.FilePickerResultEvent):
        # TODO
        # If an image is picker
        # it'll remain in context
        # until file picker is opened again
        # 2 things may happen post that,
        # 2.1 picker was closed without selection, we lose the old context (the prior image)
        # 2.2 new image was selected, we're good
        try:
            self.listview.current.controls.append(
                ImageControl(
                    message=Message(body=self.filepicker.current.result.files[0].path)
                )
            )
        except (IndexError, TypeError):
            # If dialog was closed without any selection
            # .pop() would remove it off the list
            # and we can't reuse it through the ref
            pass
        else:
            self.page.update()

    def __fab_on_click(self, e: ft.ControlEvent):
        self.filepicker.current.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )

    def __textfield_suffix_on_click(self, e: ft.ControlEvent):
        if self.textfield.current.value and self.filepicker.current.result.files:
            self.listview.current.controls.append(
                MessageControl(message=Message(body=self.textfield.current.value))
            )
            print("DEUBG:", self.filepicker.current.result.files)
            model_computation(
                # FIXME
                # Files is getting delicate
                # Indexing may throw
                path=self.filepicker.current.result.files[0].path,  # noqa
                query=self.textfield.current.value,
                app_context=self.page,
                error_callback=lambda: self.page.open(
                    ft.AlertDialog(
                        ref=self.dialog, title=ft.Text("Something went Wrong!")
                    )
                ),
                success_callback=lambda: (
                    self.listview.current.controls.append(
                        MessageControl(message=Message(body=body))
                    )
                    if (body := self.page.data.get("answer"))
                    else None
                ),
                extra_callback=lambda val: self.page.data.update(dict(answer=val)),
            )
            # updates
            self.textfield.current.value = None
            self.page.update()

    def __call__(self, page: ft.Page):
        print("bound 1")
        print("bound page", page)
        self.page = page
        self.page.data = dict()
        self.page.title = "CVing"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.appbar = ft.AppBar(
            ref=self.appbar,
            actions=[AppThemeToggle()],
            title=ft.Text(value=self.page.title),
            center_title=True,
        )
        self.page.overlay.append(
            ft.FilePicker(ref=self.filepicker, on_result=self.__filepicker_on_result)
        )
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     ref=self.fab,
        #     icon=ft.Icons.ATTACH_FILE,
        #     on_click=self.__fab_on_click,
        # )
        # TODO
        # refactor the dialog
        # and the callable(s)
        # need more, success, error, side_effect
        self.page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.ListView(ref=self.listview, expand=9),
                    ft.TextField(
                        ref=self.textfield,
                        expand=1,
                        multiline=True,
                        suffix=ft.IconButton(
                            icon=ft.Icons.SEND,
                            on_click=self.__textfield_suffix_on_click,
                        ),
                        filled=True,
                        hint_text="Select image and ask",
                        autofocus=True,
                        prefix=ft.IconButton(
                            ref=self.fab,
                            icon=ft.Icons.ATTACH_FILE,
                            on_click=self.__fab_on_click,
                        ),
                    ),
                ],
            )
        )
        self.page.update()
