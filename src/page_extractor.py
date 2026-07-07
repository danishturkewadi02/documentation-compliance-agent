import json
import os


def get_texts(locator):
    """
    Safely extract non-empty text from a Playwright locator.
    """
    values = []

    try:
        count = locator.count()

        for i in range(count):

            try:
                text = locator.nth(i).inner_text().strip()

                if text:
                    values.append(text)

            except:
                pass

    except:
        pass

    return values


def get_attributes(locator, attribute):

    values = []

    try:
        count = locator.count()

        for i in range(count):

            try:
                value = locator.nth(i).get_attribute(attribute)

                if value:
                    values.append(value)

            except:
                pass

    except:
        pass

    return values


def save_page(page, page_name):

    page_data = {

        "page": page_name,

        "title": page.title(),

        "url": page.url,

        "headings": get_texts(
            page.locator("h1,h2,h3,h4,h5,h6")
        ),
        "buttons": get_texts(
        page.locator("button")
        )[:30],

        "links": get_texts(
        page.locator("a")
        )[:30],
        "paragraphs": get_texts(
        page.locator("p")
        )[:20],
        "labels": get_texts(
            page.locator("label")
        ),

        "tables": get_texts(
            page.locator("table")
        ),

        "cards": get_texts(
            page.locator("[class*=card]")
        ),

        "navigation": get_texts(
            page.locator("nav")
        ),

        "list_items": get_texts(
            page.locator("li")
        ),

        "input_placeholders": get_attributes(
            page.locator("input"),
            "placeholder"
        ),

        "input_names": get_attributes(
            page.locator("input"),
            "name"
        ),

        "input_ids": get_attributes(
            page.locator("input"),
            "id"
        ),

       "all_visible_text": page.locator("body").inner_text()[:3000]
    }

    os.makedirs(
        "data/pages",
        exist_ok=True
    )

    with open(

        f"data/pages/{page_name}.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            page_data,

            file,

            indent=4,

            ensure_ascii=False

        )

    print(f"{page_name} saved successfully")