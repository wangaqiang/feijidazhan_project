import pygame
import time
import random
from pygame.locals import *


class BasePlane(object):
    def __init__(self, screen, x, y, image_name):
        self.screen = screen
        self.x = x
        self.y = y
        self.feiji = pygame.image.load(image_name)
        self.bullet_list = []  #存放子弹对象的列表

    def display(self):
        '''将飞机放在窗口上'''
        self.screen.blit(self.feiji, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()  #调用子弹的显示方法
            bullet.move()  #调用我方子弹向上移动方法
            if bullet.judge():  #越界的子弹进行删除
                self.bullet_list.remove(bullet)

class HeroPlane(BasePlane):
    '''英雄飞机类'''
    def __init__(self, screen):
        BasePlane.__init__(self, screen, 200, 700, "./feiji/hero1.png") #调用父类的__init__方法
        
    def left_move(self):
        '''向左移动'''
        self.x-=30
        
    def right_move(self):
        '''向右移动'''
        self.x+=30
        
    def up_move(self):
        '''向上移动'''
        self.y-=30

    def down_move(self):
        '''向下移动'''
        self.y+=30

    def fire(self):
        '''飞机开火'''
        #将飞机的坐标传给子弹　　让子弹随着飞机的位置变化而变化
        self.bullet_list.append(HeroBullet(self.screen, self.x, self.y))

class EnemyPlane(BasePlane):
    '''敌人飞机类'''
    def __init__(self, screen):
        super().__init__(screen, 0, 0, "./feiji/enemy0.png") #调用父类的__init__方法
        self.direction = "right" #默认移动方向向右
        
    def move(self):
        '''左右移动'''
        #判断正在向那个方向运动
        if self.direction == "right":
            self.x+=2
        else:
            self.x-=2

        #判断应该向那个方向运动
        if self.x>430:  
            self.direction = "left"
        elif self.x<0:
            self.direction = "right"

    def fire(self):
        '''飞机开火'''
        random_num = random.randint(1,80)
        if random_num == 20 or random == 60:
            #将飞机的坐标传给子弹　　让子弹随着飞机的位置变化而变化
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))

class BaseBullet(object):
    def __init__(self, screen, x, y, image_name):
        self.screen = screen
        self.x = x
        self.y = y
        self.bullet = pygame.image.load(image_name)

    def display(self):
        '''显示子弹'''
        self.screen.blit(self.bullet, (self.x, self.y))

class HeroBullet(BaseBullet):
    '''英雄子弹类'''
    def __init__(self, screen, x, y):
        #　调用父类的__init__方法
        BaseBullet.__init__(self, screen, x+40, y-20, "./feiji/bullet.png")
    
    def move(self):
        '''英雄子弹向上移动'''
        self.y-=20

    def judge(self):
        '''判断子弹是否越界'''
        if self.y<0:  #越界返回真
            return True
        else:
            return False
        
class EnemyBullet(BaseBullet):
    '''敌人子弹类'''
    def __init__(self, screen, x, y):
        super().__init__(screen, x+20, y+40, "./feiji/bullet1.png")
    
    def move(self):
        '''敌机子弹向下移动'''
        self.y += 5

    def judge(self):
        '''判断子弹是否越界'''
        if self.y>852:  #越界返回真
            return True
        else:
            return False


def key_control(feiji):
    '''控制飞机移动和开火函数'''
    for event in pygame.event.get():  #检测事件
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                feiji.left_move()
            elif event.key == K_d or event.key == K_RIGHT:
                feiji.right_move()
            elif event.key == K_w or event.key == K_UP:
                feiji.up_move()
            elif event.key == K_s or event.key == K_DOWN:
                feiji.down_move()
            elif event.key == K_SPACE:
                feiji.fire()


def main():
    '''主函数'''
    # １．创建窗口
    screen = pygame.display.set_mode((480,852), 0, 12) #FULLSCREEN
    pygame.display.set_caption("plane-combat (author:laowang)")  #标题栏
    background = pygame.image.load("./feiji/background.png") #背景
    
    # ２．创建飞机对象
    ourplane = HeroPlane(screen)
    enemyplane = EnemyPlane(screen)
    
    # ３．主循环
    while True:
        #给窗口添加背景　 
        screen.blit(background,(0,0))
        ourplane.display() #调用飞机显示在窗口的方法
        enemyplane.display() #调用敌机显示在窗口的方法
        enemyplane.fire() #敌机开火
        enemyplane.move() #调用敌机移动方法
        key_control(ourplane) #调用控制英雄移动和开火函数进行检测事件

        time.sleep(0.01)  #硬件不行需要让程序跑慢点　不然小风扇呼呼的转
        #刷新窗口准备下一帧动画
        pygame.display.update() 

if __name__ == "__main__":
    main()
