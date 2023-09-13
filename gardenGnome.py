from support import *
from typing import Optional

#Classes
class Entity:
    """ Abstract base class for any entity. """
    _id=ENTITY

    def get_class_name(self) -> str:
        """ Return the class name of this entity's class. """
        return self.__class__.__name__
    
    def get_id(self) -> str:
        """ Return the single character id of this entity class. """
        return self._id
    
    def __str__(self) -> str:
        """ Returns the string representation of this entity. """
        return str(self.get_id())

    def __repr__(self) -> str:
        """ Returns the string representation of this entity.Looks inditial to self. """
        return f"{self.get_class_name()}()"


class Plant(Entity):
    """ Plant is an Entity. It is the children class of Entity. """
    _id=PLANT

    def __init__(self, name: str):
        """ Set up the plant with a given plant name. 

        Parameters:
            name: The name of the plant
        """
        self._name = name
        self._water = 10.0
        self._HP = 10
        self._age = 0
        self._repellent = False
   
    def get_name(self) -> str:
        """ Return name of the plant. """
        return self._name

    def get_health(self) -> int:
        """ Return the plant's current HP. """
        return self._HP

    def get_water(self) -> float:
        """ Return the water levels of the plant. """
        return self._water

    def water_plant(self) -> None:
        """ Add to the plant's water level by 1. """
        self._water += 1

    def get_drink_rate(self) -> float:
        """ Return water drinking rate of the plant. """
        plant_name = PLANTS_DATA[self._name]
        drink_rate = plant_name['drink rate']
        return drink_rate

    def get_sun_levels(self) -> tuple[int, int]:
        """ Return the acceptable sun level of the plant with the lower and upper range. 

        Return:
            The range of the sun level of the plant.
            Type: tuple
        """
        plant_name = PLANTS_DATA[self._name]
        sun_lower = plant_name['sun-lower']
        sun_upper = plant_name['sun-upper']
        return (sun_lower,sun_upper)

    def decrease_water(self, amount: float):
        """ Decrease the plants water by a specified amount. 

        Parameters:
            amount: The amount of the water to decrease
        """	
        self._water -= amount
        
    def drink_water(self):
        """ Reduce water levels by plant’s drink rate. """
        self._water -= self.get_drink_rate()
        if self._water <= 0:
            self._HP -= 1

    def add_health(self, amount: int) -> None:
        """ Add to the plant’s health levels by a specified amount. 

        Parameters:
            amount: The amount of the health point to add
        """
        self._HP += amount

    def decrease_health(self, amount: int = 1):
        """ Decrease the plants health by a specified amount, decrease by 1 by default. 

        Parameters:
            amount: The amount of the health point to decrease
        """
        self._HP -= amount

    def set_repellent(self, applied: bool) -> None:
        """ Apply or remove repellent from plant. 
        
        Parameters:
            applied: Add repellent to the plant if applied is True. False otherwise.
        """
        self._repellent = applied

    def has_repellent(self) -> bool:
        """ Return True if the plant has repellent, False otherwise. """
        return self._repellent

    def get_age(self) -> int:
        """ Return how many days this plant has been planted. """
        return self._age

    def increase_age(self):
        """ Increase the number of days this plant has been planted by 1. """
        self._age += 1

    def is_dead(self) -> bool:
        """ Return True if the plant’s health is 
            less than or equals to zero, False otherwise. 
        """
        if self._HP <= 0:
            return True
        else:
            return False

    def __repr__(self):
        """ Returns the string representation of 
            this entity.Looks inditial to self, with name. 
        """
        return f"{self.get_class_name()}('{self.get_name()}')"


class Item(Entity):
    """ Abstract subclass of Entity.
        It provides base functionality for all items in the game. 
    """
    _id = ITEM

    def apply(self, plant: 'Plant') -> None:
        raise NotImplementedError


class Water(Item):
    """ Subclass of Item.
        Adds to plant's water level by 1 when applied. 
    """
    _id = WATER

    def apply(self, plant: 'Plant') -> None:
        """ Parameters:
                plant: The plant to be watered
        """
        plant.water_plant()


class Fertiliser(Item):
    """ Subclass of Item.
        Adds to plant's health by 1 when applied. 
    """
    _id = FERTILISER

    def apply(self, plant: Plant) -> None:
        """ Parameters:
                plant: The plant to be fertilised
        """
        plant.add_health(1)


class PossumRepellent(Item):
    """ Subclass of Item.
        Cancel a possum attach when applied. 
    """
    _id = POSSUM_REPELLENT

    def apply(self, plant: 'Plant') -> None:
        """ Parameters:
                plant: The plant to be setted possumrepellent
        """
        plant.set_repellent(True)


class Inventory:
    """ A collection of items and plants. """
    def __init__(self, initial_items: Optional[list[Item]] = None, 
        initial_plants: Optional[list[Plant]] = None) -> None:
        """ Sets up this inventory with the initial items and plants.
            Else set up an empty inventory.

        Parameter:
            initial_items: An optional list of initial items to put in inventory
            initial_plants: An optional list of initial plants to put in inventory
        """
        self._items = []
        self._plants = []
        if initial_items is not None:
            for item in initial_items:
                self._items.append(item)
        if initial_plants is not None:
            for plant in initial_plants:
                self._plants.append(plant)
    
    def add_entity(self, entity: Item | Plant) -> None:
        """ Adds the given item or plant to this inventory's collection of entities. """
        #if the entity type is Item, add to the self._initial_items
        if entity.get_class_name() in ['Water','Fertiliser','PossumRepellent']:
            self._items.append(entity)

        #if the entity type is Plant, add to the self._initial_plants
        elif entity.get_class_name() == 'Plant':
            self._plants.append(entity)

    def get_entities(self, entity_type: str) -> dict[str, list[Item | Plant]]:
        """ Returns the a dictionary mapping entity (item or plant) names to the 
            instances of the entity with that name in the inventory. 
        
        Parameters:
            entity_type: The type of the entity (Plant or Item)

        Return: 
            A dictionary of Item or Plant
        """
        items_dict = dict()
        plants_dict = dict()

        #if the entyti_type is Item, return the dict of the items in the inventory
        if entity_type == 'Item':
            for item in self._items:
                if str(item) not in items_dict:
                    items_dict[str(item)] = [item]
                else:
                    items_dict[str(item)].append(item)
            return items_dict

        #if the entyti_type is Plant, return the dict of the plants in the inventory
        if entity_type == 'Plant':
            for plant in self._plants:
                if plant.get_name() not in plants_dict:
                    plants_dict[plant.get_name()] = [plant]
                else:
                    plants_dict[plant.get_name()].append(plant)
            return plants_dict

    def remove_entity(self, entity_name: str) -> Optional[Item | Plant]:
        """ Removes one instance of the entity (item or plant) 
            with the given name from inventory,if one exists.

        Parameters:
            entity_name: The name of the entity 

         Return:
            The delated entity  
        """
        for item in range(0,len(self._items)):
            if entity_name == self._items[item].get_id():
                item_pop = self._items.pop(item)
                return item_pop
            
        for plant in range(0,len(self._plants)):
            if entity_name == self._plants[plant].get_name():
                plant_pop = self._plants.pop(plant)
                return plant_pop

    def __str__(self) -> str:
        """ Returns a string containing information about 
            quantities of items available in the inventory. 
        """
        str_term=''
        # put the items and plants (string) into str_term separately
        for item in self.get_entities('Item'):
            str_term += f"{item}: {len(self.get_entities('Item')[item])}\n"

        for plant in self.get_entities('Plant'):
            str_term += f"{plant}: {len(self.get_entities('Plant')[plant])}\n"
    
        # return the str_term without the last blank line
        return str_term.strip()

    def __repr__(self) ->str:
        """ Returns a string that could be used to construct 
            a new instance of Inventory containing the same items 
            as self currently contains. 
        """
        return f"Inventory(initial_items={self._items}, initial_plants={self._plants})"
        

class Pot(Entity):
    """ An Entity that has growing conditions information and an instance of plant. """
    _id=POT

    def __init__(self) -> None:
        """ Sets up an empty pot. """
        self._sun_range = None
        self._evaporation = None
        self._plant_pot = None

    def set_sun_range(self, sun_range: tuple[int, int]) -> None:
        """ Sets the sun range experienced by the pot. 

        Parameters:
            sun_range: The range of the sun level that wo want the plant to have
        """
        self._sun_range = sun_range
  
    def get_sun_range(self) -> tuple[int, int]:
        """ Returns the sun range experienced by the pot. 

        Return:
            The sun_range that you set.
        """
        return self._sun_range

    def set_evaporation(self, evaporation: float) -> None:
        """ Sets the evaporation rate of the pot. 

        Parameters:
            evaporation: The evaporation you want the plant to have
        """
        self._evaporation = evaporation

    def get_evaporation(self) -> float:
        """ Returns the evaporation rate of the pot. 
        
        Return:
            The evaporation you set.
        """
        return self._evaporation

    def put_plant(self, plant: Plant) -> None:
        """ Adds an instance of a plant to the pot. 

        Parameters:
            plant: The plant you want to add to the pot
        """
        self._plant_pot = plant

    def look_at_plant(self) -> Optional[Plant]:
        """ Returns the plant in the pot and without removing it.

        Return:
            The plant in the pot that you want to check.
        """
        return self._plant_pot

    def remove_plant(self) -> Optional[Plant]:
        """ Returns the plant in the pot and removes it from the pot. 

        Return:
            The plant that has been removed.
        """
        self._plant_pot_copy = self.look_at_plant()
        self._plant_pot = None
        return self._plant_pot_copy

    def progress(self) -> None:
        """Progress the state of the plant and check 
           if the current plant is suitable in the given conditions. 
           Decrease the plant's water levels based on the evaporation.
           Decrease the HP in some given conditions. 
        """
        # Check if the plant is dead. If it is dead, it don't need to be progressed.
        if self.look_at_plant().is_dead():
            print(self.look_at_plant().get_name()+ " is dead")
            return

        # define the vairables   
        sun_range_lower = self._sun_range[0]
        sun_range_upper = self._sun_range[1]
        sun_level_lower = self.look_at_plant().get_sun_levels()[0]
        sun_level_upper = self.look_at_plant().get_sun_levels()[1]
        plant_name = PLANTS_DATA[self.look_at_plant().get_name()]
        plant_drink_rate = plant_name['drink rate']

        # check the water level and sun_range to decide if its HP needs to be decreased
        if self.look_at_plant().get_water() < 0:
            self.look_at_plant().decrease_health(1)
        if (sun_range_upper < sun_level_lower or sun_range_lower > sun_level_upper):
            self.look_at_plant().decrease_health(1)
            print("Poor "+self.look_at_plant().get_name()+" dislikes the sun levels.")

        # decrease the water level
        self.look_at_plant()._water -= (self.get_evaporation() + plant_drink_rate)

    def animal_attack(self) -> None:
        """ Decreases the health of the plant by the animal attack damage dealt
            and print out a sentence.
            Do nothing if there is no plant in the pot.
            Attack should fail if plant has animal repellent. 
        """
        if self.look_at_plant() != None:
            if self.look_at_plant()._repellent:
                self.look_at_plant().decrease_health(ANIMAL_ATTACK_DAMAGE)
                print("There has been an animal attack! But luckily the " +\
                     self.look_at_plant().get_name()+" has repellent.")
            else:
                print("There has been an animal attack! Poor " +\
                     self.look_at_plant().get_name()+".")

    def __str__(self) -> str:
        """ Returns the string representation of this entity. """
        return str(self.get_class_name())
    
    def __repr__(self) -> str:
        """ Returns the string representation of this entity.
            Do the same thing as __str__. 
        """
        return f"{self.get_class_name()}()" 


class Room:
    """ A Room instance represents the space in which
        plants can be planted and the 
        instances of plants within the room. 
    """
    def __init__(self, name):
        """ Set up an empty room of given room name.

        Parameters:
            name: The name of the room
        """
        self._room_name = name
        self._initial_plants = {0: None, 1: None, 2: None, 3: None}
        self._initial_pots = {0: Pot(), 1: Pot(), 2: Pot(), 3: Pot()}
        
    def init_positions(self): 
        pass
        
    def get_plants(self) -> dict[int, Plant | None]:
        """ Return the Plant instances in this room.
            With the keys being the positions and value being the corresponding plant.

        Return:
            A dictionary of the plants in the room 
        """
        for index_num in self._initial_pots:
            self._initial_plants[index_num] = self._initial_pots[index_num].look_at_plant()
        return self._initial_plants
        
    def get_number_of_plants(self) -> int:
        """ Return the total number of live plants in the room. """
        plant_num = 0
        for index_plant in self.get_plants():
            if self.get_plants()[index_plant] is not None and\
                 self.get_plants()[index_plant]._HP > 0:
                plant_num += 1
        return plant_num
        
    def add_pots(self, pots: dict[int, Pot]) -> None:    
        """ Add a pot to the room.

        Parameter:
            pots: a dictionary of the pot
        """
        for index_pot in pots:
            self._initial_pots[index_pot] = pots[index_pot]    

    def get_pots(self) -> dict[int, Pot]:
        """ Return all pots within the room. """
        return self._initial_pots

    def get_pot(self, position: int) -> Pot:
        """ Return the Pot instance at the given position.

        Parameter:
            position: The position of the pot.
        """
        return self._initial_pots[position]

    def add_plant(self, position: int, plant: Plant):
        """ Add a plant instance to Pot at a given position
            if no plant exist at that position.
            Do nothing if a plant is already there.

        Parameters:
            position: The position of the pot (in [0,1,2,3]) 
            plant: The plant to add
        """
        self._initial_pots[int(position)].put_plant(plant)
        
    def get_name(self) -> str:
        """ Return the name of this room instance. """
        return self._room_name
        
    def remove_plant(self, position: int) -> Plant | None:
        """ Removes the plant from a pot at the given position.

        Parameters:
            position: The position of the pot.

        Return:
            The removed plant.
        """
        plant_obj = self._initial_pots[position].look_at_plant()
        if plant_obj is not None:
            new_plant = self._initial_pots[position].remove_plant()
            return new_plant
        else:
            return None
        
    def progress_plant(self, pot: Pot) -> bool:
        """ Return True if pot is not empty and triggers a given pot
            to check on plant condition and plant to age. 
            False if pot is empty.
        
        Parameters:
            pot: The pot to be progressed
        """
        if pot.look_at_plant() is not None:
            pot.progress()
            pot.look_at_plant().increase_age()
            return True
        elif pot.look_at_plant() is None:
            return False

    def progress_plants(self) -> None:
        """ Progress each pot with the progress_plant method
            in ascending order of position.
        """
        for pot in self.get_pots():
            self.progress_plant(self.get_pots()[pot])
        
    def __str__(self) -> str:
        """ Return the string representation of this room. """
        return self._room_name
        
    def __repr__(self) -> str:
        """ Return a string that could be copied and pasted
            to construct a new Room instance 
            with the same name as this Room instance.
        """
        return f"{self.__class__.__name__}('{self._room_name}')"
        
        
class OutDoor(Room):
    """ An OutDoor is a Room but outdoors.
        It is the children class of Room.
    """
    def progress_plant(self, pot: Pot) -> bool:
        """ Returns True if pot is not empty and triggers a given pot 
            to check on plant condition and plant to age. 
            False if pot is empty.
            Checks to see if an animal attack has occured.
        
        Parameters:
            pot: The pot to be progressed
        """
        if pot.look_at_plant() is not None:
            pot.progress()
            pot.look_at_plant().increase_age()
            if dice_roll():
                pot.animal_attack()
            return True
        elif pot.look_at_plant() is None:
            pot.animal_attack()
            return False


class Model:
    """ This is the model class that the controller 
        uses to understand and mutate the house state.
        The model keeps track of multiple Room instances and an inventory.
    """

    def __init__(self, house_file: str):
        """ Parameters:
                house_file: The path to the file
        """
        self._house_file_name = house_file
        self._house = load_house(house_file)
        self._day = 1
        self._initial_number = 0
        self._current_number = 0
        self._Item = []
        self._Plant = []

        # get the initial number of plants
        for room in self._house[0]:
            self._initial_number += self.get_rooms()[room[1]].get_number_of_plants() 
        
        # get the items and plants to add to the iventory
        for plant in self._house[1]:
            for plant_index in range(0,self._house[1][plant]):
                self._Plant.append(Plant(plant))
        for item in self._house[2]:
            for item_index in range(0,self._house[2][item]):
                if item == 'W':
                    self._Item.append(Water())
                elif item == 'F':
                    self._Item.append(Fertiliser())
                elif item == 'R':
                    self._Item.append(PossumRepellent())
        self._inventory = Inventory(self._Item,self._Plant)
        
    def get_rooms(self) -> dict[str, Room]:
        """ Returns all rooms with room name as keys with a corresponding room instance.

        Return:
            A dictionary of the plants
        """
        room_dict = dict()
        for room in self._house[0]:
            room_dict[room[1]] = room[0]
        return room_dict
        
    def get_all_rooms(self) -> list[Room]:
        """ Returns a list of all the room instances. """
        room_list = []
        for room in self._house[0]:
            room_list.append(room[0])
        return room_list
        
    def get_inventory(self) -> Inventory:
        """ Returns the inventory. """
        return self._inventory
        
    def get_days_past(self) -> int:
        """ Returns the number of days since the start. """
        return self._day

    def next(self, applied_items: list[tuple[str, int, Item]]) -> None:
        """ 1.Move to the next day.
            2.If there are items in the list of applied items,then apply all affects.
            3.Add fertiliser and possumrepellent to the inventory every 3 days.
            4.Progress all plants in all rooms.
        
        Parameters:
            applied_items: The item to be added to the plant in the special position
        """
        self._day += 1

        # Add fertiliser and possumrepellent to the inventory every 3 days.
        if (self._day-1)%3 == 0:
                self.get_inventory().add_entity(Fertiliser())
                self.get_inventory().add_entity(PossumRepellent())

        # apply the items to the plants
        for index in applied_items:
            if index[2] is not None:
                if index[2].get_class_name() == 'Water':
                    self.get_rooms().get(index[0]).get_pot(index[1]).look_at_plant().water_plant()
                if index[2].get_class_name() == 'PossumRepellent':
                    self.get_rooms().get(index[0]).get_pot(index[1]).look_at_plant().set_repellent(True)
                if index[2].get_class_name() == 'Fertiliser':
                    self.get_rooms().get(index[0]).get_pot(index[1]).look_at_plant().add_health(1)

        # progress all the plants in all rooms
        for room in self.get_all_rooms():
            room.progress_plants()
        
    def move_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None: 
        """Move a plant from a room at a given position 
           to a room with the given position.

        Parameters:
            from_room_name: The name of the initial room of the plant
            from_position: The initial position
            to_room_name: The given room 
            to_position: The given position
        """
        plant = self.get_rooms().get(from_room_name).get_pot(from_position).look_at_plant()
        self.get_rooms()[from_room_name].remove_plant(from_position)
        self.get_rooms()[to_room_name].add_plant(to_position , plant)
        
    def plant_plant(self, plant_name: str, room_name: str, 
        position: int) -> None:
        """ Plant a plant in a room at a given position.

        Parameters:
            plant_name: The name of the plant to plant
            room_name: The name of the room to plant the plant
            position: The position to plant the plant
        """
        self.get_inventory().remove_entity(plant_name)
        self.get_rooms()[room_name].add_plant(position,Plant(plant_name))
        
    def swap_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None:
        """ Swap the two plants from a room at a given position 
            to a room with the given position.
        
        Parameters:
            from_room_name: The initial room of the plant1
            from_position: The initial position of the plant1
            to_room_name: The initial room of the plant2
            to_position: The initial position of the plant2
        """
        plant1 = self.get_rooms().get(from_room_name).get_pot(from_position).look_at_plant()
        plant2 = self.get_rooms().get(to_room_name).get_pot(to_position).look_at_plant()
        self.get_rooms()[from_room_name].remove_plant(from_position)
        self.get_rooms()[to_room_name].remove_plant(to_position)
        self.get_rooms()[to_room_name].add_plant(to_position , plant1)
        self.get_rooms()[from_room_name].add_plant(from_position , plant2)
        
    def get_number_of_plants_alive(self) -> int:
        """ Return the number of plants that are alive in all rooms. """
        for room in self.get_all_rooms():
            self._current_number += room.get_number_of_plants()
        return self._current_number

    def has_won(self) -> bool:
        """ Return True if number of plants alive > 50% of number 
            from start of the 15 day period. 
            And 15 days has passed.
        """
        if self._day >= 15:
            if (self._initial_number/2 < self.get_number_of_plants_alive()):
                return True
        return False
           
    def has_lost(self) -> bool:
        """ Return True if number of plants alive <= 50% of number 
            from start of the 15 day period.
        """
        if self._day <= 15:
            if (self._initial_number/2 >= self.get_number_of_plants_alive()):
                return True
        return False

    def __str__(self) -> str:
        """ Returns the text required to construct a new instance 
            of Model with the same game file used to construct self.
        """
        return f"{self.__class__.__name__}('{self._house_file_name}')"

    def __repr__(self) -> str:
        """ Does the same thing as __str__. """
        return f"{self.__class__.__name__}('{self._house_file_name}')"
        

class GardenSim:
    """ The controller class. """
    def __init__(self, game_file: str, view: View):
        """ Parameters:
                game_file: Path to the file 
                view: A class to manage the display of information
        """
        self._model = Model(game_file)
        self._view = view
        self._applied_items = []

    def play(self):
        """ Executes the entire game until a win or loss occurs. """
        while True:
            # print the board of the house
            self._view.draw(self._model.get_all_rooms())
            move = input('\nEnter a move: ')

            # doing actions according to the input string
            if move[0] == 's' and len(move) == 15:
                self._model.swap_plant(move[2:6],int(move[7]),move[9:13],int(move[14]))
            elif move[0] == 'm' and len(move) == 15:
                self._model.move_plant(move[2:6],int(move[7]),move[9:13],int(move[14]))
            elif move[0:2] == 'rm' and len(move) == 9:
                print(f"{self._model.get_rooms().get(move[3:7]).get_pot(int(move[8])).remove_plant().get_name()} has been removed.")
            elif move[0:2] == 'ls' and (len(move) == 2 or len(move) == 9):
                # according to the length of the string to decide what to output
                if len(move) == 2:
                    self._view.display_rooms(self._model.get_rooms())
                    self._view.display_inventory(self._model.get_inventory().get_entities('Plant'),'Plant')
                    self._view.display_inventory(self._model.get_inventory().get_entities('Item'),'Item')
                if len(move) == 9:
                    self._view.display_room_position_information(self._model.get_rooms().get(move[3:7]),\
                        int(move[8]),self._model.get_rooms().get(move[3:7]).get_pot(int(move[8])).look_at_plant())
            elif move[0] == 'p':
                self._model.plant_plant(move[2:len(move)-7],move[len(move)-6:len(move)-2],move[int(len(move)-1)])
            elif move[0] == 'w' and len(move) == 8:
                self._model.get_rooms().get(move[2:6]).get_pot(int(move[7])).look_at_plant().water_plant()
            elif move[0] == 'n' and len(move) == 1:
                self._model.next(self._applied_items)
                # remove the items in the inventory that have been used
                for index in self._applied_items:
                    if index[2].get_id() == 'W':
                        self._model.get_inventory().remove_entity(WATER)
                    if index[2].get_id() == 'F':
                        self._model.get_inventory().remove_entity(FERTILISER)
                    if index[2].get_id() == 'R':
                        self._model.get_inventory().remove_entity(POSSUM_REPELLENT)
                # clear the information in the list
                self._applied_items.clear()
            elif move[0] == 'a' and len(move) == 10:
                # when input a, add the information to the list in order to apply in the next day
                if move[9] == 'W':
                    self._applied_items.append([move[2:6],int(move[7]),Water()])
                if move[9] == 'F':
                    self._applied_items.append([move[2:6],int(move[7]),Fertiliser()])
                if move[9] == 'R':
                    self._applied_items.append([move[2:6],int(move[7]),PossumRepellent()])

            # Invalid input
            else:
                print(invalid_message(move[0:len(move)+1]))
            
            # Decide if you have won or lost. If one of them is True, end the game.
            if self._model.has_won():
                print(WIN_MESSAGE)
                return 
            elif self._model.has_lost():
                print(LOSS_MESSAGE)
                return
        

# Functions
# provided function
def load_house(filename: str) -> tuple[list[tuple[Room, str]], dict[str, int]]:
    """ Reads a file and creates a dictionary of all the Rooms.
    
    Parameters:
        filename: The path to the file
    
    Return:
        A tuple containing 
            - a list of all Room instances amd their room name,
            - and a dictionary containing plant names and number of plants
    """
    rooms = []
    plants = {}
    items = {}
    room_count = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Room'):
                _, _, room = line.partition(' - ')
                name, room_number = room.split(' ')
                room_number = int(room_number)
                if room_count.get(name) is None:
                    room_count[name] = 0
                room_count[name] += 1
                if ROOM_LAYOUTS.get(name).get('room_type') == 'Room':
                    room = Room(name)
                elif ROOM_LAYOUTS.get(name).get('room_type') == 'OutDoor':
                    room = OutDoor(name)
                rooms.append((room, name[:3] + str(room_count[name])))
                row_index = 0

            elif line.startswith('Plants'):
                _, _, plant_names = line.partition(' - ')
                plant_names = plant_names.split(',')
                for plant in plant_names:
                    plant = plant.split(' ')
                    plants[plant[0]] = int(plant[1])

            elif line.startswith('Items'):
                _, _, item_names = line.partition(' - ')
                item_names = item_names.split(',')
                for item in item_names:
                    item = item.split(' ')
                    items[item[0]] = int(item[1])

            elif len(line) > 0 and len(rooms) > 0:
                pots = line.split(',')
                positions = {}
                for index, pot in enumerate(pots):
                    sun_range, evaporation_rate, plant_name = pot.split('_')
                    pot = Pot()
                    if plant_name != 'None':
                        pot.put_plant(Plant(plant_name))
                    sun_lower, sun_upper = sun_range.split('.')
                    pot.set_evaporation(float(evaporation_rate))
                    pot.set_sun_range((int(sun_lower), int(sun_upper)))
                    positions[index] = pot
                rooms[-1][0].add_pots(positions)
                row_index += 1

    return rooms, plants, items


def main():
    """ Entry-point to gameplay """
    view = View()
    house_file = input('Enter house file: ')
    garden_gnome = GardenSim(house_file, view)
    garden_gnome.play()

if __name__ == '__main__':
    main()
