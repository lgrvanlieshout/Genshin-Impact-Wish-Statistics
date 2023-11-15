# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:11:47 2023

@author: Levi van Lieshout (Netherlands), also known as Togira_ on HoyoLab

You can edit, implement, store, sell, whatever you want to do with this code, 
as long as you credit me properly. 
Also, I would love to hear it if you are some Genshin assisting website such 
as paimon.moe, genshin.hotgames.gg, genshin optimizer, etc. and you want to 
add a wishing chance calculating feature to your website.

The mathematical basis of this code is explained in this article on HoYoLab: 
    ...

If you have any questions regarding this program, you can e-mail me on:
    165093adriestarleerling.nl@gmail.com


"""

import matplotlib.pyplot as plt




# --------------------- list initializations -----------------------

p_C0_pity_list = []
p_C0_list = []
p_w_pity_list = []
p_w_list = []

# --------------------- construct drop chance lists ------------------------

# create list of drop chance of 5-star characters
drop_chance = [0]
for x in range(73):
    drop_chance.append(0.006)
for x in range(16):
    drop_chance.append((x+1)*0.06+0.006)
drop_chance.append(1)



# create list of drop chance of 5-star weapons
drop_chance_w = [0]
for x in range(62):
    drop_chance_w.append(0.007)
for x in range(14):
    drop_chance_w.append((x+1)*0.07+0.007)
drop_chance_w.append(1)


#---------------------- function definitions character banner -----------------------

# pulling distribution functions of getting a 5-star character for the first time at pull a

def p(a, pity=0):
    if type(a) == int:
        if a+pity>90:
            return 0
        else:
            prod = 1
            for x in range(pity, a+pity):
                prod = prod*(1-drop_chance[x])
            return drop_chance[a+pity]*prod
    if type(a) == range:
        value = []
        for x in range(len(a)):
            prod = 1
            if x+pity>90:
                value.append(0)
            else:
                for b in range(pity, x+pity):
                    prod = prod*(1-drop_chance[b])
                value.append(drop_chance[x+pity]*prod)
        return value
    else:
        return 0



# ------------------ function definitions for weapon banner -------------------


# Probability distribution function of getting a 5-star weapon for the first time at pull a.
def p_w(a, pity=0):
    if type(a) == int:
        if a+pity>77:
            return 0
        else:
            prod = 1
            for x in range(pity,a):
                prod = prod*(1-drop_chance_w[x])
            return drop_chance_w[a]*prod
    if type(a) == range:
        value = []
        for x in range(len(a)):
            if x+pity>77:
                value.append(0)
            else:
                prod = 1
                for b in range(pity,x):
                    prod = prod*(1-drop_chance_w[b])
                value.append(drop_chance_w[x]*prod)
        return value
    else:
        return 0



# -------------------- function definitions to combine the above functions ----------------------
# --------------------              and to make stuff easier               ----------------------


def p_combine(f_list, g_list, a):
    values = []
    for x in range(a+1):
        chance = 0
        for b in range(x):
            chance+=f_list[b]*g_list[x-b]
        values.append(chance)
    return values


def P_f(f_list, a):
    if type(a) == int:
        return round(sum(f_list)*100, 2)
    elif type(a) == range:
        values = []
        for b in range(len(a)):
            values.append(sum(f_list[0:b+1]))
        return values


def plot(f_list, title, ylabel, xlabel):
    a = len(f_list)
    w = range(a)
    plt.plot(w,f_list)
    plt.axis((0,a,plt.axis()[2],plt.axis()[3]))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()
    

# ------------------------ final function --------------------------

def chance(goal, wishes=0, character_pity=0, weapon_pity=0, guarantee = "no"):
    """
    This function returns the chance of obtaining the goal within "wishes" number of wishes
    given a certain pity and guarantee or not.

    Parameters
    ----------
    goal : string
        choose from: "any 5-star character", "any 5-star weapon", or any combination of 
        constellations and refinements. For example: "C0" means the featured character.
        "C1" is two copies of the featured character."R1" means obtaining the desired 
        featured weapon once. "C3R1" means four copies of a featured character and a 
        signature weapon.
    wishes : integer or list, optional
        Number of wishes you want to spend. The default is 0.
    character_pity : integer, optional
        The amount of pity you have for the character banner. The default is 0.
    weapon_pity : integer, optional
        The amount of pity you have for the weapon banner. The default is 0.
    guarantee : string, optional
        "yes" or "no". Applies to character banner only. The default is "no".

    Returns
    -------
    float
        Chance of obtaining the goal within "wishes" number of wishes, given pity and guarantee.

    """
    if type(wishes) == int:
        a = wishes
    elif type(wishes) == range:
        a = max(wishes)
    goal = goal.lower()
    
    #------------------- easy computations ---------------------
    
    if goal == "any character" or (goal == "c0" and guarantee == "yes"):
        p_pity_list = []
        for i in range(a+1):
            p_pity_list.append(p(i, character_pity))
        
        print(str(P_f(p_pity_list, wishes))+"%")
        return P_f(p_pity_list, wishes)
    
    
    elif goal == "any weapon":
        p_pity_list = []
        for i in range(a+1):
            p_pity_list.append(p_w(i, weapon_pity))
        
        print(str(P_f(p_pity_list, wishes))+"%")
        return P_f(p_pity_list, wishes)
    
    
    
    #------------------- determining goal ---------------------
    
    characters, refinements = 0,0
    
    prev = ''
    for letter in goal:
        if letter.isdigit() == True and prev == "c":
            characters = int(letter)+1
        elif letter.isdigit() == True and prev == "r":
            refinements = int(letter)
        prev = letter
    
    
    
    #------------------- function definitions --------------------
    
    def p_C0(a, pity=0):
        if type(a) == int:
            chance = p(a, pity)/2
            for b in range(a):
                chance+=p(b, pity)*p(a-b)/2
            return chance
        if type(a) == range:
            values = []
            for x in range(len(a)):
                chance = p(x, pity)/2
                for b in range(x):
                    chance+=p(b, pity)*p(x-b)/2
                values.append(chance)
            return values
    
    
    def p_R1(a, pity=0):
        if type(a) == int:
            value = p_w_pity_list[a]*3/8
            for b in range(a):
                # value+=(p_w_list[b]*1/4)*(p_w_list[a-b]*1/2)
                # value+=(p_w_list[b]*3/8)*(p_w_list[a-b]*3/8)
                value+= p_w_pity_list[b]*p_w_list[a-b]*17/64
                for c in range(b):
                    # value+= (p_w_list[c]*3/8)*(p_w_list[b-c]*5/8)*p_w_list[a-b]
                    # value+= (p_w_list[c]*0.25)*(p_w_list[b-c]*0.5)*p_w_list[a-b]
                    value += p_w_pity_list[c]*p_w_list[b-c]*p_w_list[a-b]*23/64
            return value
        if type(a) == range:
            values = []
            for x in range(len(a)):
                value = p_w_list(x)*3/8
                for b in range(x):
                    value+= p_w_list[b]*p_w_list[x-b]*17/64
                    for c in range(b):
                        value += p_w_list[c]*p_w_list[b-c]*p_w_list[x-b]*23/64
                values.append(value)
            return values
    
    
    #------------------- setup of lists to reduce computation time --------------------
    
    if characters>0:
        p_pity_list = []
        for i in range(a+1):
            p_pity_list.append(p(i, character_pity))
        
        p_C0_pity_list = []
        for i in range(a+1):
            p_C0_pity_list.append(p_C0(i, character_pity))

        if character_pity == 0:
            p_C0_list = p_C0_pity_list
        else:
            p_C0_list = []
            for i in range(a+1):
                p_C0_list.append(p_C0(i))
                
    if refinements>0:
        p_w_pity_list = []
        for i in range(a+1):
            p_w_pity_list.append(p_w(i, weapon_pity))
        
        if weapon_pity == 0:
            p_w_list = p_w_pity_list
        else:
            p_w_list = []
            for i in range(a+1):
                p_w_list.append(p_w(i))
        
        p_R1_pity_list = []
        for i in range(a+1):
            p_R1_pity_list.append(p_R1(i, weapon_pity))
            
        
        if weapon_pity == 0:
            p_R1_list = p_R1_pity_list
        else:
            p_R1_list = []
            for i in range(a+1):
                p_R1_list.append(p_R1(i))
    
    
    
    #------------------- mix and match functions -----------------
    
    if guarantee == "no" and characters>0:
        char_fct_lists = [p_C0_pity_list]
    elif guarantee == "yes" and characters>0:
        char_fct_lists = [p_pity_list]
    elif characters == 0:
        pass
    else:
        print("invalid guarantee input")
    if refinements>0:
        weap_fct_lists = [p_R1_pity_list]
    
    
    for i in range(characters-1):
        char_fct_lists.append(p_combine(p_C0_list, char_fct_lists[-1], a))
    
    for i in range(refinements-1):
        weap_fct_lists.append(p_combine(p_R1_list, weap_fct_lists[-1], a))

    
    if characters>0 and refinements>0:
        chance_list = p_combine(char_fct_lists[-1], weap_fct_lists[-1], a)
        print(str(P_f(chance_list, wishes))+"%")
        return P_f(chance_list, wishes)
    elif characters>0 and refinements == 0:
        print(str(P_f(char_fct_lists[-1], wishes))+"%")
        return P_f(char_fct_lists[-1], wishes)
    elif characters == 0 and refinements>0:
        print(str(P_f(weap_fct_lists[-1], wishes))+"%")
        return P_f(weap_fct_lists[-1], wishes)
    
    print("You probably made a typo. Please try again.")


# -------------------------- program loop ------------------------------

running = True
noob = True

while running:
    if noob:
        print("Welcome to this wish chance calculator. The questions you will get "+
              "(if applicable) to calculate your odds, are:\n"+"\n"+
              "goal (any character, any weapon, C0, R1, C4R2, etc.):\n"+
              "number of wishes:\n"+
              "pity for the character banner:\n"+
              "guarantee (yes/no):\n"+
              "pity for the weapon banner:\n"+
              "Would you like to see a graph of your chances? (yes/no):\n"+"\n"+
              "The tutorial will explain each question in more detail.")
        tutorial = input("Would you like to follow the tutorial? (yes/no): ")
    noob = False
    
    if tutorial == "yes":
        print("\n Welcome to the tutorial. You will now be guided step-by-step through" +  
              " program. Let's get started.\n" + 
              "(hit enter to reveal a new line of the tutorial).")
        input()
        input("The first question is about your goal.")
        input("You will now be shown all possible entries for this question, "+
              "hopefully making clear what the question is about.\n")
        input("If you want to know your chances of obtaining your next 5-star character, "+
              "just enter: any character.")
        input("Please do not enter the name of the character, because this program "+
              "doesn't know the names of Genshin characters.\n ")
        input("If you want to know your odds of obtaining your next 5-star weapon "+
              "on the weapon banner, just enter: any weapon. Note that this program also doesn't "+
              "recognize weapon names.\n")
        input("If you would like your odds of getting a featured 5-star character, enter: C0. " + 
              "This is because a new 5-star character is a C0 character (it has constellation 0).\n")
        input("You can also calculate your chances for higher constellations or more characters. "+
              "Simply enter the constellation you want, for example: C2.")
        input("Note that a C2 character is the same as getting featured characters three times.\n")
        input("You can also calculate the chance of getting the 5-star weapon you select on the "+
              "weapon banner. Enter 'R1' for the chances of obtaining the selected weapon once, "+ 
              "and R2 for getting the weapon twice, etc.\n")
        input("Lastly, you can also combine characters and weapons. For example, entering: C2R1 "+
              "means that you will calculate the odds of getting a featured character three times "+
              "and the weapon you selected on the weapon banner.\n")
        input("This is all you need to know about the 'goal' question, we will now review the "+
              "rest of the program quickly.\n")
        input("The next question you get is to enter the number of wishes. This is the number of "+
              "wishes you want to calculate your chances for. For example, if you enter 50, the "+
              "program will calculate your odds of obtaining your goal within 50 wishes.\n")
        input("Next, depending on your goal, the program will ask about your pity for the "+
              "character banner, the weapon banner or both. Your pity is the number of "+
              "wishes that you have made after obtaining your previous 5-star item. You can"+
              " check your pity in the wish history in Genshin Impact, or you can use a "+
              "website as paimon.moe or a similar website to calculate your pity.\n")
        input("After you get a standard character on a non-standard banner, you are guaranteed "+
              "that the next 5-star is the featured 5-star character. This question asks "+
              "whether this is the case or not.\n")
        input("Finally, the program asks whether you want to see a graph of your chances. This "+
              "question is pretty straightforward.\n Last, but not least: you can quit this program "+
              "simply by hitting 'enter' as answer to a question.\n"+
              "\n"+"Enjoy!\n")
        tutorial = "no"
        
    
    
    goal = input("goal (any character, any weapon, C0, R1, C4R2, etc.): ").lower()
    if goal == "":
        running = False
        continue
    wishes = input("number of wishes: ")
    if wishes == "":
        running = False
        continue
    wishes = int(wishes)
    
    
    # --------- determining goal -------------
    characters, refinements = 0,0
    
    prev = ''
    for letter in goal:
        if letter.isdigit() == True and prev == "c":
            characters = int(letter)+1
        elif letter.isdigit() == True and prev == "r":
            refinements = int(letter)
        prev = letter
    
    # ---------- determining next questions ----------
    character_pity = 0
    weapon_pity = 0
    guarantee = "no"
    
    if characters>0 or goal == "any character":
        character_pity = int(input("pity for the character banner: "))
        if character_pity == "":
            running = False
            continue
        if characters>0:
            guarantee = input("guarantee (yes/no): ")
            if guarantee == "":
                running = False
                continue
    if refinements>0 or goal == "any weapon":
        weapon_pity = int(input("pity for the weapon banner: "))
        if weapon_pity == "":
            continue
    
    graph = input("Would you like to see a graph of your chances? (yes/no): ")
    print("")
    if graph == "":
        running = False
        continue
    if graph == "yes":
        plot(chance(goal, range(wishes+40), character_pity, weapon_pity, guarantee), 
             "Chance of pulling " + goal, "chance", "number of pulls")
    else:
        print("The chance of obtaining your goal is: ")
        chance(goal, wishes, character_pity, weapon_pity, guarantee)
    print("")


# -------------------------- test space ------------------------------


















