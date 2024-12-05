import flet as ft


class ChatMessage(ft.Row):
    def __init__(self, message: str):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(value='Y'),
            ),
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