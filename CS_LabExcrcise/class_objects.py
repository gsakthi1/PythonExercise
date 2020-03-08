# Class & Objects

import matplotlib.pyplot as plt
 

class Circle(object):

    #Constructor
    def __init__(self, radius=3, color='blue'):
        self.radius = radius
        self.color = color

    #Method
    def add_radius(self,r):
        self.radius = self.radius+r
        return(self.radius)

    #Method
    def drawCircle(self):
        plt.gca().add_patch(plt.Circle((0, 0), radius=self.radius, fc=self.color))
        plt.axis('scaled')
        plt.show() 

class Rectangle(object):

    #Constructor
    def __init__(self,len=4,hgt=5,color='red'):
        self.width = len
        self.height = hgt
        self.color = color
        
    #Method
    def drawRect(self):
        plt.gca().add_patch(plt.Rectangle((0, 0), width=self.width, height=self.height, fc=self.color))
        plt.axis('scaled')
        plt.show()         

RedCircle = Circle(10,'red')
print(dir(RedCircle))
print(RedCircle.radius)
print(RedCircle.color)
RedCircle.drawCircle()

BlueCircle = Circle(5,'blue')
BlueCircle.drawCircle()

RedRectangle = Rectangle(1,2,'green')
BluRectangle = Rectangle(2,3,'brown')
RedRectangle.drawRect()
BluRectangle.drawRect()
