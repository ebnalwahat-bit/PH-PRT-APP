import flet as ft
from services.local_db import LocalDB
from services.app_settings import AppSettings
from screens.home_screen import HomeScreen
from screens.add_part_screen import AddPartScreen
from screens.edit_part_screen import EditPartScreen
from screens.settings_screen import SettingsScreen

def main(page: ft.Page):
    # Initialize services
    db = LocalDB()
    settings = AppSettings()

    # App Configuration
    page.title = settings.get_string("app_title")
    page.theme_mode = ft.ThemeMode.DARK
    
    # RTL Support for Arabic
    if settings.lang_code == "ar":
        page.rtl = True
    
    page.window_width = 400
    page.window_height = 800

    def route_change(route):
        page.views.clear()
        
        # Route logic
        if page.route == "/":
            page.views.append(HomeScreen(page, db, settings))
        elif page.route == "/add":
            page.views.append(AddPartScreen(page, db, settings))
        elif page.route.startswith("/edit/"):
            part_id = int(page.route.split("/")[-1])
            page.views.append(EditPartScreen(page, db, settings, part_id))
        elif page.route == "/settings":
            page.views.append(SettingsScreen(page, settings))
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initial navigation
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
