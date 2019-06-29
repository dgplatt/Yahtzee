from tkinter import *
import tkinter
from tkinter import messagebox
import random as rm
import os
from pathlib import Path
import math

path  = os.path.dirname(os.path.abspath(__file__))
score_labels = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'
            , '3 of a kind', '4 of a kind', 'Sm Straight'
            , 'Lg Straight', 'Full House', 'Yahzee', 'Chance']

def start():
    root = Tk()
    root.title("Yahzee")
    lbl = Label(root, text="How many players?")
    lbl.pack()
    def click(players):
        root.destroy()
        yahzee = game(players)
        yahzee.yahzee()
    two = Button(root, text="2", width=8, command=lambda: click(2))
    two.pack()
    three = Button(root, text="3", width=8, command=lambda: click(3))
    three.pack()
    four = Button(root, text="4", width=8, command=lambda: click(4))
    four.pack()
    root.geometry('200x100')
    root.mainloop()

class game:
    def __init__(self, players):
        self.players = players
        self.board = [[None]*13 for i in range(players)]
        self.dice_list, self.dice_nums = [], [0] *5

        self.window = None
        self.board_labels = [[None]*14 for i in range(players)]
        self.dice_label, self.player_label = None, None
        self.buttons, self.dice_buttons, self.dice_list  = [], [], []
        self.photos = [None] *6

        self.done_button, self.roll_button = None, None
        self.player = 0
        self.num_rolls = 3
        self.to_score = None #number representing the type of scoring chossen
        self.make_window()

    def expected_number(self, i):
        p = self.dice_nums.count(i)
        expected_num = 0
        for x in range(6 - p):
            prob = 0
            if (self.num_rolls ==2):
                for y in range(x + 1):
                    l = math.factorial(5 - p)/(math.factorial(y)* math.factorial(5 - (p + y)))
                    k = math.factorial(5 - (p + y))/(math.factorial(x - y)* math.factorial(5 - (p + x)))
                    prob += l * k * (5/6)**((5 - (p + y))+(5 - (p + x)))*(1/6)**(x)
            else:
                l = math.factorial(5 - p)/(math.factorial(x)* math.factorial(5 - (p + x)))
                prob += l * (5/6)**(5 - (p + x))*(1/6)**(x)
            expected_num += prob * (p + x)
        return expected_num * i

        expected_num = 0
        for x in range(6):
            prob = 0
            for y in range(x + 1):
                for z in range(x + 1 - y):
                    l = math.factorial(5)/(math.factorial(y)* math.factorial(5 - y))
                    k = math.factorial(5 - y)/(math.factorial(z)* math.factorial(5 - (y + z)))
                    p = math.factorial(5 - (y + z))/(math.factorial(x - (y + z))* math.factorial(5 - x))
                    prob += l * k * p * (5/6)**((5 - y)+(5 - (y + z))+ (5 - x))*(1/6)**(x)
            expected_num += prob * x
        return expected_num * i

    def expected_3_of_a_kind(self, i):
        ex_list = []
        p = self.dice_nums.count(i)
        x = 3 - p
        max_not_i, max2_not_i = 0, 0
        for j in range(len(self.dice_nums)):
            if (self.dice_nums[j] != i and self.dice_nums[j] > max_not_i):
                max2_not_i = max_not_i
                max_not_i = self.dice_nums[j]
        if(max_not_i == 0):
            max_not_i = i 
        if(max2_not_i == 0):
            max2_not_i = i
        if (max_not_i < max2_not_i):
            temp = max2_not_i
            max2_not_i = max_not_i
            max_not_i = temp
        if (self.num_rolls == 2 and p < 3):
            for z in range(3):
                prob = 0
                for y in range(x + 1):
                    l = math.factorial(5 - (p + z))/(math.factorial(x - y)* math.factorial(5 - (p + z + x - y)))
                    k = math.factorial(5 - (p + z + x - y))/(math.factorial(y)* math.factorial(5 - (p + z + x)))
                    prob += l * k * (5/6)**(5 - (p + z + x - y))*(1/6)**(x)
                if (z == 0):
                    ex_list.append(prob * (3*i +7))
                elif(z == 1):
                    ex_list.append(prob * (3*i + 3.5 + max_not_i))
                else:
                    ex_list.append(prob * (3*i + max2_not_i + max_not_i))
        elif(self.num_rolls == 1 and p < 3):
            for z in range(3):
                l = math.factorial(5 - (p + z))/(math.factorial(x)* math.factorial(5 - (p  + z + x)))
                prob = l*(1/6)**(x)
                if (z == 0):
                    ex_list.append(prob * (3*i +7))
                elif(z == 1):
                    ex_list.append(prob * (3*i +3.5 + max_not_i))
                else:
                    ex_list.append(prob * (3*i + max2_not_i + max_not_i))
        elif(p >= 3):
            if (self.num_rolls ==2):
                exp = (1/12) + 2*(1/12) + 3*(1/12) + 4*(1/4) + 5*(1/4) + 6*(1/4)
            else:
                exp = 3.5
            ex_list.append(3*i + 2*exp)
            ex_list.append(3*i + exp + max_not_i)
            ex_list.append(3*i + max2_not_i + max_not_i)
        return [max(ex_list), ex_list.index(max(ex_list))]

    def expected_4_of_a_kind(self, i):
        ex_list = []
        p = self.dice_nums.count(i)
        x = 4 - p
        max_not_i = 0
        for j in range(len(self.dice_nums)):
            if (self.dice_nums[j] != i and self.dice_nums[j] > max_not_i):
                max_not_i = self.dice_nums[j]
        if(max_not_i == 0):
            max_not_i = i
        if (self.num_rolls == 2 and p < 4):
            for z in range(2):
                prob = 0
                for y in range(x + 1):
                    l = math.factorial(5 - (p + z))/(math.factorial(x - y)* math.factorial(5 - (p + z + x - y)))
                    k = math.factorial(5 - (p + z + x - y))/(math.factorial(y)* math.factorial(5 - (p + z + x)))
                    prob += l * k * (5/6)**(5 - (p + z + x - y))*(1/6)**(x)
                if (z == 0):
                    ex_list.append(prob * (4*i +3.5))
                else:
                    ex_list.append(prob * (4*i + max_not_i))
        elif(self.num_rolls == 1 and p < 4):
            for z in range(2):
                l = math.factorial(5 - (p + z))/(math.factorial(x)* math.factorial(5 - (p  + z + x)))
                prob = l *(1/6)**(x)
                if (z == 0):
                    ex_list.append(prob * (4*i + 3.5))
                else:
                    ex_list.append(prob * (4*i + max_not_i))
        elif(p >= 4):
            if(self.num_rolls ==2):
                exp = (1/12) + 2*(1/12) + 3*(1/12) + 4*(1/4) + 5*(1/4) + 6*(1/4)
            else:
                exp = 3.5
            ex_list.append(4*i + exp)
            ex_list.append(4*i + max_not_i)
        return [max(ex_list), ex_list.index(max(ex_list))]

    def expected_straight(self, i):
        min_changes = 6
        min_start = 0
        for num in self.dice_nums:
            start = num
            changes = 0
            for j in range(1,i):
                if (num + j not in self.dice_nums):
                    changes += 1
            if(changes < min_changes):
                min_changes = changes
                min_start = start
        prob = 0
        if(self.num_rolls == 2):
            for x in range (min_changes):
                prob += math.factorial(min_changes + 5 - i) * ((6 - (min_changes + x))/6)**(min_changes - x + (5 - i))*(1/6)**(min_changes)
            if (min_changes == 0):
                prob = 1
        else:
            prob = math.factorial(min_changes + 5 - i)*(1/6)**(min_changes)
        return [10*(i-1)*prob, min_start]

    def expected_full_house(self):
        ex_list = []
        index_list = []
        for i in range(1,6):
            n = min(self.dice_nums.count(i), 3)
            for j in range(i + 1,7):
                m = min(self.dice_nums.count(j), 3)
                prob = 0
                for x in range(4-n):
                    for y in range(4 - m - (n+x)//3):
                        l = math.factorial(5 - n - m)/(math.factorial(x)*math.factorial(5 - (n + x) - m))
                        k = math.factorial(5 - (n + x) - m)/(math.factorial(y)*math.factorial(5 - (n + x) - (m + y)))
                        if(x + n < 3 and y + m < 3):
                            l_3 = math.factorial(5 - (n + x) - (m + y))/(math.factorial(2 - (m + y))*math.factorial(3 - (n + x)))
                            k_3 = math.factorial(5 - (n + x) - (m + y))/(math.factorial(2 - (n + x))*math.factorial(3 - (m + y)))
                        else:
                            l_3 = int(x + n == 3)
                            k_3 = int(y + m == 3)
                        prob += l*k*(l_3 + k_3)*(1/6)**(5 - n - m)*(4/6)**(5 - (n + x) - (m + y))
                ex_list.append(prob*25)
                index_list.append([i,j])
        ex_list = ex_list[::-1]
        index_list = index_list[::-1]
        index = ex_list.index(max(ex_list))
        return(max(ex_list), index_list[index])

    def expected_yahzee(self, i):
        if (self.board[self.player][11] != None):
            result = 100
        else:
            result = 50
        p = self.dice_nums.count(i)
        prob = 0
        if (self.num_rolls == 2):
            for x in range(5 - p + 1):
                l = math.factorial(5 - p)/(math.factorial(x)* math.factorial(5 - (p + x)))
                prob += l * (5/6)**(5 - (p + x))*(1/6)**(5 - p)
        else:
            prob = (1/6)**(5 - p)
        return prob * result

    def max_optimal(self,list):
        list_x = [list[i][0] for i in range(len(list))]
        return(list[list_x.index(max(list_x))])

    def optimal(self):
        #Find probablity of each solution given dice
        #Find score of possible solution that can be chosen for certain if fails
        max_values  = [5, 10, 15, 20, 25, 30, 30, 30, 30, 40, 25, 50, 30]
        possibilities = []
        for i in range(1,7):
            if(self.board[self.player][i - 1] == None):
                possibilities.append([(self.expected_number(i))/max_values[i - 1], str(i) + "s"])

        if(self.board[self.player][6] == None):
            for i in range(1, 7):
                possibilities.append([(self.expected_3_of_a_kind(i)[0])/max_values[6],
                                         "3_of_a_kind: " + str(i) + "s with " + str(self.expected_3_of_a_kind(i)[1]) + " constant"])

        if(self.board[self.player][7] == None):
            for i in range(1, 7):
                possibilities.append([(self.expected_4_of_a_kind(i)[0])/max_values[7],
                                         "4_of_a_kind: " + str(i) + "s with " + str(self.expected_4_of_a_kind(i)[1]) + " constant"])

        if(self.board[self.player][8] == None):
            possibilities.append([(self.expected_straight(4)[0])/max_values[8],
                                    "Small Straight starting at " + str(self.expected_straight(4)[1])])

        if(self.board[self.player][9] == None):
            possibilities.append([(self.expected_straight(5)[0])/max_values[9],
                                    "large Straight starting at " + str(self.expected_straight(5)[1])])

        if(self.board[self.player][10] == None):
            possibilities.append([(self.expected_full_house()[0])/max_values[10],
                                    "Full House index "  + str(self.expected_full_house()[1])])

        if(self.board[self.player][11] == None or self.board[self.player][11] != 0):
            for i in range(1,7):
                possibilities.append([(self.expected_yahzee(i))/max_values[11], "Yahtzee of " + str(i) + "s"])

        if(self.board[self.player][12] == None):
            possibilities.append([sum(self.dice_nums)/max_values[12], "Chance"])

        return self.max_optimal(possibilities[::-1])[1]

    def yahzee(self):
        self.window.mainloop()

    def new_game(self):
        self.window.destroy()
        start()

    def next_roll(self):
        self.num_rolls -= 1
        return self.num_rolls
    
    def end_game(self):
        totals  = [0]*self.players
        string = ''
        for i in range(self.players):
            totals[i] = sum(self.board[i])
            if (sum(self.board[i][:6]) > 62):
                totals[i] += 35
            string += "Player " + str(i+1) + ": " + str(totals[i]) + "\n"
        string += " \n PLAYER " + str(totals.index(max(totals)) + 1) + " WINS!!!"
        messagebox.showinfo("Yahtzee", string)
        if (messagebox.askyesno ("Yahtzee", "Start a new game?")):
            self.new_game()
        else:
            self.window.destroy()
            
    def no_more_spaces(self):
        return not None in self.board[self.player]

    def next_player(self):
        self.roll_button.config(state = NORMAL)
        self.done_button.config(state = DISABLED)
        self.num_rolls = 3
        for i in range(len(self.buttons)):
            self.buttons[i].config(state = NORMAL)

        self.player = (self.player + 1) % self.players
        self.player_label.config(text = "player " + str(self.player+1))
        for i in range(len(self.buttons)):
            if (self.board[self.player][i] != None and i != 11):
                self.buttons[i].config(state = DISABLED)
    
    def update_dice(self):
        for i in range(5):
            self.dice_buttons[i].config(image=self.photos[self.dice_nums[i] - 1])
    
    def update_score(self):
        self.board_labels[self.player][self.to_score].config(text = str(self.board[self.player][self.to_score]))

    def roll(self):
        if(self.num_rolls == 3):
            self.done_button.config(state = NORMAL)
            for i in range(5):
                self.dice_nums[i] = rm.randint(1, 6)
        elif(len(self.dice_list) == 0):
            return
        else:
            for i in self.dice_list:
                self.dice_nums[i] = rm.randint(1, 6)
                self.dice_buttons[i].config(text = '')
        self.dice_list = []
        self.update_dice()
        if (self.next_roll() == 0):
            self.roll_button.config(state = DISABLED)
        if(self.num_rolls > 0):
            print(self.optimal())

    def select(self,i):
        if(i in self.dice_list):
            self.dice_buttons[i].config(text = '')
            self.dice_list.remove(i)
        elif(self.num_rolls < 3):
            self.dice_buttons[i].config(text = "x", compound=CENTER, font = ("Helvetica",100))
            self.dice_list.append(i)
 
    def find_of_a_kind(self, i):
        for num in set(self.dice_nums):
            if (self.dice_nums.count(num) > i - 1):
                return True
        return False

    def find_straight(self, i):
        for num in self.dice_nums:
            for j in range(1,i + 1):
                if (num + j not in self.dice_nums):
                    break
            if(j == i):
                return True
        return False  

    def find_full_house(self):
        return len(list(set(self.dice_nums))) == 2
     
    def find_yahtzee(self):
        return self.dice_nums.count(self.dice_nums[0]) == 5

    def error(self):
        return messagebox.askyesno ("Yahtzee", "This is not a " + score_labels[self.to_score]  + ".\n End your turn anyways?")

    def choose(self, i):
        if(self.to_score == None):
            self.to_score = i
            self.buttons[i].config(text = "** " + score_labels[i] + " **")
        elif(i == self.to_score):
            self.to_score = None
            self.buttons[i].config(text = score_labels[i])
        else:
            self.buttons[self.to_score].config(text = score_labels[self.to_score])
            self.to_score = i
            self.buttons[i].config(text = "** " + score_labels[i] + " **")
    
    def done(self):
        self.dice_list = []
        for i in range(5):
            self.dice_buttons[i].config(text = '')
        if(self.to_score == None):
            return
        i = self.to_score
        self.buttons[i].config(text = score_labels[i])
        if(i < 6):
            self.board[self.player][i] = self.dice_nums.count(i+1) * (i+1)
        elif (i < 8):
            if (not self.find_of_a_kind(i - 3)):
                if (self.error()):
                    self.board[self.player][i] = 0
                else:
                    return
            else:
                self.board[self.player][i] = sum(self.dice_nums) 
        elif(i < 10):
            if (not self.find_straight(i - 4)):
                if (self.error()):
                    self.board[self.player][i] = 0
                else:
                    return
            else:
                self.board[self.player][i] = (i - 5)*10
        elif(i == 10):
            if (not self.find_full_house()):
                if (self.error()):
                    self.board[self.player][i] = 0
                else:
                    return
            else:
                self.board[self.player][i] = 25
        elif(i == 11):
            if (not self.find_yahtzee() and self.board[self.player][i] == None):
                if (self.error()):
                    self.board[self.player][i] = 0
                else:
                    return
            elif(not self.find_yahtzee()):
                return
            elif(self.board[self.player][i] != None):
                self.board[self.player][i] += 100
            else:
                self.board[self.player][i] = 50
        else:
            self.board[self.player][i] = sum(self.dice_nums)
        self.update_score()
        self.to_score = None
        self.next_player()
        for i in range(self.players):
            if (self.no_more_spaces()):
                self.next_player()
            else:
                return
        self.end_game()

    def make_window(self):
        self.window = Tk()
        self.window.title("Yahzee")
        menu = Menu(self.window)
        self.window.config(menu=menu)
        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Optimize", command=self.window.quit)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.window.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Intructions", command=lambda: print("Yahtzee rules!"))
        helpmenu.add_command(label="About...", command=lambda: print("about"))

        self.make_photos()
        self.make_buttons()
        self.make_labels()

        self.dice_label.grid(column = 0, row = 0, columnspan = 2)
        self.player_label.grid(column = 2 , row = 0)
        for i in range(self.players):
            for j in range(13):
                self.board_labels[i][j].grid(column = 3 + i , row = j + 1, columnspan = 1)

        for i in range(4):
            self.dice_buttons[i].grid(column = i%2, row = 2*(i - i%2)+ 1, columnspan = 1,rowspan=4)
        self.dice_buttons[4].grid(column = 0, row = 9, columnspan = 2,rowspan=4)

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column = 2 , row = i + 1)
        self.roll_button.grid(column = 0 , row = 13, columnspan = 2)
        self.done_button.grid(column = 3 , row = 0, columnspan = 3)

    def make_photos(self):
        for photo in os.listdir(path + "/photos"):
            num = int(photo.split('.')[0].split('_')[1]) - 1
            self.photos[num] =  PhotoImage(file=path + "/photos/" + photo)

    def make_buttons(self):
        for i in range(5):
            self.dice_buttons.append(Button(self.window, justify = LEFT, image=self.photos[i]
                                            , command = lambda i = i: self.select(i)))
        for i in range(13):
            self.buttons.append(Button(self.window, text = score_labels[i], width = 11, height = 2
                                        ,command = lambda i = i: self.choose(i)))
        self.roll_button = Button(self.window, text = 'Roll', width = 11, height = 2, command = lambda: self.roll())
        self.done_button = Button(self.window, text = 'Done', width = 11, height = 2, command = lambda: self.done(), state = DISABLED)
    
    def make_labels(self):
        self.dice_label = Label(self.window, text = 'Dice', width = 15, font=("Courier", 30))
        self.player_label = Label(self.window, text = 'Player 1', font=("Courier", 20))
        for i in range(self.players):
            for j in range(13):
                self.board_labels[i][j] = Label(self.window, text = '---')

if __name__ == "__main__":
    start()