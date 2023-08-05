# loopie

This python framework is to provide a skeleton for managing a looping mainthread, with the ability of spawning childern threads that either loop of just do any other code and exit.

The project is designed to create a commandline application to loop through a custom python code while creating a skeleton for each project similar to the Arduino sketch code; meaning, for a loop to run there should be a loop_setup routine and a loop_logic routine that will be called on every loop.

One of the main uses of this project is to create a startup script (systemd) on a Raspberry Pi 2/3 that will run your custom python application, for example, to interact with the GPIO pins from the very start of the Pi.


A dominent feature of the project is it's web interface.
