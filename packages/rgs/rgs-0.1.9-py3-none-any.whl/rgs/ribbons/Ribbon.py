'''
Created on Jan 17, 2021

@author: vladislavkargin
'''

#import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Ribbon(object):
    '''
    This class realizes a ribbon tile for ribbon tilings.
    
    Ribbon is deetermined by its root square 
    s_{xy} (south-west corner is at (x, y)) and its shape:  
    a sequence of (n-1) zeros and ones. 
    0 means go right, 1 means go up. This list can be empty which will 
    corresponds to a ribbon tile that consist of a single square. 
    
    The ribbon has also attribute squares
    which is the list of squares in the ribbon.   
    '''


    def __init__(self, x, y, shape):
        '''
        creates a ribbon with root square s_{xy} (south-west corner is at (x, y))
        and a list of 0 and 1 that determines the shape.   
        Also creates a list of squares inside the ribbon. 
        '''
        self.x = x 
        self.y = y 
        self.shape = shape
        s = x
        t = y
        self.squares = [(s, t)]
        for d in shape:
            if d == 0:
                s = s + 1
                self.squares.append((s, t))
            else:
                t = t + 1
                self.squares.append((s, t))
     
    def __str__(self):
        '''
        Returns a string representation of this ribbon.
        return the graph
        '''
        s = '(' + str(self.x) + ',' + str(self.y) + '), ' + str(self.shape)
        return s   
                
    def level(self):
        ''' return the level of the ribbon '''
        return self.x + self.y
         
    def contains(self, x, y):
        ''' check if square (x, y) belong to ribbon 
        
        Parameters
        ----------
        x, y - integers
            The coordinates of the square
        Returns
        ----------
        boolean 
            true if the square is in the ribbon
        '''
        return (x, y) in self.squares
    
    def draw(self, ax = None, 
            colormap = 'prism',
            colorType = "Shape", 
            block = False, MaxLength = None):
        '''
        draw the ribbon.
        
        Parameters:   
        ax : matplotlib axis
            axis in which to draw (default = None)
        colormap : 'prism' 
            the name of the coloring scheme ("palette"), used to color the tiling,
            default = "prism"
            other possibilities: "jet"and many others, see matplotlib docs.
        colorType : string
            defines the type of coloring. Possible choices:
            "Shape" -- color only depends on shape
            "ShapePosition" -- color depends on shape and level (mod n)
            "Length" -- color only depends on length of the ribbon
            (default = "Shape")
            
        MaxLength : integer 
            a fine-tuning parameter used in the choice of coloring (default = None)
        block: boolean
            if True, stops the execution and draws the graph (default = False)
        
        '''
        if (ax == None):
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
        
        l = len(self.shape) # l = n - 1
        cmap = cm.get_cmap(colormap)
        if MaxLength == None:
            MaxLength = l + 2**l #this is actually not maxLength but 
                                #the max parameter for the number of 
                                #colors
        else: 
            MaxLength = max([MaxLength, l])
        
        if colorType == "Length":
            c = cmap(l/MaxLength) #for floats cmap converts interval [0,1]
                                #to the RGB range, so l should be comparable to 
                                # Maxlength
        elif colorType == "ShapePosition":
            #calculate a number that depends on the level and on 
            #the shape of the ribbon
            factor = (self.x + self.y) % (l + 1)
            i = 0
            for _, v in enumerate(self.shape):
                i = 2 * i + v 
            factor = ((factor + i) * 79) % cmap.N
            #print("Factor = ", factor)
            #print("Max Len = ", MaxLength)             
            #c = cmap(factor/MaxLength)
            c = cmap(factor) #for integers cmap converts its range 
                                    #(given by cmap.N) to RGB colors.
                                    #for prism the range is 256
        else: 
            #calculate a number that depends on 
            #the shape of the ribbon
            i = 0
            for _, v in enumerate(self.shape):
                i = 2 * i + v 
            factor = (i * 79) % cmap.N
            #print("Factor = ", factor)
            #print("Max Len = ", MaxLength)             
            #c = cmap(i/MaxLength)
            c = cmap(factor) #for integers cmap converts its range 
                                    #(given by cmap.N) to RGB colors.
            
        
        rectangle = plt.Rectangle((self.x,self.y), 1, 1, fc=c ,ec="black")
        ax.add_patch(rectangle)
        
        sx = self.x
        sy = self.y
        for i in range(len(self.shape)):
            if self.shape[i] == 0:
                rectangle = plt.Rectangle((sx,sy), 2, 1, fc=c,ec="black")
                ax.add_patch(rectangle)
                if i > 0 and self.shape[i - 1] == 0:
                    line = plt.Line2D((sx, sx),(sy, sy + 1), color = c)
                    ax.add_line(line)
                elif i > 0 and  self.shape[i - 1] == 1:
                    line = plt.Line2D((sx, sx + 1),(sy, sy), color = c)
                    ax.add_line(line) 
                sx = sx + 1 
            else:
                rectangle = plt.Rectangle((sx,sy), 1, 2, fc=c,ec="black")
                ax.add_patch(rectangle) 
                if i > 0 and self.shape[i - 1] == 0:
                    line = plt.Line2D((sx, sx),(sy, sy + 1), color = c)
                    ax.add_line(line)
                elif i > 0 and  self.shape[i - 1] == 1:
                    line = plt.Line2D((sx, sx + 1),(sy, sy), color = c)
                    ax.add_line(line) 
                sy = sy + 1
            
            
        if block:            
            plt.show()
        else:
            plt.draw()
        return fig, ax
    
    
def squares2ribbon(squares):
    ''' build a ribbon from a collection of squares.
    
    parameters
    -------------
    squares: a list of tuples (x,y)
        represent a ribbon as a collection of squares. 
        they should be in right order. (either x or y increases at each 
        step.)
    '''
    x0 = squares[0][0]
    y0 = squares[0][1]
    x = x0
    y = y0
    shape = []
    for i in range(1, len(squares)):
        if squares[i][0] - x == 1:
            shape.append(0)
            x += 1
        else: 
            shape.append(1)
            y  += 1      
    ribbon = Ribbon(x0, y0, shape)
    return ribbon
        
'''
For testing methods
'''
def main():
    print('Ribbon methods are used')  
    ribbon = Ribbon(0, 0, [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]) 
    _, ax1 = plt.subplots()
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    print(ribbon)
    print(ribbon.squares)
    ribbon.draw(ax = ax1)
    
    '''
    checking squares to ribbon
    '''
    #squares = [(0,0), (0, 1), (1, 1)]
    squares = [(0, 2), (0, 3), (0, 4)]
    ribbon = squares2ribbon(squares)
    print(ribbon)
    _, ax2 = plt.subplots()
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ribbon.draw(ax = ax2)
    print(ribbon.contains(1, 4))
    
    
    '''
    checking the coloring scheme
    '''
    '''
    ribbon = Ribbon(0, 0, [0, 1]) 
    _, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    print(ribbon)
    print(ribbon.squares)
    ribbon.draw(ax = ax, colorByLength = False)
    
    ribbon = Ribbon(0, 0, [1, 1]) 
    _, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    print(ribbon)
    print(ribbon.squares)
    ribbon.draw(ax = ax, colorByLength = False)
    
    ribbon = Ribbon(1, 0, [1, 1]) 
    _, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    print(ribbon)
    print(ribbon.squares)
    ribbon.draw(ax = ax, colorByLength = False)
    
    ribbon = Ribbon(2, 0, [1, 1]) 
    _, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    print(ribbon)
    print(ribbon.squares)
    ribbon.draw(ax = ax, colorByLength = False)
    '''
    plt.show()
    
    
if __name__ == "__main__":
    main() 
    
    