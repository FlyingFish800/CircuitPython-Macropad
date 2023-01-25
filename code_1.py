from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import neopixel, kdl
from pbm_codec import pbm_to_framebuf

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)

display=SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.show()

pixels = neopixel.NeoPixel(Pin(14), 12)

buttons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(2,14)]

macro_pad_size = [4,4,4]

i_to_row_col = [(i%3, (i//3)) for i in range(sum(macro_pad_size))]

interpreter = kdl.kdl_interpreter([4,4,4], "test.kdl")
display.text("Display init!",0,0)
display.show()

for i in range(len(pixels)):
    print(i_to_row_col[i],i)
    if interpreter.get_lit(*i_to_row_col[i]): pixels[i] = interpreter.get_color(*i_to_row_col[i])
    else: pixels[i] = (0,0,0)
    print("Done if")
pixels.write()

display.fill(0)
display.text("Pix init!",0,0)
display.show()

honk = pbm_to_framebuf("LL_Honoka3_128x64.pbm")
display.blit(honk,0,0)
display.show()

prev_state = [1 for i in range(len(buttons))]

while 1:
    for i in range(len(buttons)):
        value = buttons[i].value()
        row_col = i_to_row_col[i]

        if not prev_state[i] == value:
            prev_state[i] = value
            if not value:
                # Return list of commands to be run by keyboard
                layer_change, led_updated, display_command, press_sequence, type_str, errors = interpreter.key_pressed(*row_col)
            else:
                layer_change, led_updated, display_command, press_sequence, type_str, errors = interpreter.key_released(*row_col)

            if led_updated: 
                pixels[i] = interpreter.get_color(*i_to_row_col[i])
                pixels.write()

            if layer_change:
                j = 0
                while j < len(pixels):
                    pixels[j] = interpreter.get_color(*i_to_row_col[j])
                    j += 1
                layer_change = False
                pixels.write()

            for command in display_command:
                #print (command)
                if command == "clear":
                    #print("Command -> clear")
                    display.fill(0) # TODO: handle background stuff
                    display.show()
                elif command[0] == "write":
                    #print("write")
                    _, x, y, msg = command
                    display.text(msg, x, y, 1)
                    display.show()