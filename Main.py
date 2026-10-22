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
DARKGREY = (100,100,100)

QuitButton = pygame.Rect(850, 500, 200, 100) #defines buttons as a rectangle
PlayButton = pygame.Rect(500, 500,200,100)
SettingsButton = pygame.Rect(150, 500, 200, 100)
MenuButton = pygame.Rect(1000, 50, 150, 75)
DeckRect = pygame.Rect(100,100,150,200)
DiscardRect = pygame.Rect(1000,550,150,200)
EscapeRect = pygame.Rect(100,350,150,60)

#List of fonts:
font = pygame.font.Font(None,30)
bigfont = pygame.font.Font(None,80)

menuOpen = 'Main' # Varible to keep track of which menu is open
DisplayDeckBackButton = pygame.Rect(75,650,150,75)
gameOver = False
hp = 20
maxHp = 20
Cooldown = 0

Suits = ["hearts", "diamonds", "spades", "clubs"] # Allows me to loop through this and go through each suit in each loop
Deck = [] #Deck list
discardPile = []
EscapeList = []
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print(Deck)
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
                    for x in discardPile:
                        Deck.append(x)
                    discardPile = []
                    tableCards = []
                    tableCount = 0
                    hp = 20
                    CoolDown = 0
                menuOpen = 'Main'
            if menuOpen == 'DisplayDeck' or menuOpen == 'DisplayDiscard':
                if DisplayDeckBackButton.collidepoint(pygame.mouse.get_pos()): #check if return button has been pressed
                    menuOpen = 'Play' #returns back to play
            if menuOpen == 'Play':
                count = 0
                for x in tableCards: #checks each card on the table
                    if pygame.Rect(325 + (160 * count), 100, 150, 200).collidepoint(pygame.mouse.get_pos()):#if the card on the table has been clicked
                        if x[2] == 'hearts': #If suit is hearts
                            hp += x[1] #heal hp = to rank
                            if hp > maxHp: #hp goes over max it sets hp to max
                                hp = maxHp
                        elif x[2] == 'spades' or x[2] == 'clubs': #repeat same process for spades and clubs but they harm you
                            hp -= x[1]
                            if hp < 0: #hp goes bellow 0 set it to 0
                                hp = 0
                        else:
                            pass
                        discardPile.append(x) #moves the card from table to discard
                        tableCards.remove(x)
                        tableCount -= 1
                        Cooldown -= 1 #decrease escape cooldown
                    count += 1
                if EscapeRect.collidepoint(pygame.mouse.get_pos()) and Cooldown <= 0: #If the escape buttons pressed and cooldown isnt 0
                    EscapeList = tableCards #sets the escapelist to the table cards
                    tableCards = [] #removes all the table cards
                    random.shuffle(EscapeList) #shuffles the escape cards list
                    for x in EscapeList: #then adds those cards back at the bottom of the deck
                        Deck.append(x)
                    tableCount = 0
                    Cooldown = 3 #set cooldwon back to 3

                if DeckRect.collidepoint(pygame.mouse.get_pos()): #if you click on the deck
                    menuOpen = 'DisplayDeck' #sends you to the deck preview area
                if DiscardRect.collidepoint(pygame.mouse.get_pos()):
                    menuOpen = 'DisplayDiscard'




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
        if Cooldown <= 0: #Draws the button a different colour if it's not able to be used
            drawButton(EscapeRect, WHITE, "Escape",40,20)
        else:
            drawButton(EscapeRect, DARKGREY, "Escape", 40, 20)

        textSurface = font.render("Hp: %d/%d" % (hp,maxHp), True, BLACK)  # Draws the hp/max hp
        screen.blit(textSurface, ((10, 10)))
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

        if hp == 0:
            gameOver = True
        if gameOver == True:
            pygame.draw.rect(screen, DARKGREY, (100,100,1000,600))
            textSurface = bigfont.render("You lose", True, WHITE)  # Draws the hp/max hp
            screen.blit(textSurface, ((150, 150)))


    if menuOpen == 'Settings':
        screen.fill(GREY)
        drawButton(MenuButton, RED, "Menu", 50, 30)

    if menuOpen == 'DisplayDeck':
        screen.fill(GREY)
        countH,countD,countS,countC = 0,0,0,0 #Set each count for each suit to 0
        for x in range(2,15): #for each rank
            for y in Deck: #check every card
                if y[2] == 'hearts' and y[1] == x: #if the ranks match draw it for each suit
                    drawCard(75,(75+(countH*40)),y[0],y[2])
                    countH += 1 #add 1 to the count for each suit so next time it is drawn in a different postion
                if y[2] == 'diamonds' and y[1] == x:
                    drawCard(275,(75+(countD*40)),y[0],y[2])
                    countD += 1
                if y[2] == 'spades' and y[1] == x:
                    drawCard(475,(75+(countS*40)),y[0],y[2])
                    countS += 1
                if y[2] == 'clubs' and y[1] == x:
                    drawCard(675,(75+(countC*40)),y[0],y[2])
                    countC += 1
        drawButton(DisplayDeckBackButton, RED, "Return", 40,25)
        textSurface = font.render("Draw Pile", True, BLACK)
        screen.blit(textSurface, ((10, 10)))

    if menuOpen == 'DisplayDiscard':
        screen.fill(GREY)
        countH,countD,countS,countC = 0,0,0,0 #Set each count for each suit to 0
        for x in range(2,15): #for each rank
            for y in discardPile: #check every card
                if y[2] == 'hearts' and y[1] == x: #if the ranks match draw it for each suit
                    drawCard(75,(75+(countH*40)),y[0],y[2])
                    countH += 1 #add 1 to the count for each suit so next time it is drawn in a different postion
                if y[2] == 'diamonds' and y[1] == x:
                    drawCard(275,(75+(countD*40)),y[0],y[2])
                    countD += 1
                if y[2] == 'spades' and y[1] == x:
                    drawCard(475,(75+(countS*40)),y[0],y[2])
                    countS += 1
                if y[2] == 'clubs' and y[1] == x:
                    drawCard(675,(75+(countC*40)),y[0],y[2])
                    countC += 1
        drawButton(DisplayDeckBackButton, RED, "Return", 40,25)
        textSurface = font.render("Discard Pile", True, BLACK)
        screen.blit(textSurface, ((10, 10)))


    pygame.display.update() #Finishes the running loop, then updating the screen with the changes
