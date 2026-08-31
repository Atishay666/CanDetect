from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf(
    filename,
    total,
    fraud,
    genuine,
    fraud_rate,
    summary,
    results
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b><font size=20>CanDetect AI</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "AI Based Financial Fraud Detection Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            f"<b>Total Transactions:</b> {total:,}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Fraud Transactions:</b> {fraud:,}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Genuine Transactions:</b> {genuine:,}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Fraud Rate:</b> {fraud_rate:.2f}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "<b>AI Fraud Analysis Summary</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(summary, styles["BodyText"])
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "<b>Top 20 High Risk Transactions</b>",
            styles["Heading2"]
        )
    )

    data = [
        [
            "#",
            "Amount",
            "Prediction",
            "Probability",
            "Risk"
        ]
    ]

    for i, row in enumerate(results, start=1):

        data.append([
            str(i),
            str(row["Amount"]),
            row["Prediction"],
            f'{row["Fraud Probability"]*100:.2f}%',
            row["Risk"]
        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    story.append(table)

    pdf.build(story)