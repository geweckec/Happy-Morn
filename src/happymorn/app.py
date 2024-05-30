"""
My first application
"""

import toga
import httpx
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def greeting(name):
    if name:
        return "Here are your recipes!"
    else:
        return "No recipes can be created"

class HappyMorning(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Recipe Ingredient: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Make Recipes!",
            on_press=self.say_hello,
            style=Pack(padding=5),
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def say_hello(self, widget):
        with httpx.Client() as client:
            response= client.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={self.name_input}")

        meals = []
        js = json.loads(response.text)
        for meal in js["meals"]:
            meals.append(meal["strMeal"])

        self.main_window.info_dialog(greeting(self.name_input.value), meals,)


def main():
    return HappyMorning()
