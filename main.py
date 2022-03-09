# Kivy latest version: 2.0.0

# Imports
try:
    import os
    import datetime
    import subprocess
    import webbrowser
    from dotenv import load_dotenv
    from mysql.connector import connect
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.uix.button import Button
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
    database='medmart'
)
cursor = connection.cursor()
print("Connection to DB established.")

# Variables
medList = []

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
        if self.firstname.text and self.lastname.text and self.username.text and self.password.text is not None and self.password.text != "":
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

    @staticmethod
    def exitApp():
        exit()


class BuyMedicinesScreen(Screen):

    def addToCart(self, instance):
        global medList
        # for childLayout in self.children:
        #     for childFeature in childLayout.children:
        #         if isinstance(childFeature, Button):
        #             if childFeature.state == "down":
        #                 medList.append("Pressed")
        # Maybe use widgets here? :pepethink:
        print(self, instance)
        print(medList)
        popup = Popup(
            title="Message",
            content=Label(text="Med added to cart.", color="white"),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


class CartScreen(Screen):
    
    @staticmethod
    def medsInCart():
        global medList
        return ",".join(medList)

    def totalPrice(self):
        global medList
        cursor.execute("SELECT * FROM prices")
        data = cursor.fetchall()
        priceList = []
        with open("bills.txt", "w") as bill:
            bill.write("------------------ BILL RECEIPT ------------------\n\n")
            bill.write("Date: {}\n".format(datetime.datetime.today()))
            bill.write("Meds Purchased:-\n\n")
            # compare meds in medlist with meds in table
            for item in data:
                priceList.append(item[1])
                bill.write("{}:    Rs {}\n".format(str(item[0]).capitalize(), item[1]))
            bill.write("\nTotal Price: Rs {}\n\n".format(sum(priceList)))
            bill.write("Thank you for your purchase!\n")
            bill.write("---------------------------------------------------\n\n")
        if len(priceList) > 0:
            popup = Popup(
                title="Message",
                content=Label(text="Bill Receipt has been generated.", color="white"),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            subprocess.Popen(['notepad.exe', 'bills.txt']) # for showing bill in notepad
        else:
            popup = Popup(
                title="Message",
                content=Label(text="You didn't purchase anything.\nBill couldn't be generated.", color="white"),
                size_hint=(None, None),
                size=(300, 200) 
            )
            popup.open()
        medList.clear()
        priceList.clear()
        

class AboutScreen(Screen):
    
    @staticmethod
    def information():
        return "This app is made by Tamonud Sharma, Siddhant Ghosh & Sarvesh Sai as a part of our 12th grade Computer\nScience project. Click the 'Source Code' button to head over to source code for this app. Click 'User Profile' to\ncheck out my profile on github. Thank you!"
        
    @staticmethod
    def linkToRepo():
        webbrowser.open("https://github.com/spidey711/MediBuddy-Clone")
        
    @staticmethod
    def linkToProfile():
        webbrowser.open("https://github.com/spidey711")


class WindowManager(ScreenManager):
    pass

# -------------------- App Setup -------------------------

class MedmartApp(App):
    
    # load UI into app
    def build(self):
        return Builder.load_file("medmart.kv")

if __name__ == "__main__":
    MedmartApp().run()
