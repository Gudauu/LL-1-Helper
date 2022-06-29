import re
from reprlib import recursive_repr
import tkinter
import tkinter.messagebox
import customtkinter
import sys
from icecream import ic
#from more_itertools import first
from sqlalchemy import false
from tkinter import scrolledtext
from tabulate import tabulate

# Set dark appearance mode:
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
   

class App(customtkinter.CTk):

    App_NAME = "CustomTkinter complex example"
    WIDTH = 1700
    HEIGHT = 1500
    BUTTON_WIDTH = 250
    BUTTON_HEIGHT = 80

    MAIN_COLOR = "#5EA880"
    MAIN_COLOR_DARK = "#2D5862"
    MAIN_HOVER = "#458577"
    MAIN_GREY = "#2a2d2e"
    MAIN_DARK = "#212325"
    VERY_DARK = "#101719"
    FONT_PALE_GREEN = "#a1ccc1"
    
    num_rules = 0
    num_iteration = 0
    
    start_symbol = None
    terminal_list = ['$']
    non_terminal_list = list()
    
    rules = dict()
    basic_rules = dict()
    explain_rules = dict()
    explain_first = dict()
    explain_follow = dict()
    first = dict()
    follow = dict()
    nullable = dict()
    table = dict()

    IsLL1 = True
    
    ofile = None
    ifile = None

    basic_rule_str = "NUM\tRULE\n\n"
    cur_fact_input = ""

    break_line = "_"*38 + '\n'
    short_break_line = "_"*32 + '\n'
    input_intro = ''

    input_edited = False
    
    
    def clear_grammar_status(self):
        # each time a grammar edit happens, clear grammar asscociated data
        self.num_rules = 0
        self.num_iteration = 0
        self.start_symbol = None
        self.terminal_list = ['$']
        self.non_terminal_list = list()
        self.rules = dict()
        self.basic_rules = dict()
        self.first = dict()
        self.follow = dict()
        self.explain_rules = dict()
        self.explain_first = dict()
        self.nullable = dict()
        self.table = dict()
        self.IsLL1 = True
        self.ofile = None
        self.ifile = None
        self.basic_rule_str = "NUM\tRULE\n\n"
        self.cur_fact_input = ""
        self.input_edited = False

    def __init__(self, *args, **kwargs):

        # GUI initialzation
        
        super().__init__(*args, **kwargs)
        
        self.title(App.App_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=App.WIDTH/2, #200,
                                                 height=App.HEIGHT-40,
                                                 corner_radius=20)
        self.frame_left.place(relx=0.3, rely=0.5, anchor=tkinter.E)

        

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=App.WIDTH*2/3-40, #420,
                                                  height=App.HEIGHT-40,
                                                  corner_radius=15)
        self.frame_right.place(relx=0.32, rely=0.5, anchor=tkinter.W)

        self.frame_rightmost = customtkinter.CTkFrame(master=self,
                                                  width=App.WIDTH/2+40, #420,
                                                  height=App.HEIGHT-40,
                                                  corner_radius=15)
        self.frame_rightmost.place(relx=0.68, rely=0.5, anchor=tkinter.W)

        # ============ frame_left ============

        label_GRAMMAR = customtkinter.CTkLabel(master=self.frame_left,
                                       text="GRAMMAR HERE:",
                                       width=120,
                                       height=25,
                                       text_font = (None,35),
                                       text_color = self.MAIN_COLOR,
                                       fg_color=(self.MAIN_COLOR, self.MAIN_GREY))
        label_GRAMMAR.place(relx=0.5, rely=0.04, anchor=tkinter.N)

        
        self.input_text = scrolledtext.ScrolledText(master = self.frame_left,
                                            width = 38, #int(App.WIDTH/2)-20, 
                                            height = 20, #int(App.HEIGHT/2)-20,
                                            fg = (self.FONT_PALE_GREEN),
                                            bg = App.MAIN_GREY,
                                            bd = 0,
                                            border = None,
                                            wrap = tkinter.WORD)
        self.input_text.pack(side = 'left') 
        
        
        self.input_text.place(relx=0.5, rely=0.11, anchor=tkinter.N)
        self.input_text.config(font=("Times New Roman", 28),state = 'disabled',highlightthickness = 0, borderwidth=0)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                width=self.BUTTON_WIDTH,
                                                height=self.BUTTON_HEIGHT,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="EDIT",
                                                text_font=(None,30),
                                                text_color=self.FONT_PALE_GREEN,
                                                command=self.button_edit_event,
                                                border_width=6,
                                                corner_radius=10)
        self.button_1.place(relx=0.43, rely=0.9, anchor=tkinter.E)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                width=self.BUTTON_WIDTH,
                                                height=self.BUTTON_HEIGHT,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="SAVE",
                                                text_font=(None,30),
                                                text_color=self.FONT_PALE_GREEN,
                                                command=self.button_save_event,
                                                border_width=6,
                                                corner_radius=10)
        self.button_2.place(relx=0.95, rely=0.9, anchor=tkinter.E)

        # ============ frame_right ============
        
        label_PROGRESS = customtkinter.CTkLabel(master=self.frame_right,
                                       text="INFERENCE GOES HERE!",
                                       width=120,
                                       height=25,
                                       text_font = (None,35),
                                       text_color = self.MAIN_COLOR,
                                       fg_color=(self.MAIN_COLOR, self.MAIN_GREY))
        label_PROGRESS.place(relx=0.5, rely=0.04, anchor=tkinter.N)
        

        self.input_intro = "READ THIS CAREFULLY WHILE EDITING !\n\n"
        self.input_intro += "Your grammar should contain three part:\n\n"
        self.input_intro += "1. A start phrase indicating start symbol. Format: \'start X\'(X is your start symbol) \n\n"
        self.input_intro += "2. Production rules. Format: \'A > aBcD \' Different rules cannot share the same line. Use as many lines as necessary.\n\n"
        self.input_intro += "3. Terminals. Format: \'{a,B,c,@}\' \n\n"
        self.input_intro += "Other Appdes:\n\n"
        self.input_intro += "1. Each symbol must occupy letter only. \n\n"
        self.input_intro += "2. We use \'@\' as empty symbol and \'$\' as EOF. You should have \'@\' in grammar part 3 but no need to write \'$\' for the entire input section.\n\n"
        self.input_intro += "3. Special symbols like '{','}','>' cannot be used elsewhere.\n\n"
        self.input_intro += "That's it. Gook luck !\n\n"
        self.input_intro += self.break_line

        self.progress_text = scrolledtext.ScrolledText(master = self.frame_right,
                                            width = 45, #int(App.WIDTH/2)-20, 
                                            height = 24, #int(App.HEIGHT/2)-20,
                                            fg = "grey",
                                            bg = App.MAIN_GREY,
                                            bd = 0,
                                            border = None,
                                            wrap = tkinter.WORD)
        self.progress_text.pack(side = 'left') # expand = True,
        self.progress_text.place(relx=0.52, rely=0.1, anchor=tkinter.N)
        self.progress_text.config(font=("Times New Roman", 32),state = 'disabled',highlightthickness = 0, borderwidth=0)

        # ============ frame_rightmost ============


        self.label_EXPLAIN = customtkinter.CTkLabel(master=self.frame_rightmost,
                                       text="EXPLANATION SECTION",
                                       width=120,
                                       height=25,
                                       text_font = (None,35),
                                       text_color = self.MAIN_COLOR,
                                       fg_color=(self.MAIN_COLOR, self.MAIN_GREY))
        self.label_EXPLAIN.place(relx=0.5, rely=0.04, anchor=tkinter.N)

        self.entry_explain_num = customtkinter.CTkEntry(master=self.frame_rightmost,
                                       placeholder_text="input number:",
                                       width=self.BUTTON_WIDTH*2,
                                       height=self.BUTTON_HEIGHT,
                                       fg_color=None,
                                       border_color=self.MAIN_GREY,
                                       text_font=(None,30),
                                       text_color=self.FONT_PALE_GREEN)
        self.entry_explain_num.place(relx=0.48, rely=0.1, anchor=tkinter.N)


        self.button_3 = customtkinter.CTkButton(master=self.frame_rightmost,
                                                width=self.BUTTON_WIDTH,
                                                height=self.BUTTON_HEIGHT,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="EXPLAIN!",
                                                text_font=(None,30),
                                                text_color=self.FONT_PALE_GREEN,
                                                command=self.button_explain_event,
                                                border_width=6,
                                                corner_radius=10)
        self.button_3.place(relx=0.8, rely=0.1, anchor=tkinter.N)

        self.explain_text = scrolledtext.ScrolledText(master = self.frame_rightmost,
                                            width = 36, #int(App.WIDTH/2)-20, 
                                            height = 20, #int(App.HEIGHT/2)-20,
                                            fg = self.FONT_PALE_GREEN,
                                            bg = App.MAIN_GREY,
                                            bd = 0,
                                            border = None,
                                            wrap = tkinter.WORD)
        self.explain_text.pack(side = 'left') # expand = True,
        self.explain_text.place(relx=0.52, rely=0.2, anchor=tkinter.N)
        self.explain_text.config(font=("Times New Roman", 32),state = 'disabled',highlightthickness = 0, borderwidth=0)


    def file_init(self):
        self.ofile = open("rules.txt",'w')
        self.ifile = open("facts.txt")
        
    def read_facts_into_rules(self) -> None:
        new_result = None
        self.progress_text.configure(state='normal')
        
        # read input file line by line
        for line in self.ifile:
            if len(line) > 1:
                line = line.rstrip()
                # part 3: terminals
                if line[0] == "{":
                    for t in (line[1:-1].split(',')):
                        self.num_rules += 1
                        self.terminal_list.append(t)
                        new_result = str(self.num_rules)+"\t"+str(t)+" is terminal.\n"
                        self.explain_rules[self.num_rules] = [[-1]]
                        self.explain_rules[self.num_rules].append("We know " + str(t)+" is terminal from input.\n")
                        self.ofile.write(new_result)
                        self.progress_text.insert(tkinter.END, new_result)
                # part 1: start phrase
                elif "start" in line:
                    line_set = line.split(' ')
                    self.start_symbol = line_set[1]
                    self.num_rules += 1
                    new_result = str(self.num_rules)+"\t"+str(self.start_symbol)+" is start symbol.\n"
                    self.explain_rules[self.num_rules] = [[-1]]
                    self.explain_rules[self.num_rules].append("We know " + self.start_symbol+" is start symbol from input.\n")
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                # part 2: production rules
                else:
                    (left,right) = line.split('>')
                    left = left.strip()
                    right = (right.strip()).replace(" ","")
                    if str(left) == str(self.start_symbol):
                        right = right + '$'
                    self.num_rules += 1
                    if left not in self.non_terminal_list:  ## first time nt
                        self.non_terminal_list.append(left)
                        self.basic_rules[left] = [(self.num_rules,right)]
                        self.rules[left] = [(self.num_rules,right)]
                    else:
                        self.rules[left].append((self.num_rules,right))
                        self.basic_rules[left].append((self.num_rules,right))
                    new_result = str(self.num_rules)+"\t IF left is "+left+" THEN right produces "+right+"\n"

                    # update explanation data struction
                    self.explain_rules[self.num_rules] = [[-1]]
                    self.explain_rules[self.num_rules].append("We know " + left+" produces "+right+" from input.\n")
                    self.basic_rule_str += new_result

                    # write to rules.txt and progress window
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                    
        self.num_rules += 1
        self.ofile.write(str(self.num_rules)+"\t$ is terminal.\n")
        self.progress_text.insert(tkinter.END, str(self.num_rules)+"\t$ is terminal.\n")
        self.ifile.close()
        self.progress_text.configure(state='disabled')
        
                            
    def check_left_recursion(self) -> bool:
        new_result = None
        self.progress_text.configure(state='normal')
        # left recursion happens when a production of non-terminal A has A as its starting right-hand-side symbol
        for non_terminal in self.rules:
            productions = self.rules[non_terminal]
            for production in productions:
                if production[1][0] == non_terminal:
                    self.num_rules += 1
                    new_result = str(self.num_rules)+"\t Left recursion in rule: "+str(production[0])+"\n" 
                    self.explain_rules[self.num_rules] = [[production[0]]]
                    self.explain_rules[self.num_rules].append("Left recursion in rule "+str(production[0])+".\n")

                    self.num_rules += 1
                    new_result += str(self.num_rules)+"\t Not LL(1). Terminated.\n" 
                    self.explain_rules[self.num_rules] = [[self.num_rules-1]]
                    self.explain_rules[self.num_rules].append("Grammar with left recursion is not LL(1).\n")
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                    self.IsLL1 = False
                    return False
        self.progress_text.configure(state='disabled')
        return True
        
                
    def check_left_factoring(self) -> bool:
        new_result = None
        self.progress_text.configure(state='normal')

        # common prefix happens when two productions of a non-terminal share the same prefix
        for non_terminal in self.rules:
            productions = self.rules[non_terminal]
            for i in range(len(productions)):
                for j in range(i+1,len(productions)):
                    if productions[j][1][0] == productions[i][1][0]:
                        self.num_rules += 1
                        new_result = str(self.num_rules)+"\t Common prefix in rule: "+str(productions[i][0])+" and "+str(productions[j][0])+"\n"
                        self.explain_rules[self.num_rules] = [[productions[j][0]]]
                        self.explain_rules[self.num_rules].append("Common prefix in rule "+str(productions[j][0])+".\n")
                        self.num_rules += 1
                        new_result += str(self.num_rules)+"\t Not LL(1). Terminated.\n"
                        self.explain_rules[self.num_rules] = [[self.num_rules-1]]
                        self.explain_rules[self.num_rules].append("Grammar with common prefix is not LL(1).\n")
                        self.ofile.write(new_result)
                        self.progress_text.insert(tkinter.END, new_result)
                        self.IsLL1 = False
                        return False
        self.progress_text.configure(state='disabled')
        return True
        
                    
    def check_non_terminal_complete(self,nt) -> bool:
        productions = self.rules[nt]
        for prod in productions:
            if prod[1][0] not in self.terminal_list:
                return False
        return True
                
            
    def inference_engine(self) -> None:
        # initialization
        new_result = None
        self.progress_text.configure(state='normal')

        # start inference iteration
        # keep iterating until no change
        flag_changed = True
        while flag_changed:
            flag_changed = False
            
            nt_list = list(self.rules)
            for non_terminal in nt_list:
                # a symbol is "complete" if all of its reduced productions begin with terminal
                if self.check_non_terminal_complete(non_terminal):
                    self.num_rules += 1
                    self.num_iteration += 1
                    new_result = str(self.num_rules)+"\t"+str(non_terminal)+" can be used to reduce others.\n"

                    # initialize update on explanation data structure
                    self.explain_rules[self.num_rules] = [[]]
                    str_temp = "Each of "+non_terminal+"'s latest rule: \n"
                    for prod in self.rules[non_terminal]:
                        str_temp += str(prod[0])+ " "  #"\t"+prod[1]+"\n"
                        self.explain_rules[self.num_rules][0].append(prod[0])
                    str_temp += "\n has terminal as its first right-side symbol.\n"
                    self.explain_rules[self.num_rules].append(str_temp)

                    # initialize output to rules.txt and progress window
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)

                    new_result = "\n\tIteration "+str(self.num_iteration)+" using "+non_terminal+"\n"
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                    productions = self.rules[non_terminal]
                    # find productions that can be reduced by this complete symbol
                    for sub_nt in self.rules:
                        if sub_nt is not non_terminal:
                            len_subnt_prod = len(self.rules[sub_nt])
                            which_subnt_prod = 0
                            for i in range(len_subnt_prod):
                                # complete symbol in this production. Reducable !
                                if non_terminal in self.rules[sub_nt][which_subnt_prod][1]:
                                    flag_changed = True
                                    sub_right = self.rules[sub_nt][which_subnt_prod][1]
                                    temp_explain_sub_prod_num = self.rules[sub_nt][which_subnt_prod][0]
                                    self.rules[sub_nt].pop(which_subnt_prod)
                                    # update with every production
                                    for prod in productions:
                                        self.num_rules += 1
                                        replaced_sub_right = sub_right.replace(non_terminal,prod[1])
                                        if prod[1] == '@' and len(replaced_sub_right)>1:
                                            replaced_sub_right = replaced_sub_right.replace('@','')
                                        self.rules[sub_nt].append((self.num_rules,replaced_sub_right))
                                        new_result = str(self.num_rules)+"\t IF left is "+sub_nt+" THEN right produces "+replaced_sub_right+"\n"

                                        self.explain_rules[self.num_rules] = [[temp_explain_sub_prod_num,prod[0]]]
                                        self.explain_rules[self.num_rules].append("Using rule "+str(prod[0])+" to reduce rule "+str(temp_explain_sub_prod_num)+".\n")

                                        self.ofile.write(new_result)
                                        self.progress_text.insert(tkinter.END, new_result)
                                        
                                else:
                                    which_subnt_prod += 1
                    self.rules.pop(non_terminal)
        self.ofile.write("\n\tIteration finished. No more changes.\n")
        self.progress_text.insert(tkinter.END, "\n\tIteration finished. No more changes.\n")
        self.progress_text.configure(state='disabled')
        
    
    
        
    def construct_first_and_nullable(self) -> None:
        ## initialize
        new_result = None
        record_explain_first_rule = dict()

        ## initialize first set
        for t in self.terminal_list:
            self.first[t] = [t]
            record_explain_first_rule[t] = [-1]
        ## initialize nullable set
        for t in self.non_terminal_list:
            self.nullable[t] = False
        for t in self.terminal_list:
            self.nullable[t] = False
        self.nullable['@'] = True
        self.ofile.close()

        # construct first set.
        # simply find all the right-hand-side starting terminal symbol for each non-terminal in rules already inferenced.
        with open("rules.txt",'r') as rulefile:
            for line in rulefile:
                if line[0].isdigit() and ("produces" in line): # num IF left is A THEN right produces B
                    line_list = line.rstrip().split()
                    nt = line_list[4]
                    t = line_list[8][0]
                    if t not in self.terminal_list:
                        continue
                    if nt not in self.first:
                        self.first[nt] = [t]  
                        record_explain_first_rule[nt] = [line_list[0]]
                    elif t not in self.first[nt]:
                        self.first[nt].append(t)
                        record_explain_first_rule[nt].append(line_list[0])
        rulefile.close()

        
        self.ofile = open("rules.txt","a")
        self.progress_text.configure(state='normal')
        # first set result output
        for nt in self.first:
            self.num_rules += 1
            self.explain_first[nt] = self.num_rules
            new_result = str(self.num_rules)+"\tFirst set of " + nt + ":"
            self.explain_rules[self.num_rules] = [[-1]]

            # output to rules.txt and progress window 
            self.ofile.write(new_result)
            self.progress_text.insert(tkinter.END, new_result)
            
            for t in self.first[nt]:
                self.ofile.write(t+' ')
                self.progress_text.insert(tkinter.END, t+' ')
                
            # update the explanation data structure
            if nt in self.non_terminal_list:
                self.explain_rules[self.num_rules].append("Element in its first set are found in rule: "+(' '.join(record_explain_first_rule[nt]))+ ' accordingly.\n')
            else:
                self.explain_rules[self.num_rules].append("First set of any terminal is just itself.\n")
            self.ofile.write('\n')
            self.progress_text.insert(tkinter.END, '\n')

            # nullable set result output
            if '@' in self.first[nt] and nt!= '@':
                self.nullable[nt] = True
                self.num_rules += 1
                new_result = str(self.num_rules)+"\t" + nt + " is nullable.\n"

                # update the explanation data structure
                self.explain_rules[self.num_rules] = [[self.num_rules-1]]
                self.explain_rules[self.num_rules].append(nt + " is nullable cause empty symbol is in its first set.\n")
                
                # output to rules.txt and progress window 
                self.ofile.write(new_result)
                self.progress_text.insert(tkinter.END, new_result)
        self.ofile.close()
        self.progress_text.configure(state='disabled')
                
                
    def construct_follow(self) -> None:
        # initialization
        new_result = None
        explain_from_first = dict()
        explain_from_follow = dict()
        for nt in self.non_terminal_list:
            self.follow[nt] = []
            explain_from_first[nt] = []
            explain_from_follow[nt] = []
        
        # keep iterating until no more changes
        flag_changed = True
        while flag_changed:
            flag_changed = False
            for nt in self.basic_rules:
                productions = self.basic_rules[nt]
                for prod in productions:
                    for i in range(len(prod[1])-1):
                        cur_letter = prod[1][i]
                        if cur_letter in self.terminal_list:
                                continue
                        j = i + 1
                        while j < len(prod[1]):
                            nxt_letter = prod[1][j]
                            if nxt_letter not in explain_from_first[cur_letter]:
                                explain_from_first[cur_letter].append((prod[0],nxt_letter))

                            if nxt_letter in self.terminal_list and nxt_letter != '@':
                                if nxt_letter not in self.follow[cur_letter]:
                                    self.follow[cur_letter].append(nxt_letter)
                                    flag_changed = True
                                break
                            else:
                                for t in self.first[nxt_letter]:
                                    if t not in self.follow[cur_letter] and t != '@':
                                        self.follow[cur_letter].append(t)
                                        flag_changed = True
                                
                                if self.nullable[nxt_letter]:
                                    j += 1
                                else:
                                    break

                        if j == len(prod[1]):
                            if nt not in explain_from_follow[cur_letter]:
                                explain_from_follow[cur_letter].append((prod[0],nt))

                            for t in self.follow[nt]:
                                if t not in self.follow[cur_letter] and t != '@':
                                    self.follow[cur_letter].append(t)
                                    flag_changed = True
                    # the last letter
                    last_letter = prod[1][len(prod[1])-1]
                    if last_letter in self.non_terminal_list and last_letter != '@':
                        for t in self.follow[nt]:
                            if t not in self.follow[last_letter]:
                                self.follow[last_letter].append(t)
                                flag_changed = True
                        if nt not in explain_from_follow[last_letter]:
                            explain_from_follow[last_letter].append((prod[0],nt))
                
        self.ofile = open("rules.txt","a")
        self.progress_text.configure(state='normal')

        # write to rules.txt and progress window
        orig_num_rules = self.num_rules
        for nt in self.follow:
            self.num_rules += 1
            self.explain_follow[nt] = self.num_rules
            new_result = str(self.num_rules)+"\tFollow set of " + nt + ":\t"
            self.ofile.write(new_result)
            self.progress_text.insert(tkinter.END, new_result)
            for t in self.follow[nt]:
                self.ofile.write(t+' ')
                self.progress_text.insert(tkinter.END, t+' ')
            self.ofile.write('\n')
            self.progress_text.insert(tkinter.END, '\n')

        # write to explanation section
        for nt in self.follow:  
            orig_num_rules += 1 
            self.explain_rules[orig_num_rules] = [[]]
            explain_str = str(nt)+"'s follow set consists of the first set(s) of symbol: \n"
            # if empty, show None
            if len(explain_from_first[nt]) ==0:
                explain_str += "None\n"
            for (num,symbol) in explain_from_first[nt]:
                rule_num_first_symbol = self.explain_first[symbol]
                if rule_num_first_symbol not in self.explain_rules[orig_num_rules][0]:
                    self.explain_rules[orig_num_rules][0].append(rule_num_first_symbol)
                    explain_str += str(symbol)+"\t<rule "+str(num)+">\n"

            explain_str += "and the follow set(s) of symbol: \n"
            # if empty, show None
            if len(explain_from_follow[nt]) ==0:
                explain_str += "None\n"
            for (num,symbol) in explain_from_follow[nt]:
                # avoids follow recursion
                if symbol == nt:
                    continue
                rule_num_follow_symbol = self.explain_follow[symbol]
                if rule_num_follow_symbol not in self.explain_rules[orig_num_rules][0]:
                    self.explain_rules[orig_num_rules][0].append(rule_num_follow_symbol)
                    explain_str += str(symbol)+"\t<rule "+str(num)+">\n"
            self.explain_rules[orig_num_rules].append(explain_str)


        self.ofile.close()
        self.progress_text.configure(state='disabled')

    def get_basic_rule(self,num) -> str:
        for nt in self.basic_rules:
            for rule in self.basic_rules[nt]:
                if rule[0] == num:
                    return str(rule[1])
        return " "    


    def get_rule_from_file(self,num) -> str:
        with open("rules.txt") as findfile:
            for line in findfile:
                if len(line) > 1:
                    line_list = line.split()
                    if str(line_list[0]) == str(num):
                        linestr = line[len(str(num)):].strip()
                        return linestr
        return " "      

    def construct_table(self) -> bool:
        # The parsing table. 
        # Each entry indicates which production should be applied for each non-terminal on each terminal.

        ## initialization
        table = dict()
        for nt in self.non_terminal_list:
            for t in self.terminal_list:
                table[(nt,t)] = []
        for nt in self.non_terminal_list:
            for rule in self.basic_rules[nt]:
                rule_num = rule[0]
                rule_cont = rule[1]
                i = 0
                ## first
                while i < len(rule_cont):
                    letter = rule_cont[i]
                    for t in self.first[letter]:
                        if rule_num not in table[(nt,t)] and t != '@':
                            table[(nt,t)].append(rule_num)
                    if not self.nullable[letter]:
                        break
                    i += 1
                ## follow
                if i == len(rule_cont):
                    for t in list(self.follow[nt]):
                        if rule_num not in table[(nt,t)] and t != '@':
                            table[(nt,t)].append(rule_num)

        
        copy_tlist = self.terminal_list.copy()
        copy_tlist.remove("@")

        # maximum of column of table shown on progress window
        max_col = 4
        divided_t_list = []
        cur_nt_list = []
        i = 0
        while i< len(copy_tlist):
            cur_nt_list.append(copy_tlist[i])
            i += 1
            if i%max_col == 0 or i == len(copy_tlist):
                divided_t_list.append(cur_nt_list)
                cur_nt_list = []
                
        
        self.ofile = open("rules.txt","a")
        self.progress_text.configure(state='normal')

        self.ofile.write("\n\n\tFinal table:\n")
        self.progress_text.insert(tkinter.END,"\n\n\tFinal table:\n"+self.break_line+"\n") 


        # the last rule indicates whether this grammar is LL(1).
        self.num_rules += 1
        # for the last rule, explanation just refers to whether duplicity exists in parsing table.
        self.explain_rules[self.num_rules] = [[-1]]
        self.explain_rules[self.num_rules].append("Check the table for zero duplicity !\n")

        # construct and output table
        for t_list in divided_t_list:
            self.table = []
            first_list = [" "]
            for t in t_list:
                first_list.append(t)
            self.table.append(first_list)
            for nt in self.non_terminal_list:
                cur_nt_list = [nt]
                for t in t_list:
                    if len(table[(nt,t)])==0:
                        cur_nt_list.append("")
                    else:
                        str_nums = ''
                        # duplicity
                        if len(table[(nt,t)]) > 1:
                            self.IsLL1 = False
                            self.explain_rules[self.num_rules][1] = "Oops ! Duplicity in table entry ( "+str(nt)+", "+str(t)+").\n"
                        for i in range(len(table[(nt,t)])-1):
                            str_nums += str(table[(nt,t)][i])
                            str_nums += ','
                        str_nums += str(table[(nt,t)][-1])
                        cur_nt_list.append(str_nums)
                self.table.append(cur_nt_list)

            # start outputing 
            self.ofile.write(tabulate(self.table,tablefmt="fancy_grid"))
            self.ofile.write('\n\n')

            
            for line in self.table:
                new_result = ""
                for element in line:
                    new_result += element + '\t'
                new_result += '\n'
                self.progress_text.insert(tkinter.END,new_result) 
            self.progress_text.insert(tkinter.END,'\n'+self.break_line+'\n') 

        if not self.IsLL1:
            new_result = str(self.num_rules)+"\t Not LL(1). Terminated.\n" 
        else:
            new_result = str(self.num_rules)+"\t No conflict in table. Is LL(1) !\n" 

        
        self.progress_text.insert(tkinter.END,new_result) 
        self.ofile.write(new_result)

        self.ofile.close()
        self.progress_text.configure(state='disabled')

                    
    def check_grammar_input(self) -> bool:
        fact_input = self.input_text.get("1.0", tkinter.END)
        flag_has_start = False
        flag_has_terminal = False
        flag_has_rule = False
        lines = fact_input.replace("\n\n","\n")
        for line in lines.split('\n'):
            # pass blank line
            if len(line) <= 1:
                continue
            line = line.replace(" ","")
            if line[0] == '{':
                if not re.match(r"^\{([^$>],)+[^$>]\}$",line):
                    self.show_intro("Terminal definition not right!\n\n")
                    return False
                if flag_has_terminal:
                    self.show_intro("Terminal redefinition!\n\n")
                    return False
                if not '@' in line:
                    self.show_intro("Missing empty symbol in phrase!\n\n")
                    return False
                flag_has_terminal = True
            elif '>' in line:
                if "{" in line or "}" in line or "$" in line:
                    self.show_intro("Rule definition cannot have predefined symbols!\n\n")
                    return False
                if not re.match(r"^[^>]>[^>]+$",line.strip()):
                    self.show_intro("Rule definition not right!\n\n")
                    return False
                flag_has_rule = True
            else:
                if not re.match(r"^start[^$>]$",line.strip()):
                    self.show_intro("Start phrase definition not right!\n\n")
                    return False
                if flag_has_start:
                    self.show_intro("Start phrase redefinition!\n\n")
                    return False
                flag_has_start = True
        if not flag_has_start:
            self.show_intro("Missing start phrase!\n\n")
            return False
        elif not flag_has_rule:
            self.show_intro("Missing rule phrase!\n\n")
            return False
        elif not flag_has_terminal:
            self.show_intro("Missing terminal phrase!\n\n")
            return False
        return True  
            
            
    def restore_facts_rules(self):
        # on editing, restore the user input
        self.input_text.configure(state = 'normal')  
        self.input_text.delete("1.0", tkinter.END)
        self.input_text.insert("1.0",self.cur_fact_input)
        self.input_text.configure(state='disabled')


            
    def show_basic_rules(self):
        # show the original grammar
        self.input_text.configure(state = 'normal')  
        self.input_text.delete("1.0", tkinter.END)
        self.input_text.insert("1.0",self.basic_rule_str)
        self.input_text.configure(state='disabled')

        

    def change_progress_txt_into_normal(self):
        self.progress_text.configure(state='normal')
        self.progress_text.delete("1.0", tkinter.END)
        self.progress_text.configure(state='disabled',fg = self.FONT_PALE_GREEN)
        
    def show_intro(self,intro = input_intro):
        # show grammar introduction(or other indicated message intro)
        self.progress_text.configure(state='normal',fg = "grey")
        self.progress_text.insert("1.0",intro)
        self.progress_text.configure(state='disabled')


    def button_save_event(self):
        # only react on editing 
        if not self.input_edited:
            return

        # check grammar
        if not self.check_grammar_input():
            return

        self.input_text.configure(state='disabled',bg = self.MAIN_GREY)
        self.input_edited = False

        # apply new grammar
        self.clear_grammar_status()
        self.change_progress_txt_into_normal()

        # save input into "cur_fact_input"
        self.cur_fact_input = self.input_text.get("1.0", tkinter.END)
        fact_file = open("facts.txt","w")
        fact_file.write(self.cur_fact_input)
        fact_file.close()
        
        # start inference
        self.file_init()
        self.read_facts_into_rules()

        # basic_rule str is ready. Output to input text.
        self.show_basic_rules()


        # check left recursion and common prefix
        if not self.check_left_recursion() or (not self.check_left_factoring()):
            self.ofile.close()
            return 

        # start rule inferencing
        self.inference_engine()
        
        # construct first and follow set
        self.construct_first_and_nullable()
        self.construct_follow()
        
        # construct parsing table
        self.construct_table()
        
        self.ofile.close()
    
    def button_edit_event(self):
        # get the fact input back for easy editing 
        self.restore_facts_rules()
        self.input_text.configure(state='normal',bg = self.MAIN_DARK)

        # change state of input
        self.input_edited = True

        # show introduction on top
        self.show_intro(self.input_intro)
        
    
    def recurse_explain(self,num):
        # -1 as num means reaching end of recursion(self-explanable rules)
        if num == -1:
            return
        # read content of rule indicated by rule num from "rules.txt"
        rule_content = self.get_rule_from_file(num)

        # write to explanation section
        self.explain_text.insert(tkinter.END,"\n\n"+str(num)+". "+rule_content+"\n"+self.short_break_line+self.explain_rules[num][1])
        # recurse on num on logic recursion path
        for n in self.explain_rules[num][0]:
            self.recurse_explain(n)

        
    def button_explain_event(self):
        # do nothing if no grammar yet received
        if self.num_rules ==0:
            return 

        explain_num = int(self.entry_explain_num.get())

        # check explain_num
        if (explain_num <=0) or (explain_num > self.num_rules):
            self.explain_text.configure(state='normal') 
            self.explain_text.delete("1.0", tkinter.END)
            self.explain_text.insert("1.0","Rule number out of range !\n")
            self.explain_text.insert(tkinter.END,"Should be an interger between 1 and "+str(self.num_rules)+".\n")
            self.progress_text.configure(state='disabled')
            return

        # complete check, start explanation
        cur_num = explain_num
        self.explain_text.configure(state='normal')
        self.explain_text.delete("1.0", tkinter.END)
        
        self.recurse_explain(cur_num)

        self.progress_text.configure(state='disabled')




    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
        
        

        

        
        
    
        
        


if __name__ == "__main__":
    app = App()
    app.start()
