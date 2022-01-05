# InstaSecretary

InstaSecretary is a Python solution for automating a service provider's administrative tasks such as:
1. Booking of Appointments
2. Informing clients about Pricelist

## Usage

Setup the following parameters on top of the script according to your preferences:

```python

#Weekdays of work
working_days = "Monday:Tuesday"

#Hours of work throughout a day
working_hours = "09:11"

#Duration of each appointment in minutes
duration_of_appointment=30

#For how many ahead can secretary plan
days_ahead = 7

#Pricelist
pricelist = {"an hour of occupation":"50E", "an analysis report":"150E", "a dashboard":"200E" }

#Username & Password for login
my_username = "" 
my_password = ""

```

Run script and pay your attention to anything else other than Instagram.

At the end of the day, pause script and collect these global variables to get a summary of the day

```python
customers_reached_out
appointments_booked
asked_for_pricelist
asked_for_reachout
not_found_an_appointment
```

## Installation

Prior to running it, use the package manager [pip](https://pip.pypa.io/en/stable/) to install:
1. pyautogui
```bash
pip install pyautogui
```
2. pyperclip
```bash
pip install pyperclip
```
3. selenium
```bash
pip install selenium
```
4. webdriver_manager
```bash
pip install webdriver_manager
```
5. opencv
opencv-python
```bash
pip install opencv-python
```
