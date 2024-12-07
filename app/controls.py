import flet as ft
from typing import List


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
