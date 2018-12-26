## Coded by SergentThomasKelly
################################################################################
#                          INITIALISATION                                      #
################################################################################
import pygame as pg; import sys, pytmx, os, webbrowser
import savesystem as save; from settings import *;


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
        pg.joystick.init
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
        fxFolder = os.path.join(musicFolder,'fx')
        fontFolder = os.path.join(gameFolder, 'font')
        loadingFolder = os.path.join(imgFolder, 'loading')
        menuFolder = os.path.join(imgFolder, 'menus')
        mapFolder = os.path.join(gameFolder, 'map')
        iconFolder = os.path.join(imgFolder, 'icon'); self.icon = pg.image.load(os.path.join(iconFolder,'icon2.png')).convert_alpha(); pg.display.set_icon(self.icon)
        self.clear = lambda: os.system('cls')
        self.loadingScreen = pg.image.load(os.path.join(loadingFolder, 'loading.png')).convert_alpha()
        self.warningVersion = pg.image.load(os.path.join(loadingFolder, "warn.png")).convert_alpha()
        self.dialogBox = pg.image.load(os.path.join(menuFolder, 'ui.png')).convert_alpha(); #self.dialogBox = pg.transform.scale(self.dialogBox, (1280,300))
        self.state = 'loadingScreen'; self.renderWindow()
        self.guiFont= pg.font.Font(os.path.join(fontFolder, 'Savior1.ttf'), 95)
        self.guiFontSub = pg.font.Font(os.path.join(fontFolder, 'Savior1.ttf'), 65)
        self.dialogFont = pg.font.Font(os.path.join(fontFolder, 'ToxTypewriter.ttf'), 45)
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
        self.musicIcon = pg.image.load(os.path.join(menuFolder, "music.jpg")).convert()
        self.actualChoicePreview = self.screenWasher
        self.textColorPlay = self.textColorSettings = self.textColorHelp = self.textColorQuit = self.colorGrey
        self.textColorContinue = self.textColorNewGame = self.textColorReturn = self.colorGrey
        self.textColorMale = self.textColorFemale = self.textColorReturn = self.colorGrey
        self.textColorMusicToggle = self.textColorFullscreenToggle = self.textColordisplayFPSToggle = self.resetSaveColor = self.resetSettingsColor = self.textColorReturn = self.colorGrey
        self.textColorResume = self.textColorQuitGame = self.textColorMainMenu = self.colorGrey
        self.textColorMusicPlus = self.textColorMusicMoins = self.textColorFxPlus = self.textColorFxMoins = self.colorGrey
        self.textColorReturn = self.colorMusicMenu = self.textColorCredits = self.colorGrey
        self.textColorYes = self.textColorNo = self.textColorMusicMenu = self.textColorBandcamp = self.colorGrey
        self.lastMove = "+Y"
        self.mapPosX = self.decalageX; self.mapPosY = self.decalageY
        if os.path.isfile("settings.txt"):
            settingsSaved = save.readSettings()
            self.musicState=settingsSaved[0]; self.fullscreenState=settingsSaved[1]; self.displayFPS=settingsSaved[2]
            self.musicLevel=float(settingsSaved[3]); self.fxLevel=float(settingsSaved[4])
            if self.fullscreenState == "ON":
                pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.musicState = "ON"; self.displayFPS = "OFF"; self.fullscreenState = "OFF"; self.musicLevel = 0.5; self.fxLevel = 1.0
        self.wallsList = []
        for walls in WALLS:
            self.wallsList.append((walls[0]+self.decalageX, walls[1]+self.decalageY,
                    walls[2], walls[3]))
        self.posX = POS[0]+self.decalageX; self.posY = POS[1]+self.decalageY
        self.mainMenuMusic = pg.mixer.Sound(os.path.join(musicFolder, 'mainMenu.ogg'))
        self.playMusic = pg.mixer.Sound(os.path.join(musicFolder, 'play.ogg'))
        self.positiveFx = pg.mixer.Sound(os.path.join(fxFolder, 'positive.ogg'));self.negativeFx = pg.mixer.Sound(os.path.join(fxFolder, 'negative.ogg'))
        self.changeMenuFx = pg.mixer.Sound(os.path.join(fxFolder, 'changeMenu.ogg'))
        print("Joystick/Controller detected : " + str(pg.joystick.get_count()))
        if pg.joystick.get_count() >= 1:
            pg.joystick.Joystick(0).init()
            print("Hats detected : " + str(pg.joystick.Joystick(0).get_numhats()))
            print("Joystick name : " + str(pg.joystick.Joystick(0).get_name()))

    # >>> CHANGE THE MENU YOU ARE INTO >>>
    def changeMenu (self, nextState):
        pg.key.set_repeat(0, 100); self.previousState = self.state; pg.mouse.set_visible(True)
        if nextState == "pause":
            self.screen.blit(self.dimScreen,(0,0))
            save.saveGame(self.gender, self.lifeLevel, self.gameLevel)
            if self.musicState == "ON" and pg.mixer.Channel(0).get_busy():
                pg.mixer.Channel(0).pause()
        else:
            if self.musicState == "ON":
                pg.mixer.Channel(1).play(self.changeMenuFx, 0)
            self.washTheScreen()
            if nextState == "mainMenu":
                if not pg.mixer.Channel(0).get_busy() or pg.mixer.Channel(0).get_sound() != self.mainMenuMusic:
                    if self.musicState == "ON":
                        pg.mixer.Channel(0).play(self.mainMenuMusic, -1)
        self.state = nextState
        if self.state != 'loading':
            self.screen.blit(self.warningVersion,(0,0))
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

    # >>> TOGGLE FULLSCREEN MODE >>>
    def toggleFullscreen(self):
        if self.screen.get_flags() != pg.FULLSCREEN:
            pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN); self.fullscreenState = "ON"
            if self.musicState == "ON":
                pg.mixer.Channel(1).play(self.positiveFx, 0)
        else:
            pg.display.set_mode((WIDTH, HEIGHT)); self.fullscreenState = "OFF"
            if self.musicState == "ON":
                pg.mixer.Channel(1).play(self.negativeFx, 0)

    # >>> TOGGLE MUSIC STATE >>>
    def toggleMusic(self):
        if self.musicState == "ON":
            self.musicState = "OFF"
            if pg.mixer.Channel(0).get_busy():
                pg.mixer.Channel(0).stop()
        else:
            self.musicState = "ON"
            pg.mixer.Channel(0).play(self.mainMenuMusic, -1)
            pg.mixer.Channel(1).play(self.positiveFx, 0)

    # >>> TOGGLE FPS COUNTER >>>
    def toggleFPS(self):
        if self.displayFPS == "ON":
            self.displayFPS = "OFF"
            if self.musicState == "ON":
                pg.mixer.Channel(1).play(self.negativeFx, 0)
        else:
            self.displayFPS = "ON"
            if self.musicState == "ON":
                pg.mixer.Channel(1).play(self.positiveFx, 0)

    # >>> INFINITE LOOP TO LISTEN KEYS AND THEN RENDER WINDOW >>>
    def run(self):
        while True:
            self.clock.tick(60); self.lastUpdate = pg.time.get_ticks()
            if self.displayFPS == "ON":
                pg.display.set_caption(str(TITLE)+"  -- FPS :"+str(int(self.clock.get_fps())))
            else:
                pg.display.set_caption(TITLE)
            self.renderWindow()
            if self.state == "game":
                self.collideWithWalls()
            pg.mixer.Channel(0).set_volume(self.musicLevel); pg.mixer.Channel(1).set_volume(self.fxLevel)
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

    # >>> NICE DIALOG BOX >>>
    def dialogBoxShow(self, character, text):
        pg.key.set_repeat(0, 100); self.previousState = self.state; pg.mouse.set_visible(True)
        save.saveGame(self.gender, self.lifeLevel, self.gameLevel)
        self.screen.blit(self.dimScreen,(0,0))
        character += str(" said :")
        self.whoSpoke = character; self.textDialog = text
        self.state = "dialog"
        self.run()

    # >>> CHANGE MUSIC AND EFFECTS VOLUME >>>
    def changeVolume(self, channel, moreOrLess):
        self.washTheScreen()
        if moreOrLess == "more":
            if channel == "music":
                self.musicLevel += 0.25
                if self.musicLevel >= 1.25:
                    self.musicLevel = 1.0
            if channel == "fx":
                self.fxLevel += 0.25
                if self.fxLevel >= 1.25:
                    self.fxLevel = 1.0
        if moreOrLess == "less":
            if channel == "music":
                self.musicLevel -= 0.25
                if self.musicLevel <= -0.25:
                    self.musicLevel = 0.0
            if channel == "fx":
                self.fxLevel -= 0.25
                if self.fxLevel <= -0.25:
                    self.fxLevel = 0.0

    # >>> LISTEN INPUT FROM PLAYER (MOUSE, KEYS,...) >>>
    def KeyListener(self):
        # ========================================== GAME STATE ====================================================== #
        if self.state == 'game':
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    #print("Your position is X=" + str(self.posX) + " and Y=" + str(self.posY))
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
                        self.changeMenu("pause")
                    if self.posX >= 975 and self.posY <= 995:
                        if self.posY >= 285:
                            if not L1EVENTLIST[0]:
                                L1EVENTLIST[0] = True
                                self.dialogBoxShow("GOD",["Welcome in this game.", "Enjoy! And please report bugs."])
                    if event.key == pg.K_F11:
                        self.toggleFullscreen(); print('fullscreen toggled to ' + str(self.fullscreenState))
                elif event.type == pg.KEYUP:
                    if self.lastMove == "+Y":
                        self.picCoordinates = playerAnimation('noneDown', self.gender)
                    elif self.lastMove == "+X":
                        self.picCoordinates = playerAnimation('noneRight', self.gender)
                    elif self.lastMove == "-X":
                        self.picCoordinates = playerAnimation('noneLeft', self.gender)
                    elif self.lastMove == "-Y":
                        self.picCoordinates = playerAnimation('noneUp', self.gender)
                elif event.type == pg.QUIT:
                    self.changeMenu("pause")
        # ========================================== DIALOG BOX ====================================================== #
        if self.state == 'dialog':
            for event in pg.event.get():
                if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                    self.continueGame()
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
                        print("quit game"); self.changeMenu("areYouSureToQuit")
                        break
                else:
                    self.textColorQuitGame = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        print("quit"); self.changeMenu("areYouSureToQuit")
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
                        print("female"); save.newGame("female"); self.continueGame()
                    if event.key == pg.K_SEMICOLON:
                        print("male"); save.newGame("male"); self.continueGame()
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print("return"); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")
        # ========================================== MUSIC MENU ==================================================== #
        if self.state == 'musicMenu':
            for event in pg.event.get():
                if self.musicToggleBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMusicToggle = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.toggleMusic(); print('music toggle to ' + str(self.musicState))
                        break
                else:
                    self.textColorMusicToggle = self.colorGrey
                if self.musicButtonMoinsBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMusicMoins = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.changeVolume("music","less"); print("music - volume set to " +str(self.musicLevel))
                        break
                else:
                    self.textColorMusicMoins = self.colorGrey
                if self.musicButtonPlusBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMusicPlus = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.changeVolume("music","more"); print("music + volume set to " +str(self.musicLevel))
                        break
                else:
                    self.textColorMusicPlus = self.colorGrey
                if self.fxButtonMoinsBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorFxMoins = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.changeVolume("fx","less"); print("fx - volume set to " +str(self.musicLevel))
                        break
                else:
                    self.textColorFxMoins = self.colorGrey
                if self.fxButtonPlusBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorFxPlus = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.changeVolume("fx","more"); print("fx + volume set to " +str(self.musicLevel))
                        break
                else:
                    self.textColorFxPlus = self.colorGrey
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS, self.musicLevel, self.fxLevel)
                        self.changeMenu("settingsMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SEMICOLON:
                        self.washTheScreen(); self.toggleMusic(); print('toggle music')
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS, self.musicLevel, self.fxLevel)
                        self.changeMenu("settingsMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")
        # ========================================== SETTINGS MENU 2 ================================================= #
        if self.state == 'settingsMenu':
            for event in pg.event.get():
                if self.musicMenuBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorMusicMenu = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); print('music menu'); self.changeMenu("musicMenu")
                        break
                else:
                    self.textColorMusicMenu = self.colorGrey
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
                        self.washTheScreen(); self.lastDestroy = "saves"; self.changeMenu("areYouSureToDestroy")
                        break
                else:
                    self.resetSaveColor = self.colorGrey
                if self.resetSettingsBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.resetSettingsColor = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.washTheScreen(); self.lastDestroy = "settings" ; self.changeMenu("areYouSureToDestroy")
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
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS, self.musicLevel, self.fxLevel)
                        self.changeMenu("mainMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.washTheScreen(); self.changeMenu("musicMenu"); print('music menu')
                    if event.key == pg.K_f:
                        self.washTheScreen(); self.toggleFullscreen(); print('fullscreen toggle to ' + str(self.fullscreenState))
                    if event.key == pg.K_c:
                        self.washTheScreen(); self.toggleFPS(); print('displayFPS toggle to ' + str(self.displayFPS))
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); save.saveSettings(self.musicState, self.fullscreenState, self.displayFPS, self.musicLevel, self.fxLevel)
                        self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")
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
                        print('no'); self.changeMenu(self.previousState)
                        break
                else:
                    self.textColorNo = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        print('yes'); self.quit()
                    if event.key == pg.K_n or event.key == pg.K_ESCAPE:
                        print('no'); self.changeMenu(self.previousState)
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
                    self.changeMenu("areYouSureToDestroy")
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
                        print('continue'); self.continueGame()
                    if event.key == pg.K_n:
                        print('new game'); self.changeMenu("newGame")
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); self.changeMenu("mainMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit"); print('quit')
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
                        print("quit"); self.changeMenu("areYouSureToQuit")
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
                        print('quit'); self.changeMenu("areYouSureToQuit")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")
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
                if self.creditsBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorCredits = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('credits menu'); self.changeMenu("creditsMenu")
                        break
                else:
                    self.textColorCredits = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); self.changeMenu("mainMenu")
                    if event.key == pg.K_r or event.key == pg.K_c :
                        print('credits menu'); self.changeMenu("creditsMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")
        # ========================================== CREDITS MENU =================================================== #
        if self.state == 'creditsMenu':
            for event in pg.event.get():
                if self.returnBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorReturn = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('return'); self.changeMenu("helpMenu")
                        break
                else:
                    self.textColorReturn = self.colorGrey
                if self.openBandcampBlit.collidepoint(pg.mouse.get_pos()) == True:
                    self.textColorBandcamp = self.colorWhite
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        print('open bandcamp'); webbrowser.open("https://donbor.bandcamp.com", new=2)
                        break
                else:
                    self.textColorBandcamp = self.colorGrey
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r or event.key == pg.K_ESCAPE:
                        print('return'); self.changeMenu("helpMenu")
                if event.type == pg.QUIT:
                    self.changeMenu("areYouSureToQuit")

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
            self.fullScreenToggleBlit = self.screen.blit(self.guiFontSub.render("(F) - Fullscreen : " + str(self.fullscreenState), 4, self.textColorFullscreenToggle), (115,250))
            self.displayFPSToggleBlit = self.screen.blit(self.guiFontSub.render("(C) - FPS Counter : " + str(self.displayFPS),4, self.textColordisplayFPSToggle), (115,300))
            self.musicMenuBlit = self.screen.blit(self.guiFontSub.render("(A) - Audio Menu",4,self.textColorMusicMenu),(115,350))
            self.resetSaveBlit = self.screen.blit(self.guiFontSub.render("/!\ RESET SAVES /!\ ", 4, self.resetSaveColor),(115,400))
            self.resetSettingsBlit = self.screen.blit(self.guiFontSub.render("/!\ RESET SETTINGS /!\ ", 4, self.resetSettingsColor),(115,450))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 500))
            self.settingsWheelBlit = self.screen.blit(self.settingsWheel, (700,100))
        if self.state == 'musicMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Audio Menu", 4, (255,255,255)), (100,175))
            self.musicToggleBlit = self.screen.blit(self.guiFontSub.render("(M) - Music : " + str(self.musicState), 4, self.textColorMusicToggle), (115, 250))
            self.musicButtonPlusBlit = self.screen.blit(self.guiFontSub.render("+",4, self.textColorMusicPlus), (385,300))
            self.musicButtonMoinsBlit = self.screen.blit(self.guiFontSub.render("-",4, self.textColorMusicMoins), (115,300))
            self.musicBlit = self.screen.blit(self.guiFontSub.render("Music Level",4, self.colorGrey), (150,300))
            self.musicLevelBlit = self.screen.blit(self.guiFontSub.render("["+str(self.musicLevel)+"]",4,self.colorGrey),(420,300))
            self.fxButtonPlusBlit = self.screen.blit(self.guiFontSub.render("+",4, self.textColorFxPlus), (385,350))
            self.fxButtonMoinsBlit = self.screen.blit(self.guiFontSub.render("-",4, self.textColorFxMoins), (115,350))
            self.fxBlit = self.screen.blit(self.guiFontSub.render("FX Level",4, self.colorGrey), (175,350))
            self.fxLevelBlit = self.screen.blit(self.guiFontSub.render("["+str(self.fxLevel)+"]",4,self.colorGrey),(420,350))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 400))
            self.musicIconBlit = self.screen.blit(self.musicIcon, (700,100))
        if self.state == 'helpMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Help Menu", 4, (255,255,255)), (100,175))
            self.helpText1Blit = self.screen.blit(self.guiFontSub.render("This game is a project from SergentThomasKelly", 4, self.colorGrey), (115,250))
            self.helpText2Blit = self.screen.blit(self.guiFontSub.render("This is a post apolyptic game about strategy and", 4, self.colorGrey), (115,300))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("saving your life (at least). And Philosophy too.", 4, self.colorGrey), (115,350))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("> To move, use arrows and ZQSD or WASD. <", 4, self.colorGrey), (115,400))
            self.creditsBlit = self.screen.blit(self.guiFontSub.render ("(C) - Credits", 4, self.textColorCredits), (115, 460))
            self.returnBlit = self.screen.blit(self.guiFontSub.render ("(R) - Return", 4, self.textColorReturn), (115, 510))
        if self.state == 'creditsMenu':
            self.titleBlit = self.screen.blit(self.guiFont.render("Credits Menu", 4, (255,255,255)), (100,175))
            self.helpText1Blit = self.screen.blit(self.guiFontSub.render("Main Menu Music : Donbor - Void643", 4, self.colorGrey), (115,250))
            self.helpText2Blit = self.screen.blit(self.guiFontSub.render("Level1 Music : Donbor - Blind", 4, self.colorGrey), (115,300))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("Visit his bandcamp ", 4, self.colorGrey), (115,350))
            self.openBandcampBlit = self.screen.blit(self.guiFontSub.render(">here<", 4, self.textColorBandcamp), (500,350))
            self.helpText3Blit = self.screen.blit(self.guiFontSub.render("All credits to this artist ! He's doing an amazing job !", 4, self.colorGrey), (115,400))
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
        if self.state == 'dialog':
            self.screen.blit(self.dialogBox,(230,400))
            self.screen.blit(self.dialogFont.render(self.whoSpoke, 4, self.colorWhite), (275, 435))
            self.screen.blit(self.dialogFont.render(self.textDialog[0], 4, self.colorWhite), (300, 500))
            self.screen.blit(self.dialogFont.render(self.textDialog[1], 4, self.colorWhite), (300, 540))
            self.screen.blit(self.dialogFont.render("Press RETURN", 4, self.colorGrey),(710,635))
        pg.display.update()

    # >>> WASH THE SCREEN >>>
    def washTheScreen(self):
        self.screen.blit(self.screenWasher, (0,0))
        if self.state != 'loading':
            self.screen.blit(self.warningVersion,(0,0))
        pg.display.update()

    # >>> DO YOU REALLY NEED COMMENTS FOR THIS ONE ? >>>
    def quit(self):
        pg.quit()
        #sys.exit()

    # >>> RESTART THE WHOLE GAME >>>
    def restartGame(self):
        os.startfile(r"core.py")
        self.quit()

Game()
