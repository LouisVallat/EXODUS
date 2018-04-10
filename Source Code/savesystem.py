##Coded by SergentThomasKelly
################################################################################
#                          INITIALISATION                                      #
################################################################################
import os

################################################################################
#                          SAVE SYSTEM                                         #
################################################################################
# >>> CREATE A NEW GAME >>>
def newGame(gender):
    if os.path.isfile("savegames.txt") == True:
        savegames = open("savegames.txt","a")
        savegames.write("\n0:"+ "100:" + str(gender))
        savegames.close()
    else:
        savegames = open("savegames.txt","w")
        savegames.write("0:"+ "100:" + str(gender))
        savegames.close

# >>> READ GAME SAVES >>>
def readGame():
    savegames = open("savegames.txt","r")
    lastSave = savegames.readline(); savegames.close()
    lastSS = lastSave.split(":")
    level = lastSS[0]; life = lastSS[1]; gender = lastSS[2]
    return [gender, life, level]

# >>> SAVE GAME >>>
def saveGame(gender, life, level):
    savegames = open("savegames.txt","w")
    savegames.write(str(level)+":"+str(life)+":"+str(gender))
    savegames.close

# >>> RESET GAME SAVES >>>
def resetSave():
    if os.path.isfile("savegames.txt"):
        os.remove("savegames.txt")

# >>> SAVE SETTINGS >>>
def saveSettings(musicState,fullscreenState,fpsCounterState):
    if os.path.isfile("settings.txt")==True:
        settings = open("settings.txt","a")
        settings.write(str(musicState)+str(":")+str(fullscreenState)+str(":")+str(fpsCounterState)+str(":"))
        settings.close()
    else:
        settings = open("settings.txt","w")
        settings.write(str(musicState)+str(":")+str(fullscreenState)+str(":")+str(fpsCounterState)+str(":"))
        settings.close()

# >>> LOAD SETTINGS SAVED PREVIOUSLY >>>
def readSettings():
    settings = open("settings.txt","r")
    settingsSaved = settings.readline()
    settingsSaved = settingsSaved.split(":")
    musicState = settingsSaved[0]; fullscreenState = settingsSaved[1]; fpsCounterState = settingsSaved[2]
    return [musicState, fullscreenState, fpsCounterState]

# >>> RESET THE SETTINGS TO THE DEFAULT VALUES >>>
def resetSettings():
    if os.path.isfile("settings.txt"):
        os.remove("settings.txt")

# >>> WRITE ALL WALLS IN A TEXT >>>
def writeWalls(offline, map):
    wallstext = open("walls.txt","w")
    if not offline:
        for tile_object in map.mapDATA.objects:
            if tile_object.name == 'wall':
                    wallstext.write("("+str(tile_object.x)+","+str(tile_object.y)+","+str(tile_object.width)+","+str(tile_object.height)+"),\n")
    wallstext.close()
