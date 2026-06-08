import flet as ft
from services.local_db import LocalDB
from services.app_settings import AppSettings

class EditPartScreen(ft.View):
    def __init__(self, page: ft.Page, db: LocalDB, settings: AppSettings, part_id: int):
        super().__init__(
            route=f"/edit/{part_id}",
            scroll=ft.ScrollMode.AUTO,
            padding=20
        )
        self.page = page
        self.db = db
        self.settings = settings
        self.part_id = part_id
        self.part_data = self.db.get_part_by_id(part_id)
        self.build_ui()

    def build_ui(self):
        if not self.part_data:
            self.controls = [ft.Text("Error: Part not found")]
            return

        self.appbar = ft.AppBar(
            title=ft.Text(self.settings.get_string("edit_part")),
            bgcolor=ft.colors.SURFACE_VARIANT,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/"))
        )

        self.name_field = ft.TextField(label=self.settings.get_string("part_name"), value=self.part_data[1], border_radius=10)
        self.category_dropdown = ft.Dropdown(
            label=self.settings.get_string("category"),
            value=self.part_data[2],
            options=[
                ft.dropdown.Option("Power IC"),
                ft.dropdown.Option("Charging IC"),
                ft.dropdown.Option("SMD Capacitor"),
                ft.dropdown.Option("Diode"),
                ft.dropdown.Option("Resistor"),
                ft.dropdown.Option("FPC Connector"),
            ],
            border_radius=10
        )
        self.quantity_field = ft.TextField(label=self.settings.get_string("quantity"), value=str(self.part_data[3]), keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
        self.price_field = ft.TextField(label=self.settings.get_string("price"), value=str(self.part_data[4]), keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
        self.description_field = ft.TextField(label=self.settings.get_string("description"), value=self.part_data[5], multiline=True, min_lines=3, border_radius=10)
        self.compatibility_field = ft.TextField(label=self.settings.get_string("mobile_compatibility"), value=self.part_data[6], border_radius=10)

        self.controls = [
            self.name_field,
            self.category_dropdown,
            ft.Row([self.quantity_field, self.price_field], spacing=10),
            self.description_field,
            self.compatibility_field,
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    self.settings.get_string("update"),
                    icon=ft.icons.UPDATE,
                    on_click=self.update_part,
                    expand=True
                ),
                ft.ElevatedButton(
                    self.settings.get_string("delete"),
                    icon=ft.icons.DELETE,
                    bgcolor=ft.colors.RED_700,
                    color=ft.colors.WHITE,
                    on_click=self.delete_part,
                    expand=True
                ),
            ], spacing=10)
        ]

    def update_part(self, e):
        self.db.update_part(
            self.part_id,
            self.name_field.value,
            self.category_dropdown.value,
            int(self.quantity_field.value or 0),
            float(self.price_field.value or 0.0),
            self.description_field.value,
            self.compatibility_field.value
        )
        self.page.snack_bar = ft.SnackBar(ft.Text(self.settings.get_string("success_update")))
        self.page.snack_bar.open = True
        self.page.go("/")

    def delete_part(self, e):
        def confirm_delete(ev):
            self.db.delete_part(self.part_id)
            self.page.dialog.open = False
            self.page.snack_bar = ft.SnackBar(ft.Text(self.settings.get_string("success_delete")))
            self.page.snack_bar.open = True
            self.page.go("/")

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(self.settings.get_string("confirm_delete")),
            actions=[
                ft.TextButton(self.settings.get_string("delete"), on_click=confirm_delete),
                ft.TextButton(self.settings.get_string("cancel"), on_click=lambda _: setattr(self.page.dialog, 'open', False)),
            ]
        )
        self.page.dialog.open = True
        self.page.update()
