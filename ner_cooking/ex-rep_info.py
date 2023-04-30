from glob import glob
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import argparse


def name(recipe_soup):
    tag = recipe_soup.find("h1", {"class": "gz-title-recipe gz-mBottom2x"}).text
    return tag


def category(recipe_soup):
    tag = recipe_soup.find("div", {"class": "gz-title-content gz-innerdesktop"}).div.ul.li.text
    return tag


def steps(recipe_soup):
    steps = dict()
    all_recipes_tag = recipe_soup.find_all("div", {"class": "gz-content-recipe-step"})
    for i, recipe_name in enumerate(all_recipes_tag):
        list_tag_remove = recipe_name.find_all("span", {"class": "num-step"})
        for tag in list_tag_remove:
            tag.extract()
        steps[i] = recipe_name.p.text
    return steps


def extract_ingredients(recipe_soup):
    ingredients = dict()
    all_recipes_tag = recipe_soup.find_all("dd", {"class": "gz-ingredient"})
    for recipe_name in all_recipes_tag:
        name = recipe_name.a.text.strip().replace("\t", "").replace("\n", "")
        quantity = recipe_name.span.text.strip().replace("\t", "").replace("\n", "")
        ingredients[name] = quantity
    return ingredients


def infobox(recipe_soup):
    data = dict()
    all_recipes_tag = recipe_soup.find_all("span", {"class": "gz-name-featured-data"})
    for recipe_name in all_recipes_tag:
        single_data = [i.strip() for i in recipe_name.text.split(':')]
        if len(single_data) > 1:
            data[single_data[0]] = single_data[1]

    return data


def run():

    parser = argparse.ArgumentParser(description='''script to extract the selected information from all html of the 
    recipes''')

    parser.add_argument("--input", default="./data/recipes", help='''specify the path to the folders from which to 
    extract recipe html''')

    parser.add_argument("--output", default="./data", help='''the path to the folder in which to save the results''')

    args = parser.parse_args()

    output = args.output
    input_path = args.input

    list_recipes = glob(f"{input_path}\\*", recursive=True)

    all_ingredients = set()
    all_data = list()
    for recipe in tqdm(list_recipes):
        single_recipe = dict()
        with open(recipe, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            single_recipe['recipe'] = name(soup)

            # ingredients
            ingredients = extract_ingredients(soup)
            single_recipe['ingredients'] = ingredients
            for ingredient in ingredients.keys():
                all_ingredients.add(ingredient)

            single_recipe['category'] = category(soup)
            single_recipe['infobox'] = infobox(soup)
            single_recipe['steps'] = steps(soup)
        all_data.append(single_recipe)

    with open(f'{output}//all_data.json', 'w') as f:
        json.dump(all_data, f)

    with open(f'{output}//all_ingredients.json', 'w') as f:
        json.dump({'recipe': list(all_ingredients)}, f)

# https://online.scuola.zanichelli.it/enogastronomiacucina/erbe-spezie-aromi/
# https://www.cibo360.it/cucina/glossario/glossario_cucina_il.html
# https://www.fragolosi.it/glossario/
