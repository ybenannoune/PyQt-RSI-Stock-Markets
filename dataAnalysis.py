import numpy as np
import numba as nb
import pandas



@nb.jit(nopython=True)   
def calc_rsi( array, deltas, avg_gain, avg_loss, n ):

    # Use Wilder smoothing method
    up   = lambda x:  x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_gain = ((avg_gain * (n-1)) + up(d)) / n
        avg_loss = ((avg_loss * (n-1)) + down(d)) / n
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            array[i] = 100 - (100 / (1 + rs))
        else:
            array[i] = 100
        i += 1

    return array

def get_rsi( array, n = 14 ):   

    deltas = np.append([0],np.diff(array))

    avg_gain =  np.sum(deltas[1:n+1].clip(min=0)) / n
    avg_loss = -np.sum(deltas[1:n+1].clip(max=0)) / n

    array = np.empty(deltas.shape[0])
    array.fill(np.nan)

    array = calc_rsi( array, deltas, avg_gain, avg_loss, n )
    return array

def determinePtsBelow(data,percentage,absoluteDelta):
    #find all points
    pX = []
    pY = []         

    #iterator
    for x in range(data.size):
        dateValue = data.index[x]     
        prevVal = x - 90
        if(prevVal < 0):
            prevVal = 0
        subRange = data.iloc[prevVal:x]
        lastValue = 0
        if(x > 0):
            lastValue = data[x - 1]                    
        currentValue = data[x]
        maxValueInRange = subRange.max()

        if( (currentValue < maxValueInRange * percentage) and abs(lastValue - currentValue) > absoluteDelta * currentValue  ):         
            pX.append(dateValue)
            pY.append(currentValue) 

    return pX,pY

def determineEtoileMatin(data,open_,close_):
    pX=[]
    pY=[]
    size = data.size
    for j in range(3, size):
        if open_[j-2]>close_[j-2] and close_[j-2]>open_[j-1] and open_[j]>close_[j-1] and open_[j]>open_[j-1] and open_[j]<close_[j] and close_[j-2]>close_[j-1]:
            pX.append(data.index[j])
            pY.append(data[j])
    return pX,pY   

def rsiPointsBelow(data,rsi,value):
    pX = []
    pY = []
    it = 0
    for x in rsi:        
        if(x < value):
            pX.append(data.index.tolist()[it])
            pY.append(data[it])
        it = it + 1
    return pX,pY 
