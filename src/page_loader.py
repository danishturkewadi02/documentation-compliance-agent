import json
import os


def load_pages():

    pages = {}

    folder = "data/pages"

    for file in os.listdir(folder):

        if file.endswith(".json"):

            with open(

                os.path.join(folder,file),

                encoding="utf-8"

            ) as f:

                pages[file] = json.load(f)

    return pages