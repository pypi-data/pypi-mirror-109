import math

# Motion

def calcSpeed(distance, time):
    return distance/time

def calcVelocity(displacement, time):
    return displacement/time

def avgVelocity(pos1, pos2, time1, time2):
    diffPos = pos2 - pos1
    diffTime = time2 - time1
    return diffPos/diffTime

def calcAcceleration(vel1, vel2, time1, time2):
    deltaVel = vel2 - vel1
    deltaTime = time2 - time1
    return deltaVel/deltaTime

def calcForce(mass, acceleration):
    return mass * acceleration

gravity = 9.8

# Friction

def staticFriction(stcoeff, normForce):
    return stcoeff * normForce

def slidingFriction(slcoeff, normForce):
    return slcoeff * normForce

def calcNormForce(mass, gravity):
    return mass * gravity

def calcAccFrict(coeffFrict, gravity):
    return coeffFrict * gravity

def coeffFriction(frictionForce, normForce):
    return frictionForce/normForce

# Frictional Constants

rbdc_static = 1.0
rbdc_kinetic = 0.7
rbwc_static = 0.7
rbwc_kinetic = 0.5
ww_static = 0.5
ww_kinetic = 0.3
mw_static = 0.5
mw_kinetic = 0.3
ssdry_static = 0.6
ssdry_kinetic = 0.3
ssoil_static = 0.05
ssoil_kinetic = 0.03
sw_static = 0.9
sw_kinetic = 0.7
si_static = 0.1
si_kinetic = 0.05
ii_static = 0.1
ii_kinetic = 0.03

# Linear Motion

def calcFinalVelocity(initVelocity, acceleration, time):
    return initVelocity + acceleration * time

def distance(finalVel, initVel, time):
    return ((finalVel + initVel)(time))/2

def distance2(initVelocity, time, acceleration):
    return (initVelocity * time) + (acceleration*(time)^2)/2

def finalVeocity(initVel, acceleration, distance):
    return math.sqrt(initVel + 2(acceleration)(distance))

# Momentum and Impulse

def calcMomentum(mass, velocity):
    return mass * velocity

def calcImpulse(force, time1, time2):
    return force*(time2 - time1)

# Projectile Motion
def horizDisplacement(horizontalVel, time):
    return horizontalVel * time

def vertDisplacement(height, initVertVel, time, acceleration):
    return height + initVertVel * time + (acceleration*(time)^2)/2

def time(distance, gravity):
    return math.sqrt(2(distance)/gravity)

# Circular Motion
def tanSpeed(radialDistance, rotationalSpeed):
    return radialDistance * rotationalSpeed

def period(frequency):
    return 1/frequency

def frequency(period):
    return 1/period

def linearSpeed(radius, time):
    return (2(math.pi)(radius))/time

def centripetalAcceleration(v, r):
    return (v^2)/r

# Universal Graviation
G = 6.67E-11
def lug(m1, m2, d):
    return G(m1*m2)/(d^2)

massEarth = 6 * (10^24)

# Electricity
propConst = 8.99E9

def coulombLaw(charge1, charge2, distance):
    return propConst((charge1 * charge2)/(d^2))

def elecStrength(eForce, charge):
    return eForce/charge

# Work and Power

def calcWork(force, distance):
    return force * distance

def calcPower(mass, acceleration, distance, time):
    return (mass * acceleration * distance)/time