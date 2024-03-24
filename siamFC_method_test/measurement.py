import numpy as np
def measurement(X1,X2,A,w):
# X1 = 784       #left camera
# X2 = 892       #right camera
#     w1 = w2 = 107
    H1 = H2 = 1280
    # A = 33.8

    B1 = B2 = (180-w)/2

    P2 = X2
    P1 = H1 - X1

    a = ((P2*w/H2)+B2)         #degree
    b = ((P1*w/H1)+B1)         #degree

    sina = np.sin(a*np.pi/180)
    sinb = np.sin(b*np.pi/180)


    num = A * sina * sinb
    den = np.sin((180-(a+b))*np.pi/180)
    distance = num/den
    return (distance)
