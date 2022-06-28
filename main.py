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
   

class GUI(customtkinter.CTk):

    GUI_NAME = "CustomTkinter complex example"
    WIDTH = 1700
    HEIGHT = 1500
    BUTTON_WIDTH = 250
    BUTTON_HEIGHT = 50

    MAIN_COLOR = "#5EA880"
    MAIN_COLOR_DARK = "#2D5862"
    MAIN_HOVER = "#458577"
    MAIN_GREY = "#2a2d2e"
    MAIN_DARK = "#212325"
    VERY_DARK = "#101719"
    
    num_rules = 0
    num_iteration = 0
    
    start_symbol = None
    terminal_list = ['$']
    non_terminal_list = list()
    
    rules = dict()
    basic_rules = dict()
    first = dict()
    follow = dict()
    nullable = dict()
    table = dict()
    
    ofile = None
    ifile = None
    
    
    

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        # self.ofile = open("rules.txt",'w')
        # self.ifile = open("facts.txt")
        
        self.title(GUI.GUI_NAME)
        self.geometry(str(GUI.WIDTH) + "x" + str(GUI.HEIGHT))
        self.minsize(GUI.WIDTH, GUI.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=GUI.WIDTH/3, #200,
                                                 height=GUI.HEIGHT-40,
                                                 corner_radius=15)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tkinter.E)

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=GUI.WIDTH*2/3, #420,
                                                  height=GUI.HEIGHT-40,
                                                  corner_radius=15)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tkinter.W)

        # ============ frame_left ============

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                width=self.BUTTON_WIDTH,
                                                height=self.BUTTON_HEIGHT,
                                                border_color=GUI.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=GUI.MAIN_HOVER,
                                                text="CTkButton",
                                                text_font=(None,30),
                                                command=self.button_event,
                                                border_width=3,
                                                corner_radius=6)
        self.button_1.place(relx=0.5, y=50, anchor=tkinter.CENTER)

        # ============ frame_right ============

        # self.frame_progress = customtkinter.CTkFrame(master=self.frame_right,
        #                                          width=GUI.WIDTH/2,
        #                                          height=GUI.HEIGHT*5/6,
        #                                          fg_color=GUI.VERY_DARK,
        #                                          corner_radius=15)
        # self.frame_progress.place(relx=0.5, rely=0.07, anchor=tkinter.N)


        # ============ frame_right -> frame_info ============
        
        
        
        self.progress_text = scrolledtext.ScrolledText(master = self.frame_right,
                                            width = 38, #int(GUI.WIDTH/2)-20, 
                                            height = 24, #int(GUI.HEIGHT/2)-20,
                                            fg = ("white"),
                                            bg = GUI.MAIN_GREY,
                                            bd = 0,
                                            border = None,
                                            wrap = tkinter.WORD)
        self.progress_text.pack(side = 'left') # expand = True,
        self.progress_text.place(relx=0.52, rely=0.07, anchor=tkinter.N)
        # self.progress_text.grid(row = 10,column = 32, columnspan=13)
        # self.progress_text.insert(tkinter.END,"test\n1\n2\n3\n4\n")
        # self.progress_text.insert(tkinter.END,"test again")
        self.progress_text.config(font=("Times New Roman", 32),state = 'disabled',highlightthickness = 0, borderwidth=0)


        # self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
        #                                            text="CTkLabel: Lorem ipsum dolor sit,\n" +
        #                                                 "amet consetetur sadipscing elitr,\n" +
        #                                                 "sed diam nonumy eirmod tempor\n" +
        #                                                 "invidunt ut labore",
        #                                            width=250,
        #                                            height=100,
        #                                            corner_radius=6,
        #                                            fg_color=("white", "gray20"),
        #                                            text_font=(None,30),
        #                                            text_color=GUI.MAIN_COLOR,
        #                                            justify=tkinter.LEFT)
        # self.label_info_1.place(relx=0.5, rely=0.15, anchor=tkinter.N)
        # self.label_info_1.set_text("Hello GUIle tree")

        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info,
        #                                                 progress_color=GUI.MAIN_COLOR,
        #                                                 width=250,
        #                                                 height=12)
        # self.progressbar.place(relx=0.5, rely=0.85, anchor=tkinter.S)
        # self.progressbar.set(0.65)

        # ============ frame_right <- ============

        # self.label_info_2 = customtkinter.CTkLabel(master=self.frame_right,
        #                                            text="CTkLabel: Lorem ipsum",
        #                                            fg_color=None,
        #                                            width=180,
        #                                            height=20,
        #                                            justify=tkinter.CENTER)
        # self.label_info_2.place(x=310, rely=0.6, anchor=tkinter.CENTER)

        # self.button_4 = customtkinter.CTkButton(master=self.frame_right,
        #                                         border_color=GUI.MAIN_COLOR,
        #                                         fg_color=None,
        #                                         hover_color=GUI.MAIN_HOVER,
        #                                         height=28,
        #                                         text="CTkButton",
        #                                         command=self.button_event,
        #                                         border_width=3,
        #                                         corner_radius=6)
        # self.button_4.place(x=310, rely=0.7, anchor=tkinter.CENTER)

        # self.entry = customtkinter.CTkEntry(master=self.frame_right,
        #                                     width=120,
        #                                     height=28,
        #                                     corner_radius=6)
        # self.entry.place(relx=0.33, rely=0.92, anchor=tkinter.CENTER)
        # self.entry.insert(0, "CTkEntry")

        # self.button_5 = customtkinter.CTkButton(master=self.frame_right,
        #                                         border_color=GUI.MAIN_COLOR,
        #                                         fg_color=None,
        #                                         hover_color=GUI.MAIN_HOVER,
        #                                         height=28,
        #                                         text="CTkButton",
        #                                         command=self.button_event,
        #                                         border_width=3,
        #                                         corner_radius=6)
        # self.button_5.place(relx=0.66, rely=0.92, anchor=tkinter.CENTER)


    def file_init(self):
        self.ofile = open("rules.txt",'w')
        self.ifile = open("facts.txt")
        
    def read_facts_into_rules(self) -> None:
        new_result = None
        self.progress_text.configure(state='normal')
        
        for line in self.ifile:
            if len(line) > 1:
                line = line.rstrip()
                if line[0] == "{":
                    for t in (line[1:-1].split(',')):
                        self.num_rules += 1
                        self.terminal_list.append(t)
                        new_result = str(self.num_rules)+"\t"+str(t)+" is terminal.\n"
                        self.ofile.write(new_result)
                        self.progress_text.insert(tkinter.END, new_result)

                elif "start" in line:
                    line_set = line.split(' ')
                    self.start_symbol = line_set[1]
                    self.num_rules += 1
                    new_result = str(self.num_rules)+"\t"+str(self.start_symbol)+" is start symbol.\n"
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                else:
                    (left,right) = line.split('>')
                    left = left.strip()
                    right = right.strip()
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
                    new_result = str(self.num_rules)+"\t"+left+" produces "+right+"\n"
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
        for non_terminal in self.rules:
            productions = self.rules[non_terminal]
            for production in productions:
                if production[1][0] == non_terminal:
                    self.num_rules += 1
                    new_result = str(self.num_rules)+"\t Left recursion in rule: "+str(production[0]) #+non_terminal+" produces "+production
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                    return False
        self.progress_text.configure(state='disabled')
        
                
    def check_left_factoring(self) -> bool:
        new_result = None
        self.progress_text.configure(state='normal')
        for non_terminal in self.rules:
            productions = self.rules[non_terminal]
            for i in range(len(productions)):
                for j in range(i+1,len(productions)):
                    if productions[j][1][0] == productions[i][1][0]:
                        self.num_rules += 1
                        new_result = str(self.num_rules)+"\t Left factoring in rule: "+str(productions[i][0])+" and "+str(productions[j][0])
                        self.ofile.write(new_result)
                        self.progress_text.insert(tkinter.END, new_result)
                        return False
        self.progress_text.configure(state='disabled')
        
                    
    def check_non_terminal_complete(self,nt) -> bool:
        productions = self.rules[nt]
        for prod in productions:
            if prod[1][0] not in self.terminal_list:
                return False
        return True
                
            
    def inference_engine(self) -> None:
        new_result = None
        self.progress_text.configure(state='normal')
        # start inference iteration
        flag_changed = True
        
        while flag_changed:
            flag_changed = False
            
            nt_list = list(self.rules)
            for non_terminal in nt_list:
                if self.check_non_terminal_complete(non_terminal):
                    self.num_iteration += 1
                    new_result = "\n\tIteration "+str(self.num_iteration)+" using "+non_terminal+"\n"
                    self.ofile.write(new_result)
                    self.progress_text.insert(tkinter.END, new_result)
                    productions = self.rules[non_terminal]
                    for sub_nt in self.rules:
                        if sub_nt is not non_terminal:
                            len_subnt_prod = len(self.rules[sub_nt])
                            which_subnt_prod = 0
                            for i in range(len_subnt_prod):
                                if non_terminal in self.rules[sub_nt][which_subnt_prod][1]:
                                    flag_changed = True
                                    sub_right = self.rules[sub_nt][which_subnt_prod][1]
                                    self.rules[sub_nt].pop(which_subnt_prod)
                                    for prod in productions:
                                        self.num_rules += 1
                                        replaced_sub_right = sub_right.replace(non_terminal,prod[1])
                                        if prod[1] == '@' and len(replaced_sub_right)>1:
                                            replaced_sub_right = replaced_sub_right.replace('@','')
                                        self.rules[sub_nt].append((self.num_rules,replaced_sub_right))
                                        new_result = str(self.num_rules)+"\t"+sub_nt+" produces "+replaced_sub_right+"\n"
                                        self.ofile.write(new_result)
                                        self.progress_text.insert(tkinter.END, new_result)
                                        
                                else:
                                    which_subnt_prod += 1
                    self.rules.pop(non_terminal)
        self.ofile.write("\n\tIteration finished. No more changes.\n")
        self.progress_text.insert(tkinter.END, "\n\tIteration finished. No more changes.\n")
        self.progress_text.configure(state='disabled')
        
    
    
        
    def construct_first_and_nullable(self) -> None:
        new_result = None
        ## ini first
        for t in self.terminal_list:
            self.first[t] = [t]
        ## ini nullable
        for t in self.non_terminal_list:
            self.nullable[t] = False
        for t in self.terminal_list:
            self.nullable[t] = False
        self.nullable['@'] = True

            
        self.ofile.close()
        with open("rules.txt",'r') as rulefile:
            for line in rulefile:
                if line[0].isdigit() and ("produces" in line):
                    line_list = line.rstrip().split()
                    nt = line_list[1]
                    t = line_list[3][0]
                    if t not in self.terminal_list:
                        continue
                    if nt not in self.first:
                        self.first[nt] = [t]  
                    elif t not in self.first[nt]:
                        self.first[nt].append(t)
        rulefile.close()
        self.ofile = open("rules.txt","a")
        self.progress_text.configure(state='normal')
        for nt in self.first:
            self.num_rules += 1
            new_result = str(self.num_rules)+"\tFirst set of " + nt + ":"
            self.ofile.write(new_result)
            self.progress_text.insert(tkinter.END, new_result)
            
            for t in self.first[nt]:
                self.ofile.write(t+' ')
                self.progress_text.insert(tkinter.END, t+' ')
            self.ofile.write('\n')
            self.progress_text.insert(tkinter.END, '\n')
            if '@' in self.first[nt] and nt!= '@':
                self.nullable[nt] = True
                self.num_rules += 1
                new_result = str(self.num_rules)+"\t" + nt + " is nullable.\n"
                self.ofile.write(new_result)
                self.progress_text.insert(tkinter.END, new_result)
        self.ofile.close()
        self.progress_text.configure(state='disabled')
                
                
    def construct_follow(self) -> None:
        new_result = None
        for nt in self.basic_rules:
            self.follow[nt] = []
            
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
        self.ofile = open("rules.txt","a")
        self.progress_text.configure(state='normal')

        for nt in self.follow:
            self.num_rules += 1
            new_result = str(self.num_rules)+"\tFollow set of " + nt + ":"
            self.ofile.write(new_result)
            self.progress_text.insert(tkinter.END, new_result)
            for t in self.follow[nt]:
                self.ofile.write(t+' ')
                self.progress_text.insert(tkinter.END, t+' ')
            self.ofile.write('\n')
            self.progress_text.insert(tkinter.END, '\n')
        self.ofile.close()
        self.progress_text.configure(state='disabled')

    def get_basic_rule(self,num) -> str:
        for nt in self.basic_rules:
            for rule in self.basic_rules[nt]:
                if rule[0] == num:
                    return str(rule[1])
        return " "        

    def construct_table(self) -> bool:
        table = dict()
        ## ini
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

        max_col = 3
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


        break_line = "_"*38

        self.ofile.write("\n\n\tFinal table:\n")
        self.progress_text.insert(tkinter.END,"\n\n\tFinal table:\n"+break_line+"\n") 

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
            self.progress_text.insert(tkinter.END,'\n'+break_line+'\n') 


        self.ofile.close()
        self.progress_text.configure(state='disabled')




        # self.table = []
        # first_list = [" "]
        # for t in self.terminal_list:
        #     first_list.append(t)
        # self.table.append(first_list)
        # for nt in self.non_terminal_list:
        #     cur_nt_list = [nt]
        #     for t in self.terminal_list:
        #         if len(table[(nt,t)])==0:
        #             cur_nt_list.append("")
        #         else:
        #             str_nums = ''
        #             for i in range(len(table[(nt,t)])-1):
        #                 str_nums += str(table[(nt,t)][i])
        #                 str_nums += ','
        #             str_nums += str(table[(nt,t)][-1])
        #             cur_nt_list.append(str_nums)
        #     self.table.append(cur_nt_list)

        
        
                        
                        

                    
            
            
            
                      
                
                    
        
        

    def button_event(self):
        self.progress_text.insert(tkinter.END,"new_result\n")

        self.file_init()
        self.read_facts_into_rules()
        self.check_left_recursion()
        self.check_left_factoring()
        
        self.inference_engine()
        
        self.construct_first_and_nullable()
        self.construct_follow()
        
        self.construct_table()
        
            
            
        
        self.ofile.close()


    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
        
        

        

        
        
    
        
        


if __name__ == "__main__":
    app = GUI()
    app.start()
