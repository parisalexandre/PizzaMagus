#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Main function - see README for more informations

Author: Alexandre Paris
"""

import sys
import random
from spellchecker import SpellChecker

sys.path.append('./libs')
from read_menu_euro import read_menu_euro
from read_menu_point import read_menu_point


################################################################################
def questions(list_ingredients, spell, beurk, miam):
    """
    Ask questions about favorite ingredients (miams)
    and non-wanted ingredients (beurks)
    """
    beurks = list(map(str, beurk.lower().split(' ')))

    for i, b in enumerate(beurks):
        if b not in spell and b not in list_ingredients:
            beurks[i] = spell.correction(b)

    miams = list(map(str, miam.lower().split(' ')))

    if '' in miams:
        miams = []

    for i, m in enumerate(miams):
        if m not in spell and m not in list_ingredients:
            miams[i] = spell.correction(m)

    not_in_list = []
    for i, m in enumerate(miams):
        if m in list_ingredients:
            pass
        else:
            not_in_list.append(m)

    if len(not_in_list) > 0:
        if len(not_in_list) == 1:
            raise ValueError(f"Sorry, your favorite ingredient '{not_in_list[0]}' is not available...")
        else:
            raise ValueError(f"Sorry, your favorite ingredients '{', '.join(not_in_list[:-1])} and '{not_in_list[-1]}' are not available")

    for i, ingredient in enumerate(not_in_list):
        miams.remove(ingredient)

    return beurks, miams


################################################################################
def language(lan_input):
    """
    Ask the language of the menu for good text detection
    """
    #print("What is the language of the pizzeria menu ?")
    lan = lan_input
    if lan not in ['en', 'es', 'fr', 'it']:
        raise ValueError("Invalid language code. Please use 'en' for English, 'es' for Spanish, 'fr' for French, or 'it' for Italian.")
    spel = SpellChecker(language=f'{lan}')
    return spel


################################################################################
def random_select(pizz):
    """
    Select a random pizza in the list 'pizz'
    """
    sel = random.randint(0, len(pizz) - 1)
    for i, n in enumerate(pizz):
        if i == sel:
            name = n
    ingr = list(map(str.lower, pizz[name]['ingredients']))
    pri = pizz[name]['price']
    return name, ingr, pri


################################################################################
def log_message(message, condition):
    if condition:
        return message
    return None


################################################################################
def choice(inclus, exclus, pizz):
    """
    Main algorithm
    """
    message1 = None
    message2 = None
    # Start with the exclusion of pizzas that contain beurks/exclus
    pcop = pizz.copy()
    for i, n in enumerate(pcop):
        for exc in exclus:
            if n in pizz.keys():
                if exc in list(map(str.lower, pizz[n]['ingredients'])):
                    pizz.pop(n)
    if len(pizz) == 0:
        raise ValueError("Sorry, none of the pizzas correspond to your choices...\nThere are too many ingredients you don't like")

    # Now let's get a pizza that contains miams/inclus
    name, ingr, pri = random_select(pizz)
    # Case with only one ingredient chosen
    if len(inclus) == 1:
        pcop = pizz.copy()
        for i, n in enumerate(pcop):
            if inclus[0] not in list(map(str.lower, pizz[n]['ingredients'])):
                pizz.pop(n)
        if len(pizz) > 0:
            name, ingr, pri = random_select(pizz)
        else:
            raise ValueError('Sorry, none of the pizzas correspond to your choices...\nPlease try again with other ingredients!')

    # Case with more than 1 favorite ingredient
    elif len(inclus) > 1:
        # Keep only pizzas with at least 1 favorite ingredient
        pcop = pizz.copy()
        interlist = []
        for i, n in enumerate(pcop):
            if len(list(set(inclus).intersection(map(str.lower, pizz[n]['ingredients'])))) == 0:
                pizz.pop(n)
            else:
                interlist.append(list(set(inclus).intersection(map(str.lower,
                                                                   pizz[n]['ingredients']))))

        # First selection
        max_count = 100
        name, ingr, pri = random_select(pizz)
        # Check if all favorite ingredients are in the selected pizza
        for wrong in range(max_count):
            message1 = log_message('Your pizza contains all your favorite ingredients!',
                                   all(item in ingr for item in inclus))
            if message1 is not None:
                break
            # If not all, find the most
            message2 = log_message('Sorry, none of the pizzas contain all your favorite ingredients...\nYour pizza contains as many as your favorite ingredients as possible!',
                                   all(item in ingr for item in max(interlist, key=len)))
            if message2 is not None:
                break                
            name, ingr, pri = random_select(pizz)

    return name, ingr, pri, message1, message2


###################################################################################################
def main_choice(image, lan, beurk, miam):
    spell = language(lan)
    pizzas = {}
    list_ingredients = []
    for i, im in enumerate(image):
        pizza, list_ingredient = read_menu_euro(im, spell)
        if len(pizza) == 0:
            pizza, list_ingredient = read_menu_point(im, spell)
        pizzas.update(pizza)
        list_ingredients.extend(item for item in list_ingredient if item not in list_ingredients)
    
    beurks, miams = questions(list_ingredients, spell, beurk, miam)
    
    name, ingr, pri, message1, message2 = choice(miams, beurks, pizzas)
   
    result = [name, ingr, pri] 
    return result, message1, message2
    print('---------------------------------------')
    print('Here is your pizza: >>> ', name, ' <<<')
    print(f'It costs {pri} and here is the list of ingredients:', ', '.join(ingr))
    
    print(' ____        ')
    print('/    \                            ')
    print('  u  u|      _______     ')
    print('    \ |  .-``#%&#&%#``-. ')
    print('   = /  ((%BON APPETIT%))')
    print("    |    `-._#%&##&%_.-' ")
    print(" /\/\`--.   `-.``.-`     ")
    print(' |  |    \   /`./        ')
    print(" |\/|  \  `-'  /         ")
    print(' || |   \     /          ')


##################################################################################################

if __name__ == '__main__':
    main_choice(image, spell)
