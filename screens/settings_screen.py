import flet as ft
from services.app_settings import AppSettings

class SettingsScreen(ft.View):
    def __init__(self, page: ft.Page, settings: AppSettings):
        super().__init__(
            route="/settings",
            scroll=ft.ScrollMode.AUTO,
            padding=20
        )
        self.page = page
        self.settings = settings
        self.build_ui()

    def build_ui(self):
        self.appbar = ft.AppBar(
            title=ft.Text(self.settings.get_string("settings")),
            bgcolor=ft.colors.SURFACE_VARIANT,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/"))
        )

        self.theme_switch = ft.Switch(
            label=self.settings.get_string("dark_mode"),
            value=self.page.theme_mode == ft.ThemeMode.DARK,
            on_change=self.toggle_theme
        )

        self.lang_dropdown = ft.Dropdown(
            label=self.settings.get_string("language"),
            value=self.settings.lang_code,
            options=[
                ft.dropdown.Option("ar", "العربية"),
                ft.dropdown.Option("en", "English"),
                ft.dropdown.Option("es", "Español"),
                ft.dropdown.Option("ru", "Русский"),
            ],
            on_change=self.change_language,
            border_radius=10
        )

        self.controls = [
            ft.ListTile(
                leading=ft.Icon(ft.icons.PALETTE),
                title=ft.Text(self.settings.get_string("dark_mode")),
                trailing=self.theme_switch
            ),
            ft.Container(padding=10, content=self.lang_dropdown),
            ft.Divider(),
            ft.Text(self.settings.get_string("mobile_compatibility"), size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Grid logic for cross-platform optimization enabled.", size=14, color=ft.colors.GREY_500),
            ft.Container(
                content=ft.Column([
                    ft.Text("System: Android/iOS/Desktop", size=12),
                    ft.Text("Framework: Flet (Python)", size=12),
                    ft.Text("Version: 1.0.0", size=12),
                ]),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_700),
                border_radius=5
            )
        ]

    def toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        self.settings.toggle_theme()
        self.page.update()

    def change_language(self, e):
        lang_code = e.control.value
        self.settings.set_language(lang_code)
        
        # Update RTL based on language
        self.page.rtl = True if lang_code == "ar" else False
        
        # Force refresh UI by re-building the current view
        self.build_ui()
        self.page.update()
