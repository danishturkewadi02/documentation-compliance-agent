import json
import time
from collections import defaultdict

from src.groq_client import client


def find_page(requirement, pages):

    requirement = requirement.lower()

    # Settings
    if (
        "settings" in requirement
        or "profile" in requirement
        or "notification" in requirement
        or "change password" in requirement
        or "save changes" in requirement
        or "security" in requirement
    ):
        return pages.get("settings.json", {})

    # Login
    elif (
        "login" in requirement
        or "email" in requirement
        or "forgot" in requirement
        or (
            "password" in requirement
            and "change password" not in requirement
            and "security" not in requirement
        )
    ):
        return pages.get("login.json", {})

    # My Applications
    elif (
        "my applications" in requirement
        or "dashboard" in requirement
    ):
        return pages.get("my_applications.json", {})

    # Facilities
    elif (
        "facility" in requirement
        or "facilities" in requirement
    ):
        return pages.get("facilities.json", {})

    # Action Items
    elif "action" in requirement:
        return pages.get("action_items.json", {})

    # User Management
    elif "user" in requirement:
        return pages.get("user_management.json", {})

    # Announcements
    elif "announcement" in requirement:
        return pages.get("announcements.json", {})

    # FAQs
    elif "faq" in requirement:
        return pages.get("faqs.json", {})

    # Tickets
    elif "ticket" in requirement:
        return pages.get("tickets.json", {})

    # Contact
    elif "contact" in requirement:
        return pages.get("contact.json", {})

    # Landing Page
    return pages.get("landing_page.json", {})


def analyze(requirements, pages):

    print("\n========== GROUPING REQUIREMENTS ==========\n")

    grouped = defaultdict(
        lambda: {
            "page_json": {},
            "requirements": []
        }
    )

    for requirement in requirements:

        page = find_page(
            requirement,
            pages
        )

        page_name = page.get(
            "page",
            "landing_page"
        )

        grouped[page_name]["page_json"] = page

        grouped[page_name]["requirements"].append(
            requirement
        )

    results = []

    passed = 0

    print("\n========== AI ANALYSIS ==========\n")

    # One Groq request per page
    for page_name, info in grouped.items():

        print(f"\nAnalyzing Page : {page_name}")

        page = info["page_json"]

        requirement_text = "\n".join(info["requirements"])

        prompt = f"""
You are a Software Documentation Compliance Auditor.

Compare the following documentation requirements with the website page.

Requirements:

{requirement_text}

Website JSON:

{json.dumps(page, indent=2)}

Instructions:

1. Compare EVERY requirement.
2. Return one result for EACH requirement.
3. Status must be PASS, FAIL or PARTIAL.
4. Mention the correct page.
5. Give a short reason.

Return ONLY valid JSON.

Example:

[
  {{
    "requirement":"Enter your Email",
    "status":"PASS",
    "page":"login",
    "reason":"Email textbox exists."
  }},
  {{
    "requirement":"Forgot Password",
    "status":"FAIL",
    "page":"login",
    "reason":"Forgot Password link missing."
  }}
]
"""

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0

            )

            answer = response.choices[0].message.content

            answer = answer.replace("```json", "")
            answer = answer.replace("```", "")
            answer = answer.strip()

            data = json.loads(answer)

        except Exception as e:

            print("Groq Error:", e)

            # Create FAIL entries if AI request fails
            data = []

            for req in info["requirements"]:

                data.append({

                    "requirement": req,

                    "status": "ERROR",

                    "page": page_name,

                    "reason": "AI analysis could not be completed because the Groq API daily quota was exceeded. Please try again after the quota resets."
                })

        for item in data:

            req = item["requirement"].lower()

    # ---------- SETTINGS ----------
            if (
             "profile" in req
                or "settings" in req
                or "notification" in req
                or "change password" in req
                or "save changes" in req
                or "security" in req
            ):

                item["page"] = "settings"

    # ---------- LOGIN ----------
            elif (
             "login" in req
                or "email" in req
                or "forgot" in req
            or (
            "password" in req
            and "change password" not in req
            and "security" not in req
            )
            ):

                item["page"] = "login"

    # ---------- MY APPLICATIONS ----------
            elif (
        "my applications" in req
        or "dashboard" in req
            ):

                 item["page"] = "my_applications"

    # ---------- FACILITIES ----------
            elif (
        "facility" in req
        or "facilities" in req
            ):

                item["page"] = "facilities"

    # Keep original page if no rule matches
            else:

                item["page"] = page_name

            if item["status"] == "PASS":

                 passed += 1

            results.append(item)

        # Small delay between page requests
        time.sleep(2)

    compliance = round(

        (passed / len(results)) * 100,

        2

    ) if results else 0

    return {

        "overall_compliance": compliance,

        "results": results

    }