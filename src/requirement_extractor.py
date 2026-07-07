import re


def extract_requirements(text):

    requirements = []

    keywords = [

        "email",
        "password",
        "login",
        "forgot",
        "logout",
        "search",
        "notification",
        "profile",
        "change password",
        "save changes",
        "settings",
        "facilities",
        "action items",
        "user management",
        "announcements",
        "tickets",
        "contact",
        "faqs",
        "new waiver request",
        "my applications",
        "dashboard"

    ]

    # Ignore these lines completely
    ignore_words = [

        "figure",
        "section",
        "workspace",
        "navigation",
        "application workspace",
        "the sidebar",
        "the header",
        "management",
        "provides navigation",
        "signed-in workspace",
        "url shared by all signed-in pages"

    ]

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) < 2:
            continue

        lower = line.lower()

        # Ignore unwanted lines
        if any(word in lower for word in ignore_words):
            continue

        # Keep only useful requirements
        if any(keyword in lower for keyword in keywords):
            requirements.append(line)

    # Remove duplicates
    requirements = list(dict.fromkeys(requirements))

    return requirements