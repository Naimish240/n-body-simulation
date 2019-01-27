from math import sqrt
from random import choice
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from copy import deepcopy
from os import mkdir

# --------------------------------- Class Point ---------------------------------
class Point(object):
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '({},{},{})'.format(self.x,self.y,self.z)
    
# --------------------------------- Class Body ----------------------------------
class Body(object):
    # location: meters, mass: kilograms, velocity: meters per second
    def __init__(self, posn = Point(0,0,0), m = 0, v = Point(0,0,0), name = ""):
        self.posn = posn
        self.m = m
        self.v = v
        self.name = name
    
    def __repr__(self):
        s = []
        s.append("Name: {}\n".format(self.name))
        s.append("Mass: {}\n".format(self.m))
        s.append("Initial Position: {}\n".format(str(self.posn)))
        s.append("Initial Velocity: {}\n".format((str(self.v))))

        return s[0]+s[1]+s[2]+s[3]

# Function to calculate the acceleration of the body
def calAccn(bodies, i):
    G = 6.67408e-11 # Unit: m3 kg-1 s-2
    accn = Point(0,0,0)
    current = bodies[i]
    for j, other in enumerate(bodies):
        if j != i:
            r = (current.posn.x - other.posn.x)**2 + (current.posn.y - other.posn.y)**2 + (current.posn.z - other.posn.z)**2
            r = sqrt(r)
            tmp = G * other.m / r**3
            accn.x += tmp * (other.posn.x - current.posn.x)
            accn.y += tmp * (other.posn.y - current.posn.y)
            accn.z += tmp * (other.posn.z - current.posn.z)

    return accn

# Function to calculate the velocity of the body
def calVelo(bodies, dt):
    for i, current in enumerate(bodies):
        accn = calAccn(bodies, i)

        current.v.x += accn.x * dt
        current.v.y += accn.y * dt
        current.v.z += accn.z * dt 

# Function to find the updated location of the body
def newLocn(bodies, dt):
    for i in bodies:
        i.posn.x += i.v.x * dt
        i.posn.y += i.v.y * dt
        i.posn.z += i.v.z * dt

# Function to plot bodies
def plot(bodies, outfile, show = True):
    fig = plt.figure()
    colours = ['r','b','g','y','m','c']
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    for body in bodies:
        x = body['x']
        y = body['y']
        z = body['z']
        ax.plot(x,y,z, c = choice(colours), label = body['name'])

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')

    plt.savefig(outfile)

    if show:
        plt.show()

# Function to run the simulation
def run(bodies, dt , steps , report_freq):

    #create output container for each Body
    Body_locations_hist = []
    for current_Body in bodies:
        Body_locations_hist.append({"x":[], "y":[], "z":[], "name":current_Body.name})
        
    for i in range(1,steps):
        calVelo(bodies, dt = dt)
        newLocn(bodies, dt = dt)           
        
        if i % report_freq == 0:
            for i, Body_location in enumerate(Body_locations_hist):
                x = bodies[i].posn.x
                y = bodies[i].posn.y
                z = bodies[i].posn.z

                Body_location["x"].append(x)
                Body_location["y"].append(y)           
                Body_location["z"].append(z)

    return Body_locations_hist        

# Function to log the data onto a text file
def log(bodies, motions, outfile):

    with open(outfile, 'w') as fh:
        l = []
        for i in bodies:
            l.append(str(i))
        fh.writelines(l)
        
        for i in motions:
            pts = []
            for j in range(len(i['x'])):
                pts.append((i['x'][j],i['y'][j],i['z'][j]))
            fh.writelines([i['name'],'\n',str(pts),'\n'])

# Function to get input of bodies with while loop
def getInput():
    l = []
    while True:
        name = input("Enter the name of the body or 0 to quit: ")
        if '0' in name or not name:
            return l
        
        px = float(input("Enter the body's initial 'x' co ordinate: "))
        py = float(input("Enter the body's initial 'y' co ordinate: "))
        pz = float(input("Enter the body's initial 'z' co ordinate: "))
        posn = Point(px, py, pz)

        m = float(input("Enter the mass of the body: "))

        vx = float(input("Enter the body's initial 'x' velocity: "))
        vy = float(input("Enter the body's initial 'y' velocity: "))
        vz = float(input("Enter the body's initial 'z' velocity: "))
        v = Point(vx, vy, vz)

        l.append(Body(posn, m, v, name))

def main():

    #build list of bodies in the simulation
    '''
    body = [
        Body( posn = Point(0,0,0), m = 5e10, v = Point(0,0,0), name = "Body1" ),
        Body( posn = Point(0,1e5,0), m = 5e10, v = Point(0,0,0), name = "Body2" ),
        Body( posn = Point(0,0,1e5), m = 5e10, v = Point(0,0,0), name = "Body3" ),
        ]
    '''
    body = getInput()
    

    while len(body) < 2:
        print("Sorry, we need atleast two bodies to simulate")
        body = getInput()

    bodies = deepcopy(body)

    steps = int(input("Enter the total number of steps: "))    
    dt = float(input("Enter how large you want the time interval between steps to be: "))
    report = int(input("Enter the number of steps between each log: "))

    print("Running the simulation...")
    motions = run(bodies, dt, steps, report)

    # Getting current time
    time = datetime.now().strftime("%y-%m-%d-%H-%M")
    
    # Creating the folder to save the output files to 
    mkdir(r'run_{}'.format(time))

    print("Saving the log...")
    log(body, motions, outfile = r'run_{}/orbits_{}.txt'.format(time, time))
    print("Saved the log")

    print("Saving the final plot...")
    plot(motions, outfile = r'run_{}/orbits_{}.png'.format(time, time))
    print("Saved the plot")

if __name__ == '__main__':
    ch = 'y'
    while ch == 'y':
        print("Running n body simulation")
        main()
        ch = input("Enter 'y' to run again, 'n' to quit: ").lower()

    print("Simulation Terminated")
