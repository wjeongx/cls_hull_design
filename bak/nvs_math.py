def LinearInterpolation(x1,x2,y1,y2,x):
    Value = y1 - (x1 - x) * (y1 - y2) / (x1 - x2)
    return Value

    
