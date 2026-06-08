import flet as ft
from services.local_db import LocalDB
from services.app_settings import AppSettings

class AddPartScreen(ft.View):
    def __init__(self, page: ft.Page, db: LocalDB, settings: AppSettings):
        super().__init__(
            route="/add",
            scroll=ft.ScrollMode.AUTO,
            padding=20
        )
        self.page = page
        self.db = db
        self.settings = settings
        self.build_ui()

    def build_ui(self):
        self.appbar = ft.AppBar(
            title=ft.Text(self.settings.get_string("add_part")),
            bgcolor=ft.colors.SURFACE_VARIANT,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/"))
        )

        self.name_field = ft.TextField(label=self.settings.get_string("part_name"), border_radius=10)
        self.category_dropdown = ft.Dropdown(
            label=self.settings.get_string("category"),
            options=[
                ft.dropdown.Option("Power IC"),
                ft.dropdown.Option("Charging IC"),
                ft.dropdown.Option("SMD Capacitor"),
                ft.dropdown.Option("Diode"),
                ft.dropdown.Option("Resistor"),
                ft.dropdown.Option("FPC Connector"),
                ft.dropdown.Option("Display Part"),
            ],
            border_radius=10
        )
        self.quantity_field = ft.TextField(label=self.settings.get_string("quantity"), value="0", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
        self.price_field = ft.TextField(label=self.settings.get_string("price"), value="0.0", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
        self.description_field = ft.TextField(label=self.settings.get_string("description"), multiline=True, min_lines=3, border_radius=10)
        self.compatibility_field = ft.TextField(label=self.settings.get_string("mobile_compatibility"), hint_text="iPhone 13, Samsung S21...", border_radius=10)

        self.controls = [
            ft.Text(self.settings.get_string("micro_components"), size=20, weight=ft.FontWeight.BOLD),
            self.name_field,
            self.category_dropdown,
            ft.Row([self.quantity_field, self.price_field], spacing=10),
            self.description_field,
            self.compatibility_field,
            ft.Container(height=20),
            ft.ElevatedButton(
                self.settings.get_string("save"),
                icon=ft.icons.SAVE,
                on_click=self.save_part,
                width=float("inf"),
                style=ft.ButtonStyle(padding=20)
            )
        ]

    def save_part(self, e):
        if not self.name_field.value:
            self.name_field.error_text = "Required"
            self.page.update()
            return

        self.db.add_part(
            self.name_field.value,
            self.category_dropdown.value,
            int(self.quantity_field.value or 0),
            float(self.price_field.value or 0.0),
            self.description_field.value,
            self.compatibility_field.value
        )
        
        self.page.snack_bar = ft.SnackBar(ft.Text(self.settings.get_string("success_add")))
        self.page.snack_bar.open = True
        self.page.go("/")
