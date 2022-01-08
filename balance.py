"""
description: a puzzle game
language: python3
author: Lahari Chepuri(lc8104 @ RIT.EDU)
author: Smita Subhadarshinee Mishra(sm8528 @ RIT.EDU)
"""

import math
import turtle

HANGING_LENGTH = 50

class Weight:
    """
    Stores weight objects
    """

    __slots__ = "distance", "panWeight"

    def __init__(self, dist, wt):
        """
        sets the values of the instance variables
        """
        self.distance = dist
        self.panWeight = wt

    def getWeight(self):
        """
        fetches the weight of the weight object
        :return: panWeight
        """
        return self.panWeight

    def torque(self):
        """
        calculates the torque of the weight object
        :return: the value of the torque
        """
        if self.panWeight != -1:
            return self.panWeight*self.distance
        else:
            return 0

    def draw(self):
        """ 
        Draws each weight object on the turtle screen
        """
        turtle.left(90)
        turtle.forward(HANGING_LENGTH-15)
        turtle.penup()
        turtle.forward(15)
        turtle.write(int(self.panWeight), font=("Arial", 8, "normal"))
        turtle.backward(15)
        turtle.pendown()
        turtle.backward(HANGING_LENGTH-15)
        turtle.right(90)

    def __str__(self):
        """
        creates a string representation of the weight object
        :return: string representation of the weight object
        """
        return "dist: "+str(self.distance) + " wt: "+str(self.panWeight)

class Beam:
    """
    Stores beam objects
    """

    __slots__ = "name","scale_factor", "beams", "left", "right", "distance","left_scale","right_scale"

    def __init__(self):
        """
        sets the initial values of the instance variables
        """
        self.beams = []

    def add(self, beam):
        """
        if there is a beam hanging from the current beam,
        the, add(), adds that beam object to the current beam
         """
        self.beams.append(beam)

    def getWeight(self):
        """
        calculates the weight of the beam
        :return: weight of the beam
        """
        weight = 0
        for each in self.left:
            weight += each.getWeight()
        for each in self.right:
            weight += each.getWeight()
        for beam in self.beams:
            weight += beam.getWeight()
        return weight

    def get_torque(self):
        """
        returns the torque value of the left beam
        and the right part of the beam
        :return: left torque and right torque
        """
        left_torque = 0
        right_torque = 0
        for each in self.left:
            left_torque += each.torque()
        for each in self.right:
            right_torque += each.torque()
        for beam in self.beams:
            if beam.distance<0:
                left_torque += beam.getWeight()*beam.distance
            else:
                right_torque += beam.getWeight() * beam.distance
        return (left_torque, right_torque)

    def isBalanced(self):
        """
        Fetches the left and the right torque and checks
        if the beam is balanced based on the fetched torque values
        :return: True, if balanced, False, otherwise
        """
        balance_broken = False
        print("torque at ", self.name, "=> left: ", self.get_torque()[0], " right: ", self.get_torque()[1])
        if self.get_torque()[0] + self.get_torque()[1] == 0:
            if balance_broken is not True:
                for each in self.beams:
                    each.isBalanced()
        else:
            balance_broken = True
        return not balance_broken

    def clone(self):
        """
        creates a clone of the current object
        :return: a clone of the current object
        """
        b = Beam()
        b.name = self.name
        b.left = self.left
        b.right = self.right
        b.beams = self.beams
        b.distance = self.distance
        b.left_scale = self.left_scale
        b.right_scale = self.right_scale
        b.scale_factor = self.scale_factor
        return b

    def find_scale(self):
        """
        calculates the scale_factor for each beam so that two beams
        don't overlap eachother
        """
        left_beams= []
        right_beams = []
        current_scale = 40
        llr = ls = self.right_scale*current_scale
        lls = lr = self.left_scale*current_scale
        center_dist = current_scale*2
        for beam in self.beams:
            if beam.distance < 0:
                left_beams.append(beam)
            else:
                right_beams.append(beam)
        leftRight = leftLeft = rightLeft = rightRight = 0
        for each in left_beams:
            leftRight += abs(each.right_scale)*current_scale
            leftLeft += abs(each.left_scale)*current_scale
            ls = abs(each.right_scale)
            lls = abs(each.left_scale)
        for each in right_beams:
            rightLeft += abs(each.left_scale)*current_scale
            rightRight += abs(each.right_scale)*current_scale
            lr = abs(each.left_scale)
            llr = abs(each.right_scale)
        current_scale = ((leftRight*ls)+(rightLeft*lr) + (rightRight*llr) + (leftLeft*lls) + center_dist) / (ls+lr+llr+lls)
        if current_scale>self.scale_factor:
            self.scale_factor = current_scale

    def draw(self):
        """
        Draws the beam
        :pre:  turtle placed in the center, facing down, penup
        :post: turtle placed in the center, facing down, pendown
        """
        turtle.right(90)
        turtle.pendown()
        for each in self.left:
            turtle.forward(abs(each.distance)*self.scale_factor)
            each.draw()
            turtle.backward(abs(each.distance)*self.scale_factor)
        turtle.left(90)
        turtle.left(90)
        for each in self.right:
            turtle.forward(abs(each.distance)*self.scale_factor)
            turtle.left(180)
            each.draw()
            turtle.left(180)
            turtle.backward(abs(each.distance)*self.scale_factor)
        turtle.right(90)
        for beam in self.beams:
            if beam.distance<0:
                turtle.right(90)
                turtle.forward(abs(beam.distance) * self.scale_factor)
                turtle.left(90)
                turtle.forward(HANGING_LENGTH)
                beam.draw()
                turtle.backward(HANGING_LENGTH)
                turtle.left(90)
                turtle.forward(abs(beam.distance) * self.scale_factor)
                turtle.right(90)
            else:
                turtle.left(90)
                turtle.forward(abs(beam.distance) * self.scale_factor)
                turtle.right(90)
                turtle.forward(HANGING_LENGTH)
                beam.draw()
                turtle.backward(HANGING_LENGTH)
                turtle.right(90)
                turtle.forward(abs(beam.distance) * self.scale_factor)
                turtle.left(90)

    def find_Weight(self):
        """
        Calculates the missing weight
        """
        left_t = math.fabs(self.get_torque()[0])
        right_t = self.get_torque()[1]
        set_weight = math.fabs(left_t-right_t)
        for each in self.left:
            if each in self.left:
                if each.panWeight == -1:
                    each.panWeight = set_weight/math.fabs(each.distance)
                    print("weight of the missing pan is set to: ", each.panWeight)
        for each in self.right:
            if each in self.right:
                if each.panWeight == -1:
                    each.panWeight = set_weight/math.fabs(each.distance)
                    print("weight of the missing pan is set to: ", each.panWeight)
        for beam in self.beams:
            beam.find_Weight()

    def contains_beam(self, beamName):
        """
        checks if a particular beam is contained inside
        a main beam
        :param str: name of the beam
        :return: True, if the beam is present, else, False
        """
        for beam in self.beams:
            if beam.name == beamName:
                return True
        return False

def parseFile():
    """
    Stores the beam objects from the file
    :return: the main, root Beam('B')
    """
    file = open("beams.txt")
    start_node = None
    beams_dict = {}
    call_find_weight = False
    call_find_weight_obj = None
    for line in file:
        b = Beam()
        left = []
        right = []
        line = line.strip().split()
        b.name = line[0]
        for i in range(1, len(line), 2):
            dist = int(line[i])
            beam_or_L_R = line[i+1]
            if i == 1:
                b.left_scale = dist
            if i == len(line) - 2:
                b.right_scale = dist
            if (beam_or_L_R[0].upper() == 'B') and len(beam_or_L_R)>1:
                if beams_dict.get(beam_or_L_R) is not None:
                    cloned_obj = beams_dict.get(beam_or_L_R)
                    cloned_obj.distance = dist
                    b.add(cloned_obj)
            else:
                beam_or_L_R = int(beam_or_L_R)
                if beam_or_L_R == -1:
                    call_find_weight = True
                    call_find_weight_obj = b.name
                if dist < 0:
                    left.append(Weight(dist, beam_or_L_R))
                else:
                    right.append(Weight(dist, beam_or_L_R))
        b.left = left
        b.right = right
        b.distance = 0
        b.scale_factor = 20
        b.find_scale()
        beams_dict[b.name] = b
        if b.name == "B" or "b":
            start_node = b
    if call_find_weight:
        check_find = start_node.contains_beam(call_find_weight_obj)
        if check_find:
            start_node.find_Weight()
    return start_node

def is_balanced(node):
    """
    Prints an appropriate message after
    checking if the beam is balanced
     :param obj: the node that is to be checked
     """
    if node.isBalanced():
        print("The puzzle is balanced!")
    else:
        print("The puzzle is unbalanced!")

def init_turtle():
    """"
    Initialized the turtle screen and turtle
    :pre: turtle in the center, facing down, pen down
    :post: turtle in the center, facing down, pen up
    """
    turtle.speed(0)
    turtle.setup(width=1.0, height=1.0, startx=None, starty=None)
    turtle.penup()
    turtle.screensize(400, 400)
    turtle.setpos(400, 390)
    turtle.write("SMITA SUBHADARSHINEE MISHRA", font="normal")
    turtle.setpos(400, 360)
    turtle.write("LAHARI CHEPURI", font="normal")
    turtle.setpos(0,200)
    turtle.right(90)

def main():
    init_turtle()
    start_node = parseFile()
    is_balanced(start_node)
    start_node.find_scale()
    start_node.draw()
    turtle.update()
    turtle.mainloop()

if __name__ == '__main__':
    main()