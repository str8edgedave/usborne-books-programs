from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import random
import textwrap


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class Room:
    description: str
    exits: str  # String like "nsew" indicating available exits


@dataclass
class GameObject:
    name: str
    location: int  # Room number or 65 for carried
    is_hidden: bool = False
    is_carried: bool = False


class HauntedHouseAdventure:
    def __init__(self) -> None:
        # Game variables
        self.current_room: int = 57  # Starting room
        self.light_level: int = 60  # Light duration
        self.message: str = "ok"
        self.game_over: bool = False
        
        # Initialize game world
        self.rooms: List[Room] = []
        self.objects: Dict[str, GameObject] = {}
        self.special_flags: Dict[str, bool] = {
            "light_on": False,
            "rope_climbed": False,
            "magic_barrier": False,
            "door_open": False,
            "drawer_open": False,
            "ghosts_present": False,
            "vacuum_on": False,
            "movement_possible": False,
            "bats_present": True,
            "ghost_trap_active": False,
            "coffin_open": False,
        }
        
        # Direction mapping
        self.direction_map = {
            "n": Direction.NORTH,
            "s": Direction.SOUTH,
            "w": Direction.WEST,
            "e": Direction.EAST,
            "u": Direction.UP,
            "d": Direction.DOWN,
            "north": Direction.NORTH,
            "south": Direction.SOUTH,
            "west": Direction.WEST,
            "east": Direction.EAST,
            "up": Direction.UP,
            "down": Direction.DOWN,
        }
        
        # Verb mapping
        self.verbs = {
            "help": self.help,
            "carrying": self.carrying,
            "inventory": self.carrying,
            "i": self.carrying,
            "go": self.movement,
            "move": self.movement,
            "walk": self.movement,
            "n": self.movement,
            "s": self.movement,
            "w": self.movement,
            "e": self.movement,
            "u": self.movement,
            "d": self.movement,
            "north": self.movement,
            "south": self.movement,
            "west": self.movement,
            "east": self.movement,
            "up": self.movement,
            "down": self.movement,
            "get": self.get_item,
            "take": self.get_item,
            "pickup": self.get_item,
            "open": self.open_item,
            "examine": self.examine_item,
            "look": self.examine_item,
            "read": self.read_item,
            "say": self.say_word,
            "dig": self.dig,
            "swing": self.swing,
            "climb": self.climb,
            "light": self.light,
            "unlight": self.unlight,
            "extinguish": self.unlight,
            "spray": self.spray,
            "use": self.use,
            "unlock": self.unlock,
            "drop": self.leave,
            "leave": self.leave,
            "score": self.score,
            "quit": self.quit,
            "exit": self.quit,
        }
        
        self.initialize_game_data()
        
    def initialize_game_data(self) -> None:
        """Initialize the game world, rooms, and objects."""
        # Room exits and descriptions
        room_data = [
            ("dark corner", "se"),
            ("overgrown garden", "we"),
            ("by large woodpile", "we"),
            ("yard by rubbish", "swe"),
            ("weedpatch", "we"),
            ("forest", "we"),
            ("thick forest", "swe"),
            ("blasted tree", "ws"),
            ("corner of house", "ns"),
            ("entrance to kitchen", "se"),
            ("kitchen & grimy cooker", "we"),
            ("scullery door", "nw"),
            ("room with inches of dust", "se"),
            ("rear turret room", "w"),
            ("clearing by house", "ne"),
            ("path", "nsw"),
            ("side of house", "ns"),
            ("back of hallway", "ns"),
            ("dark alcove", "se"),
            ("small dark room", "we"),
            ("bottom of spiral staircase", "nwud"),
            ("wide passage", "se"),
            ("slippery steps", "wsud"),
            ("clifftop", "ns"),
            ("near crumbling wall", "n"),
            ("gloomy passage", "ns"),
            ("pool of light", "nse"),
            ("impressive vaulted hallway", "we"),
            ("hall by thick wooden door", "we"),
            ("trophy room", "nsw"),
            ("cellar with barred window", "ns"),
            ("cliff path", "ns"),
            ("cupboard with hanging coat", "s"),
            ("front hall", "nse"),
            ("sitting room", "nsw"),
            ("secret room", "s"),
            ("steep marble stairs", "nsud"),
            ("dining room", "n"),
            ("deep cellar witih coffin", "n"),
            ("cliff path", "ns"),
            ("closet", "ne"),
            ("front lobby", "nw"),
            ("library of evil books", "ne"),
            ("study with desk & hole in wall", "w"),
            ("weird cobwebby room", "nse"),
            ("very cold chamber", "we"),
            ("spooky room", "w"),
            ("cliff path by marsh", "ns"),
            ("rubble-strewn verandah", "se"),
            ("front porch", "nsw"),
            ("front tower", "e"),
            ("sloping corridor", "we"),
            ("upper gallery", "nw"),
            ("marsh by wall", "s"),
            ("marsh", "sw"),
            ("soggy path", "nw"),
            ("by twisted railing", "ne"),
            ("path through iron gate", "nwe"),
            ("by railings", "we"),
            ("beneath front tower", "we"),
            ("debris from crumbling facade", "we"),
            ("large fallen brickwork", "nwe"),
            ("rotting stone arch", "nwe"),
            ("crumbling clifftop", "w"),
        ]
        
        for desc, exits in room_data:
            self.rooms.append(Room(description=desc, exits=exits))
        
        # Initialize objects
        objects_data = [
            ("painting", 46),
            ("ring", 38),
            ("magic spells", 35),
            ("goblet", 50),
            ("scroll", 13),
            ("coins", 18),
            ("statue", 28),
            ("candlestick", 42),
            ("matches", 10),
            ("vacuum", 25),
            ("batteries", 26),
            ("shovel", 4),
            ("axe", 2),
            ("rope", 7),
            ("boat", 47),
            ("aerosol", 60),
            ("candle", 43),
            ("key", 32),
        ]
        
        for name, location in objects_data:
            self.objects[name] = GameObject(name=name, location=location)
        
        # Add special objects that can't be picked up
        special_objects = [
            "door", "bats", "ghosts", "drawer", "desk", 
            "coat", "rubbish", "coffin", "books", "xzanfar", 
            "wall", "spells"
        ]
        
        for obj in special_objects:
            self.objects[obj] = GameObject(name=obj, location=-1, is_hidden=True)
        
        # Set special flags
        self.special_flags["bats_present"] = True
        self.special_flags["coffin_open"] = False
        self.special_flags["drawer_open"] = False
        
    def display_location(self) -> None:
        """Display current room information and visible objects."""
        print("\n" + "=" * 40)
        print("HAUNTED HOUSE".center(40))
        print("=" * 40)
        print(f"Location: {self.rooms[self.current_room].description}")
        
        # Display exits
        exits = self.rooms[self.current_room].exits
        exit_names = []
        for char in exits:
            if char == "n": exit_names.append("north")
            elif char == "s": exit_names.append("south")
            elif char == "w": exit_names.append("west")
            elif char == "e": exit_names.append("east")
            elif char == "u": exit_names.append("up")
            elif char == "d": exit_names.append("down")
        
        print(f"Exits: {', '.join(exit_names)}")
        
        # Display visible objects
        visible_items = []
        for obj_name, obj in self.objects.items():
            if obj.location == self.current_room and not obj.is_hidden:
                visible_items.append(obj_name)
        
        if visible_items:
            print("\nYou can see:")
            for item in visible_items:
                print(f"  - {item}")
        
        print("-" * 40)
        # Display message if there is one
        if self.message:
            print(self.message)
            self.message = ""  # Clear message after displaying
    
    def get_input(self) -> Tuple[str, str]:
        """Get and parse user input into verb and object."""
        command = input("\nWhat will you do? ").lower().strip()
        
        # Split input into words
        words = command.split()
        
        # Default values
        verb = ""
        obj = ""
        
        # Extract verb and object
        if words:
            verb = words[0]
            
            if len(words) > 1:
                # Handle multi-word objects (take magic spells)
                obj = " ".join(words[1:])
        
        return verb, obj
    
    def process_command(self, verb: str, obj: str) -> None:
        """Process the player's command."""
        # Special conditions that happen regardless of command
        
        # Bats attacking in room 13
        if (self.special_flags["bats_present"] and 
            self.current_room == 13 and 
            random.randint(0, 2) != 2 and 
            verb != "spray"):
            self.message = "Bats attacking!"
            return
        
        # Ghosts may appear in room 44
        if (self.current_room == 44 and 
            random.randint(0, 1) == 1 and 
            not self.special_flags["vacuum_on"]):
            self.special_flags["ghosts_present"] = True
        
        # Decrement light level if light is on
        if self.special_flags["light_on"]:
            self.light_level -= 1
            
            if self.light_level < 1:
                self.special_flags["light_on"] = False
                self.message = "Your candle has burned out!"
        
        # Handle the command if we know the verb
        if verb in self.verbs:
            self.verbs[verb](obj)
        else:
            self.message = f"I don't understand '{verb}'."
        
        # Light warnings
        if self.light_level == 10 and self.special_flags["light_on"]:
            self.message = "Your candle is waning!"
        elif self.light_level == 1 and self.special_flags["light_on"]:
            self.message = "Your candle is about to go out!"
    
    def help(self, obj: str = "") -> None:
        """Display help information."""
        print("\nCommands you can use:")
        
        # Group verbs by category for better organization
        categories = {
            "Movement": ["go", "north/n", "south/s", "east/e", "west/w", "up/u", "down/d"],
            "Actions": ["get/take", "drop/leave", "examine/look", "read", "open", "unlock", "light", "unlight/extinguish", "use", "dig", "swing", "climb", "spray", "say"],
            "Game": ["inventory/i", "score", "help", "quit/exit"]
        }
        
        for category, verb_list in categories.items():
            print(f"\n{category}:")
            print("  " + ", ".join(verb_list))
        
        print("\nTip: Use commands like 'go north' or just 'n', 'get key', 'examine door', etc.")
        input("\nPress Enter to continue...")
    
    def carrying(self, obj: str = "") -> None:
        """Display carried items."""
        carried_items = [obj.name for obj in self.objects.values() if obj.is_carried]
        
        print("\nYou are carrying:")
        if carried_items:
            for item in carried_items:
                print(f"  - {item}")
        else:
            print("  Nothing")
        
        input("\nPress Enter to continue...")
    
    def determine_direction(self, verb: str, obj: str) -> Optional[Direction]:
        """Convert user input to a direction."""
        # Direction from verb (n, s, e, w, etc.)
        if verb in self.direction_map:
            return self.direction_map[verb]
        
        # Direction from object (north, south, etc.)
        if obj in self.direction_map:
            return self.direction_map[obj]
        
        return None
    
    def movement(self, obj: str) -> None:
        """Handle player movement."""
        # Determine direction from input
        direction = self.determine_direction(verb="go", obj=obj)
        
        if not direction:
            self.message = "Go where?"
            return
        
        # Special conditions
        if self.special_flags["rope_climbed"]:
            self.message = "Crash! You fell out of the tree!"
            self.special_flags["rope_climbed"] = False
            return
        
        if self.special_flags["ghosts_present"] and self.current_room == 52:
            self.message = "Ghosts will not let you move"
            return
        
        if (self.current_room == 45 and 
            "painting" in [obj.name for obj in self.objects.values() if obj.is_carried] and 
            not self.special_flags["magic_barrier"] and 
            direction in [Direction.WEST]):
            self.message = "A magical barrier to the west"
            return
        
        if ((self.current_room == 26 and not self.special_flags["light_on"]) and 
            (direction in [Direction.NORTH, Direction.EAST])):
            self.message = "You need a light"
            return
        
        if self.current_room == 54 and not self.objects["boat"].is_carried:
            self.message = "You're stuck!"
            return
        
        if (self.objects["boat"].is_carried and 
            self.current_room not in [53, 54, 55, 47]):
            self.message = "You can't carry a boat here!"
            return
        
        if (26 < self.current_room < 30 and not self.special_flags["light_on"]):
            self.message = "Too dark to move"
            return
        
        # Check if direction is valid for current room
        exits = self.rooms[self.current_room].exits
        can_move = False
        
        new_room = self.current_room
        
        # Process movement based on direction
        if direction == Direction.NORTH and "n" in exits:
            new_room = self.current_room - 8
            can_move = True
        elif direction == Direction.SOUTH and "s" in exits:
            new_room = self.current_room + 8
            can_move = True
        elif direction == Direction.WEST and "w" in exits:
            new_room = self.current_room - 1
            can_move = True
        elif direction == Direction.EAST and "e" in exits:
            new_room = self.current_room + 1
            can_move = True
        elif direction == Direction.UP and "u" in exits:
            new_room = self.current_room - 8
            can_move = True
        elif direction == Direction.DOWN and "d" in exits:
            new_room = self.current_room + 8
            can_move = True
        
        # Special room connections (these override the standard movement)
        if self.current_room == 20:
            if direction == Direction.UP:
                new_room = self.current_room - 8  # Same as north
            elif direction == Direction.DOWN:
                new_room = self.current_room - 1  # Same as west
        elif self.current_room == 22:
            if direction == Direction.DOWN:
                new_room = self.current_room + 8  # Same as south
            elif direction == Direction.UP:
                new_room = self.current_room - 1  # Same as west
        elif self.current_room == 36:
            if direction == Direction.DOWN:
                new_room = self.current_room - 8  # Same as north
            elif direction == Direction.UP:
                new_room = self.current_room - 1  # Same as west
        
        if can_move:
            self.current_room = new_room
            self.message = "OK"
            
            # Special case: door slams shut
            if self.current_room == 41 and self.rooms[49].exits == "nsew":
                self.rooms[49].exits = "sw"
                self.message = "The door slams shut!"
        else:
            self.message = "You can't go that way!"
    
    def get_item(self, obj: str) -> None:
        """Pick up an item."""
        if not obj:
            self.message = "Get what?"
            return
        
        # Check if object exists
        if obj not in self.objects:
            self.message = f"There's no {obj} here."
            return
        
        game_obj = self.objects[obj]
        
        # Check if object is in the current room
        if game_obj.location != self.current_room:
            self.message = "It isn't here."
            return
        
        # Check if object is hidden
        if game_obj.is_hidden:
            self.message = f"What {obj}?"
            return
        
        # Check if already carrying
        if game_obj.is_carried:
            self.message = "You already have it."
            return
        
        # Pick up the object
        game_obj.is_carried = True
        game_obj.location = -1  # No longer in any room
        self.message = f"You take the {obj}."
    
    def open_item(self, obj: str) -> None:
        """Open something."""
        if not obj:
            self.message = "Open what?"
            return
        
        if self.current_room == 43 and obj in ["drawer", "desk"]:
            self.special_flags["drawer_open"] = True
            self.message = "Drawer open."
        elif self.current_room == 28 and obj == "door":
            self.message = "It's locked."
        elif self.current_room == 38 and obj == "coffin":
            self.message = "That's creepy!"
            self.special_flags["coffin_open"] = True
        else:
            self.message = f"You can't open the {obj}."
    
    def examine_item(self, obj: str) -> None:
        """Examine an object."""
        if not obj:
            # If no object specified, describe the room again
            self.message = f"You see: {self.rooms[self.current_room].description}"
            return
        
        if obj == "coat":
            self.message = "There's something here!"
            self.objects["key"].location = self.current_room
            self.objects["key"].is_hidden = False
        elif obj == "rubbish":
            self.message = "That's disgusting!"
        elif obj in ["drawer", "desk"]:
            self.message = "There is a drawer."
        elif obj in ["books", "scroll"]:
            self.read_item(obj)
        elif self.current_room == 43 and obj == "wall":
            self.message = "There is something beyond..."
        elif obj == "coffin":
            self.open_item(obj)
        else:
            visible_items = [o.name for o in self.objects.values() 
                           if o.location == self.current_room and not o.is_hidden]
            carried_items = [o.name for o in self.objects.values() if o.is_carried]
            
            if obj in visible_items:
                self.message = f"You see a {obj}. You can probably take it."
            elif obj in carried_items:
                self.message = f"You're carrying the {obj}."
            else:
                self.message = "You don't see that here."
    
    def read_item(self, obj: str) -> None:
        """Read an object."""
        if not obj:
            self.message = "Read what?"
            return
        
        if self.current_room == 42 and obj == "books":
            self.message = "They are demonic works."
        elif obj in ["magic spells", "spells"] and any(o.name == "magic spells" and o.is_carried for o in self.objects.values()) and not self.special_flags["magic_barrier"]:
            self.message = "Use this word with care 'xzanfar'."
        elif obj == "scroll" and any(o.name == "scroll" and o.is_carried for o in self.objects.values()):
            self.message = "The script is in an alien tongue."
        else:
            self.message = f"You can't read the {obj}."
    
    def say_word(self, obj: str) -> None:
        """Say a word."""
        if not obj:
            self.message = "Say what?"
            return
        
        self.message = f"You said '{obj}'."
        
        if (obj == "xzanfar" and 
            any(o.name == "magic spells" and o.is_carried for o in self.objects.values())):
            self.message = "*magic occurs*"
            
            if self.current_room != 45:
                self.current_room = random.randint(0, 63)
            else:
                self.special_flags["magic_barrier"] = True
    
    def dig(self, obj: str = "") -> None:
        """Dig with the shovel."""
        if any(o.name == "shovel" and o.is_carried for o in self.objects.values()):
            self.message = "You made a hole."
            
            if self.current_room == 30:
                self.message = "Dug the bars out."
                self.rooms[self.current_room].description = "Hole in wall"
                self.rooms[self.current_room].exits = "nse"
        else:
            self.message = "You have nothing to dig with."
    
    def swing(self, obj: str) -> None:
        """Swing an object."""
        if not obj:
            self.message = "Swing what?"
            return
        
        if obj == "rope" and not any(o.name == "rope" and o.is_carried for o in self.objects.values()) and self.current_room == 7:
            self.message = "This is no time to play games."
        elif obj == "rope" and any(o.name == "rope" and o.is_carried for o in self.objects.values()):
            self.message = "You swung it."
        elif obj == "axe" and any(o.name == "axe" and o.is_carried for o in self.objects.values()):
            self.message = "Whoosh."
            
            if self.current_room == 43:
                self.rooms[self.current_room].exits = "wn"
                self.rooms[self.current_room].description = "Study with secret room"
                self.message = "You broke the thin wall."
        else:
            self.message = f"You can't swing the {obj}."
    
    def climb(self, obj: str) -> None:
        """Climb something."""
        if not obj:
            self.message = "Climb what?"
            return
        
        if obj == "rope" and any(o.name == "rope" and o.is_carried for o in self.objects.values()):
            self.message = "It isn't attached to anything!"
        elif obj == "rope" and not any(o.name == "rope" and o.is_carried for o in self.objects.values()) and self.current_room == 7:
            if not self.special_flags["rope_climbed"]:
                self.message = "You see thick forest and cliff south."
                self.special_flags["rope_climbed"] = True
            else:
                self.message = "Going down!"
                self.special_flags["rope_climbed"] = False
        else:
            self.message = f"You can't climb the {obj}."
    
    def light(self, obj: str) -> None:
        """Light the candle."""
        if not obj or obj != "candle":
            self.message = "Light what?"
            return
        
        candle_carried = any(o.name == "candle" and o.is_carried for o in self.objects.values())
        candlestick_carried = any(o.name == "candlestick" and o.is_carried for o in self.objects.values())
        matches_carried = any(o.name == "matches" and o.is_carried for o in self.objects.values())
        
        if candle_carried and not candlestick_carried:
            self.message = "It will burn your hands."
        elif candle_carried and not matches_carried:
            self.message = "Nothing to light it with."
        elif candle_carried and matches_carried and candlestick_carried:
            self.message = "It casts a flickering light."
            self.special_flags["light_on"] = True
        else:
            self.message = "You don't have a candle."
    
    def unlight(self, obj: str = "") -> None:
        """Extinguish the candle."""
        if self.special_flags["light_on"]:
            self.special_flags["light_on"] = False
            self.message = "Extinguished."
        else:
            self.message = "Nothing is lit."
    
    def spray(self, obj: str) -> None:
        """Spray the aerosol."""
        if not obj:
            self.message = "Spray what?"
            return
        
        if obj == "bats" and any(o.name == "aerosol" and o.is_carried for o in self.objects.values()):
            self.message = "Hissss."
            
            if self.special_flags["bats_present"]:
                self.special_flags["bats_present"] = False
                self.message = "Pfft! Got them."
        else:
            self.message = f"You can't spray the {obj}."
    
    def use(self, obj: str) -> None:
        """Use an item."""
        if not obj:
            self.message = "Use what?"
            return
        
        vacuum_carried = any(o.name == "vacuum" and o.is_carried for o in self.objects.values())
        batteries_carried = any(o.name == "batteries" and o.is_carried for o in self.objects.values())
        
        if obj == "vacuum" and vacuum_carried and batteries_carried:
            self.message = "Switched on."
            self.special_flags["vacuum_on"] = True
            
            if self.special_flags["ghosts_present"]:
                self.message = "Whizz - vacuumed the ghosts up!"
                self.special_flags["ghosts_present"] = False
        else:
            self.message = f"You can't use the {obj} right now."
    
    def unlock(self, obj: str) -> None:
        """Unlock something."""
        if not obj:
            self.message = "Unlock what?"
            return
        
        if self.current_room == 43 and obj in ["drawer", "desk"]:
            self.open_item(obj)
        elif (self.current_room == 28 and 
              obj == "door" and 
              not self.special_flags["door_open"] and 
              any(o.name == "key" and o.is_carried for o in self.objects.values())):
            self.special_flags["door_open"] = True
            self.rooms[self.current_room].exits = "sew"
            self.rooms[self.current_room].description = "Huge open door"
            self.message = "The key turns!"
        else:
            self.message = f"You can't unlock the {obj}."
    
    def leave(self, obj: str) -> None:
        """Drop an item."""
        if not obj:
            self.message = "Drop what?"
            return
        
        if obj not in self.objects:
            self.message = f"You don't have a {obj}."
            return
        
        game_obj = self.objects[obj]
        
        if game_obj.is_carried:
            game_obj.is_carried = False
            game_obj.location = self.current_room
            self.message = f"Dropped the {obj}."
        else:
            self.message = f"You don't have the {obj}."
    
    def score(self, obj: str = "") -> None:
        """Display score."""
        treasures = ["painting", "ring", "magic spells", "goblet", "scroll", 
                     "coins", "statue", "candlestick", "key"]
        
        carried_treasures = [o.name for o in self.objects.values() 
                           if o.is_carried and o.name in treasures]
        score = len(carried_treasures)
        
        print(f"\nYou are carrying {score} treasures.")
        
        if score == 8 and not self.objects["boat"].is_carried and self.current_room != 57:
            print("You have everything.")
            print("Return to the gate for final score.")
        
        if score == 8 and self.current_room == 57:
            print("Double score for reaching here!")
            score *= 2
        
        print(f"Your score = {score} out of a possible 18")
        
        if score > 16:
            print("Well done! You finished the game!")
            self.game_over = True
        
        input("\nPress Enter to continue...")
    
    def quit(self, obj: str = "") -> None:
        """Quit the game."""
        confirm = input("\nAre you sure you want to quit? (y/n): ").lower()
        if confirm == "y":
            self.game_over = True
            print("Thanks for playing!")
        else:
            self.message = "Game continues."
    
    def play_game(self) -> None:
        """Main game loop."""
        while not self.game_over:
            self.display_location()
            verb, obj = self.get_input()
            self.process_command(verb, obj)


def display_intro() -> None:
    """Display game introduction."""
    title = """
    ██   