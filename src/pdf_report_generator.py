from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import green, red, orange, black


def generate_pdf(ai_response):

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    pdf = SimpleDocTemplate(
        "reports/compliance_report.pdf"
    )

    elements = []

    # ---------------- TITLE ----------------

    elements.append(
        Paragraph(
            "Documentation Compliance Report",
            title_style
        )
    )

    elements.append(Spacer(1, 20))
    

    # ---------------- SUMMARY ----------------

    total = len(ai_response["results"])

    passed = len(
        [x for x in ai_response["results"] if x["status"] == "PASS"]
    )

    failed = len(
        [x for x in ai_response["results"] if x["status"] == "FAIL"]
    )

    partial = len(
        [x for x in ai_response["results"] if x["status"] == "PARTIAL"]
    )
    summary = f"""
    The uploaded documentation was compared with the extracted website pages.

    A total of {total} requirements were analyzed.

    {passed} requirements passed,
    {failed} requirements failed,
    and {partial} requirements were partially implemented.

    Overall compliance score: {ai_response['overall_compliance']}%.

T   he report highlights missing or partially implemented
    features to help identify documentation and website
    mismatches.
"""
    elements.append(
    Paragraph(
        "<b>AI Compliance Summary</b>",
        heading_style
    )
)

    elements.append(
    Paragraph(
        summary,
        normal_style
    )
)

    elements.append(
    Spacer(1,20)
)
    elements.append(
        Paragraph(
            f"<b>Overall Compliance :</b> {ai_response['overall_compliance']}%",
            heading_style
        )
    )

    elements.append(
        Paragraph(f"<font color='green'><b>PASS :</b> {passed}</font>", normal_style)
    )

    elements.append(
        Paragraph(f"<font color='red'><b>FAIL :</b> {failed}</font>", normal_style)
    )

    elements.append(
        Paragraph(f"<font color='orange'><b>PARTIAL :</b> {partial}</font>", normal_style)
    )

    elements.append(
        Paragraph(f"<b>Total Requirements :</b> {total}", normal_style)
    )

    elements.append(Spacer(1, 20))

    # ---------------- REQUIREMENTS ----------------

    for i, item in enumerate(ai_response["results"], start=1):

        if item["status"] == "PASS":
            color = "green"

        elif item["status"] == "FAIL":
            color = "red"

        elif item["status"] == "PARTIAL":
            color = "orange"

        else:
            color = "black"

        elements.append(
            Paragraph(
                f"<b>Requirement {i}</b>",
                heading_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Requirement :</b><br/>{item['requirement']}",
                normal_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Status :</b> <font color='{color}'>{item['status']}</font>",
                normal_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Page :</b> {item['page']}",
                normal_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Reason :</b><br/>{item['reason']}",
                normal_style
            )
        )
        # ---------------- SCREENSHOT ----------------

        if item["status"] in ["FAIL", "PARTIAL"]:

            image_path = f"reports/screenshots/{item['page']}.png"

            if os.path.exists(image_path):

                elements.append(Spacer(1, 8))

                elements.append(
                Paragraph(
                "<b>Screenshot:</b>",
                normal_style
              )
            )

            elements.append(Spacer(1, 5))

            elements.append(
            Image(
                image_path,
                width=420,
                height=230
            )
             )

        else:

            elements.append(
            Paragraph(
                "<b>Screenshot:</b> Not Available",
                normal_style
            )
        )
        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph(
                "<font color='grey'>------------------------------------------------------------</font>",
                normal_style
            )
        )

        elements.append(Spacer(1, 15))

    pdf.build(elements)

    print("Professional PDF Report Generated Successfully")