import pygame
from pygame.locals import *
from pygame.mixer import *
import time
import ConfigParser
import sys


#loads tile table used to fill in pygame window
def load_tile_table(filename, width, height):
    #loads image then converts it
    image = pygame.image.load(filename)
    image = image.convert()

    #get image with and height
    image_width = image.get_width()
    image_height = image.get_width()
    tile_table = []

    #iterates through xtiles and ytiles and appends them to image
    for tile_x in range(0, image_width//width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height//height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))

    #returns tile table array
    return tile_table
    pass


class Level():
    #function to load the map file used to generate map
    def load_file(self, filename):
        self.puzzle1 = (10, 15)
        self.puzzle2 = (3, 8)
        self.puzzle3 = (15, 12)
        self.puzzle4 = (12, 4)
        #map will become a list of lists
        #key dict used to store info of tiles
        self.map = []
        self.key = {}
        #ConfigParser used to read through specified file
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        #gets map splits it up and is assigned as an array within an array
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        #height is the amount of rows in the list (map)
        #while width is the amount of items in a row (map[0])
        self.width = len(self.map[0])
        self.height = len(self.map)

    #function used to get current tile
    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    # another function used to test true or false values
    # used for high cohesion
    def get_bool(self, x, y, name):
        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    #function to check if tile is a wall
    def isWall(self, x, y):

        return self.get_bool(x, y, 'wall')

    #check if tile is a secret passage
    def isSecret(self, x, y):

        return self.get_bool(x, y, 'secret')
    
    #check to see if tile is finish
    def isFinish(self, x, y):

        return self.get_bool(x, y, 'finish')

    #function to check if tile is a puzzle
    def isPuzzle(self, x, y):
        
            return self.get_bool(x, y, 'puzzle')

    def puzzleComplete(self, puzzle):
        if(puzzle == puzzle1):
            puzzle1 = False
            puzzle = puzzle1
        if(puzzle == puzzle2):
            puzzle2 = False
            puzzle = puzzle2
        if(puzzle == puzzle3):
            puzzle3 = False
            puzzle = puzzle3
        if(puzzle == puzzle4):
            puzzle4 = False
            puzzle = puzzle4

        return puzzle

    # checks to see if tile blocks movement
    def isBlocking(self, x, y):
        
        value = self.get_tile(x, y).get(block)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')
    
    #renders map and prints it to screen
    def render(self):
        wall = self.isWall
        puzzle = self.isPuzzle
        secret = self.isSecret
        finish = self.isFinish
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}

        #go thru whole file and assign tiles from tile table
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    tile = 1, 0

                if secret(map_x, map_y):
                    tile = 1, 0
                elif puzzle(map_x, map_y):
                    tile = 0, 1
                elif finish(map_x, map_y):
                    tile = 0, 1
                else:
                    tile = 0, 0
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 0
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))

        #return the image and overlays for the map
        return image, overlays

#player class for the player on the level(duh.)
class Player():
    def __init__(self, x, y):
        #initializes player object with health air and a size
        #added coordinates for player as instance variables
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(( self.x, self.y), (30, 30))
        self.moves = 0
        self.health = 5
        self.air = 25

    def createPlayer(self):
        #creates the player sprite on the screen and gives image
        file = "player1.gif"

        player = pygame.sprite.Sprite()
        playerImage = pygame.image.load(file).convert_alpha()
        playerRect = self.rect

        #returns an image and a rect for the image
        return playerImage, playerRect
        
        
    #function to calculate how much air is left
    def airCounter(self):
        
        self.air -= 1
        airLeft = self.air

        print(airLeft)

        return airLeft
    
        if(totalAir % 5 == 0):
            #if the air is divisible by 5, depending on how high that is set pins
                pass

    def lifeAmount(self):
        health = self.health
        #set pins to match amount of health
        
        pass

    #function to calculate score
    def score(self):
        time = (pygame.time.get_ticks()//1000)
        
        air = self.airCounter()
        health = self.health
        #score is calculated so faster time = bigger multiplier
        score = air * health * ((1/time)*100)

        print(time, score)

        return score
    

    #print coordinates of player (use for debugging)
    def printCoords(self, x, y):
        print("{}, {}\n".format(x, y))

    #make player and put him in that location
    def playerLocation(self, x, y, f):
        
        file = f
        
        player = pygame.sprite.Sprite()
        playerImage = pygame.image.load(file).convert_alpha()
        playerRect = self.rect
        screen.blit(background, (0,0))
        screen.blit(playerImage, (self.x, self.y))

        return x, y


    #viewlimit function used to give character limited field of vision
    #l is the level it is referring to, x and y are the player coords
    def viewLimit(self, l, x, y):
        wall = l.isWall
        puzzle = l.isPuzzle
        secret = l.isSecret
        finish = l.isFinish
        tiles = MAP_CACHE[l.tileset]
        image = pygame.Surface((l.width*30, l.height*30))
        overlays = {}

        #make surfaces and load images
        view = pygame.Surface((17*30, 17*30))
        blankRect = pygame.Surface((30, 30))
        black = pygame.image.load('black.gif').convert_alpha()
        blank = pygame.image.load('blank.png').convert_alpha()
        transColor = blank.get_at((0,0))
        blank.set_colorkey(transColor)
        
        #goes through every tile in map
        for map_y, line in enumerate(l.map):
            for map_x, c in enumerate(line):
                #keeps gap of 2 in cardinal directions
                if(map_x <  self.x//30 - 2):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_x > self.x//30+2):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_y > self.y//30 + 2):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_y < self.y//30 - 2):
                    view.blit(black, (map_x * 30, map_y * 30))

                #draws top right corner of view
                elif(map_x > self.x//30 and map_y < self.y//30 -1):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_x > player.x//30 + 1 and map_y < player.y//30):
                    view.blit(black, (map_x * 30, map_y * 30))
                    
                #draws top left corner
                elif(map_x < self.x//30 and map_y < self.y//30 -1):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_x < self.x//30 - 1 and map_y < self.y//30):
                    view.blit(black, (map_x * 30, map_y * 30))
                    
                #draws bottom left corner
                elif(map_x < self.x//30 and map_y > self.y//30 + 1):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_x < self.x//30 - 1 and map_y > self.y//30):
                    view.blit(black, (map_x * 30, map_y * 30))
                    
                #draws bottom right corner
                elif(map_x > self.x//30 and map_y > self.y//30 + 1):
                    view.blit(black, (map_x * 30, map_y * 30))
                elif(map_x > self.x//30 + 1 and map_y > self.y//30):
                    view.blit(black, (map_x * 30, map_y * 30))
                #if the map is within the view add map tiles
                else:
                    if wall(map_x, map_y):
                        tile = 1, 0

                    elif secret(map_x, map_y):
                        tile = 1, 0
                    elif puzzle(map_x, map_y):
                        tile = 0, 1
                    elif finish(map_x, map_y):
                        tile = 0, 1
                    else:
                        tile = 0, 0
                        try:
                            tile = l.key[c]['tile'].split(',')
                            tile = int(tile[0]), int(tile[1])
                        except (ValueError, KeyError):
                            # Default to ground tile
                            tile = 0, 0
                            
                    tile_image = tiles[tile[0]][tile[1]]
                    view.blit(tile_image,
                           (map_x*30, map_y*30))
                
        return view
                
        
#main function of pygame used to create window
if __name__ == "__main__":
    screen = pygame.display.set_mode((510, 610))
    pygame.mixer.init()

    MAP_TILE_WIDTH = 30
    MAP_TILE_HEIGHT = 30
    MAP_CACHE = {
        'tileset.gif': load_tile_table('tileset.gif', MAP_TILE_WIDTH,
                                      MAP_TILE_HEIGHT),
    }

    #initialize level ovjects
    level = Level()
    level.load_file('level.py')

    level2 = Level()
    level3 = Level()
    level4 = Level()
    level5 = Level()

    #make player object
    player = Player(60, 420)
    player.moves = 0

    #make pygame clock
    clock = pygame.time.Clock()

    pygame.display.set_caption("Scuba Trouble")
    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()

    for (x, y), image in list(overlay_dict.items()):
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 30, y * 30)
        screen.blit(background, (0, 0))
    overlays.draw(screen)
    view = player.viewLimit(level ,player.x//30, player.y//30)
    #start l as level and counter @ 4
    l = level
    counter = 4

    image, rect = player.createPlayer()
    pygame.display.update()
    BLACK = (0,0,0)
    pygame.display.flip()

    #load music file
    pygame.mixer.music.load('beep2.wav')
    file = 'player.gif'

pygame.event.clear()
#while loop until game is over
game_over = False
while not game_over:

    #set view to viewLimit()
    #render that level and set background/overlay
    #blit view on to background and display player
    view = player.viewLimit(l ,player.x//30, player.y//30)
    background, overlay_dict = l.render()
    background.blit(view, (0,0))
    player.playerLocation(player.x, player.y, file)
    for event in pygame.event.get():
        
        #counter makes it so you can only get into each puzzle once
        #for every move check if these are true
        if(player.x//30 == 9 and player.y//30 == 14 and counter > 3):
            level.load_file('puzzle1.py')
            background, overlay_dict = level.render()
            l = level
            counter = counter
            view = player.viewLimit(level ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()
            player.x = 240
            player.y = 240
        

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))
        if (player.x//30 ==14 and player.y//30 ==4):
            player.air += 20
            counter -= 1
            print(counter)
            level2.load_file('level2.py')
            background, overlay_dict = level2.render()
            l = level2
            player.x = 270
            player.y = 420
            view = player.viewLimit(level2 ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()
            

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))
            
        if(player.x//30 == 2 and player.y//30 == 7 and counter > 2):
            player.air += 20
            counter -= 1
            print(counter)
            level3.load_file('level3.py')
            background, overlay_dict = level3.render()
            l = level3
            view = player.viewLimit(level3 ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))

            
        if(player.x//30 == 14 and player.y//30 == 11 and counter > 1):
            player.air += 20
            counter -= 1
            level4.load_file('level4.py')
            background, overlay_dict = level4.render()
            l = level4
            view = player.viewLimit(level4 ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))


        if(player.x//30 == 11 and player.y//30 == 3 and counter > 0):
            player.air += 20
            counter -= 1
            level5.load_file('level5.py')
            l = level5
            background, overlay_dict = level5.render()
            view = player.viewLimit(level5 ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))

        if(player.x//30 == 2 and player.y//30 == 2):
            player.air += 20
            counter -= 1
            level5.load_file('puzzle5.py')
            l = level5
            player.x = 240
            player.y = 450
            background, overlay_dict = level5.render()
            view = player.viewLimit(level5 ,player.x//30, player.y//30)
            overlays = pygame.sprite.RenderUpdates()

            for (x, y), image in list(overlay_dict.items()):
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * 30, y * 30)
                screen.blit(background, (0, 0))

        if (player.x//30 == 5 and player.y
            //30 == 1):    
            game_over = True
            print(player.score())
            pygame.quit()
            sys.exit()

        
        pygame.display.update()
        #based on user input adjust x or y coordinates of player (or exit)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not l.isWall(player.x//30, (player.y//30-1)):
                #adjust coord, printrect and adjust air (add more later)
                file = 'player4.gif'
                player.y -= 30
                player.playerLocation(player.x, player.y, file)
                player.airCounter()
                pygame.mixer.music.play(loops=0, start=0.0)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not l.isWall(player.x//30, (player.y//30+1)):
                file = 'player3.gif'
                player.y += 30
                player.playerLocation(player.x, player.y, file)
                player.airCounter()
                pygame.mixer.music.play(loops=0, start=0.0)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not l.isWall((player.x//30) + 1, player.y//30):
                file = 'player.gif'
                player.x += 30
                player.playerLocation(player.x, player.y, file)
                player.airCounter()
                pygame.mixer.music.play(loops=0, start=0.0)
                
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT and not l.isWall((player.x//30) - 1, player.y//30):
                file = 'player2.gif'
                player.x -= 30
                player.playerLocation(player.x, player.y, file)
                player.airCounter()
                pygame.mixer.music.play(loops=0, start=0.0)
    
    
    pygame.display.flip()
    clock.tick(15)
    screen.fill(BLACK)

    
pygame.quit()





