import pygame, random
pygame.init()  # Initialises pygame

screen = pygame.display.set_mode((1200,800)) #defines the screen and its size
running = True

#List of colours:
WHITE = (255,255,255) #Stores the rgb values so I can go back to commonly used colours
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GREY = (170,170,170)
BLACK = (0,0,0)

QuitButton = pygame.Rect(850, 500, 200, 100) #defines buttons as a rectangle
PlayButton = pygame.Rect(500, 500,200,100)
SettingsButton = pygame.Rect(150, 500, 200, 100)
MenuButton = pygame.Rect(1000, 50, 150, 75)
DeckRect = pygame.Rect(100,100,150,200)
DiscardRect = pygame.Rect(1000,550,150,200)

#List of fonts:
font = pygame.font.Font(None,30)

menuOpen = 'Main' # Varible to keep track of which menu is open

Suits = ["hearts", "diamonds", "spades", "clubs"] # Allows me to loop through this and go through each suit in each loop
Deck = [] #Deck list
discardPile = []
for x in Suits: #Repeat for each 4 suits
    for y in range(2,15): # Repats from ranks 2-14
        if y == 11 and (x == "spades" or x == "clubs"): #ranks 11, 12, 13, 14 have special names so have a special condtion for them
            card = [("Jack of " + x),y,x] # makes a card with the name, rank then suit as a list, then adds this list to the deck list
            Deck.append(card)             # making a 2d array
        elif y == 12 and (x == "spades" or x == "clubs"):
            card = [("Queen of " + x), y, x]
            Deck.append(card)
        elif y == 13 and (x == "spades" or x == "clubs"):
            card = [("King of " + x), y, x]
            Deck.append(card)
        elif y == 14 and (x == "spades" or x == "clubs"):
            card = [("Ace of " + x), y, x]
            Deck.append(card)
        elif y <= 10:
            card = [(str(y) + " of " + x), y, x]
            Deck.append(card)

random.shuffle(Deck)

tableCards = []
tableCount = 0


def drawButton(button, colour, words, wordx, wordy): #Function to draw buttons more efficiently
    pygame.draw.rect(screen, colour, button)
    pygame.draw.rect(screen, BLACK, button, 3)
    textSurface = font.render(words, True, BLACK)
    screen.blit(textSurface, (button.x + wordx, button.y + wordy))

def drawCard(x,y,name,suit): #Function to draw placeholder carde
    if suit == "hearts" or suit == "diamonds": #changes text to match suit
        tempColour = RED
    else:
        tempColour = BLACK
    pygame.draw.rect(screen, WHITE, (x,y,150,200)) #draws a white rectangle for card base
    pygame.draw.rect(screen, BLACK, (x, y, 150, 200),3)
    textSurface = font.render(name, True, tempColour) #Then draws the cards name on top
    screen.blit(textSurface, ((x + 10, y + 10)))

while running: #The Main running loop where everything on the screen will update
    for event in pygame.event.get(): #Checks all events
        if event.type == pygame.QUIT: #If the X button is pressed
            running = False #Stops the running loop which stops the program
        if event.type == pygame.MOUSEBUTTONUP:
            if QuitButton.collidepoint(pygame.mouse.get_pos()) and menuOpen == 'Main': #Checks if your on the right menu
                running = False
            if PlayButton.collidepoint(pygame.mouse.get_pos()) and menuOpen == 'Main':
                menuOpen = 'Play'
                random.shuffle(Deck)
            if SettingsButton.collidepoint(pygame.mouse.get_pos()) and menuOpen == 'Main':
                menuOpen = 'Settings'
            if MenuButton.collidepoint(pygame.mouse.get_pos()) and (menuOpen == 'Settings' or menuOpen == 'Play'):
                if menuOpen == 'Play':
                    for x in tableCards:
                        Deck.append(x)
                    tableCards = []
                    tableCount = 0
                menuOpen = 'Main'
            if menuOpen == 'DisplayDeck':
                if pygame.Rect(0,0,1200,800).collidepoint(pygame.mouse.get_pos()): #check if anywhere on the screen has opened
                    menuOpen = 'Play' #returns back to play
            if menuOpen == 'Play':
                count = 0
                for x in tableCards: #checks each card on the table
                    if pygame.Rect(325 + (160 * count), 100, 150, 200).collidepoint(pygame.mouse.get_pos()):#if the card on the table has been clicked
                        discardPile.append(x) #moves the card from table to discard
                        tableCards.remove(x)
                        tableCount -= 1
                    count += 1
                if DeckRect.collidepoint(pygame.mouse.get_pos()): #if you click on the deck
                    menuOpen = 'DisplayDeck' #sends you to the deck preview area




    if menuOpen == 'Main': #Checks which menu is open, and draws the correct screen
        screen.fill(GREY) #Sets the screen white
        drawButton(QuitButton, RED, "Quit", 75, 40)
        drawButton(PlayButton, GREEN, "Play", 75, 40)
        drawButton(SettingsButton, BLUE, "Settings", 55, 40)

    if menuOpen == 'Play':
        screen.fill(GREY) #fills the screen and draws the decks
        drawButton(MenuButton, RED, "Menu", 50, 30)
        pygame.draw.rect(screen, RED, DeckRect)
        pygame.draw.rect(screen, BLACK, DeckRect, 3)
        pygame.draw.rect(screen, RED, DiscardRect)
        pygame.draw.rect(screen, BLACK, DiscardRect, 3)

        textSurface = font.render("Cards: %d" % (len(Deck)), True, BLACK)  # Draws the number of cards in the deck
        screen.blit(textSurface, ((10,50)))
        textSurface = font.render("Cards: %d" % (len(discardPile)), True, BLACK)  # And the discard
        screen.blit(textSurface, ((1000, 760)))

        if tableCount < 2: #while there are less than 4 cards on the table,
            while tableCount != 4:
                card = Deck[0] #adds cards from deck to table untill there are 4
                tableCards.append(card)
                Deck.remove(Deck[0])
                tableCount += 1

        count = 0
        for x in tableCards: # For each card on the table, draws the card
            drawCard(325 + (160*count), 100, x[0], x[2])
            count += 1

    if menuOpen == 'Settings':
        screen.fill(GREY)
        drawButton(MenuButton, RED, "Menu", 50, 30)

    if menuOpen == 'DisplayDeck':
        screen.fill(GREY)
        count = 0
        for x in range(2,10):
            for y in Deck:
                if y[2] == 'hearts' and y[1] == x:
                    drawCard(100,(100+(count*40)),y[0],y[2])
                    count += 1
        #for x in Deck:
           # if x[2] == 'h':
            #drawCard(100 + (count * 160), 400, x[0], x[2])
           # count += 1

    pygame.display.update() #Finishes the running loop, then updating the screen with the changes
