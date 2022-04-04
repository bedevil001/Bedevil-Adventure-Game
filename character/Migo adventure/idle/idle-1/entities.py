import pygame
from pygame.locals import *

# physics
def CollisionTest(Object1,ObjectList):
    CollisionList = []
    for Object in ObjectList:
        if Object.colliderect(Object1):
            CollisionList.append(Object)
    return CollisionList

class PhysicsObject(object):
    
    def __init__(self,x,y,x_size,y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
        
    def move(self,Movement,platforms):
        self.x += Movement[0]
        self.rect.x = int(self.x)
        block_hit_list = CollisionTest(self.rect,platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        for block in block_hit_list:
            if Movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
            elif Movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
            self.x = self.rect.x
        self.y += Movement[1]
        self.rect.y = int(self.y)
        block_hit_list = CollisionTest(self.rect,platforms)
        for block in block_hit_list:
            if Movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
            elif Movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
            self.change_y = 0
            self.y = self.rect.y
        return collision_types
            
    def Draw(self):
        pygame.draw.rect(screen,(0,0,255),self.rect)
        
    def CollisionItem(self):
        CollisionInfo = [self.rect.x,self.rect.y,self.width,self.height]
        return CollisionInfo

def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)

class entity(object):
    global animation_database
    
    def __init__(self,x,y,size_x,size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.obj = PhysicsObject(x,y,size_x,size_y)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]

    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y

    def move(self,momentum,platforms):
        collisions = self.obj.move(momentum,platforms)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions

    def rect(self):
        return pygame.Rect(self.x,self.y,self.size_x,self.size_y)

    def set_flip(self,boolean):
        self.flip = boolean

    def set_animation_tags(self,tags):
        self.animation_tags = tags

    def set_animation(self,sequence):
        self.animation = sequence
        self.animation_frame = 0

    def clear_animation(self):
        self.animation = None

    def set_image(self,image):
        self.image = image

    def set_offset(self,offset):
        self.offset = offset

    def set_frame(self,amount):
        self.animation_frame = amount

    def change_frame(self,amount):
        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation)-1

    def get_current_img(self):
        if self.animation == None:
            if self.image != None:
                return flip(self.image,self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]],self.flip)

    def display(self,surface,scroll):
        if self.animation == None:
            if self.image != None:
                surface.blit(flip(self.image,self.flip),(int(self.x)-scroll[0]+self.offset[0],int(self.y)-scroll[1]+self.offset[1]))
        else:
            surface.blit(flip(animation_database[self.animation[self.animation_frame]],self.flip),(int(self.x)-scroll[0]+self.offset[0],int(self.y)-scroll[1]+self.offset[1]))

# animation stuff
global animation_database
animation_database = {}

# a sequence looks like [[0,1],[1,1],[2,1],[3,1],[4,2]]
# the first numbers are the image name(as integer), while the second number shows the duration of it in the sequence
def animation_sequence(sequence,base_path,colorkey=(255,255,255),transparency=255):
    global animation_database
    result = []
    for frame in sequence:
        image_id = base_path + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result


def get_frame(ID):
    global animation_database
    return animation_database[ID]

