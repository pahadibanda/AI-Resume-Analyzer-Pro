from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def generate_report(
    filename,
    resume_score,
    match_score,
    ai_review,
    jd_review
):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Analyzer Report</b>", styles["Title"]))

    story.append(
        Paragraph(
            f"<b>Resume Score:</b> {resume_score}/100",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Job Match Score:</b> {match_score}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<b>Gemini AI Resume Review</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(ai_review.replace("\n", "<br/>"), styles["BodyText"])
    )

    story.append(
        Paragraph("<b>Resume vs Job Description</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(jd_review.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(story)