import flet as ft
from app import RoutePages


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Cving"
    page.on_route_change = RoutePages(page).route_change
    page.on_view_pop = RoutePages(page).view_pop
    page.go(page.route)


if __name__ == "__main__":
    # NOTE
    # Run app from the current dir as -
    # flet run main.py
    ft.app(target=main)
