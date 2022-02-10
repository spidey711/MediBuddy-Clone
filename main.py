# Imports
try:
    import os
    import webbrowser
    from dotenv import load_dotenv
    from mysql.connector import connect
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.properties import ObjectProperty
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.screenmanager import Screen, ScreenManager
    print('All packages loaded.')
except ImportError as ie:
    print(ie)


# Database Connection
load_dotenv(".env")
passwd = os.getenv("passwd")
try:
    connection = connect(host='localhost', user='root', passwd=passwd, database='medibuddy')
    cursor = connection.cursor()
    print('Connection to DB established.')
except Exception as exception:
    print(exception)


# Function for quit button + Misc
quit = lambda: exit()


# ------------------- Screens ----------------------------
# Backend Stuff (include methods which will be mapped to buttons)
class WelcomeScreen(Screen):
    pass


class RegisterScreen(Screen):
    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    # saves data in db
    def register(self):
       # making sure no details are empty 
        if self.firstname.text and self.lastname.text and self.username.text and self.password.text is not None:
            cursor.execute("""INSERT INTO userdata VALUES("{}", "{}", "{}", "{}")""".format(
                self.firstname.text, 
                self.lastname.text, 
                self.username.text, 
                self.password.text
            ))
            connection.commit()
            print("Data saved.")
            return True
        else: return False


class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def login(self):
        verify = (self.username.text, self.password.text)
        # [i][0] -> username [i][1] -> password
        cursor.execute("SELECT username, password FROM userdata")
        data = cursor.fetchall()
        # verification
        if verify in data: return True
        else: return False


class HomeScreen(Screen):
    pass


class BuyMedicines(Screen):
    pass


class Cart(Screen):
    pass


class About(Screen):
    
    @staticmethod
    def information():
        return "This app is made by Tamonud Sharma, Siddhant Ghosh & Sarvesh Rai as a part of our 12th grade Computer\nScience project. Click the 'Source Code' button to head over to source code for this app. Click 'User Profile' to\ncheck out my profile on github."
        
    @staticmethod
    def linkToRepo():
        webbrowser.open("https://github.com/spidey711/MediBuddy-Clone")
        
    @staticmethod
    def linkToProfile():
        webbrowser.open("https://github.com/spidey711")


class WindowManager(ScreenManager):
    pass

# -------------------------------------------------------

# App Setup
class MediBuddyApp(App):
    def build(self):
        return Builder.load_file("medibuddy.kv")

if __name__ == "__main__":
    MediBuddyApp().run()
