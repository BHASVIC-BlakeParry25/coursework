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

#List of fonts:
font = pygame.font.Font(None,30)

menuOpen = 'Main' # Varible to keep track of which menu is open

Suits = ["Hearts", "diamonds", "spades", "clubs"] # Allows me to loop through this and go through each suit in each loop
Deck = [] #Deck list
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

for z in Deck:
    print(z) #Tempary check, amde before loop otherwise I would crash python printing a large list multiple times per second

def drawButton(button, colour, words, wordx, wordy): #Function to draw buttons more efficiently
    pygame.draw.rect(screen, colour, button)
    pygame.draw.rect(screen, BLACK, button, 3)
    textSurface = font.render(words, True, BLACK)
    screen.blit(textSurface, (button.x + wordx, button.y + wordy))

def drawCard(x,y,name,suit):
    if suit == "hearts" or suit == "diamonds":
        tempColour = RED
    else:
        tempColour = BLACK
    pygame.draw.rect(screen, WHITE, (x,y,150,200))
    pygame.draw.rect(screen, BLACK, (x, y, 150, 200),3)
    textSurface = font.render(name, True, tempColour)
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
            if SettingsButton.collidepoint(pygame.mouse.get_pos()) and menuOpen == 'Main':
                menuOpen = 'Settings'
            if MenuButton.collidepoint(pygame.mouse.get_pos()) and (menuOpen == 'Settings' or menuOpen == 'Play'):
                menuOpen = 'Main'


    if menuOpen == 'Main': #Checks which menu is open, and draws the correct screen
        screen.fill(GREY) #Sets the screen white
        drawButton(QuitButton, RED, "Quit", 75, 40)
        drawButton(PlayButton, GREEN, "Play", 75, 40)
        drawButton(SettingsButton, BLUE, "Settings", 55, 40)

    if menuOpen == 'Play':
        screen.fill(GREY)
        drawButton(MenuButton, RED, "Menu", 50, 30)
        pygame.draw.rect(screen, RED, DeckRect)
        pygame.draw.rect(screen, BLACK, DeckRect, 3)

        if tableCount < 4:
            card = Deck[0]
            tableCards.append(card)
            Deck.remove(Deck[0])
            tableCount += 1

        count = 0
        for x in tableCards:
            drawCard(325 + (160*count), 100, x[0], x[1])
            count += 1

    if menuOpen == 'Settings':
        screen.fill(GREY)
        drawButton(MenuButton, RED, "Menu", 50, 30)

    pygame.display.update() #Finishes the running loop, then updating the screen with the changes
