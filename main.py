from abc import ABC, abstractmethod
import json
import sys
import tkinter as tk
from PIL import Image, ImageTk
import math
import random
import constants

class World(tk.Tk):
    def create_save_button(self):
        save_button = tk.Button(self.master, text="Save Game", command=self.__save_game, bg="#3498db", fg="black", font=("Cascadia Code", 12))
        save_button.place(relx=0.9, rely=0.2, anchor=tk.CENTER)  
        save_button.bind("<Enter>", lambda event, button=save_button: self.__on_enter(button))  # Hover effect
        save_button.bind("<Leave>", lambda event, button=save_button: self.__on_leave(button))  # Hover effect

    def create_new_button(self):
        new_game_button = tk.Button(self.master, text="New Game", command=self.__new_game, bg="#3498db", fg="black", font=("Cascadia Code", 12))
        new_game_button.place(relx=0.9, rely=0.1, anchor=tk.CENTER)
        new_game_button.bind("<Enter>", lambda event, button=new_game_button: self.__on_enter(button))  # Hover effect
        new_game_button.bind("<Leave>", lambda event, button=new_game_button: self.__on_leave(button))  # Hover effect

    def __new_game(self):
        with open("game_state.json", "w") as file:
            file.write("")
        self.master.destroy()        
        main()

    def __save_game(self):
            data = {
                "rows": self.rows,
                "cols": self.cols,
                "size": self.size,
                "humanList": [(human.x, human.y, human.powerCooldown) for human in self.humanList],
                "animals": [(animal.x, animal.y, animal.symbol, animal.strength, animal.initiative) for animal in self.animals],
                "plants": [(plant.x, plant.y, plant.symbol, plant.strength, plant.initiative) for plant in self.plants]
            }
            with open("game_state.json", "w") as file:
                json.dump(data, file)
            print("Game saved successfully")

    def __on_enter(self, button):
        button.config(bg="#2980b9") 

    def __on_leave(self, button):
        button.config(bg="#3498db") 


class PrintRedirector:
    def __init__(self, target):
        self.target = target

    def write(self, message):
        prefixes = ['A', 'An', "Sosnowsky's", 'Human']
        if any(message.startswith(prefix) for prefix in prefixes):
            self.target.insert(tk.END, message + '\n')
            self.target.see(tk.END)  # Scroll to the end

class ConsoleRedirector(tk.Text):
    def __init__(self, master, width=40, height=30, **kwargs):
        tk.Text.__init__(self, master, width=width, height=height, **kwargs)
        self.configure(bg='#3498db', fg='black')

class SquareBoardGUI(World):
    def __init__(self, master, rows, cols, size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.board = [['0' for _ in range(cols)] for _ in range(rows)] 
        self.humanList = []
        self.animals = []
        self.plants = []
        self.canvas_width = size * cols
        self.canvas_height = size * rows
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__on_canvas_click)
        
        self.master.title("s198074")
        self.draw_square_board()
        self.create_save_button()
        self.create_new_button()
        self.console_widget = ConsoleRedirector(master, wrap='word')
        self.__setup_console_widget()

    def __setup_console_widget(self):
        self.console_widget.place(relx=1.0, rely=0.3, anchor=tk.NE)
        sys.stdout = PrintRedirector(self.console_widget)

    def __on_canvas_click(self, event):
        x = event.x
        y = event.y

        col = x // self.size
        row = y // self.size

        self.add_organism_popup(row, col)

    def add_organism_popup(self, row, col):
        popup = tk.Toplevel()
        popup.title("Add Organism")
        
        tk.Label(popup, text="Select organism type:").pack()
        organism_type_var = tk.StringVar()
        organism_type_var.set("Wolf")
        organism_type_dropdown = tk.OptionMenu(popup, organism_type_var, "Wolf", "Sheep", "Fox", "Turtle", "Antelope", "CyberSheep", "Grass", "Guarana", "Belladonna", "SowThistle", "SosnowskysHogweed")
        organism_type_dropdown.pack()

        confirm_button = tk.Button(popup, text="Add Organism", command=lambda: self.add_organism(row, col, organism_type_var.get(), popup))
        confirm_button.pack()

    def add_organism(self, col, row, organism_type, popup):
        if organism_type == "Wolf":
            organism = Wolf(self.board, row, col, strength=9, initiative=5)
            self.animals.append(organism)
        elif organism_type == "Sheep":
            organism = Sheep(self.board, row, col, strength=4, initiative=4)
            self.animals.append(organism)
        elif organism_type == "Fox":
            organism = Fox(self.board, row, col, strength=3, initiative=7, board_gui=self)
            self.animals.append(organism)
        elif organism_type == "Turtle":
            organism = Turtle(self.board, row, col, strength=2, initiative=1)
            self.animals.append(organism)
        elif organism_type == "Antelope":
            organism = Antelope(self.board, row, col, strength=4, initiative=4)
            self.animals.append(organism)
        elif organism_type == "CyberSheep":
            organism = CyberSheep(self.board, row, col, strength=6, initiative=6)
            self.animals.append(organism)
        elif organism_type == "Grass":
            organism = Grass(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "Guarana":
            organism = Guarana(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "Belladonna":
            organism = Belladonna(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "SowThistle":
            organism = SowThistle(self.board, row, col, self)
            self.plants.append(organism)
        elif organism_type == "SosnowskysHogweed":
            organism = SosnowskysHogweed(self.board, row, col)
            self.plants.append(organism)

        self.canvas.delete("all")
        self.draw_square_board()
        
        popup.destroy()

    def draw_square_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.size
                y = row * self.size
                fill_color = 'white'
                self.draw_square(x, y, fill_color)
        for organism in self.humanList:
            self.draw_organism(organism)
        for animal in self.animals:
            self.draw_organism(animal)
        for plant in self.plants:
            self.draw_organism(plant)

    def draw_square(self, x, y, fill_color):
        self.canvas.create_rectangle(x, y, x + self.size, y + self.size, outline='black', fill=fill_color)

    def draw_organism(self, organism):
        x, y = organism.x * self.size + self.size / 2, organism.y * self.size + self.size / 2
     
        if isinstance(organism, Human):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Wolf):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Sheep):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Fox):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Turtle):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Antelope):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, CyberSheep):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, SowThistle):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Grass):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, SosnowskysHogweed):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Belladonna):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Guarana):
            self.canvas.create_image(x, y, image=organism.image_tk)

    def get_square_center(self, row, col):
        x = col * self.size + self.size / 2
        y = row * self.size + self.size / 2
        return x, y

class HexagonalBoardGUI(World):
    def __init__(self, master, rows, cols, size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.board = [['0' for _ in range(cols)] for _ in range(rows)] 
        self.humanList = [] 
        self.animals = []
        self.plants = []
        self.canvas_width = (3/2 * size * cols) + size/2
        self.canvas_height = ((math.sqrt(3)/2 * size) * (2 * rows + 1))
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__on_canvas_click)
        self.master.title("s198074")
        self.draw_hexagonal_board()
        self.create_save_button()
        self.create_new_button()
        self.console_widget = ConsoleRedirector(master, wrap='word')
        self.__setup_console_widget()

    def __setup_console_widget(self):
        self.console_widget.place(relx=1.0, rely=0.3, anchor=tk.NE)
        sys.stdout = PrintRedirector(self.console_widget)


    def __on_canvas_click(self, event):
        x = event.x
        y = event.y
        col = int((x - self.size / 2) / (1.5 * self.size))
        row = int((y - math.sqrt(3) / 2 * self.size * (col % 2)) / (math.sqrt(3) * self.size))
        self.add_organism_popup(row, col)


    def add_organism_popup(self, row, col):
        popup = tk.Toplevel()
        popup.title("Add Organism")
        tk.Label(popup, text="Select organism type:").pack()
        organism_type_var = tk.StringVar()
        organism_type_var.set("Wolf")
        organism_type_dropdown = tk.OptionMenu(popup, organism_type_var, "Wolf", "Sheep", "Fox", "Turtle", "Antelope", "CyberSheep", "Grass", "Guarana", "Belladonna", "SowThistle", "SosnowskysHogweed")
        organism_type_dropdown.pack()
        confirm_button = tk.Button(popup, text="Add Organism", command=lambda: self.add_organism(row, col, organism_type_var.get(), popup))
        confirm_button.pack()

    def add_organism(self, col, row, organism_type, popup):
        if organism_type == "Wolf":
            organism = Wolf(self.board, row, col, strength=9, initiative=5)
            self.animals.append(organism)
        elif organism_type == "Sheep":
            organism = Sheep(self.board, row, col, strength=4, initiative=4)
            self.animals.append(organism)
        elif organism_type == "Fox":
            organism = Fox(self.board, row, col, strength=3, initiative=7, board_gui=self)
            self.animals.append(organism)
        elif organism_type == "Turtle":
            organism = Turtle(self.board, row, col, strength=2, initiative=1)
            self.animals.append(organism)
        elif organism_type == "Antelope":
            organism = Antelope(self.board, row, col, strength=4, initiative=4)
            self.animals.append(organism)
        elif organism_type == "CyberSheep":
            organism = CyberSheep(self.board, row, col, strength=6, initiative=6)
            self.animals.append(organism)
        elif organism_type == "Grass":
            organism = Grass(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "Guarana":
            organism = Guarana(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "Belladonna":
            organism = Belladonna(self.board, row, col)
            self.plants.append(organism)
        elif organism_type == "SowThistle":
            organism = SowThistle(self.board, row, col, self)
            self.plants.append(organism)
        elif organism_type == "SosnowskysHogweed":
            organism = SosnowskysHogweed(self.board, row, col)
            self.plants.append(organism)
        self.canvas.delete("all")
        self.draw_hexagonal_board()
        popup.destroy()

    def draw_hexagonal_board(self):
        radius = self.size / 2
        for row in range(self.rows):
            for col in range(self.cols):
                x = radius + 1.5 * radius * col
                y = radius + math.sqrt(3) * radius * (row + col / 2)
                fill_color = 'white'
                self.draw_hexagon(x, y, radius, fill_color)
        for organism in self.humanList:
            self.draw_organism(organism)
        for animal in self.animals:
            self.draw_organism(animal)
        for plant in self.plants:  
            self.draw_organism(plant)  

    def draw_hexagon(self, x_center, y_center, radius, fill_color):
        points = []
        for i in range(6):
            angle_rad = math.radians(60 * i)
            x = x_center + radius * math.cos(angle_rad)
            y = y_center + radius * math.sin(angle_rad)
            points.append((x, y))

        self.canvas.create_polygon(points, outline='black', fill=fill_color)

    def draw_organism(self, organism):
        x, y = self.get_hex_center(organism.x, organism.y)

        if isinstance(organism, Human):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Wolf):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Sheep):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Fox):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Turtle):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Antelope):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, CyberSheep):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, SowThistle):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Grass):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, SosnowskysHogweed):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Belladonna):
            self.canvas.create_image(x, y, image=organism.image_tk)
        if isinstance(organism, Guarana):
            self.canvas.create_image(x, y, image=organism.image_tk)

    def get_hex_center(self, row, col):
        radius = self.size / 2
        x = radius + 1.5 * radius * col
        y = radius + math.sqrt(3) * radius * (row + col / 2)
        return x, y



class Organism(ABC):
    def __init__(self, board, x, y, symbol, strength, initiative):
        self.board = board 
        self.x = x  
        self.y = y  
        self.symbol = symbol
        self.strength = strength
        self.initiative = initiative

    def move(self, direction=None):
        directions = ['up-left', 'up', 'up-right', 'down-left', 'down', 'down-right']
        direction = random.choice(directions)
        new_x, new_y = self.x, self.y

        if direction == 'up-left':
            new_x, new_y = self.x - 1, self.y - 1
        elif direction == 'up':
            new_x, new_y = self.x - 1, self.y
        elif direction == 'up-right':
            new_x, new_y = self.x - 1, self.y + 1
        elif direction == 'down-left':
            new_x, new_y = self.x + 1, self.y - 1
        elif direction == 'down':
            new_x, new_y = self.x + 1, self.y
        elif direction == 'down-right':
            new_x, new_y = self.x + 1, self.y + 1

        if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]):
            self.board[self.x][self.y] = '0'
            self.x, self.y = new_x, new_y
            self.board[self.x][self.y] = self.symbol


class Plant(Organism):
    def __init__(self, board, x, y, symbol, strength, initiative=constants.PLANTS_INITIATIVE):
        super().__init__(board, x, y, symbol, strength, initiative)

    def move(self, direction=None):
        pass

class Grass(Plant):
    def __init__(self, board, x, y):
        super().__init__(board, x, y, 'G', strength=constants.GRASS_STRENGTH)
        self.image = Image.open("grass.png")
        new_width = int(self.image.width * 0.06)
        new_height = int(self.image.height * 0.06)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

class SowThistle(Plant):
    def __init__(self, board, x, y, board_gui):
        super().__init__(board, x, y, 'E', strength=constants.SOW_STRENGTH)
        self.image = Image.open("sow.png")
        new_width = int(self.image.width * 0.07)
        new_height = int(self.image.height * 0.07)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 
        self.board_gui = board_gui 

    def spread(self, board_gui):
        available_spots = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_x = self.x + dx
                new_y = self.y + dy
                if (dx != 0 or dy != 0) and 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]) and self.board[new_x][new_y] == '0':
                    available_spots.append((new_x, new_y))

        if random.random() < constants.CHANCE_TO_SPREAD and available_spots:
            new_x, new_y = random.choice(available_spots)
            if self.board[new_x][new_y] == '0':
                new_plant = SowThistle(self.board, new_x, new_y, board_gui)
                self.board[new_x][new_y] = self.symbol
                board_gui.plants.append(new_plant)


class Guarana(Plant):
    def __init__(self, board, x, y):
        super().__init__(board, x, y, 'U', strength=constants.GUARANA_STRENGTH)
        self.image = Image.open("guarana.png") 
        new_width = int(self.image.width * 0.12)
        new_height = int(self.image.height * 0.12)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

class Belladonna(Plant):
    def __init__(self, board, x, y):
        super().__init__(board, x, y, 'B', strength=constants.BELLADONA_STRENGTH)
        self.image = Image.open("belladona.png")
        new_width = int(self.image.width * 0.08)
        new_height = int(self.image.height * 0.08)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

class SosnowskysHogweed(Plant):
    def __init__(self, board, x, y):
        super().__init__(board, x, y, '#', strength=constants.SOSNOWSKY_STRENGTH)
        self.image = Image.open("sosnowsky.png")
        new_width = int(self.image.width * 0.3)
        new_height = int(self.image.height * 0.3)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 



class Human(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'H', strength, initiative)
        self.image = Image.open("human.png")
        new_width = int(self.image.width * 0.2)
        new_height = int(self.image.height * 0.2)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 
        self.powerCooldown = 0

    def move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == 'power':
            if self.powerCooldown == 0:
                self.powerCooldown = 5
                self.strength += 5
                print("Human activated Magic Potion!")
                return
            else:
                print("Human's cooldown for Magic Potion hasn't ended yet! Make a move!")
        if BOARD_TYPE == "Hexagonal":
            if direction == 'up-left': #Q 
                new_x, new_y = self.x , self.y - 1
            elif direction == 'up': #W
                new_x, new_y = self.x - 1, self.y
            elif direction == 'up-right': #E
                new_x, new_y = self.x -1 , self.y + 1
            elif direction == 'down-left': #A
                new_x, new_y = self.x + 1, self.y - 1
            elif direction == 'down': #S
                new_x, new_y = self.x + 1, self.y
            elif direction == 'down-right': #D
                new_x, new_y = self.x, self.y + 1
        elif BOARD_TYPE == "Square":
            if direction == 'up': #W
                new_x, new_y = self.x, self.y - 1
            elif direction == 'down-left': #A
                new_x, new_y = self.x - 1, self.y
            elif direction == 'down': #S
                new_x, new_y = self.x, self.y + 1
            elif direction == 'down-right': #D
                new_x, new_y = self.x + 1, self.y
        if self.powerCooldown != 0:
            self.powerCooldown -= 1
        if not (0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0])):
            return
        self.board[self.x][self.y] = '0'
        self.x, self.y = new_x, new_y
        self.board[self.x][self.y] = self.symbol


class Wolf(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'W', strength, initiative) 
        self.image = Image.open("wolf.png")  
        new_width = int(self.image.width * 0.04)
        new_height = int(self.image.height * 0.04)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 
 
    def move(self, direction=None):
        super().move(direction)


class Sheep(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'S', strength, initiative) 
        self.image = Image.open("sheep.png") 
        new_width = int(self.image.width * 0.035)
        new_height = int(self.image.height * 0.035)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

    def move(self, direction=None):
        super().move(direction)


class Fox(Organism):
    def __init__(self, board, x, y, strength, initiative, board_gui):
        super().__init__(board, x, y, 'F', strength, initiative)
        self.board_gui = board_gui
        self.image = Image.open("fox.png")
        new_width = int(self.image.width * 0.035)
        new_height = int(self.image.height * 0.035)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 
 
    def move(self, direction=None):
        directions = ['up-left', 'up', 'up-right', 'down-left', 'down', 'down-right']
        direction = random.choice(directions)
        new_x, new_y = self.x, self.y

        if direction == 'up-left': #works 
            new_x, new_y = self.x , self.y - 1
        elif direction == 'up': #works
            new_x, new_y = self.x - 1, self.y
        elif direction == 'up-right': #works
            new_x, new_y = self.x -1 , self.y + 1
        elif direction == 'down-left': #works
            new_x, new_y = self.x + 1, self.y - 1
        elif direction == 'down': #works
            new_x, new_y = self.x + 1, self.y
        elif direction == 'down-right': #works
            new_x, new_y = self.x, self.y + 1

        # Check if the new position is within the bounds of the board
        if not (0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0])):
            return
        
        # Check if the new position is occupied by a stronger organism
        if any(isinstance(org, Organism) and org.x == new_x and org.y == new_y and org.strength > self.strength for org in self.board_gui.humanList + self.board_gui.animals):
            return
        self.board[self.x][self.y] = '0'
        self.x, self.y = new_x, new_y
        self.board[self.x][self.y] = self.symbol


class Turtle(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'T', strength, initiative)
        self.image = Image.open("turtle.png")
        new_width = int(self.image.width * 0.035)
        new_height = int(self.image.height * 0.035)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

    def move(self, direction=None):
        if random.random() < 0.75:
            return
        super().move(direction)

class Antelope(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'A', strength, initiative)   
        self.image = Image.open("antelope.png") 
        new_width = int(self.image.width * 0.3)
        new_height = int(self.image.height * 0.3)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image)  

    def move(self, direction=None):
        directions = ['up-left', 'up', 'up-right', 'down-left', 'down', 'down-right']
        direction = random.choice(directions)
        new_x, new_y = self.x, self.y
        if direction == 'up-left': #works 
            new_x, new_y = self.x , self.y - 2
        elif direction == 'up': #works
            new_x, new_y = self.x - 2, self.y
        elif direction == 'up-right': #works
            new_x, new_y = self.x -2 , self.y + 2
        elif direction == 'down-left': #works
            new_x, new_y = self.x + 2, self.y - 2
        elif direction == 'down': #works
            new_x, new_y = self.x + 2, self.y
        elif direction == 'down-right': #works
            new_x, new_y = self.x, self.y + 2

        # Check if the new position is within the bounds of the board
        if not (0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0])):
            return  
        self.board[self.x][self.y] = '0'
        self.x, self.y = new_x, new_y
        self.board[self.x][self.y] = self.symbol

class CyberSheep(Organism):
    def __init__(self, board, x, y, strength, initiative):
        super().__init__(board, x, y, 'C', strength, initiative) 
        self.image = Image.open("cyber.png")  
        new_width = int(self.image.width * 0.015)
        new_height = int(self.image.height * 0.015)
        self.image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(self.image) 

    def move(self, direction=None):
        target_x, target_y = constants.SOSNOWSKY_X, constants.SOSNOWSKY_Y
        new_x, new_y = self.x, self.y

        if target_x < self.x:
            new_x -= 1
        elif target_x > self.x:
            new_x += 1

        if target_y < self.y:
            new_y -= 1
        elif target_y > self.y:
            new_y += 1

        # Sprawdź, czy nowa pozycja jest w granicach planszy
        if not (0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0])):
            return 
        self.board[self.x][self.y] = '0'
        self.x, self.y = new_x, new_y
        self.board[self.x][self.y] = self.symbol


def load_game(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            if not data:
                return None
            else:
                return json.loads(data)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
        return None

def choose_board_type():
    def set_board_type(board_type):
        global BOARD_TYPE
        BOARD_TYPE = board_type
        root.destroy()

    root = tk.Tk()
    root.title("Choose Board Type")
    root.configure(bg="#f0f0f0") 
    font_style = ("Cascadia Code", 12)

    label = tk.Label(root, text="Choose Board Type:", padx=20, pady=10, font=("Cascadia Code", 14, "bold"), bg="#f0f0f0")
    label.pack()

    button_hexagonal = tk.Button(root, text="Hexagonal", padx=20, pady=10, command=lambda: set_board_type("Hexagonal"), font=font_style)
    button_hexagonal.pack()

    button_square = tk.Button(root, text="Square", padx=20, pady=10, command=lambda: set_board_type("Square"), font=font_style)
    button_square.pack()
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

    root.wait_window() 

def main():
    root = tk.Tk()
    choose_board_type()
    print("Selected board type:", BOARD_TYPE)
    
    saved_game = load_game("game_state.json")

    if saved_game:
        if BOARD_TYPE == "Hexagonal":
            board_gui = HexagonalBoardGUI(root, saved_game["rows"], saved_game["cols"], saved_game["size"])
        elif BOARD_TYPE == "Square":
            board_gui = SquareBoardGUI(root, saved_game["rows"], saved_game["cols"], saved_game["size"])
        for x, y, powerCooldown in saved_game["humanList"]:
            human = Human(board_gui.board, x, y, strength=5, initiative=4)
            human.powerCooldown = powerCooldown
            board_gui.humanList.append(human)
        for x, y, symbol, strength, initiative in saved_game["animals"]:
            if symbol == 'W':
                animal = Wolf(board_gui.board, x, y, strength, initiative)
            elif symbol == 'S':
                animal = Sheep(board_gui.board, x, y, strength, initiative)
            elif symbol == 'F':
                animal = Fox(board_gui.board, x, y, strength, initiative, board_gui)
            elif symbol == 'T':
                animal = Turtle(board_gui.board, x, y, strength, initiative)
            elif symbol == 'A':
                animal = Antelope(board_gui.board, x, y, strength, initiative)
            elif symbol == 'C':
                animal = CyberSheep(board_gui.board, x, y, strength, initiative)
            else:
                continue
            board_gui.animals.append(animal)
        for x, y, symbol, strength, initiative in saved_game["plants"]:
            if symbol == 'G':
                plant = Grass(board_gui.board, x, y)
            elif symbol == 'U':
                plant = Guarana(board_gui.board, x, y)
            elif symbol == 'B':
                plant = Belladonna(board_gui.board, x, y)
            elif symbol == 'E':
                plant = SowThistle(board_gui.board, x, y, board_gui)
            elif symbol == '#':
                plant = SosnowskysHogweed(board_gui.board, x, y)
            else:
                continue
            board_gui.plants.append(plant)

        board_gui.animals = sorted(board_gui.animals, key=lambda animal: animal.initiative, reverse=True)
    else:
        if BOARD_TYPE == "Hexagonal":
            board_gui = HexagonalBoardGUI(root, rows=constants.BOARD_HEIGHT, cols=constants.BOARD_WIDTH, size=constants.CELL_SIZE)
        elif BOARD_TYPE == "Square":
            board_gui = SquareBoardGUI(root, rows=constants.BOARD_HEIGHT, cols=constants.BOARD_WIDTH, size=constants.CELL_SIZE)
        
        #HUMAN
        human = Human(board_gui.board, x=13, y=13, strength=constants.HUMAN_STRENGTH, initiative=constants.HUMAN_INITIATIVE)
        board_gui.humanList.append(human)
        #ANIMALS
        board_gui.animals.append(Wolf(board_gui.board, x=3, y=3, strength=constants.WOLF_STRENGTH, initiative=constants.WOLF_INITIATIVE))
        board_gui.animals.append(Wolf(board_gui.board, x=3, y=4, strength=constants.WOLF_STRENGTH, initiative=constants.WOLF_INITIATIVE))
        board_gui.animals.append(Sheep(board_gui.board, x=7, y=7, strength=constants.SHEEP_STRENGTH, initiative=constants.SHEEP_INITIATIVE))
        board_gui.animals.append(Sheep(board_gui.board, x=7, y=10, strength=constants.SHEEP_STRENGTH, initiative=constants.SHEEP_INITIATIVE))
        board_gui.animals.append(Fox(board_gui.board, x=9, y=9, strength=constants.FOX_STRENGTH, initiative=constants.FOX_INITIATIVE, board_gui=board_gui))
        board_gui.animals.append(Fox(board_gui.board, x=9, y=12, strength=constants.FOX_STRENGTH, initiative=constants.FOX_INITIATIVE, board_gui=board_gui))
        board_gui.animals.append(Turtle(board_gui.board, x=11, y=11, strength=constants.TURTLE_STRENGTH, initiative=constants.TURTLE_INITIATIVE))
        board_gui.animals.append(Turtle(board_gui.board, x=11, y=17, strength=constants.TURTLE_STRENGTH, initiative=constants.TURTLE_INITIATIVE))
        board_gui.animals.append(Antelope(board_gui.board, x=13, y=13, strength=constants.ANTELOPE_STRENGTH, initiative=constants.ANTELOPE_INITIATIVE))
        board_gui.animals.append(Antelope(board_gui.board, x=13, y=10, strength=constants.ANTELOPE_STRENGTH, initiative=constants.ANTELOPE_INITIATIVE))
        board_gui.animals.append(CyberSheep(board_gui.board, x=12, y=3, strength=constants.CYBER_STRENGTH, initiative=constants.CYBER_INITIATIVE))
        board_gui.animals = sorted(board_gui.animals, key=lambda animal: animal.initiative, reverse=True)
        #PLANTS
        board_gui.plants.append(Grass(board_gui.board, x=6, y=6))
        board_gui.plants.append(Guarana(board_gui.board, x=7, y=7))
        board_gui.plants.append(Belladonna(board_gui.board, x=8, y=8))
        board_gui.plants.append(SowThistle(board_gui.board, x=4, y=6, board_gui=board_gui))
        board_gui.plants.append(SosnowskysHogweed(board_gui.board, x=15, y=15))


    def move_animals():
        human_alive = any(isinstance(org, Human) for org in board_gui.humanList)

        if not human_alive:
            game_over_frame = tk.Frame(root, bg="black")
            game_over_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            game_over_label = tk.Label(game_over_frame, text="GAME OVER", font=("Helvetica", 24), fg="red", bg="black")
            game_over_label.pack()
            return

        for animal in board_gui.animals:
            animal.move()

        for plant in board_gui.plants:
            if isinstance(plant, SowThistle):
                plant.spread(board_gui)
        
        #ANIMALS VS HUMAN
        for animal in board_gui.animals[:]:
            for organism in board_gui.humanList[:]:
                if animal.x == organism.x and animal.y == organism.y:  
                    if animal.strength >= organism.strength: 
                        print(f"An animal killed a human at ({animal.x}, {animal.y}).")
                        board_gui.humanList.remove(organism)  
                    else:
                        print(f"A human killed an animal at ({organism.x}, {organism.y}).")
                        board_gui.animals.remove(animal)  
                    break 

        #ANIMALS VS ANIMALS
        for animal1 in board_gui.animals[:]:
            for animal2 in board_gui.animals[:]:
                if animal1 != animal2 and animal1.x == animal2.x and animal1.y == animal2.y:
                    if type(animal1) == type(animal2):
                        if random.random() <= constants.CHANCE_TO_BREED:
                            available_spots = []
                            for x in range(len(board_gui.board)):
                                for y in range(len(board_gui.board[0])):
                                    if board_gui.board[x][y] == '0':
                                        available_spots.append((x, y))
                            if available_spots:
                                new_x, new_y = random.choice(available_spots)
                                new_animal = type(animal1)(board_gui.board, new_x, new_y, animal1.strength, animal1.initiative)
                                board_gui.animals.append(new_animal)
                    elif animal1.strength >= animal2.strength:
                        print(f"An animal killed another animal at ({animal1.x}, {animal1.y}).")
                        board_gui.animals.remove(animal2)
                    else:
                        print(f"An animal killed another animal at ({animal2.x}, {animal2.y}).")
                        board_gui.animals.remove(animal1)
                    break

        #ANIMALS VS PLANTS
        for animal in board_gui.animals[:]:
            for plant in board_gui.plants[:]:
                if animal.x == plant.x and animal.y == plant.y:  
                    if isinstance(plant, Guarana): 
                        animal.strength += 3  
                        board_gui.plants.remove(plant)
                        print(f"An animal consumed a power-up at ({animal.x}, {animal.y}).")
                    elif isinstance(animal, CyberSheep) and isinstance(plant, SosnowskysHogweed): 
                        board_gui.plants.remove(plant)
                        print(f"A Cybersheep found Sosnowsky's Hogweed at ({animal.x}, {animal.y}).")
                    else:
                        if animal.strength >= plant.strength:  
                            print(f"An animal killed a plant at ({animal.x}, {animal.y}).")
                            board_gui.plants.remove(plant) 
                        else:
                            print(f"A plant killed an animal at ({plant.x}, {plant.y}).")
                            board_gui.animals.remove(animal) 
                    break 

        #PLANTS VS HUMAN
        for plant in board_gui.plants[:]:
            for human in board_gui.humanList[:]:
                if plant.x == human.x and plant.y == human.y:
                    if isinstance(plant, Guarana):
                        human.strength += 3
                        board_gui.plants.remove(plant)
                        print(f"A human consumed a power-up at ({human.x}, {human.y}).")
                    else:
                        if human.strength >= plant.strength: 
                            print(f"A human killed a plant at ({human.x}, {human.y}).")
                            board_gui.plants.remove(plant) 
                        else:
                            print(f"A plant killed a human at ({plant.x}, {plant.y}).")
                            board_gui.humanList.remove(human) 
                    break 

        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1), 
                            (0, -1),          (0, 1),
                            (1, -1), (1, 0), (1, 1)]

        # SOSNOWSKY KILLING NEIGHBORS
        for plant in board_gui.plants[:]:
            if isinstance(plant, SosnowskysHogweed):
                for offset in neighbor_offsets:
                    neighbor_x, neighbor_y = plant.x + offset[0], plant.y + offset[1]
                    for animal in board_gui.animals[:]:
                        if animal.x == neighbor_x and animal.y == neighbor_y and not isinstance(animal, CyberSheep):
                            print(f"Sosnowsky's Hogweed killed an animal at ({animal.x}, {animal.y}).")
                            board_gui.animals.remove(animal)
                    for human in board_gui.humanList[:]:
                        if human.x == neighbor_x and human.y == neighbor_y:
                            print(f"Sosnowsky's Hogweed killed a human at ({human.x}, {human.y}).")
                            board_gui.humanList.remove(human)

        # PLANTS VS PLANTS (FOR SPREADING)
        for plant1 in board_gui.plants[:]:
            for plant2 in board_gui.plants[:]:
                if plant1 != plant2 and plant1.x == plant2.x and plant1.y == plant2.y:
                    if plant1.strength >= plant2.strength:
                        print(f"A plant killed another plant at ({plant1.x}, {plant1.y}).")
                        board_gui.plants.remove(plant2)
                    else:
                        print(f"A plant killed another plant at ({plant2.x}, {plant2.y}).")
                        board_gui.plants.remove(plant1)
                    break

        board_gui.canvas.delete("all")
        if BOARD_TYPE == "Hexagonal":
            board_gui.draw_hexagonal_board()
        elif BOARD_TYPE == "Square":
            board_gui.draw_square_board()
        board_gui.draw_organism(human)
        for animal in board_gui.animals:
            board_gui.draw_organism(animal)
        for plant in board_gui.plants:
            board_gui.draw_organism(plant)

    def move_human(event):
        key = event.keysym
        directions = {'q': 'up-left', 'w': 'up', 'e': 'up-right', 'a': 'down-left', 's': 'down', 'd': 'down-right', 'p': 'power'}
        if key in directions:
            human.move(directions[key])
            move_animals()

    root.bind('<Key>', move_human)
    root.mainloop()

if __name__ == "__main__":
    main()


