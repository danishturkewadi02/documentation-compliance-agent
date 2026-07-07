import json
import os


def load_pages():

    pages = {}

    folder = "data/pages"

    for file in os.listdir(folder):

        if file.endswith(".json"):

            with open(

                os.path.join(folder, file),

                encoding="utf-8"

            ) as f:

                pages[file] = json.load(f)

    return pages
def check_requirement(requirement, pages):

    requirement = requirement.lower()

    for page in pages.values():

        text = json.dumps(page).lower()

        if requirement in text:

            return True

    return False
def run_compliance(requirements):

    pages = load_pages()

    report = []

    for req in requirements:

        result = check_requirement(

            req,

            pages

        )

        report.append(

            {

                "requirement": req,

                "status": "PASS" if result else "FAIL"

            }

        )

    return report    