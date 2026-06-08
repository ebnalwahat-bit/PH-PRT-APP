import flet as ft
from services.local_db import LocalDB
from services.app_settings import AppSettings

class HomeScreen(ft.View):
    def __init__(self, page: ft.Page, db: LocalDB, settings: AppSettings):
        super().__init__(
            route="/",
            scroll=ft.ScrollMode.AUTO,
            padding=20
        )
        self.page = page
        self.db = db
        self.settings = settings
        self.build_ui()

    def build_ui(self):
        self.controls.clear()
        self.appbar = ft.AppBar(
            title=ft.Text(self.settings.get_string("app_title"), weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: self.page.go("/settings")),
            ]
        )

        self.search_field = ft.TextField(
            label=self.settings.get_string("search"),
            prefix_icon=ft.icons.SEARCH,
            on_change=self.on_search_change,
            border_radius=10
        )

        self.parts_list = ft.Column(spacing=10)
        self.load_parts()

        self.controls = [
            self.search_field,
            ft.Row([
                ft.ElevatedButton(
                    self.settings.get_string("add_part"),
                    icon=ft.icons.ADD,
                    on_click=lambda _: self.page.go("/add")
                ),
                ft.ElevatedButton(
                    self.settings.get_string("export_report"),
                    icon=ft.icons.FILE_DOWNLOAD,
                    on_click=self.export_report
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            self.parts_list
        ]

    def load_parts(self, query=None):
        self.parts_list.controls.clear()
        parts = self.db.get_all_parts(query)
        
        if not parts:
            self.parts_list.controls.append(
                ft.Container(
                    content=ft.Text(self.settings.get_string("no_data"), size=16),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        else:
            for part in parts:
                self.parts_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEMORY),
                                    title=ft.Text(part[1], weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"{part[2]} | {self.settings.get_string('quantity')}: {part[3]}"),
                                    trailing=ft.IconButton(
                                        ft.icons.EDIT,
                                        on_click=lambda _, p_id=part[0]: self.page.go(f"/edit/{p_id}")
                                    )
                                ),
                                ft.Text(f"{self.settings.get_string('price')}: {part[4]}", size=12),
                            ])
                        )
                    )
                )
        self.page.update()

    def on_search_change(self, e):
        self.load_parts(e.control.value)

    def export_report(self, e):
        parts = self.db.get_all_parts()
        report_content = "PH PRT APP - Inventory Report\n" + "="*30 + "\n"
        for part in parts:
            report_content += f"Name: {part[1]}\nCategory: {part[2]}\nQty: {part[3]}\nPrice: {part[4]}\n" + "-"*20 + "\n"
        
        # Simple alert to show content (in real app, would save to file)
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Report Exported (Mock)"),
            content=ft.Text("Data formatted for text export successfully."),
            actions=[ft.TextButton("OK", on_click=lambda _: setattr(self.page.dialog, 'open', False))]
        )
        self.page.dialog.open = True
        self.page.update()
