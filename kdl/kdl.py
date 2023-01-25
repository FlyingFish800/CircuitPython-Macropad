from random import random

def is_numeric(string):
    for char in string:
        if char not in "0123456789":
            return False
    return True

class key():
    def __init__(self, state, attributes = []):
        self.color = (0,0,0)
        self.lit = False
        self.state = state
        self.lit_on_reset = False

        actions = []

        # Get static properties from the list
        # TODO: make press ["press", [...list of buttons and key names...]]
        # TODO: diplay commands. Clear, print, draw (image)
        # TODO: make type ["type", "one single string"]   make string using ' '.join()

        for i in range(len(attributes)):
            action = attributes[i]
            if action[0] == "color":
                if action[1] == "random":
                    self.color = (int(random()*255), int(random()*255), int(random()*255))
                    continue
                self.color = tuple(map(int,action[1:]))
            elif action[0] == "on":
                if action[1] == "always":
                    self.lit = True
                    self.lit_on_reset = True
                elif action[1] == "never":
                    self.lit = False
                    self.lit_on_reset = False
                else:
                    actions.append((action[0], action[1:]))
            else:
                # And add actions to the dictionary of actions
                actions.append((action[0], action[1:]))

        self.actions = actions

    def get_color(self): 
        return self.color if self.lit else (0,0,0)

    def get_lit(self): 
        return self.lit

    def pressed(self):
        led_update = False
        #print(f"Pressed! {self.actions}")
        state = self.state
        display_command = []
        press_sequence = []
        type_str = []
        errors = []

        for action, args in self.actions:
            #print(action)
            # Handle the 'on' lighting action
            if action == "on":
                if args[0] == "pressed":
                    self.lit = True
                    led_update = True

            # Handle the setstate actions. --ALWAYS DO LAST--
            if action == "setstate":
                #print(int(args[0]))
                state = int(args[0])


            

            # Return the current state for no state change
        return (state, led_update, display_command, press_sequence, type_str, errors)

    def reset(self):
        self.lit = self.lit_on_reset

    def released(self):
        led_update = False
        display_command = []
        press_sequence = []
        type_str = []
        errors = []
        for action, args in self.actions:
            # Handle the 'on' lighting action
            if action == "on":
                if args[0] == "pressed":
                    self.lit = False
                    led_update = True

            if action == "display":
                if args[0] == "clear":
                    display_command.append(("clear"))
                elif args[0] == "text":
                    display_command.append(("write", int(args[1]), int(args[2]), ' '.join(args[3:])))

        return (self.state, led_update, display_command, press_sequence, type_str, errors)     

    def __str__(self):
        return f"Key Color:{self.color} Lit:{self.lit} Actions:{self.actions}"


class kdl_interpreter():
    # TODO: Provide pointers to be called for each action. Example, lit would call 
    # keyboard_manager_pointer.lighting_on(row, col)
    def __init__(self, sizes, source_file):
        """Takes in a 1D array of sizes containing the columns for a given row. The number of rows is the length
        of the list. Also takes in a path to a kdl source file to parse"""

        self.is_pressed = [[False for _ in range(i)] for i in sizes]
        self.states = []
        self.backgrounds = []
        self.sizes = sizes
        self.state = 0
        self.state_semaphore = False
        self.changed_state = False

        keywords = ["key", "setstate", "on", "color", "press", "display"]

        with open(source_file, 'r') as file:
            # Track currently being assembled state and its number
            current_state_num = None
            current_state = [[None for _ in range(i)] for i in sizes]

            # Parse file line by line
            for line in file:
                # Split lines by spaces, makes them lowercase and removes whitespace
                tokens = list(map( lambda x : x.strip(), list(map(lambda x : x.lower(), line.split(' ')))))

                if tokens[0] == "state":
                    if not is_numeric(tokens[1]): 
                        print(f"NOT NUMERIC: |{tokens[1]}|")
                        return

                    #print(f"state: {tokens[1]}")
                    if not current_state_num == None: 
                        self.states.append(current_state)
                        current_state = [[None for _ in range(i)] for i in sizes]

                    current_state_num = int(tokens[1])
                    
                elif tokens[0] == "key":
                    if tokens[1].endswith(':') and ',' in tokens[1]:
                        # Transform x,y: to row, column tuple
                        row, column = map(int, map(lambda x : x.split(':')[0], tokens[1].split(',')))
                        print(f"{row},{column}")

                    actions = []
                    for i in range(2, len(tokens)):
                        if tokens[i] in keywords:
                            print(tokens[i])
                            actions.append([tokens[i]])
                        else:
                            actions[-1].append(tokens[i].split(',')[0])
                    current_state[row][column] = key(current_state_num, attributes=actions)

            # Append final state at the end
            self.states.append(current_state)
            print(len(self.states[0]),len(self.states[0][0]))

    def key_pressed(self, row, column):
        """Marks a given key as released and returns a tuple of actions, formatted (changed_state, led_update, display_command, press_sequence, type_str, errors)"""
        # press_sequence is sequence of key codes held until the last one is pressed
        # type_str is a sting to be pressed one key at a time
        new_state, led_update, display_command, press_sequence, type_str, errors = self.states[self.state][row][column].pressed()
        changed_state = not new_state == self.state
        self.state = new_state

        columns = len(self.states[self.state][0])
        rows = len(self.states[self.state])
        #print("push")

        if changed_state:
            [self.states[self.state][ro][col].reset() for col in range(columns) for ro in range(rows)]

        return (changed_state, led_update, display_command, press_sequence, type_str, errors)

    def key_released(self, row, column):
        """Marks a given key as released and returns a tuple of actions, formatted (changed_state, led_update, display_command, press_sequence, type_str, error)"""
        # press_sequence is sequence of key codes held until the last one is pressed
        # type_str is a sting to be pressed one key at a time
        #print("release")
        return self.states[self.state][row][column].released()

    def get_color(self, row, column):
        return self.states[self.state][row][column].get_color()

    def get_lit(self, row, column):
        return self.states[self.state][row][column].get_lit()

    def is_held(self, row, column):
        pass
        return self.is_pressed[row][column]
