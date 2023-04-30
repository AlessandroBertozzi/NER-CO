import os
import requests
from pathlib import Path
import time
from tqdm import tqdm


class CategoriesScraper:

    def __init__(self, urls: list or str, waiting_time: int, output_dir: str):
        self.urls = urls
        self.waiting_time = waiting_time
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def start(self):
        if isinstance(self.urls, list):
            for url in tqdm(self.urls):
                output_dir = os.path.join(self.output_dir, url.split('/')[-1])
                Path(output_dir).mkdir(parents=True, exist_ok=True)

                response = requests.get(url)
                page_number = url.split('/')[-2]
                if 'page' not in page_number:
                    page_number = 'page1'
                with open(output_dir + "/" + page_number + ".html", 'wb+') as f:
                    f.write(response.content)

                time.sleep(self.waiting_time)
        else:
            response = requests.get(self.urls)
            with open(f'{self.output_dir}/saving.html', 'wb+') as f:
                f.write(response.content)


class RecipesScraper:

    def __init__(self, urls: list or str, waiting_time: int, output_dir: str):
        self.urls = urls
        self.waiting_time = waiting_time
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def start(self):
        if isinstance(self.urls, list):
            for url in tqdm(self.urls):
                output_dir = os.path.join(self.output_dir, url.split('/')[-1])
                response = requests.get(url)
                with open(output_dir, 'wb+') as f:
                    f.write(response.content)

                time.sleep(15)
        else:
            response = requests.get(self.urls)
            output_dir = os.path.join(self.output_dir, self.urls.split('/')[-1])
            with open(output_dir, 'wb+') as f:
                f.write(response.content)
