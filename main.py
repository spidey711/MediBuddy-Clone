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
    from kivy.uix.widget import Widget
    from kivy.properties import ObjectProperty
    from kivy.uix.screenmanager import Screen, ScreenManager
    print('All packages loaded.')
except ImportError as ie:
    print(ie)

# Database Connection
load_dotenv(".env")
try:
    connection = connect(
        host='localhost', 
        user='root', 
        passwd=os.getenv("passwd"), 
        database='medmart'
    )
    cursor = connection.cursor()
    print("Connection to DB established.")
except Exception as error:
    print(error)

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
    
    medicine = ObjectProperty(None)
    
    def addToCart(self):
        if self.medicine.text.strip(): # no blank input box
            if self.medicine.text.isalpha() or "," in self.medicine.text: # no special characters
                li = list(self.medicine.text.split(","))
                for item in li:
                    item = item.lower().strip() # remove whitespaces
                    medList.append(item) 
                popup = Popup(
                    title="Message",
                    content=Label(text="Med(s) added to cart.", color="white"),
                    size_hint=(None, None),
                    size=(300, 200)
                )
                popup.open()
                return True
            else:
                popup = Popup(
                    title="Message",
                    content=Label(text="Following are not allowed:-\nSpecial Characters, Numbers\nexcept commas (,)", color="white"),
                    size_hint=(None, None),
                    size=(300, 200)
                )
                popup.open()
                return False
        else:
            popup = Popup(
                title="Message",
                content=Label(text="No medicine name was mentioned.", color="white"),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            return False


class CartScreen(Screen):

    @staticmethod
    def infoCrocin():
        return "Uses: Cold, Flu, Headache etc.\nContents: Paracetamol, Caffeine\nPrice: Rs 30\n(1 leaf has 6 tablets)"

    @staticmethod
    def infoNexium():
        return "Uses: Acidity, Gastric Ulcer etc.\nContents: Magnesium, R-Isomers\nPrice: Rs 25\n(1 leaf has 6 tablets)"

    @staticmethod
    def infoParacetamol():
        return "Uses: Acute Pain, Aches etc.\nContents: Purified Talc, Starches\nPrice: Rs 27\n(1 leaf has 6 tablets)"

    @staticmethod
    def infoAspirin():
        return "Uses: Swelling, Cold, Aches\nContents: Cellulose, Triacetin\nPrices: Rs 32\n(1 leaf has 6 tablets)"

    def billing(self):    
        cursor.execute("SELECT * FROM prices")
        data = cursor.fetchall()
        priceList = [] # to sum up the price of all meds
        
        with open("bills.txt", "w") as bill:
            bill.write("-------------- BILL RECEIPT --------------\n\n")
            bill.write(f"Date: {datetime.datetime.today().date()}\nTime: {datetime.datetime.today().time()}\n\nMedicines Purchased:-\n\n")
            for med in medList:             # compare meds in medlist with meds in table
                for item in data:           # item = (name of med, price)
                    if item[0] == med:
                        priceList.append(item[1])
                        bill.write("{}:  Rs {}\n".format(str(item[0]).capitalize(), item[1]))
            bill.write("\nTotal Price:  Rs {}\n\nThank you for your purchase!\n".format(sum(priceList)))
            bill.write("--------------------------------------------\n\n")

        # popups for purchasing meds with or without adding them to cart
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
        # reset variables
        medList.clear()
        priceList.clear()
        

class AboutScreen(Screen):
    
    @staticmethod
    def information():
        return "This app is made by Tamonud Sharma, Siddhant Ghosh & Sarvesh Sai as a part of our 12th grade Computer\nScience project. Click the 'Source Code' button to head over to source code for this app. Click 'User Profile' to\ncheck out my profile on github. Thank you!"
        
    @staticmethod
    def linkToRepo():
        webbrowser.open("https://github.com/spidey711/Medmart")
        
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
