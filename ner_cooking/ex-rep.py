import os
from glob import glob
from bs4 import BeautifulSoup
import argparse
from ner_cooking.scraper import RecipesScraper


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sleep_time", default=5)
    parser.add_argument("--output", default="./data")
    parser.add_argument("--max_size", default=100)

    args = parser.parse_args()

    sleep_time = int(args.sleep_time)
    max_size = int(args.max_size)
    output = args.output

    list_categories = glob("data\\categories\\*", recursive=True)
    list_recipes_already_scraped = os.listdir("data\\recipes")
    list_urls = list()
    for repo in list_categories:
        list_pages = glob(f"{repo}\\*", recursive=True)

        for page in list_pages:
            with open(page, 'rb') as f:
                soup = BeautifulSoup(f.read(), 'lxml')
            all_recipes_tag = soup.find_all("h2", {"class": "gz-title"})
            for recipe_tag in all_recipes_tag:
                recipe_url = recipe_tag.a['href']
                recipe_name = recipe_url.split('/')[-1]
                if recipe_name not in list_recipes_already_scraped:
                    list_urls.append(recipe_url)

    path_output = os.path.join(output, 'recipes')
    man = RecipesScraper(urls=list_urls[:max_size], waiting_time=sleep_time, output_dir=path_output)
    man.start()
