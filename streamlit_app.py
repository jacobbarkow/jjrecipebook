import streamlit as st
import pandas as pd
from recipe_dict import recipe_dict


def format_ingredients(ingredients):
    text = ''
    for i in range(len(ingredients)):
        if ingredients[i][0] == 'to taste':
            text += '* **' + ingredients[i][1] + \
                '**, **' + ingredients[i][0] + '**\n'
        elif ingredients[i][0].replace('-', '').isnumeric():
            text += '* **' + ingredients[i][0] + \
                ' ' + ingredients[i][1] + '**\n'
        else:
            text += '* **' + ingredients[i][0] + \
                '** of **' + ingredients[i][1] + '**\n'

    return text


def format_steps(steps, substeps):
    text = ''
    if substeps:
        for category in steps:
            text += '**' + category + '**\n'
            for i in range(len(steps[category])):
                text += str(i + 1) + '. ' + steps[category][i] + '\n'
            text += '\n'

    else:
        for i in range(len(steps)):
            text += str(i + 1) + '. ' + steps[i] + '\n'

    return text


def format_extras(extras):
    text = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    for i in range(len(extras)):
        text += '*' + extras[i] + '*' + ('' if i == len(extras) - 1 else ', ')

    return text


def integrity_check(recipe_dict, field_list):
    for r in recipe_dict:
        for f in field_list:
            if f not in recipe_dict[r]:
                st.write(f'''{f} not found in recipe {r}. Halting.''')
                st.stop()


mandatory_fields = ['substeps', 'protein']
integrity_check(recipe_dict, mandatory_fields)

st.set_page_config(layout="wide")

col1, col2 = st.columns([2, 5], gap='large')

recipe_df = pd.DataFrame.from_dict(recipe_dict, orient='index')

with col1:
    protein_list = sorted(recipe_df.protein.unique())
    proteins = st.multiselect('Select a protein:', protein_list)
    recipes = sorted(recipe_df[recipe_df.protein.isin(proteins)].index)
    recipe_name = st.selectbox('Select a recipe:', recipes)

with col2:
    with st.container(border=True):
        if recipe_name:
            recipe = recipe_dict[recipe_name]
            st.title(recipe_name)
            if 'sourceName' in recipe:
                st.write('*Adapted From*: ' + '[' + recipe['sourceName'] +
                         '](' + recipe['sourceURL'] + ')')
            st.header('Ingredients')
            st.write(format_ingredients(recipe['ingredients']))
            if 'toppings' in recipe:
                st.write('**Top With**')
                st.write(format_extras(recipe['toppings']))
            if 'veggies' in recipe:
                st.write('**Veggie Side Options**')
                st.write(format_extras(recipe['veggies']))
            if 'carbs' in recipe:
                st.write('**Carb Side Options**')
                st.write(format_extras(recipe['carbs']))
            st.header('Steps')
            st.write(format_steps(recipe['steps'], recipe['substeps']))
        else:
            st.header('Please select a recipe!')
