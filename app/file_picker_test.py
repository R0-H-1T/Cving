import flet as ft



def main(page: ft.Page):


    def file_picker_result(e: ft.FilePickerResultEvent):
        print(e.files)

    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    page.add(
        ft.ElevatedButton(
            text='Upload files', 
            on_click=lambda _: file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
        )

    )


ft.app(target=main)