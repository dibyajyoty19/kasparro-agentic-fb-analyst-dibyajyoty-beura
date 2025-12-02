from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER

pdf_path = "/mnt/data/Rahee_AI_Assignment_Dibyajyoty_Beura.pdf"

styles = getSampleStyleSheet()
style_title = ParagraphStyle('title', parent=styles['Title'], fontSize=20, spaceAfter=14)
style_heading = ParagraphStyle('heading', parent=styles['Heading2'], fontSize=14, spaceAfter=6)
style_body = ParagraphStyle('body', parent=styles['BodyText'], fontSize=11, leading=15, spaceAfter=10)

doc = SimpleDocTemplate(pdf_path, pagesize=LETTER)
content = []

content.append(Paragraph("Rahee AI – Intern Assignment", style_title))
content.append(Paragraph("Video → Personalized Itinerary | AI Approach", style_heading))
content.append(Paragraph("By: Dibyajyoty Beura", style_body))
content.append(Spacer(1, 14))

sections = [
    ("Problem Understanding",
     "Travel videos inspire people to explore destinations, but converting a reel into a usable itinerary is time‑consuming. Rahee AI should turn a shared video into a personalized itinerary—quickly and intelligently."),
    ("Key Context to Extract",
     "Destination (city, country, landmarks), activities (beach, cafes, nightlife, adventure), mood/style (romantic, party, family, luxury), duration hints (weekend/long trip), and travel group (solo/couple/friends/family)."),
    ("AI System Approach (Lightweight & Fast)",
     "1. Ingest video & metadata\n"
     "2. Extract context via small models\n"
     "3. Rank destination confidence\n"
     "4. Location Quiz for validation if confidence is low\n"
     "5. Fake/AI‑generated video detection to avoid mismatched itineraries\n"
     "6. Personalization from user preferences\n"
     "7. Retrieve POIs & generate optimized itinerary\n"
     "8. LLM final polish"),
    ("AI Enhancements",
     "• 1‑tap quiz to confirm detected location ensures accuracy\n"
     "• Fake video detection builds trust\n"
     "• Smart auto‑adjust when user edits itinerary\n"
     "• Multi‑video merging into a combined trip plan\n"
     "• Explainability button: ‘Why this plan?’"),
    ("Example Output",
     "For a Goa reel with kayaking & beach cafes → Romantic Adventure · 3 days · Budget "
     "→ Plan includes kayaking day, beach sunset points & cafe hopping."),
    ("Conclusion",
     "This system makes Rahee AI: Fast, accurate, reliable, and personal.\n"
     "Send a reel → Confirm location → Save itinerary instantly.\n"
     "Vision: Travel planning should feel magical—effortless and uniquely personalized.")
]

for title, text in sections:
    content.append(Paragraph(title, style_heading))
    content.append(Paragraph(text, style_body))

doc.build(content)

pdf_path
