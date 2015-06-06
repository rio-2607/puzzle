# -*-coding:utf-8 -*-
####################################################################################
#作者：唐门黄老邪
#时间：2013年6月4号
#邮箱：huanglaoxie2607@gmail.com
####################################################################################
#导入所需要的库
import pygame
from pygame.locals import *
from sys import exit
import random
from random import *
import time

subimage_width = 100        #切割图片的宽度
subimage_hieght = 100       #切割图片的高度
#定义常用的颜色RGB值
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
class SubImage(object):
    """定义每个切割后的子图片类，每个子图片都有一个Surface成员，用来绘制自身
    变量x,y在drawself函数中表示在父图片中的左上角坐标，其他用处则表示每个SubImage对象在主对话框中的绘制坐标
    image表示父图片
    id表示每个SubImage对象在indexlist中的索引
    """
    def __init__(self,(x,y),image,id):
        self.surface = pygame.Surface((100,100))
        self.x = x
        self.y = y
        self.image = image
        self.id = id
    def drawself(self):
        self.surface.blit(self.image.subsurface(self.x,self.y,subimage_width,subimage_hieght),(0,0))
    def setxy(self,x,y):
        self.x = x
        self.y = y
    def setid(self,newid):
        self.id = newid
    def getxy(self):
        return self.x,self.y
    def getid(self):
        return self.id
        
        
#判断能否移动图片
def move_direction(index_list):
    """思路是：根据0在列表中的位置，判断是否可以移动，如果可以移动，则字典中
    对应方向的键的值设置为True
    """
    direction_dic = {"up":False,"down":False,"left":False,"right":False}
    if 0 == index_list[0]:
        direction_dic["up"] = True
        direction_dic["left"] = True
    elif 0 == index_list[1]:
        direction_dic["up"] = True
        direction_dic["left"] = True
        direction_dic["right"] = True
    elif 0 == index_list[2]:
        direction_dic["up"] = True
        direction_dic["right"] = True
    elif 0 == index_list[3]:
        direction_dic["left"] = True
        direction_dic["down"] = True
        direction_dic["up"] = True
    elif 0 == index_list[4]:
        direction_dic["up"] = True
        direction_dic["down"] = True
        direction_dic["left"] = True
        direction_dic["right"] = True
    elif 0 == index_list[5]:
        direction_dic["up"] = True
        direction_dic["down"] = True
        direction_dic["right"] = True
    elif 0 == index_list[6]:
        direction_dic["down"] = True
        direction_dic["left"] = True
    elif 0 == index_list[7]:
        direction_dic["down"] = True
        direction_dic["left"] = True
        direction_dic["right"] = True
    else:
        direction_dic["down"] = True
        direction_dic["right"] = True
    return direction_dic

#根据方向键重绘图片
def paint(direction,screen):
    """这是程序主要的部分,根据按键的情况做相应的移动并且重新绘制图像
    以0所在的位置为中心，如果向左移，0所在列表中的索引值index应该与索引为index+1的交换，
    向右移，则与索引为index-1的数据交换，其他方向见代码
    """ 
    global indexlist
    global subimages
    global steps
    steps += 1
    zeroindex = indexlist.index(0)
    temp_x,temp_y = 0,0
    temp = 0
    temp_index = 0
    if "up" == direction:
        temp_index = zeroindex + 3
    elif "down" == direction:
        temp_index = zeroindex - 3
    elif "left" == direction:
        temp_index = zeroindex + 1
    else:
        temp_index = zeroindex - 1
    
    temp = indexlist[temp_index]
    indexlist[temp_index] = 0
    indexlist[zeroindex] = temp
    
    for image in subimages.values():
        if zeroindex == image.getid():
            image1 = image
        if temp_index == image.getid():
            image2 = image
        
    temp_x,temp_y = image1.getxy()
    image1.setxy(image2.x,image2.y)
    image2.setxy(temp_x,temp_y)
    image1.setid(temp_index)
    image2.setid(zeroindex)
    
    screen.blit(image1.surface,(image1.x,image1.y))
    screen.blit(image2.surface,(image2.x,image2.y))


def draw_info(font,surfacetodraw,step,minutes,seconds):
    surfacetodraw.fill(black)
    step_to_str = str(step)
    str_step = u"已走步数：" + step_to_str
    step_surface = font.render(str_step,True,red)
    author_surface = font.render(u"作者：唐门黄老邪",True,red)
    
    now = time.localtime()
    now_min,now_sec = now.tm_min,now.tm_sec
    time_passed = now_min * 60.0 + now_sec - (minutes * 60.0 + seconds)
    str_time_passed = u"已花费时间:" + str(time_passed) + u"秒"
    time_surface = font.render(str_time_passed,True,red)
    surfacetodraw.blit(step_surface,(0,0))
    surfacetodraw.blit(time_surface,(0,step_surface.get_height()))
    surfacetodraw.blit(author_surface,(0,step_surface.get_height() + time_surface.get_height()))


pretime = time.localtime()
pretime_min,pretime_sec = pretime.tm_min,pretime.tm_sec
puzzle_image_filename = "background.jpg"
puzzle_image_back_filename = "back.jpg"

SCREEN_SIZE_WIDTH,SCREEN_SIZE_HEIGHT = (700,450)
pygame.init()


screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH,SCREEN_SIZE_HEIGHT),0,32)
font = pygame.font.Font("simsun.ttf",40)
pygame.display.set_caption("Puzzle Game V1.0")

puzzle = pygame.image.load(puzzle_image_filename).convert()
back = pygame.image.load(puzzle_image_back_filename).convert()
back_surface = back.subsurface(0,0,50,50)
back_surface.fill(white)

info_surface = pygame.Surface((300,300))
font = pygame.font.Font("simsun.ttf",17)

coordinate = [(0,0),(100,0),(200,0),(0,100),(100,100),(200,100),(0,200),(100,200),(200,200)]

subimages = {}

for i in range(1,9):
    mysurface = SubImage(coordinate[i],puzzle,i)
    subimages[i] = mysurface
    
for image in subimages.values():
    image.drawself()
    
surface1 = SubImage(coordinate[0],puzzle,0)
surface1.surface.fill(white)
subimages[0] = surface1

#把subimages字典中的成员随机打乱
randomlist = [1,2,3,4,5,6,7,8,0]
#把randomlist列表中的数据打乱
shuffle(randomlist)
indexlist = [0,0,0,0,0,0,0,0,0]
j = 0
for i in randomlist:
    x = coordinate[i][0] + 100
    y = coordinate[i][1] + 75
    image = subimages.get(j)
    image.setxy(x,y)
    image.setid(i)
    indexlist[i] = j
    j += 1
    screen.blit(image.surface,(image.x,image.y))
    

    
direction_dic = {}

steps = 0
while True:
    for event in  pygame.event.get():
        if QUIT == event.type:
            pygame.quit()
            exit()
            
    
        if KEYDOWN == event.type:
            direction = ""
            direction_dic = move_direction(indexlist)
            if K_LEFT == event.key:
                if direction_dic["left"]:
                    direction = "left"
                    paint(direction,screen)
                else:
                    pass
            if K_RIGHT == event.key:
                if direction_dic["right"]:
                    direction = "right"
                    paint(direction,screen)
                else:
                    pass
            if K_UP == event.key:
                if direction_dic["up"]:
                    direction = "up"
                    paint(direction,screen)
                else:
                    pass
            if K_DOWN == event.key:
                if direction_dic["down"]:
                    direction = "down"
                    paint(direction,screen)
                else:
                    pass
    draw_info(font,info_surface,steps,pretime_min,pretime_sec)
    screen.blit(back,(450,75))
    screen.blit(info_surface,(450,250))
    pygame.display.update()