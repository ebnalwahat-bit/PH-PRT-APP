import json
import os

class AppSettings:
    def __init__(self):
        self.lang_code = "ar"
        self.theme_mode = "dark"
        self.translations = {}
        self.load_translations()

    def set_language(self, code):
        self.lang_code = code
        self.load_translations()

    def load_translations(self):
        # Try different possible paths for the lang files
        possible_paths = [
            f"assets/lang/{self.lang_code}.json",
            os.path.join(os.path.dirname(__file__), "..", "assets", "lang", f"{self.lang_code}.json"),
            os.path.join("PH PRT APP", "assets", "lang", f"{self.lang_code}.json")
        ]
        
        success = False
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.translations = json.load(f)
                        success = True
                        break
                except Exception as e:
                    print(f"Error reading {path}: {e}")
        
        if not success:
            print(f"Warning: Could not load translations for {self.lang_code}")
            # Fallback to empty or basic dict if needed
            self.translations = self.translations if self.translations else {}

    def get_string(self, key):
        return self.translations.get(key, key)

    def toggle_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        return self.theme_mode
