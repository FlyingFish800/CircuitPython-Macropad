# RP2040 Macropad using Micropython
## Why Micropython?
I originaly wrote the firmware in Circuitpython so that it would be easier for people to hack, but Circuitpython ended up being really slow and restrictive with what hardware could be utilized. Porting the code to Micropython yeilded significant performance increases without changing any code except that used for IO. The use of an enviroment with built in file handling also made it a lot easier to implement a KDL parser compared to trying to read a file in baremetal C.

## KDL
KDL stands for Keyboard Description Language and was created to allow those without programming experience to customize their macropad through specific commands without compromising on what could be achieved through a python script.

### KDL Syntax
Each line either starts with a 'State' or 'key' descriptor that defines either a state or a key functionality. Key descriptors also contain attributes of that key and actions taken when it is placed, seperated by commas

### States
A State is similar to a layer, and different States can be switched between by commands from different keys. A state is declared as follows:

State (statenum)

where statenum is an integer

### Keys
The functionality of a Key in kdl is described as follows:

key (row),(col): (attribute/action), (attribute/action)

where row and col are integers corresponding to a valid location on the keypad. As many attributes or actions can be specified, each seperated by commas

### Attributes and Actions
Attributes and actions are not treated any different from eachother in KDL, but some keywords (attributes) are used to describe a key and how it works, while others (actions) are executed when the key is pressed. Only attributes or actions for the current state are used

###Attributes:
color (r) (g) (b)
Defines the color a key will light up. R G and B are ints from 0 to 255, where 255 is the brightest

on (condition)
Defines when a key is lit. Condition can either be
pressed - when the key is held
always - all the time
never - light is permanently off

###Actions
display (command)
Makes the display do the specified command. Commands are
clear - clears the display so all pixels are off
text (x) (y) (string) - where x and y are ints for the position on screen, and string is the text to be displayed (Doesnt need to be in quotes)

press (key) (key)
Pressed the following keys (seperated by spaces) holding each key until the last one is pressed. Used for sequences like CTRL C or CTRL ALT T

type (string)
Types each letter in the following string one at a time. Used for typing out text. The string doesnt need to be in quotes
