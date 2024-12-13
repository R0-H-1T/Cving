import flet as ft
from typing import List


class ChatMessage(ft.Row):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def build(self):
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls.append(
            # ft.CircleAvatar(
            #     content=ft.Text(value='Y'),
            # ),
            # ft.Column(
            #     controls=[
            #         ft.Text(value=message, weight="bold", selectable=True)
            #     ]
            # ),
            ft.Card(
                expand=True,
                expand_loose=True,
                content=ft.Text(
                    value=self.message,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER,
            ),
            variant=ft.CardVariant.FILLED,
        )


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


from typing import Optional

from flet import (
    CircleAvatar,
    Column,
    Container,
    CrossAxisAlignment,
    MainAxisAlignment,
    Row,
    Text,
    TextOverflow,
    border_radius,
    colors,
    padding,
)


class Message:
    def __init__(
        self,
        author: Optional[str] = None,
        body: Optional[str] = None,
    ):
        self.author = author if author is not None else "You"
        self.author_initial = "".join(
            map(lambda x: x[0].title(), self.author.split(maxsplit=2))
        )
        self.body = body.strip() if isinstance(body, str) else body
        self.accent = self.__random()

    def __random(self):
        # TODO
        # Implement for ft.Colors that ends with `_ACCENT`
        # import random

        # return random.choice(
        #     filter(lambda color: color.name.endswith("_ACCENT"), ft.Colors.)
        # )
        return ft.Colors.BLUE_ACCENT

    def avatar(self):
        """
        Return avatar's background color
        """
        return self.accent


class MessageControl(Row):
    """
    Formatted messages
    """

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

    def build(self):
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True
        self.expand_loose = True
        self.controls = [
            CircleAvatar(
                content=Text(
                    value=self.message.author_initial,
                ),
                bgcolor=self.message.accent,
                tooltip=self.message.author,
            ),
            Column(
                controls=[
                    Text(
                        value=self.message.author,
                        weight="bold",
                    ),
                    Container(
                        content=Text(
                            value=self.message.body,
                            no_wrap=False,
                            max_lines=4,
                            overflow=TextOverflow.FADE,
                        ),
                        border=None,
                        border_radius=border_radius.only(
                            top_left=0,
                            top_right=25,
                            bottom_left=25,
                            bottom_right=25,
                        ),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        padding=padding.symmetric(8, 12),
                        expand=True,
                        expand_loose=True,
                    ),
                ],
                spacing=4,
                alignment=MainAxisAlignment.START,
                expand=True,
                expand_loose=True,
            ),
        ]


class ImageControl(Row):
    """
    Formatted images
    """

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

    def build(self):
        self.alignment = MainAxisAlignment.END
        self.vertical_alignment = CrossAxisAlignment.END
        self.expand = True
        self.expand_loose = True
        self.controls = [
            CircleAvatar(
                content=Text(
                    value=self.message.author_initial,
                ),
                bgcolor=self.message.accent,
                tooltip=self.message.author,
            ),
            Column(
                controls=[
                    Text(
                        value=self.message.author,
                        weight="bold",
                    ),
                    Container(
                        content=ft.Image(
                            src=self.message.body,
                            width=256,
                            height=256,
                            fit=ft.ImageFit.SCALE_DOWN,
                        ),
                        border=None,
                        border_radius=border_radius.only(
                            top_right=0,
                            bottom_right=25,
                            bottom_left=25,
                            top_left=25,
                        ),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        padding=padding.symmetric(8, 12),
                        expand=True,
                        expand_loose=True,
                    ),
                ],
                spacing=4,
                alignment=MainAxisAlignment.END,
                expand=True,
                expand_loose=True,
            ),
        ]
