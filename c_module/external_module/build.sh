#!/bin/sh

cd ~/Documents/micropy/micropython/ports/rp2
make clean
make USER_C_MODULES=../../../../Keyboard/MicroPy/c_module/external_module/micropython.cmake