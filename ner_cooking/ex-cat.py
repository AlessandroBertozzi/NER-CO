from ner_cooking.scraper import CategoriesScraper
import os
import argparse


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", default="https://www.giallozafferano.it/ricette-cat")
    parser.add_argument("--category", default="Antipasti")
    parser.add_argument("--number_pages", default=10)
    parser.add_argument("--sleep_time", default=5)
    parser.add_argument("--output", default="./data/categories")

    args = parser.parse_args()

    gz_categories = [args.category]
    number_of_pages = int(args.number_pages)
    sleep_time = int(args.sleep_time)
    output = args.output

    if not os.path.exists(output):
        os.mkdir(output)

    if gz_categories == ['all']:
        gz_categories = [
            'Primi',
            'Lievitati',
            'Dolci-e-Desserts',
            'Secondi-piatti',
            'Piatti-Unici'
        ]

    request_urls = list()

    for category in gz_categories:
        for i in range(1, number_of_pages + 1):
            if i == 1:
                request_urls.append(f'{args.url}/{category}')
            else:
                request_urls.append(f'{args.url}/page{i}/{category}')

    man = CategoriesScraper(urls=request_urls, waiting_time=sleep_time, output_dir=output)
    man.start()
