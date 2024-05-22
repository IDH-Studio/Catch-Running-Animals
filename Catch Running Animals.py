# 2020/01/23~
import pygame as pg
import os
import abc
import random
import sys
import copy
import json
import platform
from datetime import datetime
from Color import *
from enum import Enum

class Language(Enum):
    EN = 0
    KR = 1

# window variable
windowWidth = 400
windowHeight = 700
FPS = 60

# center of screen
windowPos = str((1920 // 2) - (windowWidth // 2)) + ", " + str((1080 // 2) - (windowHeight // 2))
os.environ["SDL_VIDEO_WINDOW_POS"] = windowPos

divide = "\\" if platform.system() == 'Windows' else "/"
print(divide)

imgDirStr = "_resources_images"
soundDirStr = "_resources_sounds_"

imgDirStr = imgDirStr.replace("_", divide)
soundDirStr = soundDirStr.replace("_", divide)

# basic image directory
imgDir = os.path.dirname(__file__) + imgDirStr
soundDir = os.path.dirname(__file__) + soundDirStr

pg.init()

throwSound = pg.mixer.Sound(soundDir + "throw.wav")
outSound = pg.mixer.Sound(soundDir + "out.wav")

curs, mask = pg.cursors.compile(pg.cursors.thickarrow_strings, 'X', '.')
pg.mouse.set_cursor((24, 24), (0, 0), curs, mask)
# curs, mask = pg.cursors.compile(pg.cursors.sizer_x_strings, 'X', '.')
# pg.mouse.set_cursor((24, 16), (0, 0), curs, mask)
# pg.mouse.set_cursor(*pg.cursors.tri_left)

# set_mode flags
# FULLSCREEN : 전체화면
# HWSURFACE : 하드웨어 가속 사용 (FullScreen Only)
# OPENGL : OpenGL 사용
# DOUBLEBUF : 더블 버퍼 사용, HWSURFACE, OPENGL에서 사용 추천
window = pg.display.set_mode((windowWidth, windowHeight))
pg.display.set_caption("Catch Running Animals")
screenSurf = pg.Surface((windowWidth, windowHeight))
screen = screenSurf.get_rect()
clock = pg.time.Clock()
BG = None
BG_Rect = None

def flip():
    window.fill(WHITE)
    pg.display.flip()

def getTime():
    return datetime.now()

def getTick():
    return pg.time.get_ticks()

def showText(color, pos, *text, fontSize=16):
    # if gameData["lang"] == Language.EN.value:
    #     font = pg.font.SysFont("comicsansms", fontSize)
    # elif gameData["lang"] == Language.KR.value:
    #     font = pg.font.SysFont("malgungothic", fontSize)
    font = pg.font.SysFont("나눔고딕otfextraboldregularopentype", fontSize)
    margin = 5
    for txt in text:
        if type(txt) == list:
            xPos = pos[0]
            yPos = pos[1]
            for t in txt:
                textObj = font.render(t, True, color)
                textRect = textObj.get_rect()
                window.blit(textObj, (xPos, yPos))
                yPos += fontSize + margin
        elif type(txt) == str:
            textObj = font.render(txt, True, color)
            textRect = textObj.get_rect()
            window.blit(textObj, pos)

def isClick(targetA, targetB):
    # targetA = (x, y, right, bottom)
    x1 = targetA[0]
    y1 = targetA[1]
    x2 = targetA[2]
    y2 = targetA[3]

    x, y = targetB

    if x1 < x < x2 and y1 < y < y2:
        return True
    else:
        return False

def drawScreen(function):
    function()
    pg.display.flip()

def true_or_false():
    return random.choice((True, False))

def getImage(imgName, imageDir=None):
    if not imageDir is None:
        path = imgDir + divide + imageDir
    else:
        path = imgDir

    if imgName.endswith(".png") is False:
        imgName += ".png"

    image = pg.image.load(os.path.join(path, imgName)).convert_alpha()
    image.set_colorkey(BLACK)
    return image
    # return pg.image.load(os.path.join(path, imgName))
    # if os.path.isfile(imgName):
    #     return pg.image.load(os.path.join(path, imgName))
    # else:
    #     return False    

def isOddNum(num):
    if num % 2 is 0:
        return False
    else:
        return True

def isEvenNum(num):
    if num % 2 is 0:
        return True
    else:
        return False

def changeLanguage():
    menuScreen.changeLang()
    mainMenuScreen.changeLang()
    optionScreen.changeLang()
    setStoreItemData()
    store.changeLang()

def setStoreItemData():
    global StoreItemData, gameData
    if gameData["lang"] == Language.EN.value:
        StoreItemData = {
            "Foods": {
                "banana": {
                    "info": ["This is banana.", "Monkey's favorite food", "coooool :3"],
                    "price": 5,
                },
                "grass": {
                    "info": ["This is grass.", " Elephant's favorite food", " coooool :3"],
                    "price": 5,
                },
                "bamboo": {
                    "info": ["This is bamboo.", " Panda's favorite food", " coooool :3"],
                    "price": 5,
                },
            },
            "Net": {
                "info": ["You can catch an animal!"],
                "price": 10,
            },
            "Big Net": {
                "info": ["You can catch animals!"],
                "price": 10,
            },
            "Extend Max Ammo": {
                "info": ["Max Ammo +2"],
                "price": 10,
            },
            "Ironbar Upgrade": {
                "info": ["IronBar Upgrade"],
                "price": 10,
            },
            "Life recovery": { 
                "info": ["Life +1"],
                "price": 20,
            },
        }
    elif gameData["lang"] == Language.KR.value:
        StoreItemData = {
            "Foods": {
                "banana": {
                    "info": ["이건 바나나입니다.", "원숭이가 좋아하는", "음식입니다."],
                    "price": 5,
                },
                "grass": {
                    "info": ["이건 풀때기 입니다.", "코끼리가 좋아하는", "음식입니다."],
                    "price": 5,
                },
                "bamboo": {
                    "info": ["이건 대나무 입니다.", "빤다가 좋아하는", "음식입니다."],
                    "price": 5,
                },
            },
            "Net": {
                "info": ["그물로 한 마리의 동물을", "잡을 수 있습니다."],
                "price": 10,
            },
            "Big Net": {
                "info": ["대형 그물로 여러 마리의", "동물을 잡을 수 있습니다."],
                "price": 20,
            },
            "Extend Max Ammo": {
                "info": ["최대 탄약 +2"],
                "price": 10,
            },
            "Ironbar Upgrade": {
                "info": ["철창이 업그레이드 됩니다."],
                "price": 30,
            },
            "Life recovery": {
                "info": ["체력이 1회복 됩니다."],
                "price": 20,
            }
        }

def screenshot():
    global BG, BG_Rect
    rect = pg.Rect(0, 0, windowWidth, windowHeight)
    surf = window.subsurface(rect)
    pg.image.save(surf, imgDir + divide +"bg.png")

    BG = getImage("bg")
    BG_Rect = BG.get_rect()

def reset():
    '''
        When you press the Back to Mainmenu button
    '''
    global pauseCurTime
    pauseCurTime = 0

# gameData 저장 -> 게임 종료 시 호출
def save():
    print("save Data!")
    data = {
        "gameData": gameData,
        "animalData": AnimalData,
        "StageData": StageData,
    }
    with open("gameData.json", "w") as file:
        json.dump(data, file, indent="\t")

gameData = {}
# gameData 불러오기 -> 게임 실행 시 호출
def load():
    global gameData, AnimalData, StageData
    print("load Data!")
    with open("gameData.json", "r") as file:
        data = json.load(file)
    gameData = data["gameData"]
    AnimalData = data["animalData"]
    StageData = data["StageData"]
# 여기서 미리 gameData에 값을 저장함
load()

# Item Data
ItemData = {
    "throwDelayUp": 20,
    "throwDelayDown": -20,
    "speedUp": 0.2,
    "speedDown": -0.2,
    "damageUp": 1,
    "damageDown": -1,
    "coin": 1,
}
ItemTypes = list(ItemData.keys())

# Store Item Data
# itemName: "Item info explain"
# StoreItemData = {
    #     "Foods": {
    #         "banana": {
    #             "info": ["This is banana.", "Monkey's favorite food", "coooool :3"],
    #             "price": 5,
    #         },
    #         "grass": {
    #             "info": ["This is grass.", "Elephant's favorite food", "coooool :3"],
    #             "price": 5,
    #         },
    #         "bamboo": {
    #             "info": ["This is bamboo.", "Panda's favorite food", "coooool :3"],
    #             "price": 5,
    #         },
    #     },
    #     "Net": {
    #         "info": ["This is Net.", "You can catch an animal!"],
    #         "price": 10,
    #     },
    #     "Big Net": {
    #         "info": ["This is Big Net.", "You can catch animals!"],
    #         "price": 10,
    #     },
    #     "Extend Max Ammo": {
    #         "info": ["This is Extend Max Ammo.", "Max Ammo +2"],
    #         "price": 10,
    #     },
    #     "Ironbar Upgrade": {
    #         "info": ["This is Ironbar Upgrade.", "IronBar Upgrade"],
    #         "price": 10,
    #     },
    # }
setStoreItemData()
StoreItems = list(StoreItemData.keys())

# Animal Data
# "name": speed
AnimalData = {
    "monkey": {
        "speed": 3,
        "hp": 10,
        "food": "banana",
    },
    "elephant": {
        "speed": 2,
        "hp": 20,
        "food": "grass",
    },
    "panda": {
        "speed": 1,
        "hp": 30,
        "food": "bamboo",
    },
}
AnimalTypes = list(AnimalData.keys())

# Stage Data
# reversal -> True: Top, False: Bottom
# monkey: 45, 50
# elephant: 60, 70
StageData = {
    "1": {
        "animalType": "monkey",
        "width": 45,
        # "height": 50,
        # "reversal": true_or_false(),
        "timeOut": 60,
        "minSpawnDelay": 500,
        "maxSpawnDelay": 1000,
    },
    "2": {
        "animalType": "elephant",
        "width": 60,
        # "height": 70,
        # "reversal": true_or_false(),
        "timeOut": 70,
        "minSpawnDelay": 800,
        "maxSpawnDelay": 1200,
    },
    "3": {
        "animalType": "panda", # temporary
        "width": 45,
        # "reversal": true_or_false(),
        "timeOut": 80,
        "minSpawnDelay": 500,
        "maxSpawnDelay": 1000,
    }
}

# Value Variable
# 값 변수들
inGameData = {
    "Boundary": 5.5,
    "Days": "1",
    "curTime": 0,
    "isReversal": True,
}
pauseCurTime = 0
lastTime = getTick()
animalSpawnLastTime = getTick()
animalSpawnDelay = random.randint(StageData[inGameData["Days"]]["minSpawnDelay"], StageData[inGameData["Days"]]["maxSpawnDelay"])

# State Variable
# bool 변수들
gameRun = False
debugMode = False
isShowStat = False
isStageClear = False
isGameOver = False
isPause = False

# Classes
class Object(pg.sprite.Sprite):
    def __init__(self, imageName=None, speed=windowHeight // 140):
        super().__init__()
        if imageName != None:
            if imageName.endswith(".png") is False:
                imageName += ".png"
            self.image = getImage(imageName)
            self.image.convert_alpha()
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
        self.speed = speed

    @abc.abstractclassmethod
    def reset(self):
        pass


class Player(Object):
    def __init__(self):
        super().__init__()
        # width: 40, height: 50
        self.image = pg.Surface((40, 50))
        self.image.fill(RED)
        # self.image = getImage(self.imageName + "Idle", "player")
        # self.default = "player"
        # self.image = getImage(self.default, "player")
        # self.idleCount = 0
        # self.animationDelay = 0
        # self.direction = "Front"
        # self.idleImage = []
        # for i in range(1, 6):
        #     self.idleImage.append(getImage(self.default + self.direction + "Idle" + str(i), "player"))
        self.rect = self.image.get_rect()

        if inGameData["isReversal"] is True:
            self.rect.bottom = 0
        else:
            self.rect.bottom = windowHeight
        self.rect.right = windowWidth // 2

        self.life = 3
        self.maxLife = self.life
        self.lastTime = getTick()
        self.inv = Inventory(6)
        
        self.coin = 0
        self.throwDelay = 300
        self.ammo = 10
        self.maxAmmo = 10
        self.damage = 10 # Damage
        
        self.name = "Siming"
    
    def update(self):
        key = pg.key.get_pressed()

        # player move
        if key[pg.K_LEFT]:
            self.direction = "Left"
            self.rect.x += -self.speed
        if key[pg.K_RIGHT]:
            self.direction = "Right"
            self.rect.x += self.speed
        if key[pg.K_UP]:
            self.direction = "Front"
            self.rect.y += -self.speed
        if key[pg.K_DOWN]:
            self.direction = "Back"
            self.rect.y += self.speed
        if key[pg.K_SPACE]:
            self.throw()
        
        # collision to wall
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > windowWidth:
            self.rect.right = windowWidth
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > windowHeight:
            self.rect.bottom = windowHeight

        if inGameData["isReversal"] is True:            
            # collision to inGameData["Boundary"]
            if self.rect.bottom > windowHeight / inGameData["Boundary"]:
                self.rect.bottom = windowHeight / inGameData["Boundary"]
        else:            
            # collision to inGameData["Boundary"]
            if self.rect.y < windowHeight - windowHeight / inGameData["Boundary"]:
                self.rect.y = windowHeight - windowHeight / inGameData["Boundary"]
        
    # throw a food
    def throw(self):
        now = getTick()
        if now - self.lastTime > self.throwDelay:
            self.lastTime = now
            if 0 < self.ammo <= self.maxAmmo:
                throwSound.play()
                if debugMode is False:
                    self.ammo -= 1
                food = self.inv.slot[self.inv.curSlot].copy()
                food.setPos(self.rect.midtop, self.rect.bottom)
                mainSprite.add(food)
                playerFoods.add(food)
    
    def reload(self):
        self.ammo = self.maxAmmo

    def showLife(self):
        # scale(Surface, (width, height), DestSurface = None) -> Surface
        scale = 2
        uiImage = pg.transform.scale(self.image, (self.rect.width // scale, self.rect.height // scale))
        uiImageRect = uiImage.get_rect()

        uiX = screen.centerx + screen.centerx // 4
        uiY = 0
        uiWidth = screen.right - uiX

        margin = (uiWidth - (uiImageRect.width * self.maxLife)) // 4

        uiHeight = (margin * 2) + uiImageRect.height
        
        for uiPos in range(self.life):
            window.blit(uiImage, ((margin + ((margin + uiImageRect.width) * uiPos) + uiX), margin))

    def recover(self):
        if self.life < self.maxLife:
            self.life += 1
        else:
            pass

    def reset(self):
        self.__init__()


class Inventory:
    def __init__(self, slotCount=6):
        # self.image = pg.Surface((70, 70))
        self.image = getImage("inv_bg")
        # scale(Surface, (width, height), DestSurface = None) -> Surface
        # self.image = pg.transform.scale(self.image, (50, 50))
        # self.image.convert_alpha()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.slot = []
        self.slotCount = slotCount
        self.haveItem = []
        self.curSlot = 0
        self.x_margin = 5
        self.isVisible = gameData["invShow"]
        if gameData["invPos"] == "right":
            self.rect.x = windowWidth - self.x_margin - self.rect.width
        elif gameData["invPos"] == "left":
            self.rect.x = self.x_margin
        start_yPos = windowHeight / inGameData["Boundary"]
        end_yPos = windowHeight - (windowHeight / inGameData["Boundary"])
        self.y_margin = (((end_yPos - start_yPos) - (self.rect.height * self.slotCount)) / (self.slotCount + 1))

        for i in range(self.slotCount):
            self.slot.append(None)
        
        self.add(Food("banana", False))

    def add(self, item):
        # self.slot.append(item)
        # 만약 아이템이 슬롯안에 없다면
        # 빈 슬롯을 찾아 아이템을 넣는다.
        for i in range(self.slotCount):
            if self.slot[i] == None:
                self.haveItem = self.slot[i] = item
                break
            else:
                # 슬롯이 비어있지 않다면 
                # 슬롯에 있는 아이템의 타입과
                # 인자로 들어온 아이템의 이름을 비교하여
                # 같을 경우 바로 반복문을 빠져나온다.
                if item.foodType == self.slot[i].foodType:
                    break

    def draw(self):
        if self.isVisible is True:
            # 추후에 수정
            for i in range(self.slotCount):
                window.blit(self.image, (self.rect.x, (windowHeight / inGameData["Boundary"]) + (i * self.rect.height) + (self.y_margin * (i + 1))))
                if not self.slot[i] is None:
                    image = pg.transform.scale(self.slot[i].image, (self.rect.width, self.rect.height))
                    window.blit(image, (self.rect.x, (windowHeight / inGameData["Boundary"]) + (i * self.rect.height) + (self.y_margin * (i + 1))))
            pg.draw.rect(window, BLACK, (self.rect.x,
                                        (windowHeight / inGameData["Boundary"]) + (self.curSlot * self.rect.height) + (self.y_margin * (self.curSlot + 1)),
                                        self.rect.width, self.rect.height), 2)

    def show(self):
        if self.isVisible is True:
            for i in range(self.slotCount):
                window.blit(self.image, (self.rect.x, (windowHeight / inGameData["Boundary"]) + (i * self.rect.height) + (self.y_margin * (i + 1))))
                if not self.slot[i] is None:
                    image = pg.transform.scale(self.slot[i].image, (self.rect.width, self.rect.height))
                    window.blit(image, (self.rect.x, (windowHeight / inGameData["Boundary"]) + (i * self.rect.height) + (self.y_margin * (i + 1))))
            pg.draw.rect(window, BLACK, (self.rect.x,
                                        (windowHeight / inGameData["Boundary"]) + (self.curSlot * self.rect.height) + (self.y_margin * (self.curSlot + 1)),
                                        self.rect.width, self.rect.height), 2)

    def visibleConfig(self, isVisible):
        '''
            True: Visible
            False: Invisible
        '''
        gameData["invShow"] = isVisible
        self.isVisible = isVisible

    def changePos(self, invPos):
        if type(invPos) != str:
            print("Type Error!(invPos is not str)")
            return -1

        gameData["invPos"] = invPos
        if invPos == "right":
            self.rect.x = windowWidth - self.x_margin - self.rect.width
        elif invPos == "left":
            self.rect.x = self.x_margin

    def changeItem(self):
        self.curSlot += 1
        # 다음 슬롯이 인덱스를 넘어가거나 아무것도 없을 경우 첫 번째 인덱스로 넘어간다.
        if self.curSlot >= len(self.slot) or self.slot[self.curSlot] is None:
            self.curSlot = 0


class Animal(Object):
    def __init__(self, x, animalType, speed):
        super().__init__(speed=speed)
        if animalType == "monkey":
            self.image = pg.Surface((45, 50))
            self.image.fill(BROWN)
            self.hp = AnimalData[animalType]["hp"]
        elif animalType == "elephant":
            self.image = pg.Surface((60, 70))
            self.image.fill(SILVER)
            self.hp = AnimalData[animalType]["hp"]
        elif animalType == "panda":
            self.image = pg.Surface((60, 70))
            self.image.fill(BLACK)
            self.hp = AnimalData[animalType]["hp"]

        self.rect = self.image.get_rect()
        if inGameData["isReversal"] is True:
            self.rect.y = windowHeight
        else:
            self.rect.bottom = 0
        self.rect.x = x
        # self.animalType = animalType
        self.food = AnimalData[animalType]["food"]
    
    def update(self):
        # 화면 밖으로 벗어났을 때
        if inGameData["isReversal"] is True:
            self.rect.y += -self.speed
            # beyond screen
            if self.rect.bottom < 0:
                if not debugMode is True:
                    outSound.play()
                    player.life -= 1
                self.kill()
        else:
            self.rect.y += self.speed
            # beyond screen
            if self.rect.y > windowHeight:
                if not debugMode is True:
                    outSound.play()
                    player.life -= 1
                self.kill()

    def dropItem(self):
        rand = random.random() * 100
        print(rand)
        if rand < 10:
            # dropItem 10%
            item = Item(random.choice(ItemTypes), self.rect.centerx, self.rect.bottom)
            mainSprite.add(item)
            items.add(item)
        elif rand < 50:
            # dropItem 50%
            item = Item(ItemTypes[-1], self.rect.centerx, self.rect.bottom)
            mainSprite.add(item)
            items.add(item)

    def hit(self, Damage):
        self.hp -= Damage
        if self.hp <= 0:
            self.kill()
            self.dropItem()

    def foodTypeCheck(self, foodType, damage):
        if self.food == foodType:
            self.hit(damage)


# Bullet
class Food(Object):
    def __init__(self, foodType=None, reversal=False, midtop=0, bottom=0):
        super().__init__(speed=17)
        # self.image = pg.Surface((30, 30))
        # if foodType == AnimalData["monkey"]["food"]:
        #     self.image.fill(YELLOW)
        # elif foodType == AnimalData["elephant"]["food"]:
        #     self.image.fill(GREEN)
        # elif foodType == AnimalData["panda"]["food"]:
        #     self.image.fill(LIME)
        self.image = getImage(foodType)
        if reversal is True:
            if inGameData["isReversal"] == True:
                self.image = pg.transform.rotate(self.image, 180)
            else:
                self.image = pg.transform.rotate(self.image, 0)
        self.rect = self.image.get_rect()
        self.foodType = foodType
    
    def update(self):
        if inGameData["isReversal"] is True:
            self.rect.y += self.speed
            if self.rect.bottom > windowHeight:
                self.kill()
        else:
            self.rect.y += -self.speed
            if self.rect.bottom < 0:
                self.kill()

    def setPos(self, midtop, bottom):
        self.rect.midtop = midtop
        self.rect.bottom = bottom
    
    def copy(self):
        return Food(self.foodType, True, self.rect.midtop, self.rect.bottom)


class Store:
    def __init__(self):
        # super().__init__(speed=0)
        self.bg = getImage("storeBackground")

        # self.image = pg.Surface((265, 500))
        # self.image.fill(PURPLE)
        self.image = getImage("storeBG", imageDir="store")
        self.rect = self.image.get_rect()
        self.rect.center = screen.center
        self.items = []
        # self.items = [StoreItem(self.rect, 0, "banana", "Foods"),
        #                 StoreItem(self.rect, 1, "grass", "Foods"),
        #                     StoreItem(self.rect, 2, "bamboo", "Foods"),
        #                         StoreItem(self.rect, 3, "Net")]
        # self.items = [StoreItem(self.rect, 0), StoreItem(self.rect, 1)]
        
        index = 0
        for item in StoreItems:
            if item == "Foods":
                for food in list(StoreItemData[item].keys()):
                    self.items.append(StoreItem(self.rect, index, itemName=food, itemType=item))
                    index += 1
            else:
                self.items.append(StoreItem(self.rect, index, itemName=item))
                index += 1
        self.scrollSpeed = 30
        self.page = 0

        margin = 15

        # Page Up Button
        # width: 5 * 6 = 30, height: (500 - 60) / 2 = 220
        # width = margin = 15, height = 220
        # self.pageUpBtn = Button((margin, (self.rect.height - (margin * 4)) // 2), BROWN)
        self.pageUpBtn = Button((margin, (self.rect.height - (margin * 4)) // 2), imageName="pageUpButton", Dir="store")
        self.pageUpBtn.rect.x = self.items[0].bgRect.right
        self.pageUpBtn.rect.y = self.items[0].bgRect.y

        # Page Down Button
        # width: 5 * 6 = 30, height: (500 - 60) / 2 = 220
        # width = margin = 15, height = 220
        # self.pageDownBtn = Button((margin, (self.rect.height - (margin * 4)) // 2), BROWN)
        self.pageDownBtn = Button((margin, (self.rect.height - (margin * 4)) // 2), imageName="pageDownButton", Dir="store")
        self.pageDownBtn.rect.x = self.items[1].bgRect.right
        self.pageDownBtn.rect.y = self.items[1].bgRect.y

        margin = 5

        # showCoin is UI
        # self.showCoin = pg.Surface((50, 15))
        # self.showCoin.fill(WHITE)
        self.showCoin = getImage("showCoin", imageDir="store")
        self.coinRect = self.showCoin.get_rect()
        self.coinRect.x = self.rect.x + margin
        self.coinRect.y = self.rect.y + margin

        # exitBtn is Button
        self.exitBtn = Button((15, 15), imageName="storeExit", Dir="store")
        self.exitBtn.rect.right = self.rect.right - margin
        self.exitBtn.rect.y = self.rect.y + margin

    def draw(self, customer):
        if BG != None:
            window.blit(BG, (BG_Rect.x, BG_Rect.y))
        # Store Background
        window.blit(self.image, (self.rect.x, self.rect.y))
        # Show Item
        # for item in self.items:
        #     item.draw(self.image)
        self.items[self.page].draw(self.image)
        if (self.page + 1) != len(self.items):
            self.items[self.page + 1].draw(self.image)
        # page Button
        window.blit(self.pageUpBtn.image, (self.pageUpBtn.rect.x, self.pageUpBtn.rect.y))
        window.blit(self.pageDownBtn.image, (self.pageDownBtn.rect.x, self.pageDownBtn.rect.y))
        customer.inv.show()
        customer.showLife()
        # Show Coin
        window.blit(self.showCoin, (self.coinRect.x, self.coinRect.y))
        # coinText = "Coin: " + str(customer.coin)
        coinText = "      " + str(customer.coin)
        showText(BLACK, (self.coinRect.x + 10, self.coinRect.y + 2), coinText, fontSize=12)
        # Exit Button
        window.blit(self.exitBtn.image, (self.exitBtn.rect.x, self.exitBtn.rect.y))
        # showText(BLACK, (self.exitBtn.rect.x, self.exitBtn.rect.y), "X", fontSize=15)

        # pg.display.update(self.rect)
    
    def Open(self, customer):
        global isPause, lastTime
        self.coin = player.coin
        print(f"Welcome! {customer.name}")
        screenshot()

        while True:
            # drawScreen(self.draw)
            clock.tick(FPS)
            self.draw(customer)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    # 일시정지 해제
                    if event.key == pg.K_ESCAPE:
                        # 버튼의 imageText를 가져옴 (string type)
                        button = menuScreen.showScreen()
                        if button == "back":
                            return
                        else:
                            pass
                    if event.key == pg.K_s:
                        isPause = False
                        lastTime = getTick()
                        return
                    if event.key == pg.K_UP:
                        if self.page - 2 >= 0:
                            self.page -= 2
                    if event.key == pg.K_DOWN:
                        if self.page + 2 < len(self.items):
                            self.page += 2
                if event.type == pg.MOUSEBUTTONDOWN:
                    m_pos = pg.mouse.get_pos()
                    # event.button
                    # 1: Left Click
                    # 2: Wheel Click
                    # 3: Right Click
                    # 4: Wheel Up
                    # 5: Wheel Down
                    if event.button is 1:
                        # 아이템 구입 버튼 누름
                        if self.items[self.page].buyBtn.clickBtn(m_pos) is True:
                            # Buy Item
                            self.buyItem(self.items[self.page].itemName, customer)
                            print(self.items[self.page].index, "Buy!")
                        
                        if self.page + 1 != len(self.items):
                            if self.items[self.page + 1].buyBtn.clickBtn(m_pos) is True:
                                # Buy Item
                                self.buyItem(self.items[self.page + 1].itemName, customer)
                                print(self.items[self.page + 1].index, "Buy!")

                        # 일시정지 해제
                        if self.exitBtn.clickBtn(m_pos) is True:
                            isPause = False
                            lastTime = getTick()
                            return
                        # 페이지 업 버튼
                        elif self.pageUpBtn.clickBtn(m_pos) is True:
                            if self.page - 2 >= 0:
                                self.page -= 2
                        elif self.pageDownBtn.clickBtn(m_pos) is True:
                            if self.page + 2 < len(self.items):
                                self.page += 2
                    if event.button is 4:
                        if self.page - 2 >= 0:
                            self.page -= 2
                    if event.button is 5:
                        if self.page + 2 < len(self.items):
                            self.page += 2

    def buyItem(self, item, customer):
        # 아이템 이름을 받아서 해당 아이템에 관련된 행동들을 하게 한다.
        # 만약 전달된 아이템이 음식에 해당 할 경우 플레이어의 인벤토리에 들어가게 한다.
        if item in StoreItemData["Foods"].keys():
            # 인벤토리에 해당 아이템 추가
            if debugMode is False:
                if customer.coin >= StoreItemData["Foods"][item]["price"]:
                    customer.coin -= StoreItemData["Foods"][item]["price"]
                    customer.inv.add(Food(item))
            else:
                customer.inv.add(Food(item))
            pass
        elif item == "Net":
            # 인벤토리에 그물 추가
            if debugMode is False:
                if customer.coin >= StoreItemData[item]["price"]:
                    customer.coin -= StoreItemData[item]["price"]
                    customer.inv.add(item)
            else:
                customer.inv.add(item)
            pass
        elif item == "Big Net":
            # 인벤토리에 대형 그물 추가
            if debugMode is False:
                if customer.coin >= StoreItemData[item]["price"]:
                    customer.coin -= StoreItemData[item]["price"]
                    customer.inv.add(item)
            else:
                customer.inv.add(item)
            pass
        elif item == "Extend Max Ammo":
            # 탄창 + 2
            if debugMode is False:
                if customer.coin >= StoreItemData[item]["price"]:
                    customer.coin -= StoreItemData[item]["price"]
                    customer.maxAmmo += 2
            else:
                customer.maxAmmo += 2
            pass
        elif item == "Life recovery":
            # 체력 1 추가
            if debugMode is False:
                if customer.coin >= StoreItemData[item]["price"]:
                    customer.coin -= StoreItemData[item]["price"]
                    customer.recover()
            else:
                customer.recover()
        elif item == "Ironbar Upgrade":
            # 업데이트 될 예정입니다.
            pass

    def changeLang(self):
        for item in self.items:
            item.changeLang()

    def reset(self):
        self.page = 0


# 아이템에 필요한 것
# 이름, 가격, 종류
#TODO 2020/02/08~
class StoreItem:
    def __init__(self, mainRect, index=0, itemName=None, itemType=None):
        # StoreItem have Item image and Item Information
        # 전체적인 상점 아이템 부분
        self.minY = mainRect.top
        self.maxY = mainRect.bottom

        self.margin = 15
        # Width: 250 - 30 = 220
        # Height: 250 - 30 = 220
        # self.bg = pg.Surface((mainRect.width - (self.margin * 2), (mainRect.height // 2) - (self.margin * 2)))
        # self.bg.fill(GREEN)
        self.bg = getImage("storeItemBG", imageDir="store")
        self.bgRect = self.bg.get_rect()
        self.bgRect.x = mainRect.x + self.margin
        # self.originalY = self.bgRect.y = mainRect.y + ((mainRect.height // 2) * index) + self.margin
        if isEvenNum(index) is True:
            self.originalY = self.bgRect.y = mainRect.y + self.margin
        else:
            self.originalY = self.bgRect.y = mainRect.y + (mainRect.height // 2) + self.margin
        self.RelativeBgCoord = [self.bgRect.x - mainRect.x, self.bgRect.y - mainRect.y]

        # 아이템 이미지 부분
        self.itemImgBG = getImage("storeImgBG", imageDir="store")
        self.itemImgBGRect = self.itemImgBG.get_rect()
        self.itemImg = getImage(imgName=itemName, imageDir="store")
        self.itemImgRect = self.itemImg.get_rect()
        self.itemImgRect.x = self.bgRect.x + self.margin
        self.itemImgRect.y = self.bgRect.y + self.margin
        self.RelativeImgRect = [self.itemImgRect.x - self.bgRect.x, self.itemImgRect.y - self.bgRect.y]

        # 구입 버튼
        self.buyBtn = Button((80, 60), imageName="buyButton", Dir="store")
        self.buyBtn.setPos(right=self.bgRect.right - self.margin, y=self.bgRect.y + self.margin)
        self.RelativeBuyRect = [self.buyBtn.rect.x - self.bgRect.x, self.buyBtn.rect.y - self.bgRect.y]
        
        # 아이템 정보 부분
        self.itemType = itemType
        if not itemName is None:
            if itemType is "Foods":
                self.itemName = itemName
                self.itemInfoTxt = StoreItemData[itemType][itemName]["info"]
            else:
                self.itemName = itemName
                self.itemInfoTxt = StoreItemData[itemName]["info"]

        # width: 220 - (15 * 2) = 220 - 30 = 190
        # height: (220 // 2) - 15 = 110 - 15 = 95
        # self.itemInfo = pg.Surface((self.bgRect.width - (self.margin * 2), (self.bgRect.height // 2) - self.margin))
        # self.itemInfo.fill(SILVER)
        self.itemInfo = getImage("itemInfo", imageDir="store")
        self.itemInfo.convert_alpha()
        self.itemInfo.set_colorkey(BLACK)
        self.itemInfoRect = self.itemInfo.get_rect()
        self.itemInfoRect.x = self.bgRect.x + self.margin
        self.itemInfoRect.y = self.bgRect.y + (self.bgRect.height // 2)
        self.RelativeInfoRect = [self.itemInfoRect.x - self.bgRect.x, self.itemInfoRect.y - self.bgRect.y]

        self.index = index
    
    def update(self, dy):
        self.bgRect.y += dy
        self.RelativeBgCoord[1] += dy

        self.itemImgRect.x = self.bgRect.x + self.margin
        self.itemImgRect.y = self.bgRect.y + self.margin

        self.buyBtn.rect.right = self.bgRect.right - self.margin
        self.buyBtn.rect.y = self.bgRect.y + self.margin

        self.itemInfoRect.x = self.bgRect.x + self.margin
        self.itemInfoRect.y = self.bgRect.y + (self.bgRect.height // 2)
        
        # if self.bgRect.y > self.minY or self.bgRect.bottom < self.maxY:
        #     self.bgRect.y -= dy

        # if self.bgRect.y > self.originalY:
        #     self.bgRect.y -= dy

    def draw(self, bg):
        # bg.blit(self.bg, (self.RelativeBgCoord[0], self.RelativeBgCoord[1]))
        # self.bg.blit(self.itemImg, (self.RelativeImgRect[0], self.RelativeImgRect[1]))
        # self.bg.blit(self.buyBtn.image, (self.RelativeBuyRect[0], self.RelativeBuyRect[1]))
        # self.bg.blit(self.itemInfo, (self.RelativeInfoRect[0], self.RelativeInfoRect[1]))
        if self.minY < self.bgRect.y or self.bgRect.bottom> self.maxY:
            window.blit(self.bg, (self.bgRect.x, self.bgRect.y))
            self.bg.blit(self.itemImgBG, (self.RelativeImgRect[0], self.RelativeImgRect[1]))
            self.bg.blit(self.itemImg, (self.RelativeImgRect[0], self.RelativeImgRect[1]))
            self.bg.blit(self.buyBtn.image, (self.RelativeBuyRect[0], self.RelativeBuyRect[1]))
            self.bg.blit(self.itemInfo, (self.RelativeInfoRect[0], self.RelativeInfoRect[1]))
            showText(BLACK, (self.itemInfoRect.x + self.margin // 3, self.itemInfoRect.y + self.margin // 3), self.itemInfoTxt)

    def changeLang(self):
        if self.itemType is "Foods":
            self.itemInfoTxt = StoreItemData[self.itemType][self.itemName]["info"]
        else:
            self.itemInfoTxt = StoreItemData[self.itemName]["info"]


class Background(Object):
    def __init__(self, y=0):
        super().__init__("Background", speed=0)
        self.rect.y = y

    def reset(self):
        self.__init__(self.rect.y)


class IronBar(Object):
    def __init__(self):
        super().__init__(speed=0)
        self.image = pg.Surface((windowWidth, 10))
        self.image.fill(SILVER)
        self.rect = self.image.get_rect(speed=0)
    
    def blockPlayer(self):
        pass


# Item Types
    # magenta: throwDelayUp
    # olive: throwDelayDown
    # syan: speedUp
    # marron: speedDown
    # blue: damageUp
    # green: damageDown
    # gold: coin
class Item(Object):
    def __init__(self, itemType, centerx, bottom):
        super().__init__(speed=4)
        # self.image = pg.Surface((30, 30))
        self.image = getImage(itemType)
        self.itemType = itemType
        self.__wideRange = itemType[:5]
        narrowRange = itemType[-2:]

        if self.__wideRange == "throw":
            self.__iThrowDelay = ItemData[self.itemType]
            # self.image = getImage(itemType)
            # if narrowRange == "Up":
            #     # self.image.fill(MAGENTA)
            # else:
            #     # self.image.fill(OLIVE)
        elif self.__wideRange == "speed":
            self.__iSpeed = ItemData[self.itemType]
            # self.image = getImage(itemType)
            # if narrowRange == "Up":
            #     self.image.fill(SYAN)
            # else:
            #     self.image.fill(MAROON)
        elif self.__wideRange == "damag":
            self.__iDamage = ItemData[self.itemType]
            # self.image = getImage(itemType)
            # if narrowRange == "Up":
            #     self.image.fill(BLUE)  
            # else:
            #     self.image.fill(GREEN)
        elif self.__wideRange == "coin":
            self.__iCoin = ItemData[self.itemType]
            # self.image.fill(GOLD)
            # self.image = getImage("coin3")

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
    
    def update(self):
        if inGameData["isReversal"] is True:
            self.rect.y += -self.speed
            if self.rect.bottom < 0:
                self.kill()
        else:
            self.rect.y += self.speed
            if self.rect.y > windowHeight:
                self.kill()

    @property
    def wideRange(self):
        return self.__wideRange

    @property
    def iThrowDelay(self):
        return self.__iThrowDelay
    
    @property
    def iSpeed(self):
        return self.__iSpeed

    @property
    def iDamage(self):
        return self.__iDamage

    @property
    def iCoin(self):
        return self.__iCoin


class Barrel(Object):
    def __init__(self, side):
        super().__init__("Barrel", speed=0)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(CAMEL)
        # self.rect = self.image.get_rect()
        self.margin = 10

        self.replace()
        # if inGameData["isReversal"] is True:
        #     self.rect.top = screen.top + self.margin
        # else:
        #     self.rect.bottom = screen.bottom - self.margin

        self.side = side
        if side is "left":
            self.rect.left = screen.left + self.margin
        elif side is "right":
            self.rect.right = screen.right - self.margin
    
    def reload(self, player):
        if self.rect.colliderect(player) is 1:
            player.reload()

    def replace(self):
        if inGameData["isReversal"] is True:
            self.rect.top = screen.top + self.margin
        else:
            self.rect.bottom = screen.bottom - self.margin

    def reset(self):
        self.__init__(self.side)


# UI종류 : 옵션(메뉴 버튼), 상점 버튼, 목숨 UI, 탄약, 남은 시간, 현재 스테이지
class UI(Object):
    def __init__(self, size):
        super().__init__()
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.margin = 20
    
    @abc.abstractclassmethod
    def replace(self):
        if inGameData["isReversal"] is True:
            pass
        else:
            pass


class AmmoUI(UI):
    def __init__(self):
        super().__init__()

    def replace(self):
        if inGameData["isReversal"] is True:
            pass
        else:
            pass


class LifeUI(UI):
    def __init__(self):
        super().__init__()

    def replace(self):
        if inGameData["isReversal"] is True:
            pass
        else:
            pass


# 일 수로 표시를 하는게 좋을 것 같다.
# 1Day, 2Days, 3Days...
class StageUI(UI):
    def __init__(self):
        super().__init__()

    def replace(self):
        if inGameData["isReversal"] is True:
            pass
        else:
            pass


class TimeUI(UI):
    def __init__(self):
        super().__init__()

    def replace(self):
        if inGameData["isReversal"] is True:
            pass
        else:
            pass


class Button(UI):
    def __init__(self, size=(40, 40), fillColor=None, text="", fontSize=16, txtColor=BLACK, isActive=True, imageName=None, Dir=None, edgeImageName=None):
        '''
            버튼에 이미지가 있다면 무조건 imageName과 imgDir을 입력해야 한다.
        '''
        super().__init__(size)
        if fillColor != None:
            self.image.fill(fillColor)
        if imageName != None:
            # self.imageName = imageName
            self.image = getImage(imageName, imageDir=Dir)
        self.imageName = imageName
        self.Dir = Dir
        self.edgeImageName = edgeImageName
        self.text = text.split(divide)
        self.txtLength = len(text)
        self.fontSize = fontSize
        self.txtColor = txtColor
        self.isActive = isActive

        self.pos = [self.rect.x, self.rect.y]

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def showTxt(self):
        if gameData["lang"] == Language.EN.value:
            showText(self.txtColor, (self.rect.centerx - (self.txtLength * (self.fontSize // 4)),
                        self.rect.centery - (self.txtLength * (self.fontSize // 8))), self.text, fontSize=self.fontSize)
        elif gameData["lang"] == Language.KR.value:
            showText(self.txtColor, (self.rect.centerx - (self.txtLength * (self.fontSize // 4)),
                        self.rect.centery - (self.txtLength * (self.fontSize // 8))), self.text, fontSize=self.fontSize)

    def changeTxt(self, text="", fontSize=None, txtColor=None, Language=None):
        if self.imageName != None and text == "":
            if self.imageName != self.imageName[:-2] + Language:
                self.imageName = self.imageName[:-2] + Language
            # if self.imageName[-2:] == "EN":
            #     self.imageName = self.imageName[:-2] + "KR"
            # elif self.imageName[-2:] == "KR":
            #     self.imageName = self.imageName[:-2] + "EN"                
            self.image = getImage(self.imageName, self.Dir)
        else:
            pass
        self.text = text.split(divide)
        self.txtLength = len(text)
        if fontSize == None:
            pass
        else:
            self.fontSize = fontSize
        
        if txtColor == None:
            pass
        else:
            self.txtColor = txtColor

    def clickBtn(self, m_pos):
        return isClick((self.rect.x, self.rect.y, self.rect.right, self.rect.bottom), m_pos)

    def setPos(self, setTextPos=True, **kwargs):
        '''
            Key : x, y, centerx, centery, top, bottom, left, right
        '''
        for key, value in kwargs.items():
            if key == "x":
                self.rect.x = value
            elif key == "y":
                self.rect.y = value
            elif key == "centerx":
                self.rect.centerx = value
            elif key == "centery":
                self.rect.centery = value
            elif key == "top":
                self.rect.top = value
            elif key == "bottom":
                self.rect.bottom = value
            elif key == "left":
                self.rect.left = value
            elif key == "right":
                self.rect.right = value

        self.setTextPos = setTextPos


class Buttons:
    def __init__(self):
        self.btns = []  # Button => element
        self.curBtn = 0
        self.selectedBtn = None

        self.hasSubBtn = False
        self.isSubBtn = False
        self.curSubBtn = 0
        self.selectedSubBtn = None
        self.showCurBtn = None
        self.showCurBtnPos = []
    
    def add(self, btn):
        # btn은 Button클래스 이거나 리스트 혹은 튜플일 수 있다.
        if type(btn) == list or type(btn) == tuple:
            tempBtn = []
            if self.hasSubBtn is False:
                self.hasSubBtn = True

            for b in btn:
                if type(b) == list or type(b) == tuple:
                    for bb in b:
                        if bb.isActive is True:
                            tempBtn.append(bb)
                else:
                    if b.isActive is True:
                        tempBtn.append(b)
            if len(tempBtn) == 1:
                self.btns.append(tempBtn[0])
            else:
                self.btns.append(tempBtn)
        else:
            self.btns.append(btn)
        self.update()

    def getCurBtn(self):
        if type(self.btns[self.curBtn]) == list or type(self.btns[self.curBtn]) == tuple:
            return self.btns[self.curBtn][self.curSubBtn]
        else:
            return self.btns[self.curBtn]

    def changeBtn(self, index, changedObj):
        if type(changedObj) == list or type(changedObj) == tuple:
            for obj in changedObj:
                if type(obj) == Button:
                    if obj.isActive is True:
                        self.btns[index] = obj
                else:
                    self.btns[index] = obj
        else:
            self.btns[index] = changedObj
        self.update()

    def updateBtn(self, btn, index=None):
        if self.hasSubBtn is False:
            if type(btn) == list or type(btn) == tuple:
                self.hasSubBtn = True
        if index == None:
            self.btns.append(btn)
        else:
            self.btns.insert(index, btn)
        self.update()

    def remove(self, *btns):
        for btn in btns:
            print(f"Btn remove: {btn}")
            if self.btns.count(btn) != 0:
                if type(btn) == list or type(btn) == tuple:
                    if self.hasSubBtn is True:
                        self.hasSubBtn = False

                    for b in btn:
                        if b in self.btns:
                            self.btns.remove(b)
                else:
                    self.btns.remove(btn)
            else:
                return

    def select(self):
        if self.isSubBtn is False:
            if self.selectedBtn != None:
                return self.selectedBtn
        else:
            if self.selectedSubBtn != None:
                return self.selectedSubBtn   

    def clickSelect(self, m_pos):
        '''
            return Button Class
        '''
        for btn in self.btns:
            if type(btn) == list or type(btn) == tuple:
                for b in btn:
                    if b.clickBtn(m_pos) is True:
                        self.curBtn = self.btns.index(btn)
                        self.curSubBtn = self.btns[self.curBtn].index(b)
                        self.update()
                        return b
            else:
                if btn.clickBtn(m_pos) is True:
                    self.curBtn = self.btns.index(btn)
                    self.update()
                    return btn

    def update(self):
        # self.btns가 비어있지 않을 경우 존재하는 버튼을 선택한다.
        if self.btns != []:
            self.selectedBtn = self.btns[self.curBtn]
            if type(self.selectedBtn) == list or type(self.selectedBtn) == tuple:
                self.isSubBtn = True
                self.selectedSubBtn = self.btns[self.curBtn][self.curSubBtn]
                if self.selectedSubBtn.edgeImageName != None:
                    self.showCurBtn = getImage(self.selectedSubBtn.edgeImageName, imageDir=self.selectedSubBtn.Dir)
                    showCurBtnRect = self.showCurBtn.get_rect()
                    margin = (showCurBtnRect.width - self.selectedSubBtn.rect.width) // 2
                    self.showCurBtnPos = [self.selectedSubBtn.rect.x - margin, self.selectedSubBtn.rect.y - margin]
            else:
                self.isSubBtn = False
                if self.selectedBtn.edgeImageName != None:
                    self.showCurBtn = getImage(self.selectedBtn.edgeImageName, imageDir=self.selectedBtn.Dir)
                    showCurBtnRect = self.showCurBtn.get_rect()
                    margin = (showCurBtnRect.width - self.selectedBtn.rect.width) // 2
                    self.showCurBtnPos = [self.selectedBtn.rect.x - margin, self.selectedBtn.rect.y - margin]
    
    def input(self, key):
        if key == pg.K_UP:
            self.curBtn -= 1
            if self.curBtn < 0:
                self.curBtn = len(self.btns) - 1
        elif key == pg.K_DOWN:
            self.curBtn += 1
            if self.curBtn > len(self.btns) - 1:
                self.curBtn = 0

        if self.isSubBtn is True and (type(self.selectedBtn) == list or type(self.selectedBtn) == tuple):
            if key == pg.K_LEFT:
                self.curSubBtn -= 1
                if self.curSubBtn < 0:
                    self.curSubBtn = len(self.selectedBtn) - 1
            elif key == pg.K_RIGHT:
                self.curSubBtn += 1
                if self.curSubBtn > len(self.selectedBtn) - 1:
                    self.curSubBtn = 0
                
        if key == pg.K_RETURN:
            return self.select()
        
        self.update()

    def drawCurSelectedBtn(self, size=4, Color=GREEN):
        # 나중에는 선택하는 이미지를 이용
        if self.isSubBtn is False:
            if self.selectedBtn != None:
                window.blit(self.showCurBtn, self.showCurBtnPos)
                # pg.draw.rect(window, GREEN, (self.selectedBtn.rect.x, self.selectedBtn.rect.y,
                #             self.selectedBtn.rect.width, self.selectedBtn.rect.height), size)
        else:
            if self.selectedSubBtn != None:
                window.blit(self.showCurBtn, self.showCurBtnPos)
                # pg.draw.rect(window, GREEN, (self.selectedSubBtn.rect.x, self.selectedSubBtn.rect.y,
                #             self.selectedSubBtn.rect.width, self.selectedSubBtn.rect.height), size)

    def init(self):
        self.curBtn = 0
        self.curSubBtn = 0
        self.update()


class MenuButton(Button):
    def __init__(self):
        # super().__init__(fillColor=NAVY)
        super().__init__(imageName="menuButton")
        self.rect.left = self.margin

        # True : top (MenuButton : bottom)
        if inGameData["isReversal"] is True:
            self.rect.bottom = windowHeight - self.margin
        else:
            self.rect.y = self.margin

    def clickBtn(self, m_pos):
        global isPause, pauseCurTime
        if super().clickBtn(m_pos) is True:
            pauseCurTime = inGameData["curTime"]
            isPause = True
            menuScreen.showScreen()
        # print("Press the Option Button")
        # if self.rect.colliderect(m_pos) is 1:
        #     pass

    def replace(self):
        if inGameData["isReversal"] is True:
            self.rect.bottom = windowHeight - self.margin
        else:
            self.rect.y = self.margin

    def reset(self):
        self.__init__()


class StoreButton(Button):
    def __init__(self):
        super().__init__(fillColor=NAVY)
        self.rect.left = self.margin * 4
        if inGameData["isReversal"] is True:
            self.rect.bottom = windowHeight - self.margin
        else:
            self.rect.y = self.margin

    def clickBtn(self, m_pos, coin):
        global isPause
        if super().clickBtn(m_pos) is True:
            isPause = True
            store.Open(player)

    def selectBtn(self, coin):
        global isPause, pauseCurTime
        pauseCurTime = inGameData["curTime"]
        isPause = True
        store.Open(player)

    def replace(self):
        if inGameData["isReversal"] is True:
            self.rect.bottom = windowHeight - self.margin
        else:
            self.rect.y = self.margin


# 버튼을 추가하는 기능, 버튼을 삭제하는 기능
# 버튼의 갯수만큼 출력하는 기능
# 버튼의 갯수에 맞게 높이와 길이를 정하고 위치를 맞춘다.
'''
    스크린의 역할
    Screen은 Base Class이다.    
'''
class Screen(metaclass=abc.ABCMeta):
    def __init__(self, hasBtn=False, fillColor=TRANSPARENCY, BG=None, BGDir=None, SubBG=None, SubBGDir=None):
        if BG == None:
            self.screen = screenSurf.copy()
            self.screen = self.screen.convert_alpha()
            self.screen.fill(fillColor)
        else:
            self.screen = getImage(BG, BGDir)
        self.rect = self.screen.get_rect()

        if SubBG == None:
            self.subBG = None
            self.subRect = None
        else:
            self.subBG = getImage(SubBG, SubBGDir)
            self.subRect = self.subBG.get_rect()

        # 오브젝트는 리스트 형태로 되어 있다.
        # 오브젝트는 화면에 그리는 역할을 한다.
        self.objs = [] # [image, rect]
        
        self.hasBtn = hasBtn
        if self.hasBtn is True:
            self.buttons = Buttons()

        # self.addObjs([self.screen, self.rect])

    def addObjs(self, *objs):
        '''
            Queue
            FIFO: First In First Out
            First In is Layer1

            Button Class has a rect
        '''
        # 여기 잘못 건드리면 설정이 계속 이상하게 됨
        for obj in objs:
            # bg
            # saveBtn
            if type(obj) == Button:
                self.objs.append(obj)
                if obj.isActive is True:
                    self.buttons.add(obj)
            elif type(obj) == list or type(obj) == tuple:
                self.objs.append(obj)
                self.buttons.add(obj)
            else:
                self.objs.append(obj)

    def updateObjs(self, index=None, **objs):
        '''
            key: update, remove
        '''
        for key, obj in objs.items():
            if key == "update":
                self.objs.append(obj)
                # self.buttons.updateBtn(obj, index)
                self.buttons.add(obj)
            elif key == "remove":
                self.removeObjs(obj)
                self.buttons.remove(obj)
    
    def changeObjs(self, index, originalObjs, changedObjs):
        # 원래 있던 오브젝트는 없애고 바꿀 오브젝트를 넣어야 한다.
        if type(originalObjs) == list or type(originalObjs) == tuple:
            for originalObj in originalObjs:
                self.removeObjs(originalObj)
        else:
            self.removeObjs(originalObjs)
                
        self.objs.append(changedObjs)
        self.buttons.changeBtn(index, changedObjs)

    def removeObjs(self, *objs):
        # if type(obj) == list or type(obj) == tuple:
            # for o in obj:
            #     if o in self.objs:
            #         index = self.objs.index(o)
            #         del self.objs[index]
            # else:
            #     if obj in self.objs:
            #         index = self.objs.index(obj)
            #         del self.objs[index]
        for obj in objs:
            if type(obj) == list or type(obj) == tuple:
                for o in obj:
                    if o in self.objs:
                        index = self.objs.index(o)
                        del self.objs[index]
            else:
                if obj in self.objs:
                    index = self.objs.index(obj)
                    del self.objs[index]

    def setBG(self):
        self.screen = getImage("bg")
        self.rect = self.screen.get_rect()

    # 더러운 곳
    def draw(self):
        window.blit(self.screen, (self.rect.x, self.rect.y))
        if self.subBG != None:
            window.blit(self.subBG, (self.subRect.x, self.subRect.y))
        for objs in self.objs:
            if type(objs) == list or type(objs) == tuple:
                for obj in objs:
                    if type(obj) == list or type(obj) == tuple:
                        for o in obj:
                            if type(o) == list or type(o) == tuple:
                                for oo in o:
                                    oo.draw()
                                    oo.showTxt()
                            else:
                                o.draw()
                                o.showTxt()
                    else:
                        obj.draw()
                        obj.showTxt()
            else:
                objs.draw()
                objs.showTxt()

        if self.buttons.selectedBtn != None:
            self.buttons.drawCurSelectedBtn()
    
    def input(self):
        global gameRun
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return event.key
                if self.hasBtn is True:
                    return self.buttons.input(event.key)
            if event.type == pg.MOUSEBUTTONDOWN:
                m_pos = pg.mouse.get_pos()
                return self.buttons.clickSelect(m_pos)
            if event.type == pg.MOUSEMOTION:
                m_pos = pg.mouse.get_pos()

    def init(self):
        self.buttons.init()

    @abc.abstractclassmethod
    def changeLang(self):
        pass


# 메인 메뉴
# 메인메뉴는 타이틀, 플레이, 게임 불러오기, 설정, 나가기 버튼을 가진다.
class MainMenuScreen(Screen):
    def __init__(self):
        super().__init__(True, BG="mainMenuBG", BGDir="screen")
        self.loadScreen = LoadScreen()
        self.btnHeight = 500 / 9
        self.title = getImage("Title", "screen")
        self.titleRect = self.title.get_rect()
        # self.title_first = getImage("Title_First", "screen")
        # self.title_first_rect = self.title_first.get_rect()
        # self.title_second = getImage("Title_Second", "screen")
        # self.title_second_rect = self.title_second.get_rect()

        if gameData["lang"] == Language.EN.value:
            # self.playBtn = Button((200, self.btnHeight), PINK, "Play", fontSize)
            # self.loadBtn = Button((200, self.btnHeight), GRAY, "Load", fontSize)
            # self.optionBtn = Button((200, self.btnHeight), YELLOW, "Option", fontSize)
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "Exit", fontSize, WHITE)
            self.playBtn = Button((200, self.btnHeight), imageName="PlayButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.loadBtn = Button((200, self.btnHeight), imageName="LoadButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.optionBtn = Button((200, self.btnHeight), imageName="OptionButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.exitBtn = Button((200, self.btnHeight), imageName="EndButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.playBtn = Button((200, self.btnHeight), PINK, "게임 시작", fontSize)
            # self.loadBtn = Button((200, self.btnHeight), GRAY, "게임 불러오기", fontSize)
            # self.optionBtn = Button((200, self.btnHeight), YELLOW, "설정", fontSize)
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "끝내기", fontSize, WHITE)
            self.playBtn = Button((200, self.btnHeight),  imageName="PlayButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.loadBtn = Button((200, self.btnHeight), imageName="LoadButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.optionBtn = Button((200, self.btnHeight), imageName="OptionButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.exitBtn = Button((200, self.btnHeight), imageName="EndButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
        self.playBtn.setPos(centerx=screen.centerx, centery=self.rect.centery - (self.playBtn.rect.height * 3) + (152 - self.playBtn.rect.height))
        self.loadBtn.setPos(centerx=screen.centerx, centery=self.rect.centery - self.loadBtn.rect.height + (152 - self.loadBtn.rect.height))
        self.optionBtn.setPos(centerx=screen.centerx, centery=self.rect.centery + self.optionBtn.rect.height + (152 - self.optionBtn.rect.height))
        self.exitBtn.setPos(centerx=screen.centerx, centery=self.rect.centery + (self.exitBtn.rect.height * 3) + (152 - self.exitBtn.rect.height))

        # Stack or Queue
        self.addObjs(self.playBtn, self.loadBtn, self.optionBtn, self.exitBtn)

    def draw(self):
        super().draw()
        window.blit(self.title, (self.titleRect.x, self.titleRect.y))
        # window.blit(self.title_first, (self.title_first_rect.x, self.title_first_rect.y))
        # window.blit(self.title_second, (self.title_second_rect.x, self.title_second_rect.y))

    def showScreen(self):
        global gameRun, isPause, lastTime
        select = None
        while True:
            clock.tick(FPS)
            window.fill(WHITE)
            drawScreen(self.draw)
            select = self.input()
            if select != pg.K_ESCAPE:
                if select == self.playBtn:
                    gameStart()
                    playGame()
                elif select == self.optionBtn:
                    optionScreen.showScreen()
                elif select == self.loadBtn:
                    if self.loadScreen.showScreen() == "load":
                        gameLoad()
                        playGame()
                elif select == self.exitBtn:
                    gameRun = False
                    return
            else:
                return

    def changeLang(self):
        self.loadScreen.changeLang()
        if gameData["lang"] == Language.EN.value:
            self.playBtn.changeTxt(Language="EN")
            self.loadBtn.changeTxt(Language="EN")
            self.optionBtn.changeTxt(Language="EN")
            self.exitBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.playBtn.changeTxt(Language="KR")
            self.loadBtn.changeTxt(Language="KR")
            self.optionBtn.changeTxt(Language="KR")
            self.exitBtn.changeTxt(Language="KR")


# 인게임 메뉴
class MenuScreen(Screen):
    def __init__(self):
        super().__init__(True)
        # 인게임 메뉴 스크린은 세이브/로드 스크린을 가지고 있다.
        # MenuScreen has a Save_N_Load Screen
        self.saveNloadScreen = Save_n_LoadScreen()

        self.btnHeight = 500 / 9 # 55.555···
        fontSize = 24
        if gameData["lang"] == Language.EN.value:
            # self.resumeBtn = Button((200, self.btnHeight), PINK, "Resume", fontSize)
            # self.optionBtn = Button((200, self.btnHeight), GRAY, "Option", fontSize)
            # self.slBtn = Button((200, self.btnHeight), YELLOW, "Save/Load", fontSize)
            # self.back2Menu = Button((200, self.btnHeight), BLACK, "Back to\Mainmenu", 16, WHITE)
            self.resumeBtn = Button((200, self.btnHeight), imageName="ResumeButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.optionBtn = Button((200, self.btnHeight), imageName="OptionButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.slBtn = Button((200, self.btnHeight), imageName="SaveNLoadButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
            self.back2Menu = Button((200, self.btnHeight), imageName="BackToMainmenuButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.resumeBtn = Button((200, self.btnHeight), PINK, "계속하기", fontSize)
            # self.optionBtn = Button((200, self.btnHeight), GRAY, "설정", fontSize)
            # self.slBtn = Button((200, self.btnHeight), YELLOW, "저장/불러오기", fontSize)
            # self.back2Menu = Button((200, self.btnHeight), BLACK, "메인메뉴로\돌아가기", fontSize, WHITE)
            self.resumeBtn = Button((200, self.btnHeight), imageName="ResumeButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.optionBtn = Button((200, self.btnHeight), imageName="OptionButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.slBtn = Button((200, self.btnHeight), imageName="SaveNLoadButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
            self.back2Menu = Button((200, self.btnHeight), imageName="BackToMainmenuButtonKR", Dir="buttons", edgeImageName="ButtonEdge")

        self.resumeBtn.setPos(centerx=screen.centerx,
                                centery=self.rect.centery - (self.resumeBtn.rect.height * 3))
        self.optionBtn.setPos(centerx=screen.centerx,
                                centery=self.rect.centery - self.optionBtn.rect.height)
        self.slBtn.setPos(centerx=screen.centerx,
                                centery=self.rect.centery + self.slBtn.rect.height)
        self.back2Menu.setPos(centerx=screen.centerx,
                                centery=self.rect.centery + (self.back2Menu.rect.height * 3))
        
        self.addObjs(self.resumeBtn, self.optionBtn, self.slBtn, self.back2Menu)

    def showScreen(self):
        global isPause, gameRun, lastTime, pauseCurTime
        screenshot()

        while True:
            clock.tick(FPS)
            # window.fill(WHITE)
            window.blit(BG, (BG_Rect.x, BG_Rect.y))
            drawScreen(self.draw)
            select = self.input()
            if select != pg.K_ESCAPE:
                if select == self.resumeBtn:
                    isPause = False
                    lastTime = getTick()
                    # Store Open
                    return "resume"
                elif select == self.optionBtn:
                    optionScreen.showScreen()
                elif select == self.slBtn:
                    if self.saveNloadScreen.showScreen() == "load":
                        isPause = False
                        lastTime = getTick()
                        return
                elif select == self.back2Menu:
                    self.init()
                    gameRun = False
                    pauseCurTime = 0
                    # Store Open
                    return "back"
            else:
                isPause = False
                lastTime = getTick()
                return

    def changeLang(self):
        self.saveNloadScreen.changeLang()
        if gameData["lang"] == Language.EN.value:
            self.resumeBtn.changeTxt(Language="EN")
            self.optionBtn.changeTxt(Language="EN")
            self.slBtn.changeTxt(Language="EN")
            self.back2Menu.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.resumeBtn.changeTxt(Language="KR")
            self.optionBtn.changeTxt(Language="KR")
            self.slBtn.changeTxt(Language="KR")
            self.back2Menu.changeTxt(Language="KR")


# 옵션에는 언어 설정, 인벤토리 왼, 오른쪽을 결정하게 한다.
# 옵션기능
#     #? 언어 설정
#     #? 인벤토리 왼쪽, 오른쪽
class OptionScreen(Screen):
    def __init__(self):
        super().__init__(True, BG="bg", SubBG="optionBG", SubBGDir="screen")
        width = 140
        self.btnHeight = 500 / 9 # 55.555...
        if gameData["lang"] == Language.EN.value:
            self.showLang = Button((width, self.btnHeight), isActive=False, imageName="LanguageButtonEN", Dir="buttons" + divide + "optionButtons")
            # self.enBtn = Button((width, self.btnHeight), RED, "English", fontSize, BLACK, True)
            # self.krBtn = Button((width, self.btnHeight), BLUE, "Korean", fontSize, BLACK, True)
                        
            self.inv = Button((width, self.btnHeight), isActive=False, imageName="InventoryButtonEN", Dir="buttons" + divide + "optionButtons")
            # self.leftInvBtn = Button((width, self.btnHeight), BLUE, "Left", fontSize, BLACK, True)
            # self.rightInvBtn = Button((width, self.btnHeight), RED, "Right", fontSize, BLACK, True)
            # self.exitBtn = Button((width, self.btnHeight), BLACK, "Exit", fontSize, WHITE, True)
            # self.showLang = Button((width, self.btnHeight), text="Language", fontSize=fontSize, isActive=False, imageName="optionButton1")
            self.enBtn = Button((width, self.btnHeight), isActive=True, imageName="EnglishButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.krBtn = Button((width, self.btnHeight), isActive=True, imageName="KoreanButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
                        
            # self.inv = Button((width, self.btnHeight), text="Inventory", fontSize=fontSize, isActive=False, imageName="optionButton1")
            self.leftInvBtn = Button((width, self.btnHeight), isActive=True, imageName="LeftButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.rightInvBtn = Button((width, self.btnHeight), isActive=True, imageName="RightButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.inVisibleInvBtn = Button((width, self.btnHeight), isActive=True, imageName="InVisibleButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.visibleInvBtn = Button((width, self.btnHeight), isActive=True, imageName="VisibleButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.exitBtn = Button((width, self.btnHeight), isActive=True, imageName="ExitButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            self.showLang = Button((width, self.btnHeight), isActive=False, imageName="LanguageButtonKR", Dir="buttons" + divide + "optionButtons")
            # self.enBtn = Button((width, self.btnHeight), RED, "영어", fontSize, BLACK, True)
            # self.krBtn = Button((width, self.btnHeight), BLUE, "한국어", fontSize, BLACK, True)

            self.inv = Button((width, self.btnHeight), isActive=False, imageName="InventoryButtonKR", Dir="buttons" + divide + "optionButtons")
            # self.leftInvBtn = Button((width, self.btnHeight), BLUE, "왼쪽", fontSize, BLACK, True)
            # self.rightInvBtn = Button((width, self.btnHeight), RED, "오른쪽", fontSize, BLACK, True)
            # self.exitBtn = Button((width, self.btnHeight), BLACK, "나가기", fontSize, WHITE, True)
            # self.showLang = Button((width, self.btnHeight), text="언어", fontSize=fontSize, isActive=False, imageName="optionButton1")
            self.enBtn = Button((width, self.btnHeight), isActive=True, imageName="EnglishButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.krBtn = Button((width, self.btnHeight), isActive=True, imageName="KoreanButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
                        
            # self.inv = Button((width, self.btnHeight), text="인벤토리", fontSize=fontSize, isActive=False, imageName="optionButton1")
            self.leftInvBtn = Button((width, self.btnHeight), isActive=True, imageName="LeftButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.rightInvBtn = Button((width, self.btnHeight), isActive=True, imageName="RightButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.inVisibleInvBtn = Button((width, self.btnHeight), isActive=True, imageName="InVisibleButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.visibleInvBtn = Button((width, self.btnHeight), isActive=True, imageName="VisibleButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")
            self.exitBtn = Button((width, self.btnHeight), isActive=True, imageName="ExitButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="optionButtonEdge")

        self.showLang.setPos(centerx=screen.centerx, centery=self.rect.centery - (self.showLang.rect.height * 3))
        self.enBtn.setPos(right=self.showLang.rect.x + (self.enBtn.rect.width / 2), centery=self.rect.centery - (self.enBtn.rect.height * 2))
        self.krBtn.setPos(x=self.showLang.rect.right - (self.krBtn.rect.width / 2), centery=self.rect.centery - (self.krBtn.rect.height * 2))

        self.inv.setPos(centerx=screen.centerx, centery=(self.rect.centery - self.inv.rect.height) + 1)

        self.leftInvBtn.setPos(right=self.inv.rect.x + (self.leftInvBtn.rect.width / 2), centery=self.rect.centery - (self.leftInvBtn.rect.height * 0.005))
        self.rightInvBtn.setPos(x=self.inv.rect.right - (self.rightInvBtn.rect.width / 2), centery=self.rect.centery - (self.rightInvBtn.rect.height * 0.005))
        self.inVisibleInvBtn.setPos(right=self.inv.rect.x + (self.leftInvBtn.rect.width / 2), centery=self.rect.centery + (self.inVisibleInvBtn.rect.height))
        self.visibleInvBtn.setPos(x=self.inv.rect.right - (self.rightInvBtn.rect.width / 2), centery=self.rect.centery + (self.visibleInvBtn.rect.height))
        self.exitBtn.setPos(centerx=screen.centerx, centery=self.rect.centery + (self.exitBtn.rect.height * 3))
        
        self.addObjs(self.showLang, [self.enBtn, self.krBtn], self.inv, [self.leftInvBtn, self.rightInvBtn], [self.inVisibleInvBtn, self.visibleInvBtn], self.exitBtn)

    def draw(self):
        super().draw()
        player.inv.show()

    def showScreen(self):
        global gameData
        self.setBG()

        while True:
            clock.tick(FPS)
            # window.fill(WHITE)
            drawScreen(self.draw)
            select = self.input()
            if select != pg.K_ESCAPE:
                if select == self.enBtn:
                    gameData["lang"] = Language.EN.value
                    changeLanguage()
                elif select == self.krBtn:
                    gameData["lang"] = Language.KR.value
                    changeLanguage()
                elif select == self.leftInvBtn:
                    player.inv.changePos("left")
                elif select == self.rightInvBtn:
                    player.inv.changePos("right")
                elif select == self.inVisibleInvBtn:
                    player.inv.visibleConfig(False)
                elif select == self.visibleInvBtn:
                    player.inv.visibleConfig(True)
                elif select == self.exitBtn:
                    self.init()
                    return
            else:
                return

    def changeLang(self):
        if gameData["lang"] == Language.EN.value:
            self.showLang.changeTxt(Language="EN")
            self.enBtn.changeTxt(Language="EN")
            self.krBtn.changeTxt(Language="EN")
                        
            self.inv.changeTxt(Language="EN")
            self.leftInvBtn.changeTxt(Language="EN")
            self.rightInvBtn.changeTxt(Language="EN")
            self.inVisibleInvBtn.changeTxt(Language="EN")
            self.visibleInvBtn.changeTxt(Language="EN")
            self.exitBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.showLang.changeTxt(Language="KR")
            self.enBtn.changeTxt(Language="KR")
            self.krBtn.changeTxt(Language="KR")

            self.inv.changeTxt(Language="KR")
            self.leftInvBtn.changeTxt(Language="KR")
            self.rightInvBtn.changeTxt(Language="KR")
            self.inVisibleInvBtn.changeTxt(Language="KR")
            self.visibleInvBtn.changeTxt(Language="KR")
            self.exitBtn.changeTxt(Language="KR")


class LoadScreen(Screen):
    def __init__(self):
        super().__init__(True, BG="bg", SubBG="SaveNLoadBG", SubBGDir="screen")
        self.dataTables = []
        self.dataTableCount = 3
        self.btnHeight = 500 / 9 # 55.555···
        margin = 20

        # Initialize dataTables
        for index in range(self.dataTableCount):
            self.dataTables.append(LoadTable(index, margin))
            self.addObjs(self.dataTables[index].objs)

        if gameData["lang"] == Language.EN.value:
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "Exit", 16, WHITE, True)
            self.exitBtn = Button((200, self.btnHeight), isActive=True, imageName="ExitButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "나가기", 16, WHITE, True)
            self.exitBtn = Button((200, self.btnHeight), isActive=True, imageName="ExitButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
        self.exitBtn.setPos(centerx=self.rect.centerx, bottom=screen.bottom - margin)
        self.addObjs(self.exitBtn)
    
    def showScreen(self):
        self.setBG()

        for dataTable in self.dataTables:
            dataTable.isExistData()

        while True:
            clock.tick(FPS)
            # window.fill(WHITE)
            drawScreen(self.draw)
            select = self.input()
            if select != pg.K_ESCAPE:
                if select == self.exitBtn:
                    return
                else:
                    for dataTable in self.dataTables:
                        oldDataTableObjs = dataTable.objs
                        if dataTable.select(select) is True:
                            self.changeObjs(dataTable.index, oldDataTableObjs, dataTable.objs)
                            break
                        # load Button
                        elif dataTable.select(select) is False:
                            return "load"
            else:
                return

    def updateData(self, index):
        oldDataTableObjs = self.dataTables[index].objs
        self.dataTables[index].isHaveData()
        self.dataTables[index].checkSaveData()
        self.dataTables[index].isExistData()
        self.changeObjs(index, oldDataTableObjs, self.dataTables[index].objs)

    def changeLang(self):
        for dataTable in self.dataTables:
            dataTable.changeLang()
        if gameData["lang"] == Language.EN.value:
            self.exitBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.exitBtn.changeTxt(Language="KR")


class Save_n_LoadScreen(Screen):
    def __init__(self):
        super().__init__(True, BG="bg", SubBG="SaveNLoadBG", SubBGDir="screen")
        self.dataTables = []
        self.dataTableCount = 3
        margin = 20
        self.btnHeight = 500 / 9

        # Initialize dataTables
        for index in range(self.dataTableCount):
            self.dataTables.append(Save_n_LoadTable(index, margin))
            self.addObjs(self.dataTables[index].objs)

        if gameData["lang"] == Language.EN.value:
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "Exit", 16, WHITE, True)
            self.exitBtn = Button((200, self.btnHeight), isActive=True, imageName="ExitButtonEN", Dir="buttons", edgeImageName="ButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.exitBtn = Button((200, self.btnHeight), BLACK, "나가기", 16, WHITE, True)
            self.exitBtn = Button((200, self.btnHeight), isActive=True, imageName="ExitButtonKR", Dir="buttons", edgeImageName="ButtonEdge")
        self.exitBtn.setPos(centerx=screen.centerx, bottom=windowHeight - margin)
        self.addObjs(self.exitBtn)
    
    def showScreen(self):
        self.setBG()

        for dataTable in self.dataTables:
            dataTable.isExistData()

        while True:
            clock.tick(FPS)
            # window.fill(WHITE)
            drawScreen(self.draw)            
            select = self.input()
            if select != pg.K_ESCAPE:
                if select == self.exitBtn:
                    self.init()
                    return
                else:
                    for dataTable in self.dataTables:
                        oldDataTableObjs = dataTable.objs
                        # oldDataTable
                        if dataTable.select(select) is True:
                            self.changeObjs(dataTable.index, oldDataTableObjs, dataTable.objs)
                            break
                        elif dataTable.select(select) is False:
                            return
            elif select == "load":
                return select
            else:
                return

    def updateData(self, index):
        oldDataTableObjs = self.dataTables[index].objs
        self.dataTables[index].checkSaveData()
        self.dataTables[index].isExistData()
        self.changeObjs(index, oldDataTableObjs, self.dataTables[index].objs)

    def changeLang(self):
        for dataTable in self.dataTables:
            dataTable.changeLang()
        if gameData["lang"] == Language.EN.value:
            self.exitBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.exitBtn.changeTxt(Language="KR")


'''
    데이터 테이블 기능
    현재 테이블(자기 자신)에 파일이 있는지 없는지 검사한다.
    만약 파일이 있다면 불러오기/삭제 버튼을 띄워주며(obj에 추가하며)
    만약 파일이 없다면 저장 버튼을 띄워준다.
        최대한 지금 있는것과 충돌이 일어나지 않으면서
        기능들은 잘 작동하도록 만들어야한다.
'''
class dataTable(Screen):
    def __init__(self, index):
        super().__init__(True)
        self.filename = "data" + str(index) + ".json"
        self.index = index
        self.margin = 10
        self.hasSaveData = None
        self.dataText = ""

        # self.bg = Button((230, 160), NAVY, isActive=False)
        self.bg = Button((230, 160), isActive=False, imageName="dataTableBG", Dir="buttons" + divide + "dataTables", edgeImageName="dataTableBGEdge")
        self.bg.rect.centerx = screen.centerx

        if gameData["lang"] == Language.EN.value:
            # self.loadBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), BLACK, "Load", 16, WHITE)
            # self.loadBtn = Button((self.bg.rect.width, self.bg.rect.height), TEAL, self.dataText, 16, WHITE)
            self.loadBtn = Button((self.bg.rect.width, self.bg.rect.height), text=self.dataText, fontSize=16, imageName="loadButton", Dir="buttons" + divide + "dataTables", edgeImageName="loadButtonEdge", txtColor=WHITE)
            self.delBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), imageName="delButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="delButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.loadBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), BLACK, "불러오기", 16, WHITE)
            # self.loadBtn = Button((self.bg.rect.width, self.bg.rect.height), TEAL, self.dataText, 16, WHITE)
            self.loadBtn = Button((self.bg.rect.width, self.bg.rect.height), text=self.dataText, fontSize=16, imageName="loadButton", Dir="buttons" + divide + "dataTables", edgeImageName="loadButtonEdge", txtColor=WHITE)
            self.delBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), imageName="delButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="delButtonEdge")
        self.isHaveData()
    
    @abc.abstractclassmethod
    def isExistData(self):
        '''
            만약 파일이 있다면 불러오기/삭제 버튼을 띄워주며(obj에 추가하며)
            만약 파일이 없다면 저장 버튼을 띄워준다.
        '''
        if os.path.isfile(self.filename) is True:
            self.updateObjs(update=[self.loadBtn, self.delBtn])
            self.hasSaveData = True
        else:
            # self.updateObjs(update=self.saveBtn)
            self.hasSaveData = False

    def isHaveData(self):
        if os.path.isfile(self.filename) is True:
            with open(self.filename, "r") as file:
                data = json.load(file)
            
            saveTimeData = data["saveTime"]
            dayData = data["inGameData"]["Days"]

            if gameData["lang"] == Language.EN.value:
                stageText = "Stage: " + dayData
            elif gameData["lang"] == Language.KR.value:
                # stageText = "Stage: " + inGameData["Days"]
                stageText = dayData + "단계"
            
            saveTimeText = str(saveTimeData["Year"]) + "/" + str(saveTimeData["Month"]) + "/" + str(saveTimeData["Day"]) + divide + \
                            str(saveTimeData["Hour"]) + ":" + str(saveTimeData["Minute"]) + ":" + str(saveTimeData["Second"])
            self.dataText = stageText + divide + saveTimeText
            self.loadBtn.changeTxt(self.dataText)

    def setPos(self, margin):
        self.bg.rect.y = margin + (self.bg.rect.height * self.index) + (margin * self.index)
        self.loadBtn.setPos(False, centerx=self.bg.rect.centerx, centery=self.bg.rect.centery)
        self.delBtn.setPos(False, x=self.bg.rect.right + margin, centery=self.bg.rect.centery)
        # self.loadBtn.setPos(right=self.saveBtn.rect.x, bottom=self.bg.rect.bottom - self.margin)
        # self.delBtn.setPos(x=self.saveBtn.rect.right, bottom=self.bg.rect.bottom - self.margin)

    @abc.abstractclassmethod
    def checkSaveData(self):
        pass

    def load(self):
        global inGameData, player, pauseCurTime
        with open(self.filename, "r") as file:
            loadData = json.load(file)
        inGameData["Boundary"] = loadData["inGameData"]["Boundary"]
        pauseCurTime = loadData["inGameData"]["curTime"]
        inGameData["Days"] = loadData["inGameData"]["Days"]
        player.rect.x, player.rect.y = loadData["playerPos"]
        player.ammo = loadData["playerAmmo"]
        player.maxAmmo = loadData["playerMaxAmmo"]
        player.life = loadData["playerLife"]
        player.coin = loadData["coin"]
        stageSetting()

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        else:
            print(f"not exist {self.filename}")
        # menuScreen.saveNloadScreen.dataTables[self.index].isExistData()
        # menuScreen.saveNloadScreen.dataTables[self.index].checkSaveData()
        menuScreen.saveNloadScreen.updateData(self.index)
        
        # mainMenuScreen.loadScreen.dataTables[self.index].isExistData()
        # mainMenuScreen.loadScreen.dataTables[self.index].checkSaveData()
        mainMenuScreen.loadScreen.updateData(self.index)
        # self.checkSaveData()
        # self.hasSaveData = False

    def changeLang(self):
        if os.path.isfile(self.filename) is True:
            with open(self.filename, "r") as file:
                data = json.load(file)
            
            saveTimeData = data["saveTime"]
            dayData = data["inGameData"]["Days"]

            if gameData["lang"] == Language.EN.value:
                stageText = "Stage: " + dayData
            elif gameData["lang"] == Language.KR.value:
                # stageText = "Stage: " + inGameData["Days"]
                stageText = dayData + "단계"
            
            saveTimeText = str(saveTimeData["Year"]) + "/" + str(saveTimeData["Month"]) + "/" + str(saveTimeData["Day"]) + divide + \
                            str(saveTimeData["Hour"]) + ":" + str(saveTimeData["Minute"]) + ":" + str(saveTimeData["Second"])
            self.dataText = stageText + divide + saveTimeText
            self.loadBtn.changeTxt(self.dataText, txtColor=WHITE)
            
        if gameData["lang"] == Language.EN.value:
            self.delBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.delBtn.changeTxt(Language="KR")


class LoadTable(dataTable):
    def __init__(self, index, margin):
        super().__init__(index)

        # self.dummyBtn = Button((self.bg.rect.width, self.bg.rect.height), fillColor=TRANSPARENCY, isActive=True)
        self.dummyBtn = Button((self.bg.rect.width, self.bg.rect.height), isActive=True, imageName="dataTableBG", Dir="buttons" + divide + "dataTables", edgeImageName="dataTableBGEdge")
        self.setPos(margin)
        self.addObjs(self.bg)
        self.isExistData()
    
    def isExistData(self):
        '''
            만약 파일이 있다면 불러오기/삭제 버튼을 띄워주며(obj에 추가하며)
            만약 파일이 없다면 저장 버튼을 띄워준다.
        '''
        if os.path.isfile(self.filename) is True:
            self.updateObjs(update=[self.loadBtn, self.delBtn], remove=self.dummyBtn)
            self.hasSaveData = True
        else:
            self.updateObjs(update=self.dummyBtn, remove=[self.loadBtn, self.delBtn])
            self.hasSaveData = False

    def select(self, select):
        if select == self.loadBtn:
            self.load()
            return False
        elif select == self.delBtn:
            self.delete()
            return True

    def setPos(self, margin):
        super().setPos(margin)
        # self.bg.rect.y = margin + (self.bg.rect.height * self.index) + (margin * self.index)
        # self.loadBtn.setPos(right=self.bg.rect.centerx - self.loadBtn.rect.width, bottom=self.bg.rect.bottom - self.margin)
        # self.delBtn.setPos(x=self.bg.rect.centerx + self.loadBtn.rect.width, bottom=self.bg.rect.bottom - self.margin)
        # self.dummyBtn.setPos(centerx=self.bg.rect.centerx, bottom=self.bg.rect.bottom - self.margin)
        self.dummyBtn.setPos(centerx=self.bg.rect.centerx, y=margin + (self.dummyBtn.rect.height * self.index) + (margin * self.index))

    def checkSaveData(self):
        # update, add 들어가는건 스택 형식
        # Last in First Out
        # 첫번째 인자가 가장 마지막 레이어가 된다.
        if self.hasSaveData is True:
            # self.updateObjs(remove=[self.loadBtn, self.delBtn], update=self.saveBtn)
            self.changeObjs(0,  [self.loadBtn, self.delBtn], self.dummyBtn)
        else:
            # self.updateObjs(remove=self.saveBtn, update=[self.loadBtn, self.delBtn])
            self.changeObjs(0, self.dummyBtn, [self.loadBtn, self.delBtn])

    def changeLang(self):
        super().changeLang()


class Save_n_LoadTable(dataTable):
    def __init__(self, index, margin):
        super().__init__(index)
        # width  : 230 // 5 = 46
        # height : 160 // 5 = 32
        if gameData["lang"] == Language.EN.value:
            # self.saveBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), BLACK, "Save", 16, WHITE)
            self.saveBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), imageName="saveButtonEN", Dir="buttons" + divide + "optionButtons", edgeImageName="saveButtonEdge")
        elif gameData["lang"] == Language.KR.value:
            # self.saveBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), BLACK, "저장", 16, WHITE)
            self.saveBtn = Button((self.bg.rect.width // 5, self.bg.rect.height // 5), imageName="saveButtonKR", Dir="buttons" + divide + "optionButtons", edgeImageName="saveButtonEdge")
        self.setPos(margin)
        self.addObjs(self.bg)
        self.isExistData()

    def isExistData(self):
        '''
            만약 파일이 있다면 불러오기/삭제 버튼을 띄워주며(obj에 추가하며)
            만약 파일이 없다면 저장 버튼을 띄워준다.
        '''
        if os.path.isfile(self.filename) is True:
            self.updateObjs(update=[self.loadBtn, self.delBtn], remove=self.saveBtn)
            self.hasSaveData = True
        else:
            self.updateObjs(update=self.saveBtn, remove=[self.loadBtn, self.delBtn])
            self.hasSaveData = False

    def select(self, select):
        # save, delete 함수는 버튼을 바뀌게 하는 함수이다.
        if select == self.saveBtn:
            self.save()
            return True
        elif select == self.loadBtn:
            self.load()
            return False
        elif select == self.delBtn:
            self.delete()
            return True

    def setPos(self, margin):
        super().setPos(margin)
        # self.bg.rect.y = margin + (self.bg.rect.height * self.index) + (margin * self.index)
        # self.loadBtn.setPos(right=self.saveBtn.rect.x, bottom=self.bg.rect.bottom - self.margin)
        # self.delBtn.setPos(x=self.saveBtn.rect.right, bottom=self.bg.rect.bottom - self.margin)
        self.saveBtn.setPos(centerx=self.bg.rect.centerx, bottom=self.bg.rect.bottom - self.margin)

    def checkSaveData(self):
        # update, add 들어가는건 큐 형식
        # Last in First Out
        # 첫번째 인자가 가장 마지막 레이어가 된다.
        if self.hasSaveData is True:
            # self.updateObjs(remove=[self.loadBtn, self.delBtn], update=self.saveBtn)
            self.changeObjs(0, [self.loadBtn, self.delBtn], self.saveBtn)
        else:
            # self.updateObjs(remove=self.saveBtn, update=[self.loadBtn, self.delBtn])
            self.changeObjs(0, self.saveBtn, [self.loadBtn, self.delBtn])

    def changeLang(self):
        super().changeLang()
        if gameData["lang"] == Language.EN.value:
            self.saveBtn.changeTxt(Language="EN")
        elif gameData["lang"] == Language.KR.value:
            self.saveBtn.changeTxt(Language="KR")

    #? 인 게임에서 저장하는 데이터 목록
        #? 현재 시간
        #? 스테이지
        #? 플레이어 인벤토리: (need)인덱스, 아이템 이름
        #? 동물들 위치, 동물들의 수
        #? 플레이어 위치
        #? 플레이어 탄약 수
        #? 플레이어 최대 탄약 수
        #? 코인 수
        #? 플레이어 목숨
        #? 스테이지 데이터
        #? 등등..
    def save(self):
        saveTime = {
            "Year": getTime().year,
            "Month": getTime().month,
            "Day": getTime().day,
            "Hour": getTime().hour,
            "Minute": getTime().minute,
            "Second": getTime().second,
        }

        saveData = {
            "saveTime": saveTime,
            "inGameData": inGameData,
            "playerPos": [
                    player.rect.x,
                    player.rect.y
                ],
            "playerAmmo": player.ammo,
            "playerMaxAmmo": player.maxAmmo,
            "playerLife": player.life,
            "coin": player.coin,
        }
        with open(self.filename, "w") as file:
            json.dump(saveData, file, indent="\t")
        self.isHaveData()
        self.checkSaveData()
        self.hasSaveData = True
        # mainMenuScreen.loadScreen.dataTables[self.index].isExistData()
        # mainMenuScreen.loadScreen.dataTables[self.index].checkSaveData()
        mainMenuScreen.loadScreen.updateData(self.index)


# temporary Classes
class Sprites:
    def __init__(self):
        self.mainSprite = pg.sprite.Group()

    def add(self, sprite=None, spriteType=None):
        self.mainSprite.add(sprite)
        # condition to spriteType
        # accroding to spriteType add to sprite
    
    def update(self):
        # All sprites update
        self.mainSprite.update()

    def draw(self):
        # All sprites draw
        pass


class Rect:
    def __init__(self, width, height):
        # x, y, right, bottom
        # width, height, centerx, centery
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.right = self.x + width
        self.bottom = self.y + height
        self.centerx = self.x + (width // 2)
        self.centery = self.y + (height // 2)
    
    def reSetPos(self):
        self.x = self.right - self.width
        self.y = self.bottom - self.height
        self.right = self.x + width
        self.bottom = self.y + height
        self.centerx = self.x + (width // 2)
        self.centery = self.y + (height // 2)

    def setPos(self, **kwargs):
        for key, value in kwargs.items():
            if key == "x":
                self.x = value
            elif key == "y":
                self.y = value
            elif key == "right":
                self.right = value
            elif key == "bottom":
                self.bottom = value
            elif key == "centerx":
                self.centerx = value
            elif key == "centery":
                self.centery = value


# Sprite Groups
mainSprite = pg.sprite.Group()
# sprite groups for collision or other
animals = pg.sprite.Group() # enemy
playerFoods = pg.sprite.Group()   # bullet
animalFoods = pg.sprite.Group()
items = pg.sprite.Group()
barrels = pg.sprite.Group()
btns = pg.sprite.Group()

# user class
sprites = Sprites()

# Sprites
bg1 = Background(0)
bg2 = Background(-windowHeight)
mainSprite.add(bg1)
mainSprite.add(bg2)

lBarrel = Barrel("left")
mainSprite.add(lBarrel)
barrels.add(lBarrel)

rBarrel = Barrel("right")
mainSprite.add(rBarrel)
barrels.add(rBarrel)

player = Player()
mainSprite.add(player)

store = Store()

# Buttons
menuBtn = MenuButton()
# storeBtn = StoreButton()

# Screens
mainMenuScreen = MainMenuScreen()
menuScreen = MenuScreen()
optionScreen = OptionScreen()

# functions
def gameOver():
    global isGameOver, gameRun
    # print("Game Over!")
    gameOverText = "Game Over!"
    fontSize = 16
    while True:
        showText(BLACK, (screen.centerx - len(gameOverText) * (fontSize // 4), windowHeight // 2), gameOverText, fontSize=fontSize)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                # 임시
                if event.key == pg.K_TAB:
                    isGameOver = False
                    player.life = 3
                    return
                # 게임 종료
                if event.key == pg.K_RETURN:
                    isGameOver = False
                    gameRun = False
                    return

def stageSetting():
    '''
        데이터를 불러올 때 호출
        다음 스테이지를 시작할 때 호출
    '''
    global animalSpawnLastTime
    # 남아있는 동물, 아이템 삭제
    # remove remaining animals and item
    # 음.. 동물과 아이템은 각자의 그룹이 있으며 그 그룹은 또 메인 스프라이트에 속하기 때문에
    # 각자의 그룹에 있는 것들을 다 비우고 메인 스프라이트에 있는 동물과 아이템 부분을 없앤다.
    # 만약 음식(탄약도 있다면 같이 없앰)
    mainSprite.remove(animals.sprites())
    animals.empty()
    mainSprite.remove(items.sprites())
    items.empty()
    mainSprite.remove(playerFoods.sprites())
    playerFoods.empty()
    mainSprite.remove(animalFoods.sprites())
    animalFoods.empty()

    # 스테이지에 맞춰서 동물의 최소 스폰 딜레이와 최대 스폰 딜레이를 설정해야 한다.
    animalSpawnLastTime = getTick()

    # UI나 배럴을 inGameData["isReversal"]에 따라 위치를 설정하는 함수를 호출해야 한다.
    lBarrel.replace()
    rBarrel.replace()
    menuBtn.replace()
    # storeBtn.replace()

def stageStart():
    global isStageClear, lastTime, pauseCurTime, inGameData
    # 최대 시간 늘리기, 일 수(스테이지) +1, 스테이지 클러이 변수 False
    # 시간 기록 초기화
    # 스테이지에 따라 반전이 있는가 없는가 확인 후 변경
    isStageClear = False
    if eval(inGameData["Days"]) < len(StageData):
        inGameData["Days"] = str(eval(inGameData["Days"]) + 1)
    lastTime = getTick()
    pauseCurTime = 0
    inGameData["isReversal"] = true_or_false()

    stageSetting()

# loop
def stageClear():
    # stageClearText = "Stage " + inGameData["Days"] + " Clear!"
    # fontSize = 16

    store.Open(player)
    stageStart()
    return
    # while True:
    #     showText( BLACK, (screen.centerx - len(stageClearText) * (fontSize // 4), windowHeight // 2), stageClearText, fontSize=fontSize)
    #     pg.display.flip()
        
    #     for event in pg.event.get():
    #         if event.type is pg.KEYDOWN:
    #             if event.key is pg.K_BACKSLASH:
    #                 stageStart()
    #                 return
    #         if event.type is pg.MOUSEBUTTONDOWN:
    #             m_pos = pg.mouse.get_pos()
    #             store.Open(player)

def animalSpawn(animalType):
    global animalSpawnLastTime, animalSpawnDelay
    now = getTick()
    # margin = 15
    if now - animalSpawnLastTime > animalSpawnDelay:
        animalSpawnLastTime = now
        animalSpawnDelay = random.randint(StageData[inGameData["Days"]]["minSpawnDelay"], StageData[inGameData["Days"]]["maxSpawnDelay"])

        x = random.randint(0, windowWidth - StageData[inGameData["Days"]]["width"])

        animal = Animal(x, animalType, AnimalData[animalType]["speed"])
        mainSprite.add(animal)
        animals.add(animal)

# 분:초:초초
# def showTimeRemaining(minute, second, millisecond):
    # fontSize = 20
    # remainTimeText = str(minute) + " : " + str(second) + " : " + str(millisecond)
    # showText(BLACK, (screen.centerx - len(remainTimeText) * (fontSize // 4), 10), remainTimeText, fontSize=fontSize)

def showTime(minute, second, millisecond):
    fontSize = 20
    remainTimeText = str(minute) + " : " + str(second) + " : " + str(millisecond)
    showText(BLACK, (screen.centerx - len(remainTimeText) * (fontSize // 4), 10), remainTimeText, fontSize=fontSize)

# def TimeOutCheck():
    # global isStageClear, remainTime, now
    # if isPause is False:
    #     # 시간 줄어듬
    #     now = getTick()
    #     remainTime = now - lastTime
    #     print(remainTime)
    #     minTime = (StageData[inGameData["Days"]]["timeOut"] // 60) # 60 // 70 = 0
    #     secTime = (StageData[inGameData["Days"]]["timeOut"] - (StageData[inGameData["Days"]]["timeOut"] % 60))  # 60 % 70 = 60
    #     # 시간히 서서히 줄어든다.
    #     # 밀리세컨드 분 변환 : 시간 값(minTime)을 60000으로 나눈다.
    #     minute = minTime - (remainTime // 60000)
    #     remain = (remainTime % 60000)
    #     # 밀리세컨드 초 변환 : 시간 값(secTime)을 1000으로 나눈다.
    #     second = secTime - (remainTime // 1000)
    #     remain = (remainTime % 1000)
    #     millisecond = remain % 1000

    #     # show Time Remaining
    #     showTimeRemaining(minute, second, millisecond)

    #     if minute <= 0 and second <= 0 and millisecond <= 0:
    #         isStageClear = True

def TimeOutCheck():
    global isStageClear, inGameData
    now = getTick()
    # 문제가 되는 부분
    # 시간을 플러스 하는게 아니라 계속해서 대입을 하기 때문에
    # 무슨 짓을 해도 여기서 초기화가 되어버리기 때문에 0부터 시작하게 된다.
    # 해결!!
    inGameData["curTime"] = pauseCurTime + (now - lastTime) # tick value

    # 시간 알려주기
    minute = inGameData["curTime"] // 60000
    remain = inGameData["curTime"] % 60000
    second = remain // 1000
    millisecond = remain % 1000

    showTime(minute, second, millisecond)

    # 시간 체크하기
    checkMinute = StageData[inGameData["Days"]]["timeOut"] // 60
    checkSecond = StageData[inGameData["Days"]]["timeOut"] % 60
    if minute is checkMinute and second is checkSecond:
        isStageClear = True

def update():
    global coinText, ammoText, isGameOver 
    mainSprite.update()
    animalSpawn(StageData[inGameData["Days"]]["animalType"])
    
    # hit in First parameter
    # Catch the animal
    # Bullet hit the animal
    hits = pg.sprite.groupcollide(animals, playerFoods, False, True)
    # print(hits)
    for hita, hitb in hits.items(): # hit is animal
        # hita is Animal Class, hitb is Food Class
        # how to get the bullet?
        # hit.hit(player.damage)
        # Animal foodTypeCheck(self, foodType, damage)
        hita.foodTypeCheck(hitb[0].foodType, player.damage)
    
    # eat Item
    hits = pg.sprite.spritecollide(player, items, True)
    for hit in hits:
        if hit.wideRange == "throw":
            player.throwDelay += hit.iThrowDelay
        elif hit.wideRange == "speed":
            player.speed += hit.iSpeed
        elif hit.wideRange == "damag":
            player.damage += hit.iDamage
        elif hit.wideRange == "coin":
            player.coin += hit.iCoin

    coinText = "Coin: " + str(player.coin)
    # coinTextObj = font.render(coinText, True, BLACK)

    ammoText = "Ammo: " + str(player.ammo)
    # ammoTextObj = font.render(ammoText, True, BLACK)
    
def draw():
    window.fill(WHITE)
    mainSprite.draw(window)

    fontSize = 16
    # 코인 표시
    showText(BLACK, (20, windowHeight - fontSize * 2), coinText, fontSize=fontSize)
    # 탄약 표시
    showText(BLACK, (windowWidth - len(ammoText) * fontSize // 1.5, windowHeight - fontSize * 2), ammoText, fontSize=fontSize)

    # Inventory
    player.inv.draw()
    
    # UI
    player.showLife()

    # 스테이지 표시
    dayText = "Stage: " + inGameData["Days"]
    showText(BLACK, (screen.centerx - len(dayText) * (fontSize // 4), windowHeight - fontSize * 2), dayText)

    menuBtn.draw()

def events():
    global gameRun, debugMode, isShowStat, isPause, lastTime, pauseCurTime
    for event in pg.event.get():
        if event.type is pg.QUIT:
            gameRun = False
        if event.type is pg.KEYDOWN:
            # 종료 버튼 (임시)
            if event.key is pg.K_TAB:
                # gameRun = False
                player.inv.changeItem()
            # 디버그 모드 On/Off
            if event.key is pg.K_BACKQUOTE:
                # print(player.speed, player.throwDelay)
                debugMode = not debugMode
            # 반전 켜기 (디버그 모드 전용)
            if event.key is pg.K_BACKSLASH:
                # if debugMode is True:
                #     inGameData["isReversal"] = not inGameData["isReversal"]
                pass
            # 재장전 버튼
            if event.key is pg.K_RETURN:
                lBarrel.reload(player)
                rBarrel.reload(player)
            if pg.key.get_mods() & pg.KMOD_ALT:
                if debugMode is True:
                    # 속성 표시
                    isShowStat = not isShowStat
            # 일시정지 (인게임 메뉴)
            if event.key is pg.K_ESCAPE:
                isPause = True
                pauseCurTime = inGameData["curTime"]
                menuScreen.showScreen()
            # 인벤토리 보여주기, 안보여주기
            if event.key is pg.K_LEFTBRACKET:
                if gameData["invPos"] == "right":
                    player.inv.visibleConfig(True)
                elif gameData["invPos"] == "left":
                    player.inv.visibleConfig(False)
            if event.key is pg.K_RIGHTBRACKET:
                if gameData["invPos"] == "right":
                    player.inv.visibleConfig(False)
                elif gameData["invPos"] == "left":
                    player.inv.visibleConfig(True)
            # 상점 단축키
            if event.key == pg.K_s:
                isPause = True
                pauseCurTime = inGameData["curTime"]
                store.Open(player)
        if event.type is pg.MOUSEBUTTONDOWN:
            m_pos = pg.mouse.get_pos()

            if pg.mouse.get_pressed()[0] is 1:
                # 일시정지 (옵션, 상점)
                menuBtn.clickBtn(m_pos)
                # storeBtn.clickBtn(m_pos, player.coin)
                # pass

# debugMode
statMargin = 20
statBG = pg.Surface((140, 130))
statBG.fill(WHITE)
statBGRect = statBG.get_rect()
statBGRect.x = statBGRect.y = statMargin
def showStat():
    if isShowStat is True:
        # rect(surface, color, rect, width=0) -> Rect
        pg.draw.rect(window, BLACK, (statBGRect.x - 1, statBGRect.y - 1, statBGRect.width + 1, statBGRect.height + 1), 2)
        window.blit(statBG, (statBGRect.x, statBGRect.y))

        # oops
        speedStat = "Speed: " + str(player.speed)
        throwDelayStat = "Throw Delay Stat: " + str(player.throwDelay)
        damageStat = "Damage: " + str(player.damage)

        showText(BLACK, (statBGRect.x + (statMargin // 2), statBGRect.y + statMargin), speedStat, fontSize=12)
        showText(BLACK, ((statBGRect.x + (statMargin // 2), statBGRect.y + (statMargin * 2))), throwDelayStat, fontSize=12)
        showText(BLACK, ((statBGRect.x + (statMargin // 2), statBGRect.y + (statMargin * 3))), damageStat, fontSize=12)

def debugDisplay():
    if debugMode is True:
        # 경계선 표시
        pg.draw.line(window, BLUE, (0, windowHeight / inGameData["Boundary"]), (windowWidth, windowHeight / inGameData["Boundary"]))
        pg.draw.line(window, BLUE, (0, windowHeight - windowHeight / inGameData["Boundary"]), (windowWidth, windowHeight - windowHeight / inGameData["Boundary"]))
        
        # 중앙선 표시
            # 세로선
        pg.draw.line(window, TEAL, (screen.centerx, 0), (screen.centerx, screen.bottom))
            # 가로선
        pg.draw.line(window, TEAL, (0, screen.centery), (screen.right, screen.centery))

        # 디버그 모드 표시
        debugText = "DebugMode: " + str(debugMode)
        showText(debugText, BLACK, (screen.x + 20, screen.y + 20))

        # 스탯 창 표시
        showStat()

def gameLoad():
    '''
        Game Load
        스테이지, 반전 여부만 빼고 나머지랑 다 똑같지 않다.
        플레이어 정보도 리셋은 안된다.
    '''
    global lastTime, pauseCurTime, animalSpawnLastTime, StageData, isPause, lastTime, gameRun, inGameData
    # 게임 시작 시 데이터들을 초기화 한다.    
    isPause = False
    lastTime = getTick()
    gameRun = True

    # 초기화 목록
    # 일 수(스테이지) 1로 초기화, 플레이어 인벤토리 초기화(메소드 이용)
    # 플레이어 초기화(메소드 만들기), 시간 초기화
    lastTime = getTick()
    animalSpawnLastTime = getTick()

    # player.reset()
    lBarrel.reset()
    rBarrel.reset()
    store.reset()
    bg1.reset()
    bg2.reset()
    menuBtn.reset()

    mainSprite.remove(animals.sprites())
    animals.empty()
    mainSprite.remove(items.sprites())
    items.empty()
    mainSprite.remove(playerFoods.sprites())
    playerFoods.empty()
    mainSprite.remove(animalFoods.sprites())
    animalFoods.empty()

def gameStart():
    '''
        게임 시작 부분
    '''
    global lastTime, pauseCurTime, animalSpawnLastTime, StageData, isPause, lastTime, gameRun, inGameData
    # 게임 시작 시 데이터들을 초기화 한다.    
    isPause = False
    lastTime = getTick()
    gameRun = True
    inGameData["Days"] = "1"
    inGameData["isReversal"] = true_or_false()

    # 초기화 목록
    # 일 수(스테이지) 1로 초기화, 플레이어 인벤토리 초기화(메소드 이용)
    # 플레이어 초기화(메소드 만들기), 시간 초기화
    lastTime = getTick()
    animalSpawnLastTime = getTick()

    player.reset()
    lBarrel.reset()
    rBarrel.reset()
    store.reset()
    bg1.reset()
    bg2.reset()
    menuBtn.reset()

    mainSprite.remove(animals.sprites())
    animals.empty()
    mainSprite.remove(items.sprites())
    items.empty()
    mainSprite.remove(playerFoods.sprites())
    playerFoods.empty()
    mainSprite.remove(animalFoods.sprites())
    animalFoods.empty()

# Main game loop
def playGame():
    global isGameOver

    while gameRun:
        clock.tick(FPS)
        events()

        update()
        draw()
        if isPause is False:
            TimeOutCheck()
        debugDisplay()

        # Game Over
        if player.life == 0:
            isGameOver = True
            gameOver()

        # Stage Clear
        if isStageClear is True:
            stageClear()

        pg.display.flip()

if __name__ == '__main__':
    mainMenuScreen.showScreen()

    save()
    pg.quit()