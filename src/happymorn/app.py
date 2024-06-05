"""
My first application
"""

import toga
import httpx
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading

def donetiming(name):
    if name:
        return "Bzzzzzz!"
    else:
        return "No time entered"

class CountdownApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=(0,5)))
        self.timey = toga.Label('00:00', style=Pack(padding=10))
        timer_purpose = toga.Label("Timer Name: ", style=Pack(padding=10))
        minute_label = toga.Label("Enter time in minutes: ", style=Pack(padding=10))
        second_label = toga.Label("Enter time in seconds: ", style=Pack(padding=10))
        self.minute_input = toga.TextInput(style=Pack(flex=1))
        self.second_input = toga.TextInput(style=Pack(flex=1))
        self.purpose_input = toga.TextInput(style=Pack(flex=1))
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(timer_purpose)
        name_box.add(self.purpose_input)
        name_box.add(minute_label)
        name_box.add(self.minute_input)
        name_box.add(second_label)
        name_box.add(self.second_input)

        instant = Questions
        gobackbutton = toga.Button("Go Back",on_press=instant.startup,style=Pack(padding=5),)

        self.start_button = toga.Button('Start', on_press=self.start_timer, style=Pack(padding=10))
        self.stop_button = toga.Button('Stop', on_press=self.stop_timer, style=Pack(padding=10))

        main_box.add(name_box)
        main_box.add(self.timey)
        main_box.add(self.start_button)
        main_box.add(self.stop_button)
        main_box.add(gobackbutton)

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = main_box
        self.main_window.show()

        self.timer = None
        self.time_remaining = 0

    def start_timer(self, widget):
        if self.minute_input.value:
            minute_value = int(self.minute_input.value)
        else:
            minute_value = 0
        if self.second_input.value:
            second_value = int(self.second_input.value)
        else:
            second_value = 0
        self.time_remaining = 60*minute_value + second_value  # Set initial time here (in seconds)
        self.update_timey()
        self.timer = threading.Timer(1, self.update_timer)
        self.timer.start()

    def stop_timer(self, widget):
        if self.timer:
            self.timer.cancel()

    def update_timer(self):
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.done,style=Pack(padding=5)
        else:
            self.time_remaining -= 1
#            if self.time_remaining <= 0:
#                self.time_remaining = 0
#                self.done,style=Pack(padding=5)
            self.update_timey()
            if self.time_remaining > 0:
                self.timer = threading.Timer(1, self.update_timer)
                self.timer.start()

    def update_timey(self):
        minutes = int(self.time_remaining) // 60
        seconds = int(self.time_remaining) % 60
        if self.purpose_input.value:
            purpose = self.purpose_input.value
        else:
            purpose = 'Timer'
        if minutes <= 0 and seconds <= 0:
            #self.main_window.info_dialog("Bzzzt!", "Time's Up!",)
            self.timey.text = "Bzzt! Time's up!"
        else:
            self.timey.text = f'{purpose}: {minutes:02}:{seconds:02}'
        
#    def done(self, widget):
#        self.main_window.info_dialog("Bzzzt!", "Time's Up!",)
    def done(self, widget):
        self.main_window.info_dialog("Bzzzt!", "Time's Up!",)

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
        
        instant = Questions
        gobackbutton = toga.Button("Go Back",on_press=instant.startup,style=Pack(padding=5),)

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
        main_box.add(gobackbutton)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def say_hello(self, widget):
        with httpx.Client() as client:
            response= client.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={self.name_input.value}")

        payload = response.json()
        if payload["meals"]:
            meals = []
            for i in range(0,len(payload["meals"])):
                meals.append(payload["meals"][i]["strMeal"])
            stringy = ("\n".join(meals))
            self.main_window.info_dialog(greeting(self.name_input.value), stringy,)
        else:
            self.main_window.info_dialog(greeting(self.name_input.value), "No recipes available",)


class Questions(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        name_label = toga.Label("What do you want to do?", style=Pack(padding=(0, 5)),)
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        
        button = toga.Button("Start a Timer", on_press=lambda widget: mainy(CountdownApp), style=Pack(padding=5),)
        button1 = toga.Button("Plan Breakfast", on_press=lambda widget: mainy(HappyMorning), style=Pack(padding=5),)


        
        main_box.add(name_box)
        main_box.add(button)
        main_box.add(button1)
        
        self.main_window = toga.MainWindow(title="Good Morning!")
        self.main_window.content = main_box
        self.main_window.show()
    
        def mainy(app):
            return app()
        

def main():
    return Questions()
#if __name__ == '__main__':
    #main().main_loop()
