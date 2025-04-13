import random

class HauntedHouseAdventure:
    def __init__(self):
        # Game constants
        self.v = 25  # Number of verbs
        self.w = 36  # Number of words/objects
        self.g = 18  # Number of gettable objects
        
        # Game variables
        self.rm = 57  # Current room
        self.ll = 60  # Light level
        self.m = "ok"  # Message
        
        # Initialize arrays
        self.r = [""] * 64  # Room exits
        self.d = [""] * 64  # Room descriptions
        self.o = [""] * (self.w + 1)  # Object names
        self.v_words = [""] * (self.v + 1)  # Verb words
        self.c = [0] * (self.w + 1)  # Carrying status (0=no, 1=yes)
        self.l = [0] * (self.g + 1)  # Object locations
        self.f = [0] * (self.w + 1)  # Object flags
        
        # Initialize game data
        self.initialize_game_data()
        
    def initialize_game_data(self):
        # Set initial object locations
        locations = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 43, 32]
        for i in range(1, self.g + 1):
            self.l[i] = locations[i-1]
        
        # Set verb words
        verbs = ["help", "carrying", "go", "n", "s", "w", "e", "u", "d", "get", "take", 
                 "open", "examine", "read", "say", "dig", "swing", "climb", "light", 
                 "unlight", "spray", "use", "unlock", "leave", "score"]
        for i in range(1, self.v + 1):
            self.v_words[i] = verbs[i-1]
        
        # Set room exits
        exits = ["se", "we", "we", "swe", "we", "we", "swe", "ws",
                "ns", "se", "we", "nw", "se", "w", "ne", "nsw",
                "ns", "ns", "se", "we", "nwud", "se", "wsud", "ns",
                "n", "ns", "nse", "we", "we", "nsw", "ns", "ns",
                "s", "nse", "nsw", "s", "nsud", "n", "n", "ns",
                "ne", "nw", "ne", "w", "nse", "we", "w", "ns",
                "se", "nsw", "e", "we", "nw", "s", "sw", "nw",
                "ne", "nwe", "we", "we", "we", "nwe", "nwe", "w"]
        for i in range(64):
            self.r[i] = exits[i]
        
        # Set room descriptions
        descriptions = ["dark corner", "overgrown garden", "by large woodpile", "yard by rubbish",
                      "weedpatch", "forest", "thick forest", "blasted tree",
                      "corner of house", "entrance to kitchen", "kitchen & grimy cooker", "scullery door",
                      "room with inches of dust", "rear turret room", "clearing by house", "path",
                      "side of house", "back of hallway", "dark alcove", "small dark room",
                      "bottom of spiral staircase", "wide passage", "slippery steps", "clifftop",
                      "near crumbling wall", "gloomy passage", "pool of light", "impressive vaulted hallway",
                      "hall by thick wooden door", "trophy room", "cellar with barred window", "cliff path",
                      "cupboard with hanging coat", "front hall", "sitting room", "secret room",
                      "steep marble stairs", "dining room", "deep cellar witih coffin", "cliff path",
                      "closet", "front lobby", "library of evil books", "study with desk & hole in wall",
                      "weird cobwebby room", "very cold chamber", "spooky room", "cliff path by marsh",
                      "rubble-strewn verandah", "front porch", "front tower", "sloping corridor",
                      "upper gallery", "marsh by wall", "marsh", "soggy path",
                      "by twisted railing", "path through iron gate", "by railings", "beneath front tower",
                      "debris from crumbling facade", "large fallen brickwork", "rotting stone arch", "crumbling clifftop"]
        for i in range(64):
            self.d[i] = descriptions[i]
        
        # Set object names
        objects = ["painting", "ring", "magic spells", "goblet", "scroll", "coins", "statue", "candlestick",
                 "matches", "vacuum", "batteries", "shovel", "axe", "rope", "boat", "aerosol", "candle", "key",
                 "north", "south", "west", "east", "up", "down", "door", "bats", "ghosts", "drawer", "desk", 
                 "coat", "rubbish", "coffin", "books", "xzanfar", "wall", "spells"]
        for i in range(1, self.w + 1):
            self.o[i] = objects[i-1]
        
        # Set initial flags
        self.f[18] = 1
        self.f[17] = 1
        self.f[2] = 1
        self.f[26] = 1
        self.f[28] = 1
        self.f[23] = 1
        
    def display_location(self):
        print("\nHAUNTED HOUSE")
        print("--------------")
        print("Your location")
        print(self.d[self.rm])
        print("Exits:", end=" ")
        
        for i in range(len(self.r[self.rm])):
            print(self.r[self.rm][i] + ",", end=" ")
        print()
        
        for i in range(1, self.g + 1):
            if self.l[i] == self.rm and self.f[i] == 0:
                print(f"You can see {self.o[i]} here")
        
        print("============================")
        print(self.m)
        self.m = "what"
    
    def get_input(self):
        q = input("What will you do now? ").lower()
        
        v_str = ""
        w_str = ""
        vb = 0
        ob = 0
        
        # Parse input into verb and object
        words = q.split()
        if len(words) > 0:
            v_str = words[0]
        if len(words) > 1:
            w_str = words[1]
        
        # Find verb number
        for i in range(1, self.v + 1):
            if v_str == self.v_words[i]:
                vb = i
                break
        
        # Find object number
        for i in range(1, self.w + 1):
            if w_str == self.o[i]:
                ob = i
                break
        
        # Error message conditions
        if w_str != "" and ob == 0:
            self.m = "That's silly"
        if vb == 0:
            vb = self.v + 1
        if w_str == "":
            self.m = "I need two words"
        if vb > self.v and ob > 0:
            self.m = f"You can't '{q}'"
        if vb > self.v and ob == 0:
            self.m = "You don't make sense"
        if vb < self.v and ob > 0 and self.c[ob] == 0:
            self.m = f"You don't have '{w_str}'"
        
        # Special game conditions
        if self.f[26] == 1 and self.rm == 13 and random.randint(0, 2) != 2 and vb != 21:
            self.m = "Bats attacking!"
            return vb, ob
        
        if self.rm == 44 and random.randint(0, 1) == 1 and self.f[24] != 1:
            self.f[27] = 1
        
        if self.f[0] == 1:
            self.ll -= 1
        
        if self.ll < 1:
            self.f[0] = 0
        
        return vb, ob
    
    def process_command(self, vb, ob):
        # Process the verb
        if vb <= 14:
            if vb == 1:
                self.help()
            elif vb == 2:
                self.carrying()
            elif vb in range(3, 10):  # Movement commands
                self.movement(vb, ob)
            elif vb in (10, 11):  # Get/take
                self.get_item(ob)
            elif vb == 12:  # Open
                self.open_item(ob)
            elif vb == 13:  # Examine
                self.examine_item(ob)
            elif vb == 14:  # Read
                self.read_item(ob)
        else:
            if vb == 15:  # Say
                self.say_word(ob)
            elif vb == 16:  # Dig
                self.dig()
            elif vb == 17:  # Swing
                self.swing(ob)
            elif vb == 18:  # Climb
                self.climb(ob)
            elif vb == 19:  # Light
                self.light(ob)
            elif vb == 20:  # Unlight
                self.unlight()
            elif vb == 21:  # Spray
                self.spray(ob)
            elif vb == 22:  # Use
                self.use(ob)
            elif vb == 23:  # Unlock
                self.unlock(ob)
            elif vb == 24:  # Leave
                self.leave(ob)
            elif vb == 25:  # Score
                self.score()
        
        # Light-related messages
        if self.ll == 10:
            self.m = "Your candle is waning!"
        if self.ll == 1:
            self.m = "Your candle is out!"
    
    def help(self):
        print("Words I know:")
        for i in range(1, self.v + 1):
            print(self.v_words[i] + ",", end=" ")
        print()
        self.m = ""
        input("Press Enter to continue")
    
    def carrying(self):
        print("You are carrying:")
        carrying_something = False
        for i in range(1, self.g + 1):
            if self.c[i] == 1:
                print(self.o[i] + ",", end=" ")
                carrying_something = True
        if not carrying_something:
            print("nothing")
        print()
        self.m = ""
        input("Press Enter to continue")
    
    def movement(self, vb, ob):
        d = 0
        
        # Determine direction
        if ob == 0:
            d = vb - 3
        if ob == 19:
            d = 1
        if ob == 20:
            d = 2
        if ob == 21:
            d = 3
        if ob == 22:
            d = 4
        if ob == 23:
            d = 5
        if ob == 24:
            d = 6
        
        # Special room direction mappings
        if self.rm == 20 and d == 5:
            d = 1
        if self.rm == 20 and d == 6:
            d = 3
        if self.rm == 22 and d == 6:
            d = 2
        if self.rm == 22 and d == 5:
            d = 3
        if self.rm == 36 and d == 6:
            d = 1
        if self.rm == 36 and d == 5:
            d = 2
        
        # Special conditions
        if self.f[14] == 1:
            self.m = "Crash! You fell out of the tree!"
            self.f[14] = 0
            return
        
        if self.f[27] == 1 and self.rm == 52:
            self.m = "Ghosts will not let you move"
            return
        
        if self.rm == 45 and self.c[1] == 1 and self.f[34] == 0:
            self.m = "A magical barrier to the west"
            return
        
        if (self.rm == 26 and self.f[0] == 0) and (d == 1 or d == 4):
            self.m = "You need a light"
            return
        
        if self.rm == 54 and self.c[15] != 1:
            self.m = "You're stuck!"
            return
        
        if self.c[15] == 1 and not (self.rm == 53 or self.rm == 54 or self.rm == 55 or self.rm == 47):
            self.m = "You can't carry a boat!"
            return
        
        if (self.rm > 26 and self.rm < 30) and self.f[0] == 0:
            self.m = "Too dark to move"
            return
        
        # Process movement
        self.f[35] = 0
        rl = len(self.r[self.rm])
        
        for i in range(rl):
            u = self.r[self.rm][i]
            if u == "n" and d == 1 and self.f[35] == 0:
                self.rm -= 8
                self.f[35] = 1
            if u == "s" and d == 2 and self.f[35] == 0:
                self.rm += 8
                self.f[35] = 1
            if u == "w" and d == 3 and self.f[35] == 0:
                self.rm -= 1
                self.f[35] = 1
            if u == "e" and d == 4 and self.f[35] == 0:
                self.rm += 1
                self.f[35] = 1
            if u == "u" and d == 5 and self.f[35] == 0:
                self.rm -= 8
                self.f[35] = 1
            if u == "d" and d == 6 and self.f[35] == 0:
                self.rm += 8
                self.f[35] = 1
        
        self.m = "OK"
        
        if self.f[35] == 0:
            self.m = "Can't go that way!"
        
        if d < 1:
            self.m = "Go where?"
        
        if self.rm == 41 and self.f[23] == 1:
            self.r[49] = "sw"
            self.m = "The door slams shut!"
            self.f[23] = 0
    
    def get_item(self, ob):
        if ob > self.g:
            self.m = f"I can't get {self.o[ob]}"
            return
        
        if self.l[ob] != self.rm:
            self.m = "It isn't here"
            return
        
        if self.f[ob] != 0:
            self.m = f"What {self.o[ob]}?"
            return
        
        if self.c[ob] == 1:
            self.m = "You already have it"
            return
        
        if ob > 0 and self.l[ob] == self.rm and self.f[ob] == 0:
            self.c[ob] = 1
            self.l[ob] = 65
            self.m = f"You have the {self.o[ob]}"
    
    def open_item(self, ob):
        if self.rm == 43 and (ob == 28 or ob == 29):
            self.f[17] = 0
            self.m = "Drawer open"
        elif self.rm == 28 and ob == 25:
            self.m = "It's locked"
        elif self.rm == 38 and ob == 32:
            self.m = "That's creepy!"
            self.f[2] = 0
    
    def examine_item(self, ob):
        if ob == 30:
            self.f[18] = 0
            self.m = "Something here!"
        elif ob == 31:
            self.m = "That's disgusting!"
        elif ob == 28 or ob == 29:
            self.m = "There is a drawer"
        elif ob == 33 or ob == 5:
            self.read_item(ob)
        elif self.rm == 43 and ob == 35:
            self.m = "There is something beyond..."
        elif ob == 32:
            self.open_item(ob)
    
    def read_item(self, ob):
        if self.rm == 42 and ob == 33:
            self.m = "They are demonic works"
        elif (ob == 3 or ob == 36) and self.c[3] == 1 and self.f[34] == 0:
            self.m = "Use this word with care 'xzanfar'"
        elif self.c[5] == 1 and ob == 5:
            self.m = "The script is in an alien tongue"
    
    def say_word(self, ob):
        self.m = f"OK '{self.o[ob]}'"
        
        if self.c[3] == 1 and ob == 34:
            self.m = "*magic occurs*"
            if self.rm != 45:
                self.rm = random.randint(0, 63)
            
        if self.c[3] == 1 and ob == 34 and self.rm == 45:
            self.f[34] = 1
    
    def dig(self):
        if self.c[12] == 1:
            self.m = "You made a hole"
        
        if self.c[12] == 1 and self.rm == 30:
            self.m = "Dug the bars out"
            self.d[self.rm] = "Hole in wall"
            self.r[self.rm] = "nse"
    
    def swing(self, ob):
        if self.c[14] != 1 and self.rm == 7:
            self.m = "This is no time to play games"
            return
        
        if ob == 14 and self.c[14] == 1:
            self.m = "You swung it"
            return
        
        if ob == 13 and self.c[13] == 1:
            self.m = "Whoosh"
        
        if ob == 13 and self.c[13] == 1 and self.rm == 43:
            self.r[self.rm] = "wn"
            self.d[self.rm] = "Study with secret room"
            self.m = "You broke the thin wall"
    
    def climb(self, ob):
        if ob == 14 and self.c[14] == 1:
            self.m = "It isn't attached to anything!"
        elif ob == 14 and self.c[14] != 1 and self.rm == 7 and self.f[14] == 0:
            self.m = "You see thick forest and cliff south"
            self.f[14] = 1
        elif ob == 14 and self.c[14] != 1 and self.rm == 7 and self.f[14] == 1:
            self.m = "Going down!"
            self.f[14] = 0
    
    def light(self, ob):
        if ob == 17 and self.c[17] == 1 and self.c[8] == 0:
            self.m = "It will burn your hands"
        elif ob == 17 and self.c[17] == 1 and self.c[9] == 0:
            self.m = "Nothing to light it with"
        elif ob == 17 and self.c[17] == 1 and self.c[9] == 1 and self.c[8] == 1:
            self.m = "It casts a flickering light"
            self.f[0] = 1
    
    def unlight(self):
        if self.f[0] == 1:
            self.f[0] = 0
            self.m = "Extinguished"
    
    def spray(self, ob):
        if ob == 26 and self.c[16] == 1:
            self.m = "Hissss"
        
        if ob == 26 and self.c[16] == 1 and self.f[26] == 1:
            self.f[26] = 0
            self.m = "Pfft! Got them"
    
    def use(self, ob):
        if ob == 10 and self.c[10] == 1 and self.c[11] == 1:
            self.m = "Switched on"
            self.f[24] = 1
        
        if self.f[27] == 1 and self.f[24] == 1:
            self.m = "Whizz - vacuumed the ghosts up!"
            self.f[27] = 0
    
    def unlock(self, ob):
        if self.rm == 43 and (ob == 27 or ob == 28):
            self.open_item(ob)
        
        if self.rm == 28 and ob == 25 and self.f[25] == 0 and self.c[18] == 1:
            self.f[25] = 1
            self.r[self.rm] = "sew"
            self.d[self.rm] = "Huge open door"
            self.m = "The key turns!"
    
    def leave(self, ob):
        if self.c[ob] == 1:
            self.c[ob] = 0
            self.l[ob] = self.rm
            self.m = "Done"
    
    def score(self):
        s = 0
        for i in range(1, self.g + 1):
            if self.c[i] == 1:
                s += 1
        
        if s == 17 and self.c[15] != 1 and self.rm != 57:
            print("You have everything")
            print("Return to the gate for final score")
        
        if s == 17 and self.rm == 57:
            print("Double score for reaching here!")
            s *= 2
        
        print(f"Your score = {s}")
        
        if s > 18:
            print("Well done! You finished the game")
            return True
        
        input("Press Enter to continue")
        return False
    
    def play_game(self):
        game_over = False
        
        while not game_over:
            self.display_location()
            vb, ob = self.get_input()
            self.process_command(vb, ob)
            
            # Check if game is over
            if vb == 25:  # Score command
                game_over = self.score()

# Run the game
if __name__ == "__main__":
    print("HAUNTED HOUSE ADVENTURE")
    print("A text adventure game converted from BASIC to Python")
    print("=================================================")
    print("Find treasures in a haunted house, but beware of the dangers!")
    print("Type 'help' to see available commands")
    print("=================================================")
    
    game = HauntedHouseAdventure()
    game.play_game()
