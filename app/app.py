import flet as ft
from controls import ImgOrg, VQApp, AppBarControl


class RoutePages(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def route_change(self, e: ft.RouteChangeEvent):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                appbar=AppBarControl(),
                # TODO
                # create enums for the path routes.
                route="/",
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Visual QnA", on_click=lambda _: self.page.go("/vqa")
                            ),
                            ft.ElevatedButton(
                                "Photo Organization",
                                on_click=lambda _: self.page.go("/image_class"),
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            )
        )
        if self.page.route == "/vqa":
            self.page.views.append(
                ft.View(
                    appbar=AppBarControl(),
                    route="/vqa",
                    controls=[VQApp()],
                )
            )
        if self.page.route == "/image_class":
            self.page.views.append(
                ft.View(
                    appbar=AppBarControl(),
                    route="/image_class",
                    controls=[ImgOrg()],
                )
            )
        self.page.update()

    def view_pop(self, e: ft.ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def build(self):
        self.expand = True
        self.bgcolor = ft.Colors.AMBER_100
