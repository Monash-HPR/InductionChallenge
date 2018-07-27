# Monash HPR Dynamics Induction Challenge
Welcome to Monash High-Power(ed) Rocketry!

## What?
You will be writing a 1 degree-of-freedom (1DOF) rocket simulator.

## Why?
As part of the Dynamics team you will be helping us to write a 6DOF rocket simulator. We hope that writing a simplified version yourself will help you understand the current simulation code, and get you started with learning Cython.

## How?
In this README you are provided with all of the equations you will need to make your simulation. You can add more complex equations or algorithms if you like, however! Although this is an individual task, feel free to ask any questions, work together, and discuss what you need to do. 

# Getting Started
You will need to download some dependencies before you can get started. Start these downloads and then read some of the stuff below while they run.

Run the following command (copy it and then pase it in your terminal using the middle mouse button)
```
sudo apt-get update && sudo apt-get install build-essential git python3 cython3 python3-numpy python3-matplotlib python3-scipy -y
```

Once you've installed everything you need, make a git directory with the commands
```
cd ~
mkdir git
```

Then clone this repository to get all of the juicy boilerplate code
```
git clone https://github.com/Monash-HPR/InductionChallenge.git
```

Navigate into the newly-made directory and switch to your branch (replace <name> with your name: eg. git checkout oliver)
```
git checkout <name>
```
  
Now try building your code (this won't be too useful for now, but it checks that the installation went smoothly)
```
python3 setup.py build_ext --inplace
```
You may as well start memorising the line above, because you will be typing it a lot!

If your terminal was filled with friendly compiler statements, you're good to go.
(FATAL ERROR, MISSING DEPENDENCY, and things to that effect aren't very friendly fyi)

## Tips
Before we get to the maths, take a moment to read some of these tips.
### Optimising Your Cython Code
As Cython is compiled, you can assign types to variables to improve the speed of your program. For example, instead of writing 
```
a = 3
```
in pure Python, in Cython you can instead specify that 'a' is an integer.
```
cdef int a = 3
```
Although this is more verbose, it can often drastically improve the speed of your program. If you are writing functions, you can do the same thing. You can find examples of this in *Modules/Thrust.pyx* file.

## The Maths
To reiterate, you **don't need to use the maths we give you** - it's just here as a reference. 

### Drag
We will model drag with the (hopefully familiar?) equation

![equation](http://www.sciweavers.org/upload/Tex2Img_1532664821/eqn.png)

Where the coefficient of drag is a function of Mach number is given by the following (completely made up) equation

![equation](http://www.sciweavers.org/upload/Tex2Img_1532665492/eqn.png)

Density can be found using the state equation 

![equation](http://www.sciweavers.org/upload/Tex2Img_1532665543/eqn.png)

combined with the standard atmosphere equations 

![equation](http://www.sciweavers.org/upload/Tex2Img_1532665611/eqn.png)

![equation](http://www.sciweavers.org/upload/Tex2Img_1532665746/eqn.png)

You can calculate Mach number using the equation

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666010/eqn.png)

where *R=287.16* and *gamma=1.4*.

### Thrust
Thrust will be modelled by another made up equation (although its profile approximates a real motor)

![equation](http://www.sciweavers.org/upload/Tex2Img_1532665925/eqn.png)

where we will use a peak thrust of *T0 = 100 N* and a burnout time of *tB = 2 s*.

### Gravitation
We will use a simple inverse square model of gravitation

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666130/eqn.png)

where the standard gravitational parameter *GM=3.986*10^14* and 

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666203/eqn.png)

can be used to find the radial distance using *R_Earth=6378137 m*.

### Integration
Writing the integrator is one of the most challenging parts of the simulator. I will describe Euler's method here, however those of you who know more advanced techniques should use them!

We need to solve the 2nd ODE (Newton's law)

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666539/eqn.png)

where *F/M* has been replaced by the general function *f(t,s,v)* for brevity. Note that it is a function of time, position (altitude), and velocity. Take a moment to think about which forces require each of these variables. Do you think we need any more information? Don't forget that mass is not constant for a rocket!

To solve this ODE numerically, we need to reduce it to a pair of 1st order ODEs. This is done by simply introducing velocity, leaving us with the pair of equations

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666684/eqn.png)

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666660/eqn.png)

The general formula for Euler's method is

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666744/eqn.png)

where the subscript represents the solution estimate (ie. it estimates the new state *i+1* using the current state *i*).
To be more specific to our system of ODEs, we have

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666839/eqn.png)

![equation](http://www.sciweavers.org/upload/Tex2Img_1532666868/eqn.png)

Euler's method has a global truncation error of O(dt), so you will need to decrease the step size in your simulation to obtain good results (although this will take longer).

If you have trouble with anything described above **ask questions!** This exercise should be challenging, but ultimately fun.
