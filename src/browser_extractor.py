from playwright.sync_api import sync_playwright
from src.navigation_mapper import get_pages
from src.page_extractor import save_page


def open_website(url, email, password):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # -----------------------
        # Landing Page
        # -----------------------

        page.goto(url)

        page.wait_for_timeout(3000)

        print("Website opened successfully")

        save_page(page, "landing_page")

        # -----------------------
        # Login Page
        # -----------------------
        
        page.get_by_text("Getting started").click()

        print("Clicked Getting started")

        page.wait_for_selector('input[type="email"]')

        save_page(page, "login")
        # -----------------------
        # Fill Credentials
        # -----------------------

        # Fill email
        page.fill(
        'input[type="email"]',
        email
        )

        # Fill password
        page.fill(
             'input[type="password"]',
            password
        )

        print("Credentials entered")

        # Wait until login page is fully loaded
        page.wait_for_timeout(2000)

            # Save Login screenshot
        page.screenshot(
          path="reports/screenshots/login.png",
          full_page=True
            )

# Save Login JSON
        save_page(
         page,
            "login"
        )

        print("Login page saved successfully")

# Click Login
        page.get_by_role(
        "button",
     name="Login"
    ).click()

        print("Login button clicked")

        page.get_by_role(
            "heading",
            name="My Applications"
        ).wait_for(timeout=15000)

        print("Dashboard loaded successfully!")

        save_page(page, "my_applications")

        page.screenshot(
            path="reports/screenshots/my_applications.png",
            full_page=True
        )

        website_text = page.locator("body").inner_text()

        with open(
            "data/website_text.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(website_text)

        print("Website text saved successfully!")

        pages = get_pages()

        base_url = "https://white-cliff-0bca3ed00.1.azurestaticapps.net"

        for page_info in pages:

            if page_info["name"] in [
            "Landing Page",
            "Login",
            "My Applications"
             ]:
                continue

            print("Visiting:", page_info["name"])

            page.goto(
                base_url + page_info["url"]
            )

            page.wait_for_timeout(3000)

            page.screenshot(
                path=f'reports/screenshots/{page_info["name"].replace(" ","_").lower()}.png',
                full_page=True
            )

            save_page(
                page,
                page_info["name"].replace(" ","_").lower()
            )

        browser.close()