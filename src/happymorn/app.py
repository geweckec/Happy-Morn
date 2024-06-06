"""
My first application
"""

import toga
import httpx
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading


class CountdownApp(toga.App):
    '''This class controls the countdown timer feature of the app'''
    def startup(self):
        '''this method sets up the screen for the timer and allows user to enter the time they want'''
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=(0,5))) #sets up main screen
        self.timey = toga.Label('00:00', style=Pack(padding=10)) #sets intial time to zero in a label
        timer_purpose = toga.Label("Timer Name: ", style=Pack(padding=10))
        minute_label = toga.Label("Enter time in minutes: ", style=Pack(padding=10))
        second_label = toga.Label("Enter time in seconds: ", style=Pack(padding=10))
        #make three labels for the user to enter what the timer is for, minutes, and seconds
        self.minute_input = toga.TextInput(style=Pack(flex=1))
        self.second_input = toga.TextInput(style=Pack(flex=1))
        self.purpose_input = toga.TextInput(style=Pack(flex=1))
        # allows user to input the above information
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(timer_purpose)
        name_box.add(self.purpose_input)
        name_box.add(minute_label)
        name_box.add(self.minute_input)
        name_box.add(second_label)
        name_box.add(self.second_input)
        # adds these boxes to screen
        instant = Questions
        gobackbutton = toga.Button("Go Back",on_press=instant.startup,style=Pack(padding=5),)
        # go back button
        self.start_button = toga.Button('Start', on_press=self.start_timer, style=Pack(padding=10))
        self.stop_button = toga.Button('Stop', on_press=self.stop_timer, style=Pack(padding=10))
        # when start is selected, it calls the start timer function and when stop is selected it calls the stop timer function
        main_box.add(name_box)
        main_box.add(self.timey)
        main_box.add(self.start_button)
        main_box.add(self.stop_button)
        main_box.add(gobackbutton)
        # adds to main screen
        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = main_box
        self.main_window.show()

        self.timer = None
        self.time_remaining = 0

    def start_timer(self, widget):
        '''This method starts the timer'''
        if self.minute_input.value:
            minute_value = int(self.minute_input.value) #sets minute value
        else:
            minute_value = 0
        if self.second_input.value:
            second_value = int(self.second_input.value) # sets second value
        else:
            second_value = 0
        self.time_remaining = 60*minute_value + second_value #initializes the amount of time
        self.update_timey()
        self.timer = threading.Timer(1, self.update_timer)
        self.timer.start()

    def stop_timer(self, widget):
        '''this method stops timer'''
        if self.timer:
            self.timer.cancel() #cancels timer

    def update_timer(self):
        '''this method updates the timer after each second'''
        if self.time_remaining <= 0:
            self.time_remaining = 0
            #if timer gets to zero, calls the done function to print time's up
        else:
            self.time_remaining -= 1
            self.update_timey()
            if self.time_remaining > 0:
                self.timer = threading.Timer(1, self.update_timer)
                self.timer.start() #otherwise updates timer and continues countdown

    def update_timey(self):
        '''this method updates visual timer'''
        minutes = int(self.time_remaining) // 60
        seconds = int(self.time_remaining) % 60
        if self.purpose_input.value:
            purpose = self.purpose_input.value
        else:
            purpose = 'Timer'
        if minutes <= 0 and seconds <= 0:
            self.timey.text = "Bzzt! Time's up!" #if seconds reaches zero, clock will be replaced with the time's up message
        else:
            self.timey.text = f'{purpose}: {minutes:02}:{seconds:02}' #updates visual clock
        

def greeting(name):
    '''displays the following messages on the screen when recipes are generated''' # these messages will be displayed in a pop up screen that is called later
    if name:
        return "Here are your recipes!"
    else:
        return "No recipes can be created"
def greeting2(name):
    '''displays the following messages on the screen when outfit colors are generated'''
    if name:
        return "Here are the colors for your outfit!"
    else:
        return "No colors can be generated"

class HappyMorning(toga.App):
    '''This class generates recipes for the user'''
    def startup(self):
        '''This method sets up the screen for the recipe portion of the app and allows user to enter an ingredient'''
        main_box = toga.Box(style=Pack(direction=COLUMN)) #sets up main screen

        name_label = toga.Label(
            "Recipe Ingredient: ",
            style=Pack(padding=(0, 5)),
        ) # prompt for user to answer
        self.name_input = toga.TextInput(style=Pack(flex=1)) #allows user to input an answer in the name_label box created above
        
        instant = Questions
        gobackbutton = toga.Button("Go Back",on_press=instant.startup,style=Pack(padding=5),) # creates a go back button so the user can return to home screen

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)
        # creates a box for the user to input on the main screen and then adds the prompt and the user answer

        button = toga.Button(
            "Make Recipes!",
            on_press=self.say_hello,
            style=Pack(padding=5),
        ) #when the user selects this putton, it will run the say hello function which find recipes

        main_box.add(name_box)
        main_box.add(button)
        main_box.add(gobackbutton)
        # adds all the buttons and input box + prompt to the main screen

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        # the above code worked very similarly to the startup code above and then displayed all those features in the main screen

    def say_hello(self, widget):
        '''this method uses an API to get recipes related to the inputted ingredient and then displays those recipes'''
        with httpx.Client() as client:
            response= client.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={self.name_input.value}") #gets API

        payload = response.json() # loads data from API
        if payload["meals"]:
            meals = []
            for i in range(0,len(payload["meals"])):
                meals.append(payload["meals"][i]["strMeal"])
            stringy = ("\n".join(meals)) #extracts recipe names from API
            self.main_window.info_dialog(greeting(self.name_input.value), stringy,) #calls greeting function above and underneath the text from the greeting function will print the list of recipes
        else:
            self.main_window.info_dialog(greeting(self.name_input.value), "No recipes available",)


class Questions(toga.App):
    '''This class makes the home screen part of the app'''
    def startup(self):
        '''This method sets up the screen of the home page with three puttons allowing the user to select what class they want to run'''
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        name_label = toga.Label("What do you want to do?", style=Pack(padding=(0, 5)),) #creates a box asking the user what they want to do
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        
        button = toga.Button("Start a Timer", on_press=lambda widget: mainy(CountdownApp), style=Pack(padding=5),)
        button1 = toga.Button("Plan Breakfast", on_press=lambda widget: mainy(HappyMorning), style=Pack(padding=5),)
        button2 = toga.Button("Outfit Color Generator", on_press=lambda widget: mainy(OutfitColors), style=Pack(padding=5),)
        #creates three buttons and when the user selects them, it runs the mainy function

        
        main_box.add(name_box)
        main_box.add(button)
        main_box.add(button1)
        main_box.add(button2)
        # adds all these buttons and text to the main screen
        
        self.main_window = toga.MainWindow(title="Good Morning!") #title for the main screen
        self.main_window.content = main_box
        self.main_window.show()
    
        def mainy(app):
            '''returns the app the user selects they want to run'''
            return app() #when this function is called that specific feature is run
        
class OutfitColors(toga.App):
    '''This class controls the outfit color feature of our app'''
    def startup(self):
        '''This method sets up the screen for the outfit color feature and allows user to input the main color of their outfit'''
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Main Color of your Outfit: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))
        
        instant = Questions
        gobackbutton = toga.Button("Go Back",on_press=instant.startup,style=Pack(padding=5),)

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Generate Outfit Colors!",
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
        '''This method uses an API that connects color name to hex code, and then returns complementary colors'''
        color = self.name_input.value
        color_hex_codes = {
            "aliceblue": "F0F8FF",
            "antiquewhite": "FAEBD7",
            "aqua": "00FFFF",
            "aquamarine": "7FFFD4",
            "azure": "F0FFFF",
            "beige": "F5F5DC",
            "bisque": "FFE4C4",
            "black": "000000",
            "blanchedalmond": "FFEBCD",
            "blue": "0000FF",
            "blueviolet": "8A2BE2",
            "brown": "A52A2A",
            "burlywood": "DEB887",
            "cadetblue": "5F9EA0",
            "chartreuse": "7FFF00",
            "chocolate": "D2691E",
            "coral": "FF7F50",
            "cornflowerblue": "6495ED",
            "cornsilk": "FFF8DC",
            "crimson": "DC143C",
            "cyan": "00FFFF",
            "darkblue": "00008B",
            "darkcyan": "008B8B",
            "darkgoldenrod": "B8860B",
            "darkgray": "A9A9A9",
            "darkgreen": "006400",
            "darkkhaki": "BDB76B",
            "darkmagenta": "8B008B",
            "darkolivegreen": "556B2F",
            "darkorange": "FF8C00",
            "darkorchid": "9932CC",
            "darkred": "8B0000",
            "darksalmon": "E9967A",
            "darkseagreen": "8FBC8F",
            "darkslateblue": "483D8B",
            "darkslategray": "2F4F4F",
            "darkturquoise": "00CED1",
            "darkviolet": "9400D3",
            "deeppink": "FF1493",
            "deepskyblue": "00BFFF",
            "dimgray": "696969",
            "dodgerblue": "1E90FF",
            "firebrick": "B22222",
            "floralwhite": "FFFAF0",
            "forestgreen": "228B22",
            "fuchsia": "FF00FF",
            "gainsboro": "DCDCDC",
            "ghostwhite": "F8F8FF",
            "gold": "FFD700",
            "goldenrod": "DAA520",
            "gray": "808080",
            "green": "008000",
            "greenyellow": "ADFF2F",
            "honeydew": "F0FFF0",
            "hotpink": "FF69B4",
            "indianred": "CD5C5C",
            "indigo": "4B0082",
            "ivory": "FFFFF0",
            "khaki": "F0E68C",
            "lavender": "E6E6FA",
            "lavenderblush": "FFF0F5",
            "lawngreen": "7CFC00",
            "lemonchiffon": "FFFACD",
            "lightblue": "ADD8E6",
            "lightcoral": "F08080",
            "lightcyan": "E0FFFF",
            "lightgoldenrodyellow": "FAFAD2",
            "lightgray": "D3D3D3",
            "lightgreen": "90EE90",
            "lightpink": "FFB6C1",
            "lightsalmon": "FFA07A",
            "lightseagreen": "20B2AA",
            "lightskyblue": "87CEFA",
            "lightslategray": "778899",
            "lightsteelblue": "B0C4DE",
            "lightyellow": "FFFFE0",
            "lime": "00FF00",
            "limegreen": "32CD32",
            "linen": "FAF0E6",
            "magenta": "FF00FF",
            "maroon": "800000",
            "mediumaquamarine": "66CDAA",
            "mediumblue": "0000CD",
            "mediumorchid": "BA55D3",
            "mediumpurple": "9370DB",
            "mediumseagreen": "3CB371",
            "mediumslateblue": "7B68EE",
            "mediumspringgreen": "00FA9A",
            "mediumturquoise": "48D1CC",
            "mediumvioletred": "C71585",
            "midnightblue": "191970",
            "mintcream": "F5FFFA",
            "mistyrose": "FFE4E1",
            "moccasin": "FFE4B5",
            "navajowhite": "FFDEAD",
            "navy": "000080",
            "oldlace": "FDF5E6",
            "olive": "808000",
            "olivedrab": "6B8E23",
            "orange": "FFA500",
            "orangered": "FF4500",
            "orchid": "DA70D6",
            "palegoldenrod": "EEE8AA",
            "palegreen": "98FB98",
            "paleturquoise": "AFEEEE",
            "palevioletred": "DB7093",
            "papayawhip": "FFEFD5",
            "peachpuff": "FFDAB9",
            "peru": "CD853F",
            "pink": "FFC0CB",
            "plum": "DDA0DD",
            "powderblue": "B0E0E6",
            "purple": "800080",
            "rebeccapurple": "663399",
            "red": "FF0000",
            "rosybrown": "BC8F8F",
            "royalblue": "4169E1",
            "saddlebrown": "8B4513",
            "salmon": "FA8072",
            "sandybrown": "F4A460",
            "seagreen": "2E8B57",
            "seashell": "FFF5EE",
            "sienna": "A0522D",
            "silver": "C0C0C0",
            "skyblue": "87CEEB",
            "slateblue": "6A5ACD",
            "slategray": "708090",
            "snow": "FFFAFA",
            "springgreen": "00FF7F",
            "steelblue": "4682B4",
            "tan": "D2B48C",
            "teal": "008080",
            "thistle": "D8BFD8",
            "tomato": "FF6347",
            "turquoise": "40E0D0",
            "violet": "EE82EE",
            "wheat": "F5DEB3",
            "white": "FFFFFF",
            "whitesmoke": "F5F5F5",
            "yellow": "FFFF00",
            "yellowgreen": "9ACD32"
        }
        colors = ''.join(color.split())
        hexd = color_hex_codes.get(colors)
        with httpx.Client() as client:
            response= client.get(f"https://www.thecolorapi.com/scheme?hex={hexd}&mode=complement")
        
        js = response.json()
        colorsy = []

        for x in js['colors']:
            if x['name'].get('value') not in colorsy and x['name'].get('value').lower().split() != color.split():
                colorsy.append(x['name'].get('value'))
        if colorsy != ['Black']:
            stringy = ', '.join(colorsy)
            self.main_window.info_dialog(greeting2(self.name_input.value), stringy,)
        else:
            self.main_window.info_dialog(greeting2(self.name_input.value), "No colors available, please try again",)
    #this class runs virtually the same was as the recipe class

def main():
    '''Runs initial screen'''
    return Questions()
