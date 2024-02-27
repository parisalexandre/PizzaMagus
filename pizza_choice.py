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
            print(not_in_list)
            print(f"Sorry, your favorite ingredient '{not_in_list[0]}' is not available...")
        else:
            print(f"Sorry, your favorite ingredients '{', '.join(not_in_list[:-1])} and '{not_in_list[-1]}' are not available")

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
def choice(inclus, exclus, pizz):
    """
    Main algorithm
    """
    # Start with the exclusion of pizzas that contain beurks/exclus
    pcop = pizz.copy()
    for i, n in enumerate(pcop):
        for exc in exclus:
            if n in pizz.keys():
                if exc in list(map(str.lower, pizz[n]['ingredients'])):
                    pizz.pop(n)

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
            print('\nSorry, none of the pizzas correspond to your choices...')
            print('Please try again with other ingredients!')
            sys.exit()

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
            if all((item in ingr for item in inclus)):
                print('\nYour pizza will contain all your favorite ingredients!')
                break
            # If not all, find the most
            for wrong in range(max_count):
                if max(interlist, key=len) in ingr:
                    print('\nSorry, none of the pizzas contain all your favorite ingredients...')
                    print('Your pizza will contain as many as your favorite ingredients as possible!\n')
                    break
                name, ingr, pri = random_select(pizz)

    return name, ingr, pri


###################################################################################################
def main_choice(image, lan, beurk, miam):
    print('       _              ')
    print('      (_)             ')
    print(' _ __  _ __________ _ ')
    print("| '_ \| |_  /_  / _` |")
    print('| |_) | |/ / / / (_| |')
    print('| .__/|_/___/___\__,_|')
    print('| |       ')
    print('|_|       ')
    print('          ')
    print('Welcome! Let me help you to find a pizza. First, a few questions.\n')
    
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
    
    name, ingr, pri = choice(miams, beurks, pizzas)
    
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
