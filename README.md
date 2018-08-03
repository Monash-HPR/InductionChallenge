# Monash HPR Dynamics Induction Challenge
Welcome to Monash High-Power(ed) Rocketry!

<img src="https://user-images.githubusercontent.com/22362913/42794851-7ba4ab10-89c4-11e8-8960-97f0f3f32b98.png" width="200">

## What?
You will be writing a 1 degree-of-freedom (1DOF) rocket simulator.

## Why?
As part of the Dynamics team you will be helping us to write a 6DOF rocket simulator. We hope that writing a simplified version yourself will help you understand the current simulation code, and get you started with learning Cython.

## How?
In this README you are provided with all of the equations you will need to make your simulation. You can add more complex equations or algorithms if you like, however! Although this is an individual task, feel free to ask any questions, work together, and discuss what you need to do. You may need to; this is a **tough** challenge!

# Getting Started
You will need to download some dependencies before you can get started. Start these downloads and then read some of the stuff below while they run.

Run the following command (copy it and then paste it in your terminal using the middle mouse button). You will need to type your password before it will begin.
```
sudo apt-get update && sudo apt-get install build-essential git python3 cython3 python3-numpy python3-matplotlib python3-scipy -y
```

Once you've installed everything you need, make a git directory with the command
```
cd ~ && mkdir git && cd git
```

Then clone this repository to get all of the juicy boilerplate code
```
git clone https://github.com/Monash-HPR/InductionChallenge.git
```

Navigate into the newly-made directory and make yourself a branch. This will be your playground to test and backup your code without breaking anyone else's.
```
cd InductionChallenge
git checkout -b <name>
git checkout <name>
git push origin <name>
```
  
Now try building your code (this won't be too useful for now, but it checks that the installation went smoothly)
```
python3 setup.py build_ext --inplace
```
You may as well start memorising the line above, because you will be typing it a lot!

If your terminal was filled with friendly compiler statements, you're good to go.
(FATAL ERROR, MISSING DEPENDENCY, and things to that effect aren't very friendly)

## Tips
Before we get to the maths, take a moment to read some of these tips.
### Stuck?
Running into a problem you just can't seem to solve? Getting a ridiculous error that looks like an alien language? Google your problem - 99% of the time someone else has answered your question on StackOverflow. If you are still stuck then **ask for help!** 

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
### Adding Custom Cython (*.pyx*) Files
Add the line 
```
from Modules.YourModuleName import *
```
to the *\_\_init\_\_.py* file.

## The Maths
To reiterate, you **don't need to use the maths we give you** - it's just here as a reference. Feel free to play around with different equations to see what your rocket will do!

You can find the maths used for this simulation under *Monash HPR/Dynamics/Simulation/Induction Challenge*.
