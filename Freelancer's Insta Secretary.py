# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 19:14:20 2021

@author: voulk
"""

####Global Variables####

#Weekdays of work
working_days = "Monday:Tuesday"
#Hours of work throughout a day
working_hours = "09:11"
#Duration of each appointment in minutes
duration_of_appointment=30
#For how many ahead can secretary plan
days_ahead = 7
pricelist = {"an hour of occupation":"50E", "an analysis report":"150E", "a dashboard":"200E" }

#Username & Password for login
my_username = "" 
my_password = ""

####Modules####

#To avoid ban as a bot
from time import sleep
#To handle computer operations - click, etc.
import pyautogui as pt
#To paste from clipboard
import pyperclip as pc
#To handle web browser activity
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait as ww
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
#To compute appointments
import time
#Helper functions
from random import randint
import math
import datetime
from tkinter import Tk  
import re
import os

time_started = datetime.datetime.now()

#Change working directory to where the script resides
#so that all relative paths of images can work
#otherwise working directory is engine's directory
os.chdir(os.path.dirname(__file__))


def login_handler(username, password):
    
    """
    Function that handles all login process
    
    It opens a chrome browser, 
    Surpasses cookies selection,
    Submits login credentials
    Dodges the not now prompt
    It uses XPaths to detect elements of the HTML page
    and clicks on them
    Largely based on TheoTziol's Youtube video:
    https://www.youtube.com/watch?v=U8Ga-98n4sk&t=1420s
    """
    #Chrome window must be global
    #to be accessed by the rest objects
    #if created within function, 
    #will disappear after function is run
    global driver
    
    #Always instagram, it's a function specifically for this purpose
    site = 'https://instagram.com'
    driver.get(site)
    
    #Following are the XPaths of each elements
    #We just define them, we will use them later
    
    #In case prompted to switch accounts,
    #For now is not needed
    #path_switch_accounts = '//*[@id="react-root"]/section/main/article/div[2]/div/div/div[3]/span/button'
    
    #Avoid cookies button
    path_cookies = '/html/body/div[4]/div/div/button[1]'
    #Click on it
    driver.find_element_by_xpath(path_cookies).click()
    #And wait
    time.sleep(randint(2,5))
    
    #The text forms of username and password
    path_username = '//*[@id="loginForm"]/div/div[1]/div/label/input'
    path_password = '//*[@id="loginForm"]/div/div[2]/div/label/input'
    
    #Fill them in
    driver.find_element_by_xpath(path_username).send_keys(username)
    driver.find_element_by_xpath(path_password).send_keys(password)
    
    #The submit button
    path_submit = '//*[@id="loginForm"]/div/div[3]/button'
    #Wait and press the button
    wait = ww(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH,path_submit))).click()
    
    
    #Not Now paths
    path_notnow_alt = '//*[@id="react-root"]/div/div/section/main/div/div/div/div/button'
    path_notnow_alt2 = '/html/body/div[5]/div/div/div/div[3]/button[2]'
    #path_notnow_alt2 = '/html/body/div[6]/div/div/div/div[3]/button[2]'
    
    #Press the not now button
    wait.until(EC.element_to_be_clickable((By.XPATH,path_notnow_alt))).click()
    #Wait
    time.sleep(randint(2,5))

    #Second Not now
    wait.until(EC.element_to_be_clickable((By.XPATH,path_notnow_alt2))).click()
    
    time.sleep(1)
    


def find_timeslots(working_days = "Monday:Friday", 
                   working_hours = "09:18",
                   duration_of_appointment = 60,
                   days_ahead = 5 ):
    """
    Function that returns all available timeslots for appointments
    
    Args:
        working_days (str) : the days each freelancer is working, needs whole days separated with :
        working_hours (str): the regular working hours. On a 24-hour base, starting_hour:ending_hour 
        duration_of_appointment (int): duration of each appointent in minutes
        days_ahead(int): how many days ahead from today to consider
    
    Returns:
        list: datetime values of available appointments
    """
    #Our base, current time
    now = datetime.datetime.now()
    
    def unnest_weekdays(working_days):
        
        """ 
        Function to parse the working_days sting provided in find_timeslots
        
        Returns:
            list: all_weekdays between provided days on find_timeslots
        """
        
        # weekdays as a list
        weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        wanted_weekdays = []
        
        #Boundaries
        start_day, end_day = working_days.split(":")
            
        for j in range([i for i,weekday in enumerate(weekDays) if weekday == start_day][0],[i for i,weekday in enumerate(weekDays) if weekday == end_day][0]+1):
                
            wanted_weekdays.append(weekDays[j])
                
        return wanted_weekdays
    
    
    
    #Convert Monday:Wednesday to [Monday,Tuesday,Wednesday]
    working_days_wanted = unnest_weekdays(working_days)
    
    #Out of all wanted weekdays, keep only those into the days_ahead horizon
    days_wanted = [now + datetime.timedelta(days = day) for day in range(days_ahead+1)]
    #Boundaries of hours
    start_time, end_time = working_hours.split(":")
    #How many appointments can fit in a day
    no_of_appointments_in_a_day = math.floor(((int(end_time) - int(start_time))*60)/duration_of_appointment)
    
    #Initiate
    timeslots_available = []
    
    #For each day
    for day in days_wanted:
        #Find the first appointment of the day
        first_appointment = datetime.datetime(year = day.year, 
                                        month = day.month, 
                                        day = day.day,
                                        hour = int(start_time))
        #Put it into the available timeslots
        timeslots_available.append(first_appointment)
        #The last appointment inserted into the list
        #is for now the first (the rest will come later)
        last_appointment = first_appointment
        
        #For each of the rest appointments
        for h in range(no_of_appointments_in_a_day):
            #Next appointment's start will be (last appointment's start + the time it lasted)
            appointment = last_appointment + datetime.timedelta(minutes = duration_of_appointment) 
            #And put it into our list of appointments
            timeslots_available.append(appointment)
            #Update the last_appointment for next iteration
            last_appointment = appointment
    
    #Filter only working days
    timeslots_available = [ t for t in timeslots_available if datetime.datetime.strftime(t,"%A") in working_days_wanted]

    #Filter hours passed already
    timeslots_available = [ t for t in timeslots_available if t >= now]

    #Filter appointments exceeding ending time
    timeslots_available = [ t for t in timeslots_available if t.hour < int(end_time)]

    return timeslots_available



def move_to_text_input(message):
    
    """ 
    Function that handles the message sending in instagram.
    
    Args:
        message (str): the message we want to send
    """
    
    #The insta image is next to the prompt where we type 
    position = sturdy_locate("data/insta_image.png" )
    #Move to insta_image
    pt.moveTo(position[0:2], duration = .5)
    #Move a bit to the upper left 
    pt.moveRel(-100,20,duration=.5)
    #Doubleclick
    pt.doubleClick(interval = .3)
    #Type the message
    pt.typewrite(message, interval = .01)
    
    #Locate the send button, both in English and in Greek
    send_position_gr = sturdy_locate("data/send_button.PNG" )
    send_position_eng = sturdy_locate("data/send_button_eng.PNG" )
    
    #If greek send button not found
    if send_position_gr is None:
        #go for the english location
        send_position = send_position_eng
        
    else:
        #otherwise, stay with the greek position
        send_position = send_position_gr
    #Move to send button
    pt.moveTo(send_position[0:2], duration = .5)
    #A little to the right 
    pt.moveRel(20,5,duration=.5)
    #And click
    pt.click()


def sturdy_locate(image, from_confidence= 95,to_confidence = 45, step = 5):
    
    """
    A function that tries lots of confidence levels to detect something on screen
    
    Args:
        image (driver): what is displayed on screen
        from_confidence (int): Upper confidence level, the first to start trying - defaults to 95%
        to_confidence (int): Lower confidence level, the last to start trying - defaults to 45%
        step (int): Step moving on each trial from upper confidence level to lower - defaults to 5%
    """
    
    #For all confidence levels provided
    for c in range(from_confidence,to_confidence,-step):
        #Try to locate
        location = pt.locateOnScreen(image , confidence = (c/100))
        #If you manage to locate it
        if location is not None:
            #Return the location
            return location
    #If all loop has come to no conclusion
    #Return nothing    
    return None


def get_messages():
    
    """
    Function that is copying the messages received
    """
    
    #To enter the dialogue space,
    #First locate the smiley on the lower left of the screen
    smiley_position = sturdy_locate("data/insta_smiley.PNG")
    #Move to smiley location
    pt.moveTo(smiley_position [0:2], duration = .5)
    #Move a bit higher
    pt.moveRel(50,-50,duration = .5)
    #Scroll down a lot, in case last message is not displayed
    pt.scroll(-100000)
    #Then Click, so that three dots will appear
    pt.click()
    
    #Locate three dots
    dots_position = sturdy_locate("data/triple_dots.PNG")
    #Move there
    pt.moveTo(dots_position[0:2], duration = .5)
    #Click on triple dots
    pt.click()
    
    #Locate copy message button
    #By starting to look for the English version of Copy
    #Could also include other languages too
    copy_position_eng = sturdy_locate("data/insta_copy_eng.PNG", to_confidence=75)
    
    #If English is found
    if copy_position_eng  is not None:
        #Move towards it
        pt.moveTo(copy_position_eng[0] , copy_position_eng[1] ,duration = .5)
    #Otherwise    
    else:
        #Try locating the greek one
        copy_position_gr = sturdy_locate("data/insta_copy_gr.PNG")
        #And move there
        pt.moveTo(copy_position_gr[0] , copy_position_gr[1] ,duration = .5)     
    
    #A slight move to the right
    pt.moveRel(10,10,duration = .4)
    #Click on copy button
    pt.click()
    #Get text from clipboard
    user_text = pc.paste()
    
    return user_text



available_appointments = find_timeslots(working_days = working_days,   
               working_hours = working_hours, 
               duration_of_appointment=duration_of_appointment, 
               days_ahead=days_ahead)

#What the pricelist will display
pricelist_message = "".join([pricelist[k] + " for " + k + "\n"  for i,k in enumerate(pricelist)]) + "For custom orders, please type C and wait until someone reaches out to you"

#All these lists will provide us with information
#of what happened while the bot was running
customers_reached_out = []
appointments_booked = {}
asked_for_pricelist = []
asked_for_reachout = []
not_found_an_appointment = []
#All objects of bots will be stored here
all_bots = {}

def open_messages(new_message_position):
    
    pt.moveTo(new_message_position[0:2], duration = .5)
        
    pt.moveRel(20,20,duration=.5)
        
    pt.doubleClick(interval = .2) #pt.Click()    
    
    return None


def check_for_new_messages(specific = False):

    """
    Checks whether new messages have arrived
    
    It is working both 
    on starting page and
    on messages page
    If no new messages have arrived and it's on the starting page, 
    it locates the messages button, even though it's not red
    
    Args:
        specific (bool): if True, assumes we are in the messages page and looks for the blue dot of new messages

    """    

    #If we are in the messages page
    if specific:
       #Look for the blue dot
        new_message_position = sturdy_locate("data/new_message_specific.PNG" ) 
    #If we are on the starting page           
    else:
        #look for the messages button (specifically when it's red signifying there are new messages)
        new_message_position = sturdy_locate("data/new_message.PNG")
        #If no messages have arrived
        #if new_message_position is None:
            #At least, locate the messages button
            #new_message_position = sturdy_locate("data/message.PNG" )
            
    
    if new_message_position is not None:
        return [True, new_message_position]
    else:
        return False







class insta_chatbot():   
    
    """
    A class that handles conversation
    
    It is unique for each customer
    So that it can remember previous customer's answers
    
    Args:
        customer_name
    """
    
    
    def __init__(self, customer_name):
        #Customer name, provided during object initiation
        self.customer_name = customer_name
        self.last_message = ""
        self.last_response = ""
        self.inside_appointments = False
        self.first_words = True
        self.answer_received = False
        
        self.generic_message = "Dear "+ self.customer_name + "\n This is an automatically generated message.\n Type A to book an appointment. \n Type B for Pricelist.\n Type C if you need someone to reach out to you."
    
        
    def process_message(self, message):
        
        """Main method of class handling conversation"""
        
        #Find those global variables
        #So that we can get information about current status
        #And modify them, and modifications become reachable by other objects too
        global available_appointments, pricelist_message, asked_for_pricelist, asked_for_reachout
        
        #If we haven't spoken yet
        if self.first_words:
            
            #Rule out confusion for next time
            self.first_words = False
            
            #message_to_return = "Dear "+ self.customer_name + "\n This is an automatically generated message.\n Type A to book an appointment. \n Type B for Pricelist.\n Type C if you need someone to reach out to you."
            
            return self.generic_message  
        
        #Turn input to lower case
        msg = str(message).lower()
        
        #If asking for appointment
        if msg == "a" or msg == "α" :
            
            #Are there any appointments left?
            if len(available_appointments) == 0:
                #If not
                #Keep customer's name
                not_found_an_appointment.append(self.customer_name)
                #Answer an apology
                return "Sorry, all available appointments are booked. Please try again later"
            
            #If there are available appointments left
            #Modify object's property
            self.inside_appointments = True
            #And display available appointments
            return  "\n".join(["Please Type "  + str(n+1)+" for " + datetime.datetime.strftime(appointment,"%d %B %Y, %H:%M") for n,appointment in enumerate(available_appointments)])
        
        #If we are already inside appointments 
        #(meaning we have already texted our available timeslots)
        if self.inside_appointments:
            
            #First, check whether the answer can be converted to integer
            #Type 1 for ..., Type 2 for...
            try:
                int(msg)
            
            #If it can't be converted to integer
            except:
                #Notify customer
                return "Please type a number"
                
            #if it is an integer
            #Check whether number is included in the options given
            #e.g. if Type 6 for.... was the last option for booking
            #and customer types 7, which is not valid
            if int(msg) <= len(available_appointments):
                #If customer's answer is valid
                #Remove appointment selected from list of appointments
                appointment_booked = available_appointments.pop(int(msg)-1)
                #Update the list of appointments_booked
                appointments_booked[self.customer_name] = appointment_booked
                #Notify object that we're done with appointments
                self.inside_appointments = False
                #Notify customer for their choice
                return "Your appointment for " +  datetime.datetime.strftime(appointment_booked,"%d %B %Y, %H:%M") + " is booked\nYou will get a confirmation message soon. \n Type B for Pricelist or C if you need someone to reach out to you"
            else:
                return "Please type a valid number, between 1 and " + str(len(available_appointments))
                
        #If customer typed b or greek beta
        if msg == "β" or  msg == "b":
            
            #write them down as customer that asked for pricelist
            asked_for_pricelist.append(self.customer_name)
            #display the pricelist
            return pricelist_message
        
        #If customer typed c
        if msg == "c":
            #write them down as customer that asked for reach out
            asked_for_reachout.append(self.customer_name)
            #notify them
            return "Someone will reach out to you as soon as possible. Thank you for your patience."
        
        #if none of the above happens
        while not self.inside_appointments:
            #Go on for some generic answers
            #Here, we can build a keras chatbot to handle somehow the chitchat
            if msg == "hey":
                return "Hi"
            elif msg == "how are you":
                return "I'm fine, how are you?"
            elif msg == "i'm fine too":
                return "Nice to hear that. How could I help you? Type 1 for Available Dates, 2 for Pricelist"
            #Most usually we end up on that
            else: 
                return self.generic_message 


def leave_conversation():
    
    """
    Clicks on insta home page
    """
    
    home_position = sturdy_locate("data/insta_home.PNG")
    
    #Move to smiley location
    pt.moveTo(home_position[0:2], duration = .5)
    #Move a bit higher
    pt.moveRel(25,25,duration = .5)
    #Then Click, so that three dots will appear
    pt.doubleClick(interval = 0.05)

#All these lists will provide us with information
#of what happened while the bot was running
customers_reached_out = []
appointments_booked = {}
asked_for_pricelist = []
asked_for_reachout = []
not_found_an_appointment = []
#All objects of bots will be stored here
all_bots = {}


######Bring the action######

#Initiate the chrome window driver
driver = wd.Chrome(ChromeDriverManager().install()) #wd.Chrome()
#Manipulate (global) driver to handle login
login_handler(username = my_username, password = my_password)

try:
    while True:
        
        #Now that we are in the instagram's home page
        #Locate the messages button (looks like a paper plane)
        new_messages = check_for_new_messages(specific = False)
    
        #If messages button is found
        while not isinstance(new_messages, bool):
            
            #Click on the paper plane to open the messages screen
            open_messages(new_messages[1])
            #Now that we are in the messages screen
            
           
            #Constantly
            #Check whether any blue dot appears (meaning there is an unread message)
            new_messages = check_for_new_messages(specific = True)
                
            #If a blue dot appears
            if not isinstance(new_messages, bool):
                    #Find its location
                    new_message_location = new_messages[1] 
                    #Navigate towards there
                    pt.moveTo(new_message_location[0:2], duration = .5)
                    #Move to the left so that we can click on customer's insta name
                    pt.moveRel(-210,0,duration=.5)
                    
                    #Double click twice
                    pt.doubleClick(interval = .05)
                    pt.doubleClick(interval = .05)
                    
                    #Copy selected text on clipboard
                    pt.hotkey('ctrl', 'c')
                    #Bring from clipboard to global environment
                    customer_name = Tk().clipboard_get()
                    #Clean client's username
                    customer_name = re.sub("^.*picture" , "" , re.sub("Active.*", "",customer_name.replace("\n","")))
                    #Also for Greek
                    customer_name = re.sub("^.*χρήστη" , "" , re.sub("Ενεργός.*", "",customer_name.replace("\n","")))
                    
                    #Now that we know who our client it
                    #Fetch what they're saying
                    message = get_messages()
                    
                    #If we have not already spoken with them during session
                    if customer_name not in customers_reached_out:
                        
                        #Update global list 
                        customers_reached_out.append(customer_name)
                        
                        #Initiate a chatbot dedicated to them only
                        #It will be part of a dictionary
                        #Matching with the respective customer it serves
                        all_bots[customer_name] = insta_chatbot(customer_name)
                        
                    #Use bot (either the recently initiated or one existing from before)
                    #to answer
                    move_to_text_input(all_bots[customer_name].process_message(message))
                    
                    leave_conversation()
                    
                    
            #Pause for 5 seconds between each check 
            #so that insta won't notice it's a bot
            sleep(5)
except KeyboardInterrupt: #When stopped, show us results
    
    time_ended = datetime.datetime.now()
    
    print("---------------------------")
    print("Session started at ", time_started)
    print("Ended at ", time_ended)
    print("And Lasted ", time_ended - time_started)
    print("Resulted in : ")
    print("---------------------------")
    print("Customers that reached out ",customers_reached_out)
    print("Appointments Booked ",appointments_booked)
    print("Customers asked for pricelist ",asked_for_pricelist)
    print("Customers asked for reach out ",asked_for_reachout)    
    print("Customers who didn't find an appointment", not_found_an_appointment)
