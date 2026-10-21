"""
CrimeVision AI - Official Phase 8 Demonstration PDF Generator
Generates all 5 official SmartBridge / SkillWallet demonstration documents:
1. Communication.pdf
2. Demonstration of Proposed Features.pdf
3. Team Involvement in Demonstration.pdf
4. Project Demo Planning.pdf
5. Scalability & Future Plan.pdf
"""

import os
from xml.sax.saxutils import escape as xml_escape
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "8. Project Demonstration")
os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

header_logo_left = ParagraphStyle(
    'HeaderLogoLeft',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=15,
    textColor=colors.HexColor('#0284c7')
)
header_logo_right = ParagraphStyle(
    'HeaderLogoRight',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=15,
    alignment=2,
    textColor=colors.HexColor('#1e40af')
)
doc_title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    alignment=1,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=8
)
section_title_style = ParagraphStyle(
    'SecTitle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#0f172a'),
    spaceBefore=6,
    spaceAfter=3
)
intro_style = ParagraphStyle(
    'IntroText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#334155'),
    spaceAfter=5
)
body_style = ParagraphStyle(
    'TableBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#1e293b')
)
body_bold_style = ParagraphStyle(
    'TableBodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#0f172a')
)
th_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#0f172a')
)
meta_label_style = ParagraphStyle(
    'MetaLabel',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#0f172a')
)
meta_val_style = ParagraphStyle(
    'MetaVal',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#1e293b')
)

def create_header(title: str, max_marks: str = "1 Mark"):
    story = []
    # Brand Bar
    header_data = [
        [
            Paragraph("<b>SMARTBRIDGE</b><br/><font size=7 color='#64748b'>Let's Bridge the Gap</font>", header_logo_left),
            Paragraph("<b>SKILL WALLET</b><br/><font size=7 color='#64748b'>A SmartBridge Product</font>", header_logo_right)
        ]
    ]
    header_table = Table(header_data, colWidths=[270, 270])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # Title
    story.append(Paragraph(xml_escape(title), doc_title_style))

    # Meta Table matching template
    meta_rows = [
        [Paragraph("<b>Date</b>", meta_label_style), Paragraph("15 March 2026", meta_val_style)],
        [Paragraph("<b>Team ID</b>", meta_label_style), Paragraph("Rahul-DS633", meta_val_style)],
        [Paragraph("<b>Project Name</b>", meta_label_style), Paragraph("CrimeVision AI - Intelligent Multimodal Forensic Analysis Platform", meta_val_style)],
        [Paragraph("<b>Maximum Marks</b>", meta_label_style), Paragraph(max_marks, meta_val_style)],
    ]
    meta_table = Table(meta_rows, colWidths=[140, 400])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))
    return story

def apply_table_style(table):
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))

def build_pdf(filename: str, story: list, margins=(30, 30, 28, 28)):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=margins[0],
        rightMargin=margins[1],
        topMargin=margins[2],
        bottomMargin=margins[3]
    )
    doc.build(story)
    print(f"[OK] Generated: {filepath}")

# =========================================================================
# 1. Communication
# =========================================================================
def generate_communication():
    story = create_header("Communication", max_marks="1 Mark")
    story.append(Paragraph("<b>Communication Plan:</b>", section_title_style))
    story.append(Paragraph(
        "Effective communication is essential for a successful project demonstration. This document outlines the "
        "communication strategy used within the team and with stakeholders throughout the project lifecycle, "
        "including how updates, issues, and feedback were managed.",
        intro_style
    ))

    plan_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Communication Type</b>", th_style), Paragraph("<b>Frequency</b>", th_style), Paragraph("<b>Channel / Tool</b>", th_style), Paragraph("<b>Participants</b>", th_style), Paragraph("<b>Purpose</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("Team Standup", body_bold_style), Paragraph("Daily", body_style), Paragraph("Slack / Google Meet", body_style), Paragraph("Core Development Team (Rahul Rajak & Team)", body_style), Paragraph("Review daily sprint goals, model pipeline progress (RT-DETR, Whisper, OpenCV), and active task blockers.", body_style)],
        [Paragraph("2", body_style), Paragraph("Progress Update", body_bold_style), Paragraph("Weekly", body_style), Paragraph("GitHub Projects & Email", body_style), Paragraph("Project Mentors & Evaluators", body_style), Paragraph("Report milestone completion, performance metrics, and deliverable review status.", body_style)],
        [Paragraph("3", body_style), Paragraph("Issue / Bug Discussion", body_bold_style), Paragraph("As Needed", body_style), Paragraph("GitHub Issues & Discord", body_style), Paragraph("Developers & AI Engineers", body_style), Paragraph("Troubleshoot cloud deployment memory limits, CORS policies, WebGL 3D sync, and audio conversion bugs.", body_style)],
        [Paragraph("4", body_style), Paragraph("Stakeholder Review", body_bold_style), Paragraph("Bi-Weekly", body_style), Paragraph("Google Meet / Live Demo", body_style), Paragraph("Academic Mentors & Industry Evaluators", body_style), Paragraph("Present forensic decision-support features, court-admissible PDF reports, and UI usability.", body_style)],
        [Paragraph("5", body_style), Paragraph("Final Demo Rehearsal", body_bold_style), Paragraph("Once", body_style), Paragraph("Screen Share Session", body_style), Paragraph("Entire Team & Presenter", body_style), Paragraph("End-to-end dry run of the 10-minute multimodal demonstration covering live video, audio, and image workflows.", body_style)],
    ]
    t1 = Table(plan_data, colWidths=[25, 105, 55, 95, 120, 150])
    apply_table_style(t1)
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Communication Challenges &amp; Resolutions:</b>", section_title_style))
    chal_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Challenge Faced</b>", th_style), Paragraph("<b>Resolution / Action Taken</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("Render cloud hosting free-tier 512MB RAM limitation caused out-of-memory container terminations when importing large neural network models.", body_style), Paragraph("Switched to CPU-only PyTorch build, lightweight OpenCV contour tracking, Whisper Base model, and implemented defensive fallback data responses.", body_style)],
        [Paragraph("2", body_style), Paragraph("Cross-Origin Resource Sharing (CORS) and path mismatch between Vercel frontend deployment and Render backend gateway.", body_style), Paragraph("Configured Flask-CORS (origins='*'), standardized unified /api/ endpoints, and synchronized static media assets directly to Vercel.", body_style)],
        [Paragraph("3", body_style), Paragraph("Coordinating synchronous temporal playback across 2D CCTV video player and 3D spatial coordinate projection in Three.js.", body_style), Paragraph("Implemented unified HTML5 player time-update listeners driving 3D suspect trajectory coordinates at 1Hz synchronized intervals.", body_style)],
    ]
    t2 = Table(chal_data, colWidths=[30, 240, 280])
    apply_table_style(t2)
    story.append(t2)

    build_pdf("Communication.pdf", story)

# =========================================================================
# 2. Demonstration of Proposed Features
# =========================================================================
def generate_features():
    story = create_header("Demonstration of Proposed Features", max_marks="1 Mark")
    story.append(Paragraph("<b>Demonstration of Proposed Features:</b>", section_title_style))
    story.append(Paragraph(
        "This document captures all the features that were proposed during the project planning phase and tracks "
        "whether each feature was successfully implemented and demonstrated. It serves as evidence of the "
        "team's ability to deliver on the proposed solution.",
        intro_style
    ))

    feat_th = ParagraphStyle('FTh', parent=th_style, fontSize=7.2, leading=8.8)
    feat_body = ParagraphStyle('FBody', parent=body_style, fontSize=7.2, leading=8.8)
    feat_bold = ParagraphStyle('FBold', parent=body_bold_style, fontSize=7.2, leading=8.8)

    feat_data = [
        [Paragraph("<b>S.No</b>", feat_th), Paragraph("<b>Feature Name</b>", feat_th), Paragraph("<b>Description</b>", feat_th), Paragraph("<b>Status<br/>(Implemented / Partial / Pending)</b>", feat_th), Paragraph("<b>Demonstrated<br/>(Yes / No)</b>", feat_th), Paragraph("<b>Remarks</b>", feat_th)],
        [Paragraph("1", feat_body), Paragraph("2D &amp; 3D Video Surveillance Reconstruction", feat_bold), Paragraph("OpenCV frame analysis detecting suspects, vehicles, weapons, 2D bounding boxes, and interactive 3D spatial trajectory room view.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("Demonstrated on 7 CCTV cases (retail shoplifting, traffic intersection, ATM assault, carjacking).", feat_body)],
        [Paragraph("2", feat_body), Paragraph("Multilingual Forensic Audio Analysis", feat_bold), Paragraph("OpenAI Whisper speech-to-text pipeline transcribing witness audio in English, Hindi, Telugu, and French with acoustic timeline extraction.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("Demonstrated on 911 distress calls, burglar alarms, and robbery witness depositions.", feat_body)],
        [Paragraph("3", feat_body), Paragraph("Image Forensic Analysis &amp; 3D Spatial Room View", feat_bold), Paragraph("RT-DETR object detection, scene classification, bounding box overlays, and 3D wireframe room projection of evidence locations.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("High-resolution detection of suspects, firearms, and urban objects with confidence metrics.", feat_body)],
        [Paragraph("4", feat_body), Paragraph("Second-by-Second Event Timeline", feat_bold), Paragraph("Chronological crime event timeline mapping timestamps to security threats, motion breaches, and suspect actions with 1-click playback jump.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("Interactive timeline synchronized across video and audio media feeds.", feat_body)],
        [Paragraph("5", feat_body), Paragraph("Interactive Multimodal AI Chatbot", feat_bold), Paragraph("Context-aware forensic investigation assistant answering targeted queries regarding perpetrators, vehicles, and timing using Groq Llama-3.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("Session-grounded investigation assistant with direct timeline and evidence context retrieval.", feat_body)],
        [Paragraph("6", feat_body), Paragraph("Automated Forensic PDF Report Generation", feat_bold), Paragraph("One-click export of court-ready forensic incident reports containing case metadata, timeline, evidence logs, and confidence metrics.", feat_body), Paragraph("Implemented", feat_body), Paragraph("Yes", feat_body), Paragraph("Court-admissible standardized PDF generated dynamically with ReportLab.", feat_body)],
    ]
    t1 = Table(feat_data, colWidths=[24, 115, 180, 75, 66, 90])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Feature Implementation Summary:</b>", section_title_style))
    summary_data = [
        [Paragraph("<b>Total Features Proposed</b>", feat_bold), Paragraph("6", feat_body)],
        [Paragraph("<b>Total Features Implemented</b>", feat_bold), Paragraph("6", feat_body)],
        [Paragraph("<b>Total Features Demonstrated</b>", feat_bold), Paragraph("6", feat_body)],
        [Paragraph("<b>Overall Implementation Rate (%)</b>", feat_bold), Paragraph("<b>100%</b>", feat_bold)],
    ]
    t2 = Table(summary_data, colWidths=[275, 275])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)

    build_pdf("Demonstration of Proposed Features.pdf", story, margins=(30, 30, 24, 24))

# =========================================================================
# 3. Team Involvement in Demonstration
# =========================================================================
def generate_team():
    story = create_header("Team Involvement in Demonstration", max_marks="1 Mark")
    story.append(Paragraph("<b>Team Involvement in Demonstration:</b>", section_title_style))
    story.append(Paragraph(
        "This document records the active participation and roles of each team member during the project "
        "demonstration. It ensures that every member contributes meaningfully to the presentation and that "
        "responsibilities are distributed fairly and clearly.",
        intro_style
    ))

    team_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Team Member Name</b>", th_style), Paragraph("<b>Role in Demo</b>", th_style), Paragraph("<b>Section Presented</b>", th_style), Paragraph("<b>Contribution Summary</b>", th_style), Paragraph("<b>Participation<br/>(Active / Passive)</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("Rahul Rajak", body_bold_style), Paragraph("Project Lead &amp; Lead AI Engineer", body_style), Paragraph("Introduction, 3D Video Surveillance &amp; Live Demo", body_style), Paragraph("Architected end-to-end multimodal pipeline, Three.js 3D spatial reconstruction, live UI demonstration, and full-stack integration.", body_style), Paragraph("Active", body_style)],
        [Paragraph("2", body_style), Paragraph("Team Member 2", body_bold_style), Paragraph("Computer Vision Specialist", body_style), Paragraph("Image Analysis &amp; Object Detection", body_style), Paragraph("Implemented RT-DETR object detection, bounding box overlay rendering, and scene classification modules.", body_style), Paragraph("Active", body_style)],
        [Paragraph("3", body_style), Paragraph("Team Member 3", body_bold_style), Paragraph("Audio &amp; NLP Engineer", body_style), Paragraph("Audio Forensics &amp; Multilingual ASR", body_style), Paragraph("Integrated OpenAI Whisper speech-to-text, acoustic event detection, and 4-language translation pipeline.", body_style), Paragraph("Active", body_style)],
        [Paragraph("4", body_style), Paragraph("Team Member 4", body_bold_style), Paragraph("DevOps &amp; Full-Stack Engineer", body_style), Paragraph("Cloud Architecture &amp; System Deployment", body_style), Paragraph("Managed Vercel frontend CI/CD, Render backend microservice deployment, CORS security, and test automation.", body_style), Paragraph("Active", body_style)],
    ]
    t1 = Table(team_data, colWidths=[25, 95, 95, 115, 160, 60])
    apply_table_style(t1)
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Team Coordination Notes:</b>", section_title_style))
    coord_data = [
        [Paragraph("<b>Aspect</b>", th_style), Paragraph("<b>Details</b>", th_style)],
        [Paragraph("Team Leader / Coordinator", body_bold_style), Paragraph("Rahul Rajak", body_style)],
        [Paragraph("Overall Team Coordination Rating (1-5)", body_bold_style), Paragraph("5 / 5 (Exceptional cross-functional execution and milestone delivery)", body_style)],
        [Paragraph("Any issues during demo", body_bold_style), Paragraph("Render cloud free-tier service cold-start latency (~30-40 seconds initial container spin-up).", body_style)],
        [Paragraph("How issues were resolved", body_bold_style), Paragraph("Pre-warmed the cloud backend container gateway prior to live evaluation and integrated client-side static media fallbacks for uninterrupted demonstration continuity.", body_style)],
    ]
    t2 = Table(coord_data, colWidths=[180, 370])
    apply_table_style(t2)
    story.append(t2)

    build_pdf("Team Involvement in Demonstration.pdf", story)

# =========================================================================
# 4. Project Demo Planning
# =========================================================================
def generate_demo_planning():
    story = create_header("Project Demo Planning", max_marks="1 Mark")
    story.append(Paragraph("<b>Project Demo Planning:</b>", section_title_style))
    story.append(Paragraph(
        "A well-structured demo plan ensures that the team presents the project effectively, covering all key "
        "aspects in a clear and organized manner. This document outlines the plan for demonstrating the project, "
        "including the flow of the demo, key features to highlight, and responsibilities of each team member.",
        intro_style
    ))

    plan_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Demo Section</b>", th_style), Paragraph("<b>Description</b>", th_style), Paragraph("<b>Duration (mins)</b>", th_style), Paragraph("<b>Responsible Member</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("Introduction &amp; Problem Statement", body_bold_style), Paragraph("Overview of forensic investigation bottlenecks, manual CCTV review limitations, and CrimeVision AI automated value proposition.", body_style), Paragraph("2.0 mins", body_style), Paragraph("Rahul Rajak", body_style)],
        [Paragraph("2", body_style), Paragraph("Solution Architecture Overview", body_bold_style), Paragraph("Walkthrough of multimodal pipeline architecture (Vision, Whisper, OpenCV, LLM Fusion, Three.js 3D space).", body_style), Paragraph("1.5 mins", body_style), Paragraph("DevOps / Full-Stack Engineer", body_style)],
        [Paragraph("3", body_style), Paragraph("Video Surveillance &amp; 3D Reconstruction", body_bold_style), Paragraph("Live demonstration of real CCTV footage processing, 2D bounding boxes, 3D suspect trajectory tracking, and multi-camera angles.", body_style), Paragraph("3.0 mins", body_style), Paragraph("Rahul Rajak &amp; CV Specialist", body_style)],
        [Paragraph("4", body_style), Paragraph("Forensic Audio &amp; Multilingual ASR", body_bold_style), Paragraph("Live processing of 911 distress call, Whisper speech transcription, and 4-language localization (EN, HI, TE, FR).", body_style), Paragraph("1.5 mins", body_style), Paragraph("Audio &amp; NLP Engineer", body_style)],
        [Paragraph("5", body_style), Paragraph("Image Analysis, Chatbot &amp; PDF Report", body_bold_style), Paragraph("Single crime scene image 3D projection, conversational forensic Q&amp;A chatbot, and dynamic court-admissible PDF generation.", body_style), Paragraph("1.5 mins", body_style), Paragraph("Rahul Rajak", body_style)],
        [Paragraph("6", body_style), Paragraph("Conclusion &amp; Technical Q&amp;A", body_bold_style), Paragraph("System evaluation metrics review, cloud scalability roadmap, and addressing evaluator queries.", body_style), Paragraph("0.5 mins", body_style), Paragraph("Entire Team", body_style)],
    ]
    t1 = Table(plan_data, colWidths=[25, 120, 235, 70, 100])
    apply_table_style(t1)
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Demo Flow Summary:</b>", section_title_style))
    flow_data = [
        [Paragraph("<b>Step</b>", th_style), Paragraph("<b>Activity</b>", th_style), Paragraph("<b>Notes</b>", th_style)],
        [Paragraph("1", body_bold_style), Paragraph("Introduction &amp; Problem Statement", body_bold_style), Paragraph("Highlight time-critical challenges in law enforcement surveillance triage and how AI reduces evidence processing time from hours to seconds.", body_style)],
        [Paragraph("2", body_bold_style), Paragraph("Solution Overview", body_bold_style), Paragraph("Showcase system architecture, hybrid AI stack (RT-DETR + Whisper + OpenCV + Groq), and live cloud deployment topology.", body_style)],
        [Paragraph("3", body_bold_style), Paragraph("Live Feature Demonstration", body_bold_style), Paragraph("Demonstrate live platform at https://crime-vision-ai-frontend.vercel.app/ across video, audio, and image modes using the 14-case dataset library.", body_style)],
        [Paragraph("4", body_bold_style), Paragraph("Q&amp;A Session", body_bold_style), Paragraph("Answer evaluator questions regarding model accuracy, real-time latency, memory optimization (&lt;512MB RAM), and legal compliance.", body_style)],
    ]
    t2 = Table(flow_data, colWidths=[35, 175, 340])
    apply_table_style(t2)
    story.append(t2)

    build_pdf("Project Demo Planning.pdf", story)

# =========================================================================
# 5. Scalability & Future Plan (2 Pages)
# =========================================================================
def generate_scalability():
    story = create_header("Scalability & Future Plan", max_marks="1 Mark")
    story.append(Paragraph("<b>Scalability &amp; Future Plan:</b>", section_title_style))
    story.append(Paragraph(
        "This document outlines how the current project solution can be scaled to handle larger user bases, "
        "increased data loads, or extended features in the future. It also captures the team's roadmap for "
        "enhancing and evolving the project beyond its current state.",
        intro_style
    ))

    story.append(Paragraph("<b>Current System Limitations:</b>", section_title_style))
    limits_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Limitation</b>", th_style), Paragraph("<b>Impact</b>", th_style), Paragraph("<b>Priority to Address<br/>(High / Medium / Low)</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("Single-camera monocular 3D depth projection lacks stereoscopic multi-angle parallax calibration.", body_style), Paragraph("Limits sub-millimeter metric distance accuracy in highly cluttered 3D crime scenes.", body_style), Paragraph("Medium", body_bold_style)],
        [Paragraph("2", body_style), Paragraph("Cloud free-tier hosting (512MB RAM) requires CPU-quantized models and limits concurrent high-bitrate video streams.", body_style), Paragraph("Limits simultaneous real-time video processing to 1-2 concurrent 1080p surveillance streams.", body_style), Paragraph("High", body_bold_style)],
        [Paragraph("3", body_style), Paragraph("Extreme acoustic background noise (e.g. blaring sirens, loud engines) slightly elevates Whisper speech word error rate.", body_style), Paragraph("May necessitate secondary manual confirmation of low-confidence witness audio segments.", body_style), Paragraph("Low", body_bold_style)],
    ]
    t1 = Table(limits_data, colWidths=[25, 230, 215, 80])
    apply_table_style(t1)
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Scalability Plan:</b>", section_title_style))
    scale_data = [
        [Paragraph("<b>S.No</b>", th_style), Paragraph("<b>Scalability Aspect</b>", th_style), Paragraph("<b>Current State</b>", th_style), Paragraph("<b>Proposed Upgrade / Solution</b>", th_style)],
        [Paragraph("1", body_style), Paragraph("User Load", body_bold_style), Paragraph("Single-tenant web dashboard serving up to 10 concurrent forensic investigators.", body_style), Paragraph("Containerized Kubernetes cluster deployment with Horizontal Pod Autoscalers (HPA) and Redis session caching.", body_style)],
        [Paragraph("2", body_style), Paragraph("Data Storage", body_bold_style), Paragraph("Local ephemeral file storage (data/uploads) on application instance.", body_style), Paragraph("Migrate to AWS S3 / Cloudflare R2 object storage with AES-256 encryption and PostgreSQL metadata indexing.", body_style)],
        [Paragraph("3", body_style), Paragraph("Performance", body_bold_style), Paragraph("CPU inference with 1.0 Hz video frame sampling (~1.2x video duration).", body_style), Paragraph("Deploy NVIDIA TensorRT GPU acceleration (T4/A10G) enabling real-time 30 FPS multi-camera inference at &lt;100ms latency.", body_style)],
        [Paragraph("4", body_style), Paragraph("Security", body_bold_style), Paragraph("HTTPS web endpoint with CORS restriction and session isolation.", body_style), Paragraph("Implement Role-Based Access Control (RBAC), CJIS-compliant audit logs, end-to-end encryption, and SHA-256 evidence hashing.", body_style)],
    ]
    t2 = Table(scale_data, colWidths=[25, 95, 185, 245])
    apply_table_style(t2)
    story.append(t2)

    # Page Break for clean 2-page layout matching template
    story.append(PageBreak())

    # Page 2 Brand & Header continuation
    header_data2 = [
        [
            Paragraph("<b>SMARTBRIDGE</b><br/><font size=7 color='#64748b'>Let's Bridge the Gap</font>", header_logo_left),
            Paragraph("<b>SKILL WALLET</b><br/><font size=7 color='#64748b'>A SmartBridge Product</font>", header_logo_right)
        ]
    ]
    header_table2 = Table(header_data2, colWidths=[270, 270])
    header_table2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(header_table2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Future Roadmap:</b>", section_title_style))
    roadmap_data = [
        [Paragraph("<b>Phase</b>", th_style), Paragraph("<b>Planned Feature / Enhancement</b>", th_style), Paragraph("<b>Target Timeline</b>", th_style), Paragraph("<b>Expected Impact</b>", th_style)],
        [Paragraph("<b>Phase 1</b>", body_bold_style), Paragraph("Real-time RTSP/ONVIF Live CCTV Stream Ingestion", body_style), Paragraph("Q3 2026", body_style), Paragraph("Enables continuous 24/7 automated monitoring of municipal traffic and commercial facility feeds with instant threat alerting.", body_style)],
        [Paragraph("<b>Phase 2</b>", body_bold_style), Paragraph("Multi-Camera Cross-View Re-Identification (Re-ID)", body_style), Paragraph("Q4 2026", body_style), Paragraph("Seamlessly tracks suspects across multiple disjoint camera perimeters using deep visual appearance embedding vectors.", body_style)],
        [Paragraph("<b>Phase 3</b>", body_bold_style), Paragraph("Edge Computing Deployment (NVIDIA Jetson AGX Orin)", body_style), Paragraph("Q1 2027", body_style), Paragraph("Enables on-premise forensic edge appliances for police cruisers and local command centers without cloud internet dependency.", body_style)],
        [Paragraph("<b>Phase 4</b>", body_bold_style), Paragraph("Biometric Facial Recognition &amp; National Database Integration", body_style), Paragraph("Q2 2027", body_style), Paragraph("Cross-references flagged suspect faces against lawful authorized criminal warrants databases with strict privacy safeguards.", body_style)],
    ]
    t3 = Table(roadmap_data, colWidths=[65, 185, 90, 210])
    apply_table_style(t3)
    story.append(t3)

    build_pdf("Scalability & Future Plan.pdf", story)

if __name__ == "__main__":
    generate_communication()
    generate_features()
    generate_team()
    generate_demo_planning()
    generate_scalability()
    print("[SUCCESS] All Phase 8 Demonstration PDFs generated successfully!")
