import sys
import datetime

filename = "hotels.csv"
hotels = []

class Hotel:
    def __init__(self, id, name, stars, numberOfRooms):
        self.id = id
        self.name = name
        self.stars = stars
        self.numberOfRooms = numberOfRooms
        self.reservations = []

    def __repr__(self):
        text = str(self.id) + ";" + self.name + ";" + str(self.stars) + ";" + str(self.numberOfRooms) + ";"
        for res in self.reservations:
            text += res.__repr__()
        return text

    def __str__(self):
        return self.__repr__()

class Reservation:
    def __init__(self, name, checkinDate, stayDurationDays):
        self.name = name
        self.checkinDate = checkinDate
        self.stayDurationDays = stayDurationDays

    def __repr__(self):
        return self.name + ";" + str(self.checkinDate) + ";" + str(self.stayDurationDays) + ";"

    def __str__(self):
        return self.__repr__()


def LoadFromFile():
    f = open(filename, "r")
    print("Reading File: ")
    print(f.read())


def SaveToFile():
    f = open(filename, "w")
    numOfHotels = len(hotels)

    print(str(numOfHotels),file=f)
    for hotel in hotels:
        print(hotel, file=f)

def AddHotel():
    id = int(input("Give Hotel ID: "))
    name = input("Give Hotel Name: ")
    stars = int(input("Give Hotel Stars: "))
    numberOfRooms = int(input("Give Number of Rooms: "))
    addedHotel = Hotel(id, name, stars, numberOfRooms)

    answer = input("Add a reservation? (y/n) ")
    while answer == "y":
        name = input("Give Surname: ")
        day = int(input("Day: "))
        month = int(input("Month: "))
        year = int(input("Year: "))
        duration = int(input("Duration Days: "))
        addedHotel.reservations.append(Reservation(
            name,
            datetime.date( year, month, day),
            duration
        ))
        answer = input("Add another reservation? (y/n) ")
    hotels.append(addedHotel)


def DebugPrintAll():
    print(hotels)


def SearchHotelById():
    print("Search by id")

def SearchReservationsBySurname():
    print("Search reservations")


# Main




# Menu
answer = True
while answer:
    print(60 * "*")
    print("""
    0. Debug Print data
    1. Load Hotels and Reservations from file
    2. Save Hotels and Reservations to file
    3. Add a Hotel
    4. Search and Display a Hotel by id
    5. Display Reservations by surname search
    6. Exit
    """)
    print(60 * "*")
    answer = int(input("Select option: "))
    if answer == 0:
        DebugPrintAll()
        answer = True
    elif answer == 1:
        LoadFromFile()
    elif answer == 2:
        SaveToFile()
    elif answer == 3:
        AddHotel()
    elif answer == 4:
        SearchHotelById()
    elif answer == 5:
        SearchReservationsBySurname()
    elif answer == 6:
        answer = False
    else:
        print("Invalid Option")