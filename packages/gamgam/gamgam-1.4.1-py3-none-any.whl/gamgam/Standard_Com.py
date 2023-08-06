from gamgam.Center import *
from gamgam.GameObject import *

class Component:
    def __init__(self):
        self.this_object = None
        self.component_name = "Component"

    def set(self, this_object):
        self.this_object = this_object

    def reflect(self):
        pass

class Collide(Component):
    def __init__(self):
        self.this_object = None
        self.is_crashed = False
        self.crashed_object = []
        self.crashed_direction = []
        self.component_name = "Collider"

    def set(self, this_object):
        self.this_object = this_object

    def reflect(self):
        if self.this_object is not None:
            self.crashed_object = []
            self.crashed_direction = []
            for i in GameObjects[now_scene()]:
                if i.type == "GameObject" or i.type == "EmptyObject":
                    if i != self:
                        crash = False
                        direct = Vector2()
                        if i.transform.position.x - (i.size.x / 2) <= self.this_object.transform.position.x + (self.this_object.size.x / 2) <= i.transform.position.x + (i.size.x / 2):
                            if i.transform.position.y + (i.size.y / 2) >= self.this_object.transform.position.y - (self.this_object.size.y / 2) >= i.transform.position.y - (i.size.y / 2):
                                crash = True
                            elif i.transform.position.y - (i.size.y / 2) <= self.this_object.transform.position.y + (self.this_object.size.y / 2) <= i.transform.position.y + (i.size.y / 2):
                                crash = True
                        elif i.transform.position.x + (i.size.x / 2) >= self.this_object.transform.position.x - (self.this_object.size.x / 2) >= i.transform.position.x - (i.size.x / 2):
                            if i.transform.position.y + (i.size.y / 2) >= self.this_object.transform.position.y - (self.this_object.size.y / 2) >= i.transform.position.y - (i.size.y / 2):
                                crash = True
                            elif i.transform.position.y - (i.size.y / 2) <= self.this_object.transform.position.y + (self.this_object.size.y / 2) <= i.transform.position.y + (i.size.y / 2):
                                crash = True
                        if crash is True:
                            if i.transform.position.x > self.this_object.transform.position.x:
                                direct.x = 1
                            elif i.transform.position.x < self.this_object.transform.position.x:
                                direct.x = -1
                            elif i.transform.position.x == self.this_object.transform.position.x:
                                direct.x = 0
                            if i.transform.position.y > self.this_object.transform.position.y:
                                direct.y = 1
                            elif i.transform.position.y < self.this_object.transform.position.y:
                                direct.y = -1
                            elif i.transform.position.y == self.this_object.transform.position.y:
                                direct.y = 0
                            self.is_crashed = True
                            self.crashed_object.append(i)
                            self.crashed_direction.append(direct)
                                
            if len(self.crashed_object) <= 0:   
                self.this_object.is_crashed = False
                    
    def find_crashed_object(self, game_object):
        is_exist = False
        for i in self.crashed_object:
            if i == game_object:
                return i
        if is_exist is False:
            return None

    def find_crashed_object_direction(self, game_object):
        is_exist = False
        for i in range(0, len(self.crashed_object)):
            if self.crashed_object[i] == game_object:
                return self.crashed_direction[i]
        if is_exist is False:
            return None