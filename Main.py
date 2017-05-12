import sys
import datetime
import math

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
        text = str(self.id) + " - '" + self.name + "' with " + str(self.stars) + " Star(s) and " + str(
            self.numberOfRooms) + " Room(s)\n"
        for reservation in self.reservations:
            text += "\t" + str(reservation) + "\n"
        return text


class Reservation:
    def __init__(self, name, checkinDate, stayDurationDays):
        self.name = name
        self.checkinDate = checkinDate
        self.stayDurationDays = stayDurationDays

    def __repr__(self):
        return self.name + ";" + str(self.checkinDate.strftime("%d/%m/%Y")) + ";" + str(self.stayDurationDays) + ";"

    def __str__(self):
        return "Surname: '" + self.name + "' Date: " + str(self.checkinDate) + " Stay: " + str(
            self.stayDurationDays) + " Days"


#######################
### Linear Searches ###
#######################

def LinearSearchHotels(searchId):
    for hotel in hotels:
        if hotel.id == searchId:
            return hotel
    return None


## Search by surname
def LinearSearchBySurname(searchName):
    results = []
    for hotel in hotels:
        for reservation in hotel.reservations:
            if reservation.name == searchName:
                results.append(reservation)
    return results


#####################
### Binary Search ###
#####################

def BinarySearchSortList():
    global hotelsNeedSort
    if hotelsNeedSort == True:
        hotels.sort(key=lambda hotel: hotel.id)
        hotelsNeedSort = False


def BinarySearchList(searchid):
    found = -1
    start = 0
    end = hotels.__len__() - 1
    if (end < start):
        print("List is empty")
        return None
    while found == -1:
        middle = start + int(math.floor((end - start) / 2))
        if hotels[middle].id == searchid:
            found = middle
            break
        elif hotels[middle].id < searchid:
            start = middle
        elif hotels[middle].id > searchid:
            end = middle
        # end condition
        if end - start < 2:
            if hotels[start].id == searchid:
                found = start
            elif hotels[end].id == searchid:
                found = end
            else:
                found = -2
    if found >= 0:
        return hotels[found]
    return None


############
### TRIE ###
############
TRIE_MAX_CHAR = 256


def strToIndex(Key):
    Key.encode("ascii", "ignore")
    return [ord(i) % TRIE_MAX_CHAR for i in list(Key)]


class Trie:
    def __init__(self):
        self.root = TrieNode(None, None, isRoot=True)
        self.nodes = 0

    def followPath(self, Key):
        Keys = strToIndex(Key)
        parent = self.root
        for i, x in enumerate(Keys):
            child = parent.getChild(x)
            if i == len(Keys) - 1:
                # last element returns list if exists or None
                if child != None:
                    return child.getData()
                else:
                    return []
            elif child != None:
                parent = child
            else:
                parent = TrieNode(x, parent)

    def followCreatePath(self, Key, DataToAdd):
        Keys = strToIndex(Key)
        parent = self.root
        for i, x in enumerate(Keys):
            child = parent.getChild(x)
            if i == len(Keys) - 1:
                # Adding data to final node
                AddCreateNode(x, parent, DataToAdd)
                self.nodes += 1
            elif child != None:
                parent = child
            else:
                self.nodes += 1
                parent = TrieNode(x, parent)

    def addKey(self, Key, Data):
        self.followCreatePath(Key, Data)

    def getKey(self, Key):
        print("Trie Node Count: " + str(self.nodes))
        return self.followPath(Key)


def AddCreateNode(element, parent, Data):
    if parent.child[element] != None:
        # add data
        parent.child[element].addData(Data)
    else:
        TrieNode(element, parent, setData=Data)


class TrieNode:
    def __init__(self, element, parent, isRoot=False, setData=None):
        if isRoot == False:
            parent.child[element] = self
        self.child = [None] * TRIE_MAX_CHAR
        self.data = []
        if (setData != None):
            self.data.append(setData)

    def getChild(self, Index):
        return self.child[Index]

    def getData(self):
        return self.data

    def addData(self, NewData):
        self.data.append(NewData)


################
### AVL TREE ###
################

def getAVLHeight(Node):
    if Node == None:
        return 0
    return Node.height


def AVLInsert(Node, Data):
    if Node == None:
        return AVLNode(Data)

    if Data.id < Node.data.id:
        Node.left = AVLInsert(Node.left, Data)
    elif Data.id > Node.data.id:
        Node.right = AVLInsert(Node.right, Data)
    else:
        print("Error. Equal Data. ID: " + str(Data.id) + " exists already as: " + str(Node.data))

    Node.height = max(getAVLHeight(Node.left), getAVLHeight(Node.right)) + 1

    balance = Node.getBalance()

    if balance > 1 and Data.id < Node.left.data.id:
        return Node.rotateRight()
    if balance < -1 and Data.id > Node.right.data.id:
        return Node.rotateLeft()

    if balance > 1 and Data.id > Node.left.data.id:
        Node.left = Node.left.rotateLeft()
        return Node.rotateRight()

    if balance < -1 and Data.id < Node.right.data.id:
        Node.right = Node.right.rotateRight()
        return Node.rotateLeft()

    return Node


def AVLSearch(Node, Id):
    counts = 0
    while Node != None:
        if Node.data.id == Id:
            print("Found data " + str(Id) + " in " + str(counts))
            return Node
        elif Node.data.id < Id:
            Node = Node.right
        else:
            Node = Node.left
        counts += 1
    print("Data not found, counts: " + str(counts))


class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

    def getBalance(self):
        return getAVLHeight(self.left) - getAVLHeight(self.right)

    def rotateLeft(self):
        oldright = self.right
        deepleft = oldright.left

        oldright.left = self
        self.right = deepleft

        self.height = max(getAVLHeight(self.left), getAVLHeight(self.right)) + 1
        oldright.height = max(getAVLHeight(oldright.left), getAVLHeight(oldright.right)) + 1

        return oldright

    def rotateRight(self):
        oldleft = self.left
        deepright = oldleft.right

        oldleft.right = self
        self.left = deepright

        self.height = max(getAVLHeight(self.left), getAVLHeight(self.right)) + 1
        oldleft.height = max(getAVLHeight(oldleft.left), getAVLHeight(oldleft.right)) + 1

        return oldleft


### GLOBALS  ###
filename = "hotels.csv"
hotels = []
hotelsNeedSort = True
trie = Trie()
avlRoot = None

#####################
### MENU HANDLERS ###
#####################

def LoadFromFile():


    try:
        f = open(filename, "r", encoding="latin1")
    except FileNotFoundError:
        print("File does not exist. Please save first or change the file.")
        return

    global trie
    global avlRoot
    global hotels

    hotels.clear()
    trie = Trie()
    avlRoot = None

    f.readline()  # skip number of hotels
    for inputline in f:
        values = inputline.split(";")

        appendedHotel = Hotel(int(values[0]), values[1], int(values[2]), int(values[3]))
        reservationCount = round((len(values) - 4) / 3)

        for i in range(0, reservationCount):  # TODO: find a pythonic way to do this
            Index = i * 3 + 4
            appendedHotel.reservations.append(Reservation(
                values[Index],
                datetime.datetime.strptime(values[Index + 1], "%d/%m/%Y").date(),
                int(values[Index + 2])
            ))
            trie.addKey(values[Index], appendedHotel)

        hotels.append(appendedHotel)

        avlRoot = AVLInsert(avlRoot, appendedHotel)
    global hotelsNeedSort
    hotelsNeedSort = True
    print("Imported file: " + filename)
    print("Current hotels: " + str(hotels.__len__()))



def SaveToFile():
    f = open(filename, "w")
    numOfHotels = len(hotels)

    print(str(numOfHotels), file=f)
    for hotel in hotels:
        print(repr(hotel), file=f)
    global fileIsOpen
    fileIsOpen = True


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
        trie.addKey(name, addedHotel)
        addedHotel.reservations.append(Reservation(
            name,
            datetime.datetime(year, month, day).date(),
            duration
        ))
        answer = input("Add another reservation? (y/n) ")
    hotels.append(addedHotel)

    global avlRoot
    avlRoot = AVLInsert(avlRoot, addedHotel)

    global hotelsNeedSort
    hotelsNeedSort = True


def DebugPrintAll():
    for hotel in hotels:
        print(hotel)


def SearchHotelById():
    searchId = int(input("Give the id to search: "))

    print("""
    Select Mode:
    1. Linear Search
    2. Binary Search
    3. AVL tree Search
    """)
    found = None
    answer = int(input("Mode: "))
    if answer == 1:
        found = LinearSearchHotels(searchId)
    elif answer == 2:
        BinarySearchSortList()
        found = BinarySearchList(searchId)
    else:
        found = AVLSearch(avlRoot, searchId).data

    if found == None:
        print("The id does not exist")
        return
    print("Hotel Found: ")
    print(found)


def SearchReservationsBySurname():
    # The two modes return two different kind of lists because that was requested

    searchName = input("Give name to search: ")
    print("""
    Select Mode:
    1. Linear Search (returns list of reservations)
    2. Trie Search (returns list of hotels)
    """)
    answer = int(input("Mode: "))

    if answer == 1:
        results = LinearSearchBySurname(searchName)
    else:
        results = trie.getKey(searchName)

    for result in results:
        print(result)


# Main

# File selection
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print("Using default file: " + filename)

LoadFromFile()


# Menu
answer = True
while answer:
    print(60 * "*")
    print("""
    1. Load Hotels and Reservations from file
    2. Save Hotels and Reservations to file
    3. Add a Hotel
    4. Search and Display a Hotel by id
    5. Display Reservations by surname search
    6. Exit
    10. Print All Data
    11. Change File
    12. Save as
    """)
    print(60 * "*")
    answer = int(input("Select option: "))
    if answer == 10:
        DebugPrintAll()
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
    elif answer == 11:
        confirm = input("Any unsaved changes may be lost. Please confirm (y/n): ")
        if confirm == "y":
            hotels=[]
            filename = input("Give filename: ")
            LoadFromFile()
    elif answer == 12:
        filename = input("Give filename to save as: ")
        SaveToFile()
    else:
        print("Invalid Option")
