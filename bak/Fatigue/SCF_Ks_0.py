def lagrange(x, x1, x2, x3, x4, y1, y2, y3, y4):
    c1 = (x - x2) * (x - x3) * (x - x4) / ((x1 - x2) * (x1 - x3) * (x1 - x4))
    c2 = (x - x1) * (x - x3) * (x - x4) / ((x2 - x1) * (x2 - x3) * (x2 - x4))
    c3 = (x - x1) * (x - x2) * (x - x4) / ((x3 - x1) * (x3 - x2) * (x3 - x4))
    c4 = (x - x1) * (x - x2) * (x - x3) / ((x4 - x1) * (x4 - x2) * (x4 - x3))

    answer = c1 * y1 + c2 * y2 + c3 * y3 + c4 * y4
    return answer


thk = 12.0
print 'shell - quad4, Bar Result - ABS Method'
elm1, elm2, elm3, elm4 = 6., 18., 30., 42.
sigma1, sigma2, sigma3, sigma4 = 1.585, 1.202, 1.104,1.065

p1 = lagrange(6+thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(6+thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3

print 'shell - quad4, Discreate, Non-Average'
elm1, elm2, elm3, elm4 = 6., 18., 30., 42.
sigma1, sigma2, sigma3, sigma4 = 1.603, 1.189, 1.093,1.056

p1 = lagrange(6+thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(6+thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3

print 'shell - quad4, Element Fill, Non-Average, Interpolation - DNV Method'

elm1, elm2, elm3, elm4 = 6., 18., 30., 42.
sigma1, sigma2, sigma3, sigma4 = 1.342, 1.151, 1.083, 1.051 

p1 = lagrange(6+thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(6+thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3

print 'shell - quad4, Discreat, Average, Nodal Result'

p1 = 1.390
p2 = 1.139
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3


print 'Solid - t mesh nodal result'
elm1, elm2, elm3, elm4 = 12., 24., 36., 48.
sigma1, sigma2, sigma3, sigma4 = 1.317, 1.121, 1.104,1.052

p1 = lagrange(thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3

print 'Solid - t/2 mesh nodal result'
elm1, elm2, elm3, elm4 = 12., 24., 36., 48.
sigma1, sigma2, sigma3, sigma4 = 1.348, 1.099, 1.094,1.041

p1 = lagrange(thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3


print '======================================================'
elm1, elm2, elm3, elm4 = 9.7, 19.5, 29.2, 38.9
sigma1, sigma2, sigma3, sigma4 = 144., 112., 105.,100.
thk=10.
p1 = lagrange(thk/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p2 = lagrange(thk*3/2 , elm1, elm2, elm3, elm4, sigma1, sigma2, sigma3, sigma4)
p3 = 1.5*p1 - 0.5*p2

print "0.5*t ->", p1
print "1.5*t ->", p2
print "HotSpot ->", p3

