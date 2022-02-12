# Imports
try:
    import os
    import webbrowser
    from dotenv import load_dotenv
    from mysql.connector import connect
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.properties import ObjectProperty
    from kivy.uix.screenmanager import Screen, ScreenManager
    print('All packages loaded.')
except ImportError as ie:
    print(ie)

# Database Connection
load_dotenv(".env")
passwd = os.getenv("passwd")
connection = connect(
    host='localhost', 
    user='root', 
    passwd=passwd, 
    database='medibuddy'
)
cursor = connection.cursor()
print("Connection to DB established.")

# Function for quit button + Misc
medList = []
quit = lambda: exit()

# ------------------- Screens ----------------------------

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
        if self.firstname.text and self.lastname.text and self.username.text and self.password.text is not None and self.password.text is not "":
            cursor.execute("""INSERT INTO userdata VALUES("{}", "{}", "{}", "{}")""".format(
                self.firstname.text, 
                self.lastname.text, 
                self.username.text, 
                self.password.text
            ))
            connection.commit()
            print("Data saved.")
            popup = Popup(
                title="Message", 
                content=Label(text="Registered Successfully.", color="white"), 
                size_hint=(None, None), 
                size=(300, 200)
            )
            popup.open()
            return True
        else: 
            popup = Popup(
                title="Message",
                content=Label(text="All fields are required.", color="white"),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            return False


class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
   
    def login(self):
        global cursor
        verify = (self.username.text, self.password.text)
        cursor.execute("SELECT username, password FROM userdata")
        data = cursor.fetchall()
        if verify in data: 
            popup = Popup(
                title="Message", 
                content=Label(text="Logged In.", color="white"), 
                size_hint=(None, None), 
                size=(300, 200)
            )
            popup.open()
            return True
        else: 
            popup = Popup(
                title="Message",
                content=Label(text="Username or Password Incorrect.", color="white"),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            return False


class HomeScreen(Screen):
    
    @staticmethod
    def logout():
        popup = Popup(
            title="Message", 
            content=Label(text="Logged Out.", color="white"), 
            size_hint=(None, None), 
            size=(300, 200)
        )
        popup.open()


class BuyMedicinesScreen(Screen):
    
    @staticmethod
    def cartPopup():
        popup = Popup(
            title="Message",
            content=Label(text="Med added to cart.", color="white"),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

    def addToCart(self, instance):
        global medList
        med = instance.ids
        medList.append(med)


class CartScreen(Screen):
    
    @staticmethod
    def medsInCart():
        global medList
        return ",".join(medList)

    def totalPrice(self):
        global medList
        sum = None
        cursor.execute("SELECT * FROM prices")
        data = cursor.fetchall()
        for row in data:
            for med in medList:
                if med == row[0]:
                    sum += row[1]
        return sum


class AboutScreen(Screen):
    
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

# -------------------- App Setup -------------------------

class MediBuddyApp(App):
    def build(self):
        return Builder.load_file("medibuddy.kv")

if __name__ == "__main__":
    MediBuddyApp().run()
