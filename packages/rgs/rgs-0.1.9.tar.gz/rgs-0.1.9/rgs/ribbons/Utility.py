'''
Created on Jan 23, 2021

@author: vladislavkargin
'''
import numpy as np
import matplotlib.pyplot as plt

import rgs.ribbons.Ribbon as rb
import rgs.ribbons.Tiling as tl


def flip(A, B):
    ''' check if two ribbons A and B are flippable. If yes, returns (True, A', B')
    where A', B' is a flipped pair, if no, returns (False, A, B)
    In this version, ribbons are required to be of the same length, 
    although in principle, they can be define for ribbons of different 
    length as well'''
    
    n = len(A.shape)
    if len(B.shape) != n:
        return (False, A, B)
    
    lA = A.x + A.y 
    lB = B.x + B.y
    if lA == lB:
        return (False, A, B) #the tiles at the same level can't be flipped
    
    if lA < lB:
        X = rb.Ribbon(A.x, A.y, A.shape) 
        Y = rb.Ribbon(B.x, B.y, B.shape)
    else:
        Y = rb.Ribbon(A.x, A.y, A.shape) 
        X = rb.Ribbon(B.x, B.y, B.shape)
    
    for i in range(n):
        s, t = X.squares[i]
        if X.shape[i] == 0: #instead, go up
            t = t + 1
            for j in range(n - i - 1):
                #print(B.squares[j])
                #print((s,t))
                if Y.squares[j] != (s, t):
                    #print("Breaking")
                    break
                else:
                    if X.shape[i + j + 1] == 0:
                        s = s + 1
                    else: 
                        t = t + 1
                if Y.shape[n - i - 1] == 0:
                    print(i)
                    A1 = rb.Ribbon(X.x, X.y, X.shape[:i] + [1] + X.shape[i+1:])
                    B1 = rb.Ribbon(X.squares[i + 1][0], X.squares[i+1][1], Y.shape[:(n-i -1)] + [1] + Y.shape[(n-i):])
                    return (True, A1, B1)
        else: #X.shape is 1 instead, go right
            s = s + 1
            for j in range(n - i - 1):
                #print(B.squares[j])
                #print((s,t))
                if Y.squares[j] != (s, t):
                    #print("Breaking")
                    break
                else:
                    if X.shape[i + j + 1] == 0:
                        s = s + 1
                    else: 
                        t = t + 1
                if Y.shape[n - i - 1] == 1:
                    #print(i)
                    A1 = rb.Ribbon(X.x, X.y, X.shape[:i] + [0] + X.shape[i+1:])
                    B1 = rb.Ribbon(X.squares[i + 1][0], X.squares[i+1][1], Y.shape[:(n-i -1)] + [0] + Y.shape[(n-i):])
                    return (True, A1, B1)
            
    return (False, A, B)
                
        
    
    #check what happens if we will switch from 0 to 1 or from 1 to 0 
    #in one of the shape locations for ribbon A
    

    #It looks that there are 4 different cub-cases:
    #shape of A = shape of B
    #beginning of A = end of B
    #beginning of A = end of B
    # remaining case. (which is always non-flippable)
    
    

def fibSequence(n, seed = None):
    ''' returns a random increasing sequence of indices (i1, i2, ..., ik)
    such that the indices are between 0 and n-1 and no two indices are 
    adjacent. The number of such sequence is Fibonacci number. The function 
    uses recursion
    '''
    if seed != None:
        np.random.seed(seed)
    seq = []
    if n <= 0:
        return seq
    else:
        x = np.random.randint(2)
        if x == 1: #n-1 is included
            seq = fibSequence(n - 2) + [n - 1]
        else:
            seq = fibSequence(n - 1)
        return seq

def getSquarePairs(sx0, sy0, dir0, sequence):
    ''' generates pairs of squares which should be included in a Stanley's 
    tiling. 
    parameters: s0x and s0y - coordinates of the original square
    dir0 - direction of original step : 'Down' or 'Right'
    sequence: sequence that regulates, which pairs should be included. '''
    sx = sx0
    sy = sy0
    direction = dir0
    #print(sequence)
    pairs = []
    if sequence == []:
        return pairs
    M = max(sequence) + 1
    for i in range(M):
        if i in sequence:
            if direction == 'Right':
                pairs = pairs + [(sx, sy, 'Right')]
                #print(sx, sy, 'Right') 
            else:
                pairs = pairs + [(sx, sy - 1, 'Up')]
                #print(sx, sy - 1, 'Up')
        if direction == 'Right':
            sx = sx + 1
            sy = sy
            direction = "Down"
        else:
            sx = sx
            sy = sy - 1
            direction = "Right"
    return pairs
    
def pairsForRectangle(M, N, seed = None):
    '''gets all marked pairs for an M-by-N rectangle. It is assumed that N >= M'''
    if seed != None:
        np.random.seed(seed)
    all_pairs =[]
    for i in range(M - 1):
        pairs = getSquarePairs(0, i + 1 , "Down", sequence = fibSequence(2 * i + 2))
        all_pairs = all_pairs + pairs
    for i in range (N - M):
        pairs = getSquarePairs(i, M - 1 , "Right", sequence = fibSequence(2 * M - 1))
        all_pairs = all_pairs + pairs
    for i in range (M - 1):
        pairs = getSquarePairs(N - M + i, M - 1 , "Right", sequence = fibSequence(2 * M - 2 - 2 * i))
        all_pairs = all_pairs + pairs
    return all_pairs

def tilingFromPairs(M, N, pairs):
    ''' creates a tiling of an M-by-N rectangle from a collection of pairs '''
    marked = np.zeros((N,M)) #contains information if a particular cell is in the tiling
    ribbons = []
    pairs_set = set(pairs)
    for y0 in range(M):
        for x0 in range(N):
            if marked[x0, y0] == 0: #this cell is not yet explored.
                marked[x0, y0] = 1
                x = x0
                y = y0
                shape = []
                while (x, y, 'Up') in pairs_set or (x, y, 'Right') in pairs_set:
                    #print("x = ", x, "y = ", y)
                    if (x, y, 'Up') in pairs_set:
                        shape.append(1)
                        y = y + 1
                        marked[x, y] = 1
                    else:
                        shape.append(0)
                        x = x + 1
                        marked[x, y] = 1
                ribbon = rb.Ribbon(x0, y0, shape)
                ribbons.append(ribbon)
    tiling = tl.Tiling(ribbons)
    return tiling
                    
    
    
    
def drawPairs(M, N, pairs):
    '''draws all marked pairs for M-by-N rectangle'''
    fig, ax = plt.subplots()
    ax.set_xlim(0, N + 1)
    ax.set_ylim(0, M + 1)
    for (sx, sy, dr) in pairs:
        if dr == "Up":
            line = plt.Line2D((sx + 0.5, sx + 0.5),(sy + 0.5, sy + 1.5), color = 'black')
            ax.add_line(line)
        else: 
            line = plt.Line2D((sx + 0.5, sx + 1.5),(sy + 0.5, sy + 0.5), color = 'black')
            ax.add_line(line)
    return fig, ax    

def randomStanleyTiling(M, N):
    ''' creates a random ribbon tiling of an M-by-N rectangle using Stanley's 
    algorithm'''
    all_pairs = pairsForRectangle(M, N)
    tiling = tilingFromPairs(M,N, all_pairs)
    return tiling


def lengthCounts(tiling):
    '''creates a dictionary that measures lengths of the ribbons in the tiling. 
    Example: {1:3, 2:5, 7:1} means that there are three 1-ribbons, five two ribbons and 1 7-ribbon.'''
    
    length_counts = {}
    for ribbon in tiling.ribbons:
        l = len(ribbon.shape)
        if l + 1 not in length_counts.keys(): 
            length_counts[l + 1] = 1
        else:
            length_counts[l + 1] = length_counts[l + 1] + 1
    return length_counts    
    

'''
For testing methods
'''
def main():
    
    
    ''' some test for functions used in generating Stanley's tilings
    '''
    '''
    n = 20
    seed = 123
    seq = fibSequence(n, seed = seed)
    print(seq)
    
    pairs = getSquarePairs(10, 10, 'Right', seq)
    print(pairs)
    .'''
    
    
    '''some illustration for the Stanley tilings
    '''
    '''
    M= 9
    N = 9
    all_pairs = pairsForRectangle(M, N)
    #print("All pairs = ", all_pairs)
    drawPairs(M, N, all_pairs)
    
    tiling = tilingFromPairs(M,N, all_pairs)
    #print(tiling)
    tiling.draw(M, N, colorType = "ShapePosition")
    length_counts = lengthCounts(tiling)
    print('Length Counts = ', length_counts)
    '''
    
    ''' This is a couple of tests for the flip function 
    (seems to work OK)
    '''
    _, ax = plt.subplots(2, 2)
    
    A = rb.Ribbon(0, 0, [0, 0, 0, 1, 1, 0, 0, 1])
    B = rb.Ribbon(2, 1, [1, 1, 0, 0, 1, 0, 0, 0])
    
    tiling = tl.Tiling([A, B]) 
    print(tiling)
    tiling.draw(10, 10, ax = ax[0][0])
    
    flag, A1, B1 = flip(A,B)
    print(flag)
    print(A1)
    print(B1)
    tiling = tl.Tiling([A1, B1])
    tiling.draw(10, 10, ax = ax[0][1])
    
    
    C = rb.Ribbon(0, 0, [1, 1, 1, 1, 0])
    D = rb.Ribbon(1, 2, [1, 0, 1, 1, 0])
    tiling = tl.Tiling([C, D]) 
    print(tiling)
    tiling.draw(10, 10, ax = ax[1][0])
    
    flag, C1, D1 = flip(C,D)
    print(flag)
    print(C1)
    print(D1)
    tiling = tl.Tiling([C1, D1])
    tiling.draw(10, 10, ax = ax[1][1])
    
    
    
    _, ax = plt.subplots(2, 2)
    A = rb.Ribbon(0, 0, [0, 1])
    B = rb.Ribbon(0, 1, [1, 0])
    
    tiling = tl.Tiling([A, B]) 
    print(tiling)
    tiling.draw(10, 10, ax = ax[0][0])
    
    flag, A1, B1 = flip(B,A)
    print(flag)
    print(A1)
    print(B1)
    tiling = tl.Tiling([A1, B1])
    tiling.draw(10, 10, ax = ax[0][1])
    
    A = rb.Ribbon(0, 0, [0, 0])
    B = rb.Ribbon(0, 1, [0, 0])
    
    tiling = tl.Tiling([A, B]) 
    print(tiling)
    tiling.draw(10, 10, ax = ax[1][0])
    
    flag, A1, B1 = flip(B,A)
    print(flag)
    print(A1)
    print(B1)
    tiling = tl.Tiling([A1, B1])
    tiling.draw(10, 10, ax = ax[1][1])

    
    plt.show()

if __name__ == '__main__':
    main()