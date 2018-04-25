## Coded by SergentThomasKelly
################################################################################
#                          INITIALISATION                                      #
################################################################################
import pygame as pg; import sys; import pytmx; import os
import savesystem as save; from settings import *


################################################################################
#                             CLASS GAME                                       #
################################################################################
class Game:
    """ This class is responsible for the well shape of the whole game.
        In fact, this class IS the game. Firstly we initialize Pygame, then we
        load every bit of data we need to use, and the we run the game. First,
        we listen to keys and mouse inputs and then we render the screen."""
    # >>> INITIALISATION >>>
    def __init__(self):
        self.state = 'starting'
        self.debugMode = False
        self.offline = False
        self.decalageX, self.decalageY = 128,0
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(True)
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(100, 100)
        self.loadEverything()
        if self.debugMode == True:
            print('debugMode activé')
            self.washTheScreen()
            if self.debug():
                self.clear()
                self.run()
            else:
                self.changeMenu("mainMenu")
        else:
            self.changeMenu("mainMenu")

    # >>> HERE'S THE GOD MODE, FOR THE GOD DAMN CREATOR ! >>>
    def debug(self):
        print(" =================== WELCOME IN DEBUG MODE ! ==================== ")
        print(" |        [1] - Enter state :                                   | ")
        print(" |        [2] - Cheat Mode :                                    | ")
        print(" ================================================================ ")
        self.debugCommand = input("[?] >>> Input something : ")
        if self.debugCommand == "1":
            self.clear(); print("[i] >>> [mainMenu, newMenu, settingsMenu, helpMenu, playMenu, game]")
            self.debugState = input("[?] >>> What state to load ? "); self.state = self.debugState
            return True
        if self.debugCommand == "2":
            self.clear(); print("[!] Entered in cheat menu.")
            return False

    # >>> LOAD EVERYTHING WE NEED ONCE FOR ALL >>>
    def loadEverything(self):
        gameFolder = os.path.dirname(__file__)
        imgFolder = os.path.join(gameFolder, 'sprites')
        plyrSpriteFolder = self.playerFolder = os.path.join(imgFolder,'player')
        femaleFolder = self.femaleFolder = os.path.join(plyrSpriteFolder, 'female'); maleFolder  = self.maleFolder = os.path.join(plyrSpriteFolder,'male')
        musicFolder = os.path.join(gameFolder, 'music')
        fontFolder = os.path.join(gameFolder, 'font')
        loadingFolder = os.path.join(imgFolder, 'loading')
        menuFolder = os.path.join(imgFolder, 'menus')
        mapFolder = os.path.join(gameFolder, 'map')
        iconFolder = os.path.join(imgFolder, 'icon'); self.icon = pg.image.load(os.path.join(iconFolder,'icon2.png')).convert_alpha(); pg.display.set_icon(self.icon)
        self.clear = lambda: os.system('cls')
        self.loadingScreen = pg.image.load(os.path.join(loadingFolder, 'loading.png')).convert_alpha()
        self.warningVersion = pg.image.load(os.path.join(loadingFolder, "warn.png")).convert_alpha()
        self.state = 'loadingScreen'; self.renderWindow()
        self.guiFont= pg.font.Font(os.path.join(fontFolder, 'Savior1.ttf'), 95)
        self.guiFontSub = pg.font.Font(os.path.join(fontFolder, 'Savior1.ttf'), 65)
        self.screenWasher = pg.Surface(self.screen.get_size()).convert_alpha(); self.screenWasher.fill((0, 0, 0, 255))
        self.colorGrey = (128,128,128); self.colorWhite = (255,255,255)
        self.allSprites = pg.sprite.LayeredUpdates()
        self.mapPic = pg.image.load(os.path.join(mapFolder, 'l1.png')).convert_alpha()
        self.mapWIDTH = self.mapPic.get_width; self.mapHEIGHT = self.mapPic.get_height
        self.dimScreen = pg.Surface(self.screen.get_size()).convert_alpha(); self.dimScreen.fill((0, 0, 0, 200))
        self.playerImgFemale =  pg.image.load(os.path.join(femaleFolder, 'ante.png')).convert_alpha()
        self.playerImgMale = pg.image.load(os.path.join(maleFolder, 'ante.png')).convert_alpha()
        self.femalePreview = pg.image.load(os.path.join(plyrSpriteFolder, 'female.png')).convert_alpha(); self.femalePreview = pg.transform.scale(self.femalePreview, (500,500))
        self.malePreview = pg.image.load (os.path.join(plyrSpriteFolder, 'male.png')).convert_alpha(); self.malePreview = pg.transform.scale(self.malePreview, (500,500))
        self.menuNukem = pg.image.load(os.path.join(menuFolder, "main.jpg")).convert(); self.menuNukem = pg.transform.scale(self.menuNukem, (500,500))
        self.playButton = pg.image.load(os.path.join(menuFolder, "play.jpg")).convert(); self.playButton = pg.transform.scale(self.playButton, (500,500))
        self.settingsWheel = pg.image.load(os.path.join(menuFolder, "settings.jpg")).convert()
        self.actualChoicePreview = self.screenWasher
        self.textColorPlay = self.textColorSettings = self.textColorHelp = self.textColorQuit = self.colorGrey
        self.textColorContinue = self.textColorNewGame = self.textColorReturn = self.colorGrey
        self.textColorMale = self.textColorFemale = self.textColorReturn = self.colorGrey
        self.textColorMusicToggle = self.textColorFullscreenToggle = self.textColordisplayFPSToggle = self.resetSaveColor = self.resetSettingsColor = self.textColorReturn = self.colorGrey
        self.textColorResume = self.textColorQuitGame = self.textColorMainMenu = self.colorGrey
        self.textColorReturn = self.colorGrey
        self.textColorYes = self.textColorNo = self.colorGrey
        self.lastMove = "+Y"
        self.mapPosX = self.decalageX; self.mapPosY = self.decalageY
        if os.path.isfile("settings.txt"):
            settingsSaved = save.readSettings()
            self.musicState=settingsSaved[0]; self.fullscreenState=settingsSaved[1]; self.displayFPS=settingsSaved[2]
            if self.fullscreenState == "ON":
                pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.musicState = "ON"; self.displayFPS = "OFF"; self.fullscreenState = "OFF"
        self.wallsList = []
        for walls in WALLS:
            self.wallsList.append((walls[0]+self.decalageX, walls[1]+self.decalageY,
                    walls[2], walls[3]))
        self.posX = POS[0]+self.decalageX; self.posY = POS[1]+self.decalageY
        self.mainMenuMusic = pg.mixer.Sound(os.path.join(musicFolder, 'mainMenu.ogg'))
        self.playMusic = pg.mixer.Sound(os.path.join(musicFolder, 'play.ogg'))

    # >>> CHANGE THE MENU YOU ARE INTO >>>
    def changeMenu (self, nextState):
        pg.key.set_repeat(0, 100); self.previousState = self.state; pg.mouse.set_visible(True)
        if nextState == "pause":
            self.screen.blit(self.dimScreen,(0,0))
            if self.musicState == "ON" and pg.mixer.Channel(0).get_busy():
                pg.mixer.Channel(0).pause()
        else:
            self.washTheScreen()
            if nextState == "mainMenu":
                if not pg.mixer.Channel(0).get_busy() or pg.mixer.Channel(0).get_sound() != self.mainMenuMusic:
                    if self.musicState == "ON":
                        pg.mixer.Channel(0).play(self.mainMenuMusic, -1)
        self.state = nextState
        self.run()

    # >>> LET THE MAGIC HAPPEN >>>
    def continueGame(self):
        pg.mouse.set_visible(False)
        if self.musicState == "ON":
            if pg.mixer.Channel(0).get_sound() != self.playMusic:
                pg.mixer.Channel(0).play(self.playMusic, -1)
            if self.state == 'pause':
                pg.mixer.Channel(0).unpause()
        actualGame = save.readGame()
        self.gender = actualGame[0]; self.lifeLevel = actualGame[1]; self.gameLevel = actualGame[2]
        print("I'm a {} and I have {} percent life and I'm in level {}".format(actualGame[0],self.lifeLevel, self.gameLevel))
        if self.gender == 'male':
            self.playerImg = self.playerImgMale
        else:
            self.playerImg = self.playerImgFemale
        self.picCoordinates = playerAnimation('noneDown', self.gender)
        self.washTheScreen(); pg.key.set_repeat(100, 100); self.previousState = self.state
        self.state = 'game'
        self.run()

    # >>> VERIFY IF THE PLAYER WANTS TO QUIT GAME >>>
    def areYouSure(self):
        self.washTheScreen(); pg.key.set_repeat(0, 100); self.previousState = self.state
        pg.mouse.set_visible(True)
        self.state = 'areYouSureToQuit'
        self.run()

    # >>> VERIFY IF THE PLAYER WANTS TO QUIT GAME >>>
    def areYouSureToDestroy(self):
        self.washTheScreen(); pg.key.set_repeat(0, 100); self.previousState = self.state
        self.state = 'areYouSureToDestroy'
        self.run()

    # >>> WASH THE SCREEN >>>
    def washTheScreen(self):
        self.screen.blit(self.screenWasher, (0,0))
        pg.display.update()

    # >>> TOGGLE FULLSCREEN MODE >>>
    def toggleFullscreen(self):
        if self.screen.get_flags() != pg.FULLSCREEN:
            pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN); self.fullscreenState = "ON"
        else:
            pg.display.set_mode((WIDTH, HEIGHT)); self.fullscreenState = "OFF"

    # >>> TOGGLE MUSIC STATE >>>
    def toggleMusic(self):
        if self.musicState == "ON":
            self.musicState = "OFF"
            if pg.mixer.Channel(0).get_busy():
                pg.mixer.Channel(0).stop()
        else:
            self.musicState = "ON"
            pg.mixer.Channel(0).play(self.mainMenuMusic, -1)

    # >>> TOGGLE FPS COUNTER >>>
    def toggleFPS(self):
        if self.displayFPS == "ON":
            self.displayFPS = "OFF"
        else:
            self.displayFPS = "ON"

    # >>> INFINITE LOOP TO LISTEN KEYS AND THEN RENDER WINDOW >>>
    def run(self):
        while True:
            self.clock.tick(60);
            if self.displayFPS == "ON":
                pg.display.set_caption(str(TITLE)+"  -- FPS :"+str(int(self.clock.get_fps())))
            else:
                pg.display.set_caption(TITLE)
            self.renderWindow()
            if self.state == "game":
                self.collideWithWalls()
            self.KeyListener()

    # >>> COLLISION DETECTION (WITH WALLS OF COURSE) >>>
    def collideWithWalls(self):
        for walls in self.wallsList:
            if self.persoRect.colliderect(walls):
                if self.lastMove == "+X":
                    self.posX -= 16
                elif self.lastMove == "+Y":
                    self.posY -= 16
                elif self.lastMove == "-X":
                    self.posX += 16
                elif self.lastMove == "-Y":
                    self.posY += 16

    # >>> SCROLLING SYSTEM >>>
    def scrolling(self):
        reload = 0
        if self.posX+128 >= WIDTH:
            self.mapPosX+=16; self.decalageX+= 16; self.posX+=16; reload+=1
        elif self.posY+128 >= HEIGHT:
            self.mapPosY-=16; self.decalageY-=16; self.posY-=16; reload+=1
        elif self.posX-128 <= 0:
            self.mapPosX-=16; self.decalageX-=16; self.posX-=16; reload+=1
        elif self.posY-128 <= 0:
            self.mapPosY+=16; self.decalageY+= 16; self.posY+=16; reload+=1
        if reload != 0:
            self.wallsList = []
            for walls in WALLS:
                self.wallsList.append((walls[0]+self.decalageX, walls[1]+self.decalageY,
                        walls[2], walls[3]))

    # >>> LISTEN INPUT FROM PLAYER (MOUSE, KEYS,...) >>>
    def KeyListener(self):
        # ========================================== GAME STATE ====================================================== #
        if self.state == 'game':
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s or event.key == pg.K_DOWN:
                        self.picCoordinates = playerAnimation('down',self.gender)
                        self.posY += 16; self.lastMove = "+Y"; self.scrolling()
                    if event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.picCoordinates = playerAnimation('right',self.gender)
                        self.posX += 16; self.lastMove = "+X"; self.scrolling()
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        self.picCoordinates = playerAnimation('up',self.gender)
                        self.posY -= 16; self.lastMove = "-Y"; self.scrolling()
                    if event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.picCoordinates = playerAnimation('left',self.gender)
                        self.posX -= 16; self.lastMove = "-X"; self.scrolling()
                    if event.key == pg.K_ESCAPE:
                        self.pause()
                elif event.type == pg.KEYUP:
                    if self.lastMove == "+Y":
                        self.picCoordinates = playerAnimation('noneDown', self.gender)
                    elif self.lastMove == "+X":
                        self.picCoordinates = playerAnimation('noneRight', self.gender)
                    elif self.lastMove == "-X":
                        self.picCoordinates = playerAnimation('noneLeft', self.gender)
                    elif self.lastMove == "-Y":
                        self.picCoordinates = playerAnimation('noneUp', self.gender)
                if event.type == pg.QUIT:
                    self.changeMenu("pause")
        # ========================================== PAUSE SCREEN ==================================================== #
        if self.state == 'pause':
            for event in pg.event.get():
                if self.resumeBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorResume = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('resume game'); self.continueGame()
                        break
                else:
                    self.textColorResume = self.colorGrey
                if self.mainMenuBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMainMenu = self.colorWhite; self.actualChoicePreview = self.malePreview
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print("main menu"); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorMainMenu = self.colorGrey
                if self.quitGameBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorQuitGame = self.colorWhite; self.actualChoicePreview = self.femalePreview
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print("quit game"); self.areYouSure()
                        break
                else:
                    self.textColorQuitGame = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        print("quit"); self.areYouSure()
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print("resume game"); self.continueGame()
                    if event.key == pg.K_SEMICOLON:
                        print("main menu"); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.quit()
        # ========================================== NEW GAME ======================================================== #
        if self.state == 'newGame':
            for event in pg.event.get():
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if self.maleChoiceBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMale = self.colorWhite; self.actualChoicePreview = self.malePreview
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print("male"); save.newGame("male"); self.continueGame()
                        break
                else:
                    self.textColorMale = self.colorGrey; self.actualChoicePreview = self.screenWasher
                if self.femaleChoiceBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorFemale = self.colorWhite; self.actualChoicePreview = self.femalePreview
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print("female"); save.newGame("female"); self.continueGame()
                        break
                else:
                    self.textColorFemale = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        print("female")
                    if event.key == pg.K_SEMICOLON:
                        print("male")
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print("return"); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.areYouSure()
        # ========================================== SETTINGS MENU =================================================== #
        if self.state == 'settingsMenu':
            for event in pg.event.get():
                if self.musicToggleBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMusicToggle = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.toggleMusic(); print('music toggle to ' + str(self.musicState))
                        break
                else:
                    self.textColorMusicToggle = self.colorGrey
                if self.fullScreenToggleBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorFullscreenToggle = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.toggleFullscreen(); print('fullscreen toggle to ' + str(self.fullscreenState))
                        break
                else:
                    self.textColorFullscreenToggle = self.colorGrey
                if self.resetSaveBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.resetSaveColor = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.lastDestroy = "saves"; self.areYouSureToDestroy()
                        break
                else:
                    self.resetSaveColor = self.colorGrey
                if self.resetSettingsBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.resetSettingsColor = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.lastDestroy = "settings" ; self.areYouSureToDestroy()
                        break
                else:
                    self.resetSettingsColor = self.colorGrey
                if self.displayFPSToggleBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColordisplayFPSToggle = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.toggleFPS(); print('displayFPS toggle to ' + str(self.displayFPS))
                        break
                else:
                    self.textColordisplayFPSToggle = self.colorGrey
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SEMICOLON:
                        self.washTheScreen(); self.toggleMusic(); print('music toggle to ' + str(self.musicState))
                    if event.key == pg.K_f:
                        self.washTheScreen(); self.toggleFullscreen(); print('fullscreen toggle to ' + str(self.fullscreenState))
                    if event.key == pg.K_c:
                        self.washTheScreen(); self.toggleFPS(); print('displayFPS toggle to ' + str(self.displayFPS))
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS) ; self.mainMenu()
                if event.type == pg.QUIT:
                    self.areYouSure()
        # ========================================== SURE TO QUIT SCREEN ============================================= #
        if self.state == 'areYouSureToQuit':
            for event in pg.event.get():
                if self.yesBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorYes = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('yes'); self.quit()
                        break
                else:
                    self.textColorYes = self.colorGrey
                if self.noBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorNo= self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('no'); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorNo = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        print('yes'); self.quit()
                    if event.key == pg.K_n or event.key == pg.K_ESCAPE:
                        print('no'); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.quit()
        # ========================================== SURE TO DESTROY SCREEN ========================================== #
        if self.state == 'areYouSureToDestroy':
            for event in pg.event.get():
                if self.yesBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorYes = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('reset ' + str(self.lastDestroy))
                        if self.lastDestroy == "settings":
                            save.resetSettings(); self.restartGame()
                        elif self.lastDestroy == "saves":
                            save.resetSave(); self.changeMenu("settingsMenu")
                        break
                else:
                    self.textColorYes = self.colorGrey
                if self.noBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorNo= self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('no'); self.changeMenu("settingsMenu")
                        break
                else:
                    self.textColorNo = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        print('reset ' + str(self.lastDestroy))
                        if self.lastDestroy == "settings":
                            save.resetSettings(); self.restartGame()
                        elif self.lastDestroy == "saves":
                            save.resetSave(); self.changeMenu("settingsMenu")
                    if event.key == pg.K_n or event.key == pg.K_ESCAPE:
                        print('no'); self.changeMenu("settingsMenu")
                if event.type == pg.QUIT:
                    self.areYouSure()
        # ========================================== PLAY MENU ======================================================= #
        if self.state == 'playMenu':
            for event in pg.event.get():
                if os.path.isfile("savegames.txt") == True:
                    if self.continueBlit.collidepoint(pg.mouse.get_pos()) == True:
                        self.textColorContinue = self.colorWhite
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            print('continue'); self.continueGame()
                            break
                    else:
                        self.textColorContinue = self.colorGrey
                else:
                    if self.newGameBlit.collidepoint(pg.mouse.get_pos()) == True:
                        self.textColorNewGame= self.colorWhite
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            print('new game'); self.changeMenu("newGame")
                            break
                    else:
                        self.textColorNewGame = self.colorGrey
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        print('continue')
                    if event.key == pg.K_n:
                        print('new game'); self.changeMenu("newGame")
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.areYouSure(); print('quit')
        # ========================================== MAIN MENU ======================================================= #
        if self.state == 'mainMenu':
            for event in pg.event.get():
                if self.playOptionBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorPlay = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('play'); self.changeMenu("playMenu")
                        break
                else:
                    self.textColorPlay = self.colorGrey
                if self.settingsOptionBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorSettings = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('settings'); self.changeMenu("settingsMenu")
                        break
                else:
                    self.textColorSettings = self.colorGrey
                if self.helpOptionBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorHelp = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('help'); self.changeMenu("helpMenu")
                        break
                else:
                    self.textColorHelp = self.colorGrey
                if self.quitOptionBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorQuit = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print("quit"); self.areYouSure()
                        break
                else:
                    self.textColorQuit = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        print('play'); self.changeMenu("playMenu")
                    if event.key == pg.K_s:
                        print('settings'); self.changeMenu("settingsMenu")
                    if event.key == pg.K_h:
                        print('help'); self.changeMenu("helpMenu")
                    if event.key == pg.K_a or event.key == pg.K_ESCAPE:
                        print('quit'); self.areYouSure()
                if event.type == pg.QUIT:
                    self.areYouSure()
        # ========================================== HELP MENU ======================================================= #
        if self.state == 'helpMenu':
            for event in pg.event.get():
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.areYouSure()

    # >>> RENDER THE WINDOW. REALLY. >>>
    def renderWindow(self):
        if self.state == 'loadingScreen':
            self.loadingBlit = self.screen.blit(self.loadingScreen,(0,0))
        if self.state == 'mainMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Main Menu", 4, (255,255,255)), (100,175))
            self.playOptionBlit = self.screen.blit(self.guiFontSub.render ("(P) - Play", 4, self.textColorPlay), (115, 250))
            self.settingsOptionBlit = self.screen.blit(self.guiFontSub.render ("(S) - Settings", 4, self.textColorSettings),(115, 300))
            self.helpOptionBlit = self.screen.blit(self.guiFontSub.render ("(H) - Help", 4, self.textColorHelp), (115, 350))
            self.quitOptionBlit = self.screen.blit(self.guiFontSub.render ("(Q) - Quit", 4, self.textColorQuit), (115, 400))
            self.menuNukemBlit = self.screen.blit(self.menuNukem, (700,100))
        if self.state == 'playMenu':
            self.titleBlit = self.screen.blit (self.guiFont.render("Play Menu", 4, (255,255,255)), (100,175))
            if os.path.isfile("savegames.txt") == True :
                self.continueBlit = self.screen.blit(self.guiFontSub.render("(C) - Continue", 4, self.textColorContinue), (115, 250))
            else:
                self.newGameBlit = self.screen.blit(self.guiFontSub.render ("(N) - New game", 4, self.textColorNewGame), (115, 250))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 300))
            self.playButtonBlit = self.screen.blit(self.playButton, (700,100))
        if self.state == 'newGame':
            self.titleBlit = self.screen.blit(self.guiFont.render("New Game", 4, (255,255,255)), (100,175))
            self.femaleChoiceBlit = self.screen.blit(self.guiFontSub.render("(F) - I'm a female.", 4 , self.textColorFemale), (115,250))
            self.maleChoiceBlit = self.screen.blit(self.guiFontSub.render("(M) - I'm a male.", 4, self.textColorMale), (115, 325))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 400))
            self.actualChoicePreviewBlit = self.screen.blit(self.actualChoicePreview, (700, 100))
        if self.state == 'settingsMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Settings Menu", 4, (255,255,255)), (100,175))
            self.musicToggleBlit = self.screen.blit(self.guiFontSub.render("(M) - Music : " + str(self.musicState), 4, self.textColorMusicToggle), (115, 250))
            self.fullScreenToggleBlit = self.screen.blit(self.guiFontSub.render("(F) - Fullscreen : " + str(self.fullscreenState), 4, self.textColorFullscreenToggle), (115,300))
            self.displayFPSToggleBlit = self.screen.blit(self.guiFontSub.render("(C) - FPS Counter : " + str(self.displayFPS),4, self.textColordisplayFPSToggle), (115,350))
            self.resetSaveBlit = self.screen.blit(self.guiFontSub.render("/!\ RESET SAVES /!\ ", 4, self.resetSaveColor),(115,400))
            self.resetSettingsBlit = self.screen.blit(self.guiFontSub.render("/!\ RESET SETTINGS /!\ ", 4, self.resetSettingsColor),(115,450))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 500))
            self.settiingsWheelBlit = self.screen.blit(self.settingsWheel, (700,100))
        if self.state == 'helpMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Help Menu", 4, (255,255,255)), (100,175))
            self.helpText1Blit = self.screen.blit(self.guiFontSub.render("This game is a project from SergentThomasKelly", 4, self.colorGrey), (115,250))
            self.helpText2Blit = self.screen.blit(self.guiFontSub.render("This is a post apolyptic game about strategy and", 4, self.colorGrey), (115,300))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("saving your life (at least). And Philosophy too.", 4, self.colorGrey), (115,350))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("> To move, use arrows and ZQSD or WASD. <", 4, self.colorGrey), (115,400))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 460))
        if self.state == 'areYouSureToQuit':
            self.titleBlit = self.screen.blit(self.guiFont.render("ARE YOU SURE ?", 4, (255,255,255)), (400,175))
            self.yesBlit = self.screen.blit(self.guiFontSub.render("(Y) - Yes, let me leave", 4, self.textColorYes), (300, 250))
            self.noBlit = self.screen.blit(self.guiFontSub.render("(N) - No, I regret, let me come back", 4, self.textColorNo), (300, 300))
        if self.state == 'areYouSureToDestroy':
            self.titleBlit = self.screen.blit(self.guiFont.render("SOME DATA WILL BE DESTROYED!", 4, (255,255,255)), (100,175))
            self.yesBlit = self.screen.blit(self.guiFontSub.render("(Y) - I don't care. Destroy.", 4, self.textColorYes), (115, 250))
            self.noBlit = self.screen.blit(self.guiFontSub.render("(N) - Don't destroy!", 4, self.textColorNo), (115, 350))
        if self.state == 'pause':
            self.titleBlit = self.screen.blit(self.guiFont.render("Paused", 4, (255,255,255)), (100,175))
            self.resumeBlit = self.screen.blit(self.guiFontSub.render("(R) - Resume game", 4, self.textColorResume), (115, 250))
            self.mainMenuBlit = self.screen.blit(self.guiFontSub.render("(M) - Main Menu", 4, self.textColorMainMenu), (115, 300))
            self.quitGameBlit = self.screen.blit(self.guiFontSub.render("(Q) - Quit", 4, self.textColorQuitGame), (115, 350))
        if self.state == 'game':
            self.screen.blit(self.screenWasher,(0,0))
            self.mapBlit = self.screen.blit(self.mapPic, (self.mapPosX, self.mapPosY))
            self.persoBlit = self.screen.blit(self.playerImg, (self.posX, self.posY), self.picCoordinates); self.persoRect = pg.Rect(self.posX, self.posY, self.persoBlit.w-2, self.persoBlit.h-2)
        if self.state != 'loading':
            self.screen.blit(self.warningVersion,(0,0))
        pg.display.update()

    # >>> DO YOU REALLY NEED COMMENTS FOR THIS ONE ? >>>
    def quit(self):
        pg.quit()
        sys.exit()

    # >>> RESTART THE WHOLE GAME >>>
    def restartGame(self):
        os.startfile(r"core.py")
        self.quit()

Game()
