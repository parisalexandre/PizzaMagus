#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Contains the function to read the image
All the algorithm is based on the euro symbol detection
If failed, another function is applied to extract names, prices and ingredients

Author: Alexandre Paris
"""

import re
import unicodedata
import pytesseract
from PIL import Image
import numpy as np


def read_menu_euro(image, spell):
    """
    Read an image looking for the euro symbol
    Then pizzas names, prices and ingredients are extracted
    For now, spell is not used
    """
    text = pytesseract.image_to_string(image,
                                       lang='eng+fra+spa+ita',
                                       config='--psm 4')
    menui = np.array(list(filter(None, text.splitlines())))

    # Remove - _ emdash
    for i in range(len(menui)):
        for char in ['\u2014', '-', '_', '--', '...', '..']:
            menui[i] = menui[i].replace(char, '')

    euro = '{}'.format(unicodedata.lookup("EURO SIGN"))
    if euro not in str(menui[0:3]):
        im = Image.open(image)
        text = pytesseract.image_to_string(im,
                                           lang='eng+fra+spa+ita',
                                           config='--psm 4')
        menui = np.array(list(filter(None, text.splitlines())))

    # Case where the price is isolated
    # Find where is euro and if too small, concatenate with the name of pizza
    menu = []
    for i, m in enumerate(menui):
        if euro in m and len(m) <= 7:
            menu.append(menui[i-1]+' '+menui[i])
        else:
            menu.append(menui[i])

    # Delete the duplicates of names
    for i, m in enumerate(menu):
        if i < (len(menu) - 1):
            if m in menu[i+1]:
                menu.remove(m)

    names = []
    prices = []
    ingredients = []

    for i, p in enumerate(menu):
        # Lookin for euro symbol
        # TO-DO: adapt to other currencies
        if euro in p:
            if menu[0][-2:] == ' '+euro:
                names.append(p.rsplit(' ', 2)[0])
                prices.append(p.rsplit(' ', 2)[1]+p.rsplit(' ', 2)[2])
            elif re.match(r'^[0-9,.{}]+$'.format(euro), p.rsplit(' ', 1)[1]) is not None:
                names.append(p.rsplit(' ', 1)[0])
                prices.append(p.rsplit(' ', 1)[1])
            #else:
            #    names.append(p.rsplit(' ', 1)[0])
            #    prices.append(p.rsplit(' ', 1)[1])
            if i == (len(menu) - 1):  # case where pizzas and prices after ingredients
                if euro in menu[i-2]:
                    ingredients.append(menu[i-1].rsplit(' ', 1))
                else:
                    ingredients.append((menu[i-2]+menu[i-1]).rsplit(' ', 1))
            else:  # pizzas and prices before ingredients
                if i == (len(menu) - 2):
                    ingredients.append(menu[i+1].rsplit(' ', 1))
                else:
                    if euro in menu[i+2]:
                        ingredients.append(menu[i+1].rsplit(' ', 1))
                    else:
                        ingredients.append((menu[i+1]+menu[i+2]).rsplit(' ', 1))

    ##############################
    ## CLEAN AND TESTS
    # Clean the list of ingredients
    for n, ing in enumerate(ingredients):
        ingredients[n] = (re.sub(r'[(),".]', '', str(ing))
                          .replace('[', '')
                          .replace(']', '')
                          .replace("'", '')
                          .replace('  ', ' ')).rsplit(' ')

    # Remove lonely and/et/y/e
    rem = ['y', 'e', 'and', 'et', 'de', 'con', 'avec', 'with', 'of',
           'from', 'al', 'a', '', 'di', 'for', 'le', 'el', 'la',
           'por', 'or', 'ou', 'o', '&']
    for i, ingr in enumerate(ingredients):
        for r in enumerate(rem):
            while r[1] in ingr:
                ingr.remove(r[1])

    # List of unique ingredients
    list_ingredients = list(set(item.lower() for sub in ingredients for item in sub))

    # Test on the price
    for i, p in enumerate(prices):
        if ',' in p:
            p = p.replace(',', '.')
        try:
            if float(p[:-1]) >= 300:
                prices[i] = f'{float(p[:-1])/100}'+' '+euro
            elif float(p[:-1]) >= 100:
                prices[i] = f'{float(p[:-1])/10}'+' '+euro
        except ValueError:
            # In this case the false price is added to the name
            prices[i] = 'unknown'
            names[i] = names[i]+' '+p[:-1]

    # Put pizzas in a dict
    pizzas = {}
    for name, price, ingredient_list in zip(names, prices, ingredients):
        pizzas[name] = {'price': price, 'ingredients': ingredient_list}

    return pizzas, list_ingredients
