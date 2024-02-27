#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Second function called if no euro was detected
The detection here is based on a point at the end of the line in the menu
"""

import re
import unicodedata
import pytesseract
import numpy as np


def read_menu_point(image, spell):
    """
    Read an image looking for a point at the end of menu line
    Then pizzas names, prices and ingredients are extracted
    For now, spell is not used
    """
    text = pytesseract.image_to_string(image,
                                       lang='eng+fra+spa+ita',
                                       config='--psm 4')
    menui = np.array(list(filter(None, text.splitlines())))

    # Remove - _ emdash
    for i in range(len(menui)):
        for char in ['\u2014', '-', '_', '...', '..']:
            menui[i] = menui[i].replace(char, '')

    menu = []
    for i, m in enumerate(menui):
        # Considering pizzas names are in uppercase
        if not m[:4].isupper():
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
        # Search for price at the end
        try:
            prices.append(float(p.rsplit(' ', 1)[1]))
        except ValueError:
            prices.append('unknown')
        name = re.findall(r'\b[A-Z\xC0-\xD6\xD8-\xDE]+\b', p)
        names.append(' '.join(name))
        ingredients.append(p.replace(' '.join(name), '')
                           .split(','))

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
    euro = '{}'.format(unicodedata.lookup("EURO SIGN"))
    for i, p in enumerate(prices):
        if p != 'unknown':
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
