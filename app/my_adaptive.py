import flet as ft


def main(page: ft.Page):
    page.adaptive = True
    page.add(ft.Text(value=page.route))
    
    def route_change(e: ft.RouteChangeEvent):
        page.add(ft.Text(value=f'New route{e.route}'))

    page.on_route_change = route_change
    page.update()

    page.appbar = ft.AppBar(
        leading=ft.Text(value="New"),
        title=ft.Text(value="Adaptive Appbar"),
        actions=[
            ft.TextButton(text='Home'),
            ft.OutlinedButton('About Us'),
            ft.IconButton(icon=ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.cupertino_colors.DARK_BACKGROUND_GRAY,
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Bookmark",
            ),
        ],
        border=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0),
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Checkbox(value=False, label="Dark Mode"),
                    ft.Text("First Field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Text(value="Second Field: "),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Switch(label="A Switch"),
                    ft.FilledButton(content=ft.Text("Adaptive Button")),
                    ft.FilledButton(text='Adaptive Button', icon=ft.icons.ACCESS_ALARM),
                    ft.Text(value="Text Line 1"),
                    ft.Text(value="Text Line 2"),
                    ft.Text(value="Text Line 3"),
                ],
                width=500
            )
        )
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
