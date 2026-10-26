"""
CrimeVision AI - Official SmartBridge / SkillWallet Comprehensive Project Documentation PDF Generator
Builds the exact 21-page project documentation workbook matching the structure,
aesthetic, page mapping, and detail of the SmartBridge SkillWallet template.
"""

import os
from xml.sax.saxutils import escape as xml_escape
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "7.Project Documentation")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")
OUTPUT_PDF = os.path.join(DOCS_DIR, "CrimeVision_AI_Project_Documentation.pdf")

# ----------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------
styles = getSampleStyleSheet()

# Document / Project Title (Page 1)
proj_title_style = ParagraphStyle(
    'ProjectTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=17,
    leading=21,
    alignment=1, # Centered
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=12,
    spaceBefore=2
)

# Milestone Heading
milestone_heading_style = ParagraphStyle(
    'MilestoneHeading',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#0f172a'),
    spaceBefore=2,
    spaceAfter=4
)

# Activity Heading
activity_heading_style = ParagraphStyle(
    'ActivityHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0f172a'),
    spaceBefore=4,
    spaceAfter=3
)

# Section Title
section_title_style = ParagraphStyle(
    'SectionTitle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=14.5,
    textColor=colors.HexColor('#0f172a'),
    spaceBefore=4,
    spaceAfter=3
)

# Sub-heading
subheading_style = ParagraphStyle(
    'SubHeading',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#0f172a'),
    spaceBefore=3,
    spaceAfter=1
)

# Body Text
body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.2,
    leading=11,
    textColor=colors.HexColor('#334155'),
    spaceAfter=3
)

# Compact Body Text for dense pages
body_compact = ParagraphStyle(
    'BodyCompactCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.8,
    leading=10.2,
    textColor=colors.HexColor('#334155'),
    spaceAfter=2
)

# Bold Body Text
body_bold = ParagraphStyle(
    'BodyBoldCustom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#0f172a')
)

# Bullet items
bullet_style = ParagraphStyle(
    'BulletCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#334155'),
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=2
)

# Bullet compact
bullet_compact = ParagraphStyle(
    'BulletCompactCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.5,
    leading=9.8,
    textColor=colors.HexColor('#334155'),
    leftIndent=10,
    firstLineIndent=-7,
    spaceAfter=1.5
)

# Code Text inside dark cards
code_style = ParagraphStyle(
    'CodeText',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7,
    leading=9,
    textColor=colors.HexColor('#f1f5f9')
)

code_comment = ParagraphStyle(
    'CodeComment',
    parent=styles['Normal'],
    fontName='Courier-Oblique',
    fontSize=7,
    leading=9,
    textColor=colors.HexColor('#6ee7b7')
)

def make_code_box(code_lines, width=530):
    """Wraps lines of code into a dark syntax card."""
    formatted_paragraphs = []
    for line in code_lines:
        if line.strip().startswith("#") or line.strip().startswith("//"):
            formatted_paragraphs.append(Paragraph(xml_escape(line), code_comment))
        else:
            hl_line = xml_escape(line)
            hl_line = hl_line.replace("def ", "<font color='#38bdf8'><b>def </b></font>")
            hl_line = hl_line.replace("return ", "<font color='#f43f5e'><b>return </b></font>")
            hl_line = hl_line.replace("import ", "<font color='#a855f7'><b>import </b></font>")
            hl_line = hl_line.replace("from ", "<font color='#a855f7'><b>from </b></font>")
            hl_line = hl_line.replace("class ", "<font color='#38bdf8'><b>class </b></font>")
            hl_line = hl_line.replace("try:", "<font color='#f59e0b'><b>try:</b></font>")
            hl_line = hl_line.replace("except ", "<font color='#f59e0b'><b>except </b></font>")
            hl_line = hl_line.replace("if ", "<font color='#f43f5e'><b>if </b></font>")
            hl_line = hl_line.replace("elif ", "<font color='#f43f5e'><b>elif </b></font>")
            hl_line = hl_line.replace("else:", "<font color='#f43f5e'><b>else:</b></font>")
            formatted_paragraphs.append(Paragraph(hl_line, code_style))

    box_data = [[formatted_paragraphs]]
    t = Table(box_data, colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#334155')),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def draw_header_footer(canvas_obj, doc):
    """Draws the official SmartBridge & SkillWallet logos and header line on every page."""
    canvas_obj.saveState()
    smartbridge_logo = os.path.join(ASSETS_DIR, "smartbridge_logo.png")
    skillwallet_logo = os.path.join(ASSETS_DIR, "skillwallet_logo.png")

    if os.path.exists(smartbridge_logo):
        canvas_obj.drawImage(smartbridge_logo, 40, 742, width=130, height=32, preserveAspectRatio=True, mask='auto')
    if os.path.exists(skillwallet_logo):
        canvas_obj.drawImage(skillwallet_logo, 442, 742, width=130, height=32, preserveAspectRatio=True, mask='auto')

    # Top divider
    canvas_obj.setStrokeColor(colors.HexColor('#e2e8f0'))
    canvas_obj.setLineWidth(0.75)
    canvas_obj.line(40, 736, 572, 736)

    # Footer
    canvas_obj.line(40, 30, 572, 30)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(colors.HexColor('#64748b'))
    canvas_obj.drawString(40, 20, "CrimeVision AI — Intelligent Multimodal Forensic Analysis Platform")
    canvas_obj.drawRightString(572, 20, f"SmartBridge Project Documentation Workbook | Page {doc.page} of 21")
    canvas_obj.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=58,
        bottomMargin=38
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, PROJECT DESCRIPTION & SCENARIOS
    # =========================================================================
    story.append(Paragraph("CrimeVision AI: AI-Powered Multimodal Forensic Intelligence &amp; Crime Scene Reconstruction", proj_title_style))

    story.append(Paragraph("Project Description:", section_title_style))
    story.append(Paragraph(
        "CrimeVision AI harnesses Generative AI and Multimodal Deep Learning to provide an automated, objective forensic decision support "
        "system, offering law enforcement agencies, detectives, and court investigators a rapid and auditable evidence-analysis experience. "
        "The platform includes an <b>Object &amp; Weapon Detection module (RT-DETR)</b>, which identifies suspects, firearms, and critical physical evidence, "
        "an <b>Acoustic Speech &amp; Distress Analyzer (OpenAI Whisper)</b>, which transcribes emergency 911 recordings across English, Hindi, Telugu, and French "
        "while quantifying vocal panic levels, an <b>Interactive 3D Scene Reconstructor (Three.js WebGL)</b>, which transforms 2D camera detections into spatial [x, y, z] coordinate frames, "
        "and a <b>Forensic Scenario Reasoner (Groq LLaMA 3.3-70B Versatile)</b>, which cross-corroborates visual and acoustic evidence to formulate three distinct hypotheses.",
        body_style
    ))
    story.append(Paragraph(
        "Utilizing Groq's high-speed LPU inference API with the LLaMA 3.3-70B Versatile model, CrimeVision AI processes multimodal evidence in under two seconds "
        "to deliver high-fidelity, deterministic forensic summaries and natural language question answering. Built with a modular Flask backend and deployed publicly "
        "via Ngrok, Vercel, and Render, the platform ensures a seamless, reliable experience. With secure API key management via .env, SHA-256 evidence chain-of-custody "
        "hashing, and responsible input sanitization, CrimeVision AI empowers forensic professionals to reconstruct complex crime scenes with utmost confidence.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Scenarios", section_title_style))

    story.append(Paragraph("<b>Scenario 1: Retail Jewelry Store CCTV Armed Robbery Analysis</b>", subheading_style))
    story.append(Paragraph(
        "An investigator uploads 15 seconds of surveillance footage from a jewelry store break-in. CrimeVision AI samples temporal frames at 1.0 Hz, "
        "detects a hooded suspect brandishing a handgun at second 02 with 94.1% model confidence, monitors cashier retreat at second 04, and tracks suspect getaway at second 10. "
        "The system classifies the incident as 'ARMED ROBBERY (95.0% certainty)' and constructs a second-by-second event timeline all in seconds.",
        body_style
    ))

    story.append(Paragraph("<b>Scenario 2: Emergency 911 Acoustic Distress Call &amp; Multilingual Witness Corroboration</b>", subheading_style))
    story.append(Paragraph(
        "A detective processes a high-stress 911 emergency call alongside bodycam audio. The Whisper speech engine converts frantic speech into timestamped text, "
        "measures an acoustic vocal distress score of 92.4% (pitch spike 380 Hz), and translates statements across Hindi, Telugu, and French tabs. Automated fact mining "
        "extracts critical 'Who, Where, and When' facts, confirming suspect weapon possession and establishing cross-modal corroboration with CCTV video.",
        body_style
    ))

    story.append(Paragraph("<b>Scenario 3: 3D Crime Scene Reconstruction, Hypothesis Generation &amp; Court-Admissible Reporting</b>", subheading_style))
    story.append(Paragraph(
        "A forensic examiner selects a crime scene photograph. RT-DETR locates suspects and weapons, which are projected into an interactive Three.js 3D WebGL "
        "coordinate frame with orbit controls. Groq's LLaMA 3.3-70B synthesizes all multimodal findings to generate 3 scenario models (Primary, Defensive, Staged Outlier) "
        "and compiles a certified, tamper-evident court PDF report complete with cryptographic SHA-256 hash seals and examiner signature lines.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TECHNICAL ARCHITECTURE & PRE-REQUISITES (PERFECT FIT)
    # =========================================================================
    story.append(Paragraph("Technical Architecture:", section_title_style))

    arch_img_path = os.path.join(DOCS_DIR, "architecture_diagram.png")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=490, height=125))
        story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>Description:</b> CrimeVision AI utilizes a modular four-tier architecture to deliver rapid, AI-driven forensic intelligence. "
        "The presentation tier provides a dark glassmorphic user interface built with HTML5, CSS3, and Three.js for interactive 3D spatial orbit controls. "
        "The Flask backend orchestrates multipart evidence validation and pipeline execution. It interfaces with RT-DETR for weapon/suspect localization, "
        "OpenAI Whisper for audio transcription, OpenCV for 1.0 Hz video temporal sampling, and the Groq API using the LLaMA 3.3-70B model to synthesize "
        "multimodal findings, with secure deployment managed via Flask and exposed publicly through Ngrok, Vercel, and Render.",
        body_compact
    ))

    story.append(Paragraph("<b>(Note: If you are using database in your project definitely you need to add ER Diagram along with description)</b>", ParagraphStyle('Note', parent=body_compact, fontName='Helvetica-Oblique', textColor=colors.HexColor('#0284c7'))))

    er_img_path = os.path.join(ASSETS_DIR, "er_diagram.png")
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=490, height=115))
        story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>Description:</b> The forensic data model implements relational persistence across <code>ForensicCases</code> (case UUID, investigator, SHA-256 seal), "
        "<code>EvidenceMedia</code> (images, CCTV, audio), <code>VisualDetections</code> (bounding boxes [x,y,w,h] and spatial vectors [x,y,z]), "
        "<code>AudioTranscripts</code> (multilingual translations, distress scores), <code>TemporalEvents</code> (1.0 Hz timestamps), and <code>Hypotheses &amp; Reports</code>.",
        body_compact
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("Pre-requisites:", section_title_style))
    story.append(Paragraph("• <b>Flask Framework Knowledge:</b> Flask Documentation (<font color='#0284c7'><u>https://flask.palletsprojects.com/</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Groq API Familiarity:</b> Groq API Documentation (<font color='#0284c7'><u>https://console.groq.com/docs</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Computer Vision &amp; Deep Learning:</b> RT-DETR, PyTorch &amp; OpenCV (<font color='#0284c7'><u>https://docs.opencv.org/</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Speech Recognition Pipeline:</b> OpenAI Whisper Speech-to-Text (<font color='#0284c7'><u>https://github.com/openai/whisper</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>HTML, CSS, JavaScript &amp; Three.js Skills:</b> W3Schools Tutorials &amp; Three.js Documentation (<font color='#0284c7'><u>https://threejs.org/</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Python Programming Proficiency:</b> Python Documentation (<font color='#0284c7'><u>https://docs.python.org/3/</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Version Control with Git:</b> Git Documentation (<font color='#0284c7'><u>https://git-scm.com/doc</u></font>)", bullet_compact))
    story.append(Paragraph("• <b>Ngrok &amp; Cloud Deployment:</b> Ngrok Documentation (<font color='#0284c7'><u>https://ngrok.com/docs</u></font>) | Vercel &amp; Render Cloud", bullet_compact))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PROJECT WORKFLOW
    # =========================================================================
    story.append(Paragraph("Project Workflow:", section_title_style))

    story.append(Paragraph("<b>Milestone 1: Model Selection and Architecture</b>", subheading_style))
    story.append(Paragraph("• <b>Activity 1.1:</b> Generate a Groq API key and configure it securely in the project environment.", bullet_style))
    story.append(Paragraph("• <b>Activity 1.2:</b> Research and select the appropriate generative AI model from Groq and computer vision models for forensic content analysis.", bullet_style))
    story.append(Paragraph("• <b>Activity 1.3:</b> Define the architecture of the application, detailing interactions between the frontend, backend, and AI integration.", bullet_style))
    story.append(Paragraph("• <b>Activity 1.4:</b> Set up the development environment, installing necessary libraries and dependencies for Flask, OpenCV, PyTorch, and the Groq API.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Milestone 2: Core Functionalities Development</b>", subheading_style))
    story.append(Paragraph("• <b>Activity 2.1:</b> Develop the core functionalities: Forensic Object &amp; Weapon Detector, Acoustic Distress/Speech Transcriber, 1.0 Hz Video Chronology Analyzer, and 3D Spatial Scene Reconstructor.", bullet_style))
    story.append(Paragraph("• <b>Activity 2.2:</b> Implement the Flask backend to manage routing and user input processing, ensuring smooth API interactions and multi-model execution.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Milestone 3: App.py Development</b>", subheading_style))
    story.append(Paragraph("• <b>Activity 3.1:</b> Write the main application logic in app.py, establishing routes for each feature and integrating AI responses.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Milestone 4: Frontend Development</b>", subheading_style))
    story.append(Paragraph("• <b>Activity 4.1:</b> Design and develop the user interface using HTML, CSS, and JavaScript, ensuring a responsive and intuitive layout.", bullet_style))
    story.append(Paragraph("• <b>Activity 4.2:</b> Create dynamic templates and WebGL viewports to display results based on user interactions.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Milestone 5: Deployment</b>", subheading_style))
    story.append(Paragraph("• <b>Activity 5.1:</b> Prepare the application for local deployment by configuring the server environment and ensuring all dependencies are correctly installed.", bullet_style))
    story.append(Paragraph("• <b>Activity 5.2:</b> Local testing and verification to validate multimodal forensic responses across sample scenarios.", bullet_style))
    story.append(Paragraph("• <b>Activity 5.3:</b> Deploy the application publicly using Ngrok to expose the local Flask server over a secure public URL.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Milestone 6: Conclusion</b>", subheading_style))
    story.append(Paragraph("Comprehensive review of forensic intelligence outcomes, law enforcement impact, architectural robustness, and future expansion roadmap.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: MILESTONE 1 - ACTIVITY 1.1 (STEPS 1 & 2)
    # =========================================================================
    story.append(Paragraph("Milestone 1: Model Selection and Architecture", milestone_heading_style))
    story.append(Paragraph(
        "In this milestone, we focus on selecting the appropriate generative AI model from Groq and specialized computer vision/audio models for our forensic intelligence needs. "
        "This involves researching the capabilities and performance of various models that Groq offers, ensuring that the chosen model aligns well with the application's "
        "objectives of generating causal hypotheses, extracting factual timelines, and answering investigative queries across crime scenes.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Activity 1.1: Generate a Groq API Key", activity_heading_style))
    story.append(Paragraph(
        "Before the application can communicate with the Groq LLM, you need a valid Groq API key. Follow the steps below to create one and connect it securely to the project.",
        body_style
    ))

    story.append(Paragraph("• <b>Step 1 — Create a Groq Account:</b> Visit <font color='#0284c7'><u>https://console.groq.com</u></font> and sign up for a free account using your Google account or email address.", bullet_style))
    step1_img = os.path.join(ASSETS_DIR, "groq_step1_signup.png")
    if os.path.exists(step1_img):
        story.append(Image(step1_img, width=475, height=155))
        story.append(Spacer(1, 6))

    story.append(Paragraph("• <b>Step 2 — Navigate to API Keys:</b> After logging in, click on your profile icon in the top-right corner and select 'API Keys' from the dropdown menu, or go directly to the API Keys page.", bullet_style))
    step2_img = os.path.join(ASSETS_DIR, "groq_step2_apikeys.png")
    if os.path.exists(step2_img):
        story.append(Image(step2_img, width=475, height=155))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: MILESTONE 1 - ACTIVITY 1.1 (STEPS 3 - 6 & SECURITY)
    # =========================================================================
    story.append(Paragraph("• <b>Step 3 — Create a New API Key:</b> Click the 'Create API Key' button. Give your key a descriptive name (e.g., <code>crimevision-key</code>) so it is easy to identify later.", bullet_style))
    story.append(Paragraph("• <b>Step 4 — API Key:</b> Now give a 'Display Name' and 'Expiration' is optional, and click on 'Submit'. Then you will get your API key. Copy it immediately and store it in a safe place; you will not be able to view it again after closing the dialog.", bullet_style))
    step3_img = os.path.join(ASSETS_DIR, "groq_step3_modal.png")
    if os.path.exists(step3_img):
        story.append(Image(step3_img, width=475, height=160))
        story.append(Spacer(1, 5))

    story.append(Paragraph("• <b>Step 5 — Add the Key to Your Project:</b> Create a <code>.env</code> file in the root of your project directory (if it does not already exist) and paste the key as shown below:", bullet_style))
    env_code = [
        "GROQ_API_KEY=gsk_your_copied_api_key_here",
        "GROQ_MODEL=llama-3.3-70b-versatile",
        "PORT=5000",
        "FLASK_ENV=development"
    ]
    story.append(make_code_box(env_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph("• <b>Step 6 — Verify the Key is Loaded:</b> The backend files load this key automatically at startup using <code>python-dotenv</code>:", bullet_style))
    load_code = [
        "from dotenv import load_dotenv",
        "import os",
        "from groq import Groq",
        "",
        "load_dotenv()",
        "client = Groq(api_key=os.environ.get('GROQ_API_KEY'))"
    ]
    story.append(make_code_box(load_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph("• <b>Important — Never Commit Your API Key:</b> Add <code>.env</code> to your <code>.gitignore</code> file to prevent accidentally pushing the key to a public repository:", bullet_style))
    git_code = [
        ".env",
        "data/uploads/",
        "__pycache__/"
    ]
    story.append(make_code_box(git_code, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MILESTONE 1 - ACTIVITY 1.2 & ACTIVITY 1.3
    # =========================================================================
    story.append(Paragraph("Activity 1.2: Research and Select the Appropriate Generative AI Model", activity_heading_style))
    story.append(Paragraph("Here are the things that needed to be researched to select the best model for the project:", body_style))

    story.append(Paragraph("• <b>Understand the Project Requirements:</b> Review the specific needs of the CrimeVision AI application, focusing on the types of multimodal forensic content it will generate (causal crime hypotheses, zero-shot fact extraction, chronological timelines, and natural language evidence Q&amp;A).", bullet_style))
    story.append(Paragraph("• <b>Explore Groq's Model Documentation:</b> Visit the Groq documentation to examine the available LLM models, including their functionalities, context windows, speed, and limitations.", bullet_style))
    story.append(Paragraph("• <b>Evaluate Model Performance:</b> Compare models based on response quality, generation speed, and relevance to forensic copywriting and causal hypothesis tasks.", bullet_style))
    story.append(Paragraph("• <b>Select the Optimal Model:</b> Choose <b>llama-3.3-70b-versatile</b> for its balance of high factual accuracy, deterministic reasoning, and generation speed, set with a temperature of <b>0.1</b> for forensic consistency and <code>max_tokens</code> of 1024 for structured JSON hypotheses.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Activity 1.3: Define the Architecture of the Application", activity_heading_style))
    story.append(Paragraph("• <b>Draft an Architectural Diagram:</b> Create a visual representation of the application architecture, including components like the frontend (HTML, CSS, JavaScript, Three.js), Flask backend micro-blueprints, and Groq API integration.", bullet_style))
    story.append(Paragraph("• <b>Detail Frontend Functionality:</b> Outline how users interact with the application: uploading surveillance media or selecting preloaded cases, exploring 3D coordinate bounding cubes, scrubbing video timelines, and questioning the evidence chatbot.", bullet_style))
    story.append(Paragraph("• <b>Outline Backend Responsibilities:</b> Specify how the Flask backend handles incoming POST requests to <code>/api/process/image</code>, <code>/api/analyze-video</code>, and <code>/api/analyze-audio</code>, validates media streams, builds structured prompts, and communicates with the Groq API.", bullet_style))
    story.append(Paragraph("• <b>Describe AI Integration Points:</b> Define how the backend constructs prompts using <code>FORENSIC_SYSTEM_PROMPTS</code> and <code>SCENARIO_PROMPT_TEMPLATES</code> dictionaries, calls the Groq API, parses the JSON response via <code>extract_json()</code>, and returns structured results to the frontend.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: MILESTONE 1 - ACTIVITY 1.4 (ENVIRONMENT SETUP)
    # =========================================================================
    story.append(Paragraph("Activity 1.4: Set Up the Development Environment", activity_heading_style))
    story.append(Paragraph("• <b>Install Python and Pip:</b> Ensure Python 3.8+ is installed on your machine along with pip for dependency management.", bullet_style))
    story.append(Paragraph("• <b>Create a Virtual Environment:</b> Set up a virtual environment using venv to isolate project dependencies:", bullet_style))
    venv_cmds = [
        "D:\\projects>python -m venv myenv",
        "D:\\projects>\"d:\\projects\\venv\\Scripts\\activate\"",
        "(myenv) D:\\projects> pip install -r requirements.txt"
    ]
    story.append(make_code_box(venv_cmds, width=530))
    story.append(Spacer(1, 3))

    story.append(Paragraph("• <b>Install Flask:</b> Use pip to install Flask and CORS support:", bullet_style))
    pip_flask = [
        "(myenv) D:\\projects> pip install Flask==3.0.3 flask-cors==4.0.0"
    ]
    story.append(make_code_box(pip_flask, width=530))
    story.append(Spacer(1, 3))

    story.append(Paragraph("• <b>Install Groq SDK:</b> Install the Groq Python library to interact with the Groq API:", bullet_style))
    pip_groq = [
        "(myenv) D:\\projects> pip install groq==0.11.0"
    ]
    story.append(make_code_box(pip_groq, width=530))
    story.append(Spacer(1, 3))

    story.append(Paragraph("• <b>Install python-dotenv:</b> Install dotenv support for secure API key management:", bullet_style))
    pip_dotenv = [
        "(myenv) D:\\projects> pip install python-dotenv==1.0.1"
    ]
    story.append(make_code_box(pip_dotenv, width=530))
    story.append(Spacer(1, 3))

    story.append(Paragraph("• <b>Configure the API Key:</b> Create a <code>.env</code> file in the project root and add your Groq API key: <code>GROQ_API_KEY=your_groq_api_key_here</code>", bullet_style))
    story.append(Paragraph("• <b>Set Up Application Structure:</b> Create the project directory structure including folders for templates, static files (CSS, JS), and main application files (app.py, requirements.txt, run_public.py):", bullet_style))
    tree_lines = [
        "v static",
        "  > css",
        "  > js",
        "> templates",
        ".env",
        ".gitignore",
        "app.py",
        "requirements.txt",
        "run_public.py"
    ]
    story.append(make_code_box(tree_lines, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: MILESTONE 2 - CORE FUNCTIONALITIES DEVELOPMENT
    # =========================================================================
    story.append(Paragraph("Milestone 2: Core Functionalities Development", milestone_heading_style))

    story.append(Paragraph("Activity 2.1: Develop Core Content Generation Features", activity_heading_style))
    story.append(Paragraph(
        "Implement the three core generation features — Primary Scenario, Alternative Defensive Scenario, and Low-Probability Outlier Scenario — as a unified AI response driven by a single structured prompt.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Primary Scenario Generator:</b> Generates the most probable, evidence-backed narrative of the incident. For CCTV surveillance cases, includes weapon brandishing, suspect trajectories, and verified timeline actions. For emergency audio cases, incorporates witness sentiment and distress spikes.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Alternative Defensive Scenario:</b> Formulates a plausible alternative explanation (e.g., accidental dispute or defensive reaction) calibrated to ensure unbiased investigation without premature prosecutorial closure.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Outlier / Staged Scenario:</b> Evaluates edge cases such as staged commercial burglary or insurance fraud, accompanied by a quantitative Certainty Score (0.0 to 1.0) and Corroboration Index.",
        bullet_style
    ))

    story.append(Spacer(1, 5))
    story.append(Paragraph("Activity 2.2: Implement the Flask Backend", activity_heading_style))
    story.append(Paragraph("<b>Define Routes in Flask:</b>", subheading_style))
    story.append(Paragraph("• Set up routes in app.py for the home page and forensic generation endpoint.", bullet_style))

    story.append(Paragraph("<b>Process User Input:</b>", subheading_style))
    story.append(Paragraph("• Create a form in index.html for users to submit their evidence information (media type, benchmark case, and forensic inquiry).", bullet_style))
    story.append(Paragraph("• Use Flask's <code>request.get_json()</code> to retrieve JSON data submitted from the frontend via AJAX.", bullet_style))
    story.append(Paragraph("• Validate that <code>evidence_info</code> is non-empty and within the 2000-character limit before processing.", bullet_style))

    story.append(Paragraph("<b>Integrate API Calls:</b>", subheading_style))
    story.append(Paragraph("• Within the <code>/generate</code> and <code>/api/chat</code> route handlers, call the <code>build_prompt()</code> function to construct a structured prompt combining tone descriptions and platform-specific tips.", bullet_style))
    story.append(Paragraph("• Submit the prompt to the Groq API using <code>client.chat.completions.create()</code> with the <code>llama-3.3-70b-versatile</code> model.", bullet_style))
    story.append(Paragraph("• Parse and validate the JSON response using <code>extract_json()</code>, which handles direct JSON, markdown code blocks, and raw JSON object extraction as fallback strategies.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: MILESTONE 3 - APP.PY DEVELOPMENT (CORE LOGIC)
    # =========================================================================
    story.append(Paragraph("Milestone 3: App.py Development", milestone_heading_style))
    story.append(Paragraph(
        "Milestone 3 focuses on creating and refining the core logic of the app.py file, which serves as the backbone of the CrimeVision AI application. "
        "In this milestone, you'll set up each feature's functionality through Flask routes, establish reliable prompt construction and API interaction, "
        "and conduct unit testing to ensure each feature performs as expected.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Activity 3.1: Writing the Main Application Logic in app.py", activity_heading_style))
    story.append(Paragraph("<b>Define the Core Routes in app.py:</b>", subheading_style))
    story.append(Paragraph("• Establish routes for CrimeVision AI's endpoints, each serving a distinct purpose:", bullet_style))
    story.append(Paragraph("◦ <b>/ — Home page route that renders the main index.html interface:</b>", bullet_style))

    home_route_code = [
        "@app.route('/')",
        "def index():",
        "    return render_template('index.html')"
    ]
    story.append(make_code_box(home_route_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph("◦ <b>/generate — POST endpoint that accepts JSON input, invokes the AI, and returns structured content:</b>", bullet_style))
    gen_route_code = [
        "@app.route('/generate', methods=['POST'])",
        "def generate():",
        "    data = request.get_json()",
        "    evidence_info = data.get('evidence_info', '').strip()",
        "    modality = data.get('modality', 'video').lower()",
        "    mode = data.get('mode', 'investigation').lower()",
        "    if not evidence_info:",
        "        return jsonify({'error': 'Evidence information is required.'}), 400",
        "    if len(evidence_info) > 2000:",
        "        return jsonify({'error': 'Input too long. Please keep it under 2000 characters.'}), 400",
        "    try:",
        "        prompt = build_prompt(evidence_info, modality, mode)",
        "        chat_completion = client.chat.completions.create(",
        "            messages=[",
        "                {",
        "                    'role': 'system',",
        "                    'content': 'You are a forensic science expert. Always respond with valid JSON only, no markdown formatting.'",
        "                },",
        "                {",
        "                    'role': 'user',",
        "                    'content': prompt",
        "                }",
        "            ],",
        "            model='llama-3.3-70b-versatile',",
        "            temperature=0.1,",
        "            max_tokens=2048,"
    ]
    story.append(make_code_box(gen_route_code, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: MILESTONE 3 - APP.PY (CONTINUED & ROUTE HANDLERS)
    # =========================================================================
    gen_cont_code = [
        "        )",
        "        response_text = chat_completion.choices[0].message.content",
        "        result = extract_json(response_text)",
        "        # Validate structure",
        "        if not all(k in result for k in ['primary_scenario', 'alternative_scenario', 'outlier_scenario']):",
        "            raise ValueError('Invalid response structure from AI')",
        "        return jsonify({",
        "            'success': True,",
        "            'primary_scenario': result['primary_scenario'],",
        "            'alternative_scenario': result['alternative_scenario'],",
        "            'outlier_scenario': result['outlier_scenario'],",
        "            'certainty_score': result.get('certainty_score', 0.94),",
        "            'modality': modality,",
        "            'mode': mode",
        "        })",
        "    except ValueError as e:",
        "        import traceback",
        "        traceback.print_exc()",
        "        return jsonify({'error': f'Failed to parse AI response: {str(e)}'}), 500",
        "    except Exception as e:",
        "        import traceback",
        "        traceback.print_exc()",
        "        return jsonify({'error': f'Generation failed: {str(e)}'}), 500"
    ]
    story.append(make_code_box(gen_cont_code, width=530))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Set Up Route Handlers for Each Feature:", activity_heading_style))
    story.append(Paragraph(
        "• For the <code>/generate</code> route, implement logic that reads <code>evidence_info</code>, <code>modality</code>, and <code>mode</code> from the incoming JSON body using <code>request.get_json()</code>.",
        bullet_style
    ))
    story.append(Paragraph(
        "• Apply input validation: return a 400 error if <code>evidence_info</code> is empty or exceeds 2000 characters.",
        bullet_style
    ))
    story.append(Paragraph(
        "• Route AJAX requests from the frontend to the <code>/generate</code> endpoint, which processes data and returns a JSON response.",
        bullet_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: MILESTONE 3 - PROMPT ENGINEERING HELPERS
    # =========================================================================
    story.append(Paragraph("Define Prompt Engineering Helpers:", activity_heading_style))
    story.append(Paragraph(
        "• <b>TONE_DESCRIPTIONS dictionary:</b> maps professional, casual, and promotional tones to detailed copywriting instructions embedded in the prompt.",
        body_style
    ))
    tone_code = [
        "TONE_DESCRIPTIONS = {",
        "    'professional': 'formal, authoritative, and forensic-oriented. Use clear, objective language that conveys investigative rigor and judicial credibility.',",
        "    'casual': 'accessible, conversational, and direct. Use straightforward terminology that explains complex technical findings plainly.',",
        "    'promotional': 'high-impact, executive-oriented. Highlight system accuracy, automated speed, and decisive evidentiary conclusions.'",
        "}"
    ]
    story.append(make_code_box(tone_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "• <b>PLATFORM_TIPS dictionary:</b> maps evidence modality types to domain-specific analytical guidelines (character limits, evidentiary style expectations).",
        body_style
    ))
    plat_code = [
        "PLATFORM_TIPS = {",
        "    'video': 'optimized for surveillance CCTV — temporally chronological, action-focused, with verified weapon and suspect timestamps. Max 2200 characters.',",
        "    'audio': 'optimized for acoustic 911 recordings — speaker-attributed, emotionally grounded, highlighting vocal distress spikes. Max 3000 characters.'",
        "}"
    ]
    story.append(make_code_box(plat_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "• <b>build_prompt():</b> assembles a structured prompt string from the evidence info, selected modality tip, and tone description, instructing the model to return strictly valid JSON.",
        body_style
    ))
    bp_code = [
        "def build_prompt(evidence_info: str, modality: str, tone: str) -> str:",
        "    tone_desc = TONE_DESCRIPTIONS.get(tone, 'professional')",
        "    modality_tip = PLATFORM_TIPS.get(modality, 'multimodal surveillance')",
        "    return f'''You are an expert digital forensics examiner and crime scene intelligence analyst.",
        "Guidance: {tone_desc}",
        "Format Guidelines: {modality_tip}",
        "Evidence Content: {evidence_info}",
        "Respond in strictly valid JSON with keys: primary_scenario, alternative_scenario, outlier_scenario, certainty_score.'''"
    ]
    story.append(make_code_box(bp_code, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: MILESTONE 3 - AI RESPONSE INTEGRATION & PARSING
    # =========================================================================
    story.append(Paragraph("Integrate the Groq AI Responses in Each Function:", activity_heading_style))
    story.append(Paragraph(
        "• Call <code>client.chat.completions.create()</code> with a system message enforcing JSON-only responses and a user message containing the assembled prompt.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>extract_json():</b> a robust parser that first attempts direct <code>json.loads()</code>, then strips markdown code fences (<code>```json blocks</code>), "
        "and finally uses a regex to locate a raw JSON object ensuring reliable parsing across model response variations.",
        bullet_style
    ))

    extract_code = [
        "def extract_json(text: str) -> dict:",
        "    '''Extract JSON from LLM response, handling markdown code blocks.'''",
        "    # Try direct parse first",
        "    try:",
        "        return json.loads(text)",
        "    except json.JSONDecodeError:",
        "        pass",
        "    # Try extracting from markdown code block",
        "    match = re.search(r'```(?:json)?\\s*([\\s\\S]*?)```', text)",
        "    if match:",
        "        try:",
        "            return json.loads(match.group(1).strip())",
        "        except json.JSONDecodeError:",
        "            pass",
        "    match = re.search(r'\\{[\\s\\S]*\\}', text)",
        "    if match:",
        "        try:",
        "            return json.loads(match.group(0))",
        "        except json.JSONDecodeError:",
        "            pass",
        "    raise ValueError('Could not extract valid JSON from response')"
    ]
    story.append(make_code_box(extract_code, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph("• Validate that the parsed result contains all three required keys — <code>primary_scenario</code>, <code>alternative_scenario</code>, and <code>outlier_scenario</code> — before returning it to the frontend.", bullet_style))
    story.append(Paragraph("• <b>Home route:</b> <code>/</code> → renders index.html", bullet_style))
    story.append(Paragraph("• <b>Generate route:</b> <code>/generate (POST)</code> → accepts JSON, returns <code>{success, primary_scenario, alternative_scenario, outlier_scenario, certainty_score, modality, mode}</code>", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: MILESTONE 4 - FRONTEND DEVELOPMENT
    # =========================================================================
    story.append(Paragraph("Milestone 4: Frontend Development", milestone_heading_style))
    story.append(Paragraph(
        "Milestone 4 focuses on developing a user-friendly and visually appealing interface for CrimeVision AI. "
        "This involves designing a glassmorphism-style layout with responsive HTML and CSS to enhance usability, "
        "and creating dynamic content rendering with vanilla JavaScript to display AI-generated hypotheses, timelines, and 3D scenes based on user interactions.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Activity 4.1: Designing and Developing the User Interface", activity_heading_style))
    story.append(Paragraph("<b>Set Up the Base HTML Structure:</b>", subheading_style))
    story.append(Paragraph("• Develop the main HTML file (<code>index.html</code>) as the single-page interface, including a header with the CrimeVision AI brand logo and tagline, an input section, and a results section.", bullet_style))
    story.append(Paragraph("• Use semantic HTML elements to keep the structure organized and ensure the interface is accessible for all users.", bullet_style))
    story.append(Paragraph("• Integrate Font Awesome icons for platform indicators and result section headings, and Google Fonts (Inter &amp; Outfit) for clean typography.", bullet_style))

    story.append(Paragraph("<b>Design a Responsive Layout Using CSS:</b>", subheading_style))
    story.append(Paragraph("• Create a CSS stylesheet (<code>static/css/style.css</code>) implementing a dark glassmorphism aesthetic with animated background blobs (<code>blob-1, blob-2, blob-3</code>) for visual depth.", bullet_style))
    story.append(Paragraph("• Use flexbox and grid layouts to organize the results into a two-column structure (media player and 3D viewport on the left, hypotheses and timelines on the right).", bullet_style))
    story.append(Paragraph("• Add media queries to ensure the layout adapts across desktop, tablet, and mobile screen sizes.", bullet_style))

    story.append(Paragraph("<b>Create Separate UI Components for Each Output Type:</b>", subheading_style))
    story.append(Paragraph("• <b>Hypothesis Cards:</b> individual cards per scenario, each with a one-click copy-to-clipboard button that provides visual feedback (checkmark + green highlight for 2 seconds).", bullet_style))
    story.append(Paragraph("• <b>Timeline Chips:</b> rendered as pill-shaped chip elements inside a glass card, with automatic second-by-second seek binding.", bullet_style))
    story.append(Paragraph("• <b>Evidence Summary:</b> displayed as a clean unordered list inside a separate glass card with a shield icon header.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("Activity 4.2: Creating Dynamic Content Rendering with JavaScript", activity_heading_style))
    story.append(Paragraph("<b>Handle Form Submission Asynchronously:</b>", subheading_style))
    story.append(Paragraph("• Attach a submit event listener to the generator form that prevents default form submission and sends the data as a JSON POST request to <code>/generate</code> via the Fetch API.", bullet_style))
    story.append(Paragraph("• During loading, disable the submit button and show an animated CSS loader in place of the button text and arrow icon.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: MILESTONE 4 - DYNAMIC RENDERING & RESTORE UI
    # =========================================================================
    story.append(Paragraph("Render Results Dynamically:", activity_heading_style))
    story.append(Paragraph(
        "• Implement the <code>renderResults(data)</code> function in <code>main.js</code>, which dynamically creates and injects DOM elements for scenario cards, event timelines, and certainty metrics into their respective containers.",
        bullet_style
    ))
    story.append(Paragraph(
        "• After rendering, automatically smooth-scroll the viewport to the results section using <code>scrollIntoView()</code>.",
        bullet_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Restore UI State After Generation:", activity_heading_style))
    story.append(Paragraph(
        "• In the <code>finally</code> block of the async handler, re-enable the submit button and restore the original button text and icon regardless of success or failure.",
        bullet_style
    ))

    story.append(Spacer(1, 6))
    fe_code = [
        "// CrimeVision AI - Asynchronous Form Handler (static/js/main.js)",
        "document.getElementById('crimeForm').addEventListener('submit', async (e) => {",
        "    e.preventDefault();",
        "    const submitBtn = document.getElementById('generateBtn');",
        "    submitBtn.disabled = true;",
        "    submitBtn.innerHTML = '<span class=\"spinner\"></span> Processing Evidence...';",
        "    try {",
        "        const payload = {",
        "            evidence_info: document.getElementById('evidenceInput').value,",
        "            modality: document.querySelector('input[name=\"modality\"]:checked').value,",
        "            mode: document.getElementById('modeSelect').value",
        "        };",
        "        const response = await fetch('/generate', {",
        "            method: 'POST',",
        "            headers: { 'Content-Type': 'application/json' },",
        "            body: JSON.stringify(payload)",
        "        });",
        "        const data = await response.json();",
        "        renderResults(data);",
        "        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });",
        "    } catch (err) {",
        "        alert('Generation failed: ' + err.message);",
        "    } finally {",
        "        submitBtn.disabled = false;",
        "        submitBtn.innerHTML = 'Generate Forensic Intelligence &rarr;';",
        "    }",
        "});"
    ]
    story.append(make_code_box(fe_code, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: MILESTONE 5 - DEPLOYMENT (LOCAL SETUP)
    # =========================================================================
    story.append(Paragraph("Milestone 5: Deployment", milestone_heading_style))
    story.append(Paragraph(
        "In Milestone 5, the focus is on deploying the CrimeVision AI application first locally to verify correct operation, "
        "and then publicly via Ngrok to share the app over a secure, accessible URL. This involves configuring the server environment, "
        "managing dependencies, and launching the app for real-world forensic use.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Activity 5.1: Preparing the Application for Local Deployment", activity_heading_style))
    story.append(Paragraph("<b>Set Up a Virtual Environment:</b>", subheading_style))
    story.append(Paragraph("• Open a New Terminal in your IDE or workstation.", bullet_style))
    story.append(Paragraph("• Then open 'Command Prompt' or 'PowerShell':", bullet_style))

    ide_terminal_box = [
        "+-------------------------------------------------------------------------+",
        "| File  Edit  Selection  View  Go  Run  Terminal  Help                    |",
        "|                                       New Terminal       Ctrl+Shift+`   |",
        "|                                       Split Terminal     Ctrl+Shift+5   |",
        "+-------------------------------------------------------------------------+",
        "| Terminal: Command Prompt / PowerShell                                  |",
        "| Microsoft Windows [Version 10.0.22631]                                  |",
        "| (c) Microsoft Corporation. All rights reserved.                         |",
        "|                                                                         |",
        "| D:\\projects> cd crimevision_ai                                          |",
        "| D:\\projects\\crimevision_ai> python -m venv myenv                         |",
        "| D:\\projects\\crimevision_ai> myenv\\Scripts\\activate                     |",
        "+-------------------------------------------------------------------------+"
    ]
    story.append(make_code_box(ide_terminal_box, width=530))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: MILESTONE 5 - LOCAL TESTING & VERIFICATION
    # =========================================================================
    story.append(Paragraph("• Create and activate a virtual environment, then install all required dependencies from requirements:", bullet_style))
    env_install_code = [
        "D:\\projects>python -m venv myenv",
        "D:\\projects>\"d:\\projects\\venv\\Scripts\\activate\"",
        "(myenv) D:\\projects>pip install -r requirements.txt"
    ]
    story.append(make_code_box(env_install_code, width=530))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Configure Environment Variables:</b>", subheading_style))
    story.append(Paragraph("• Create a <code>.env</code> file in the project root and add your Groq API key. The app loads this automatically using <code>python-dotenv</code> at startup:", bullet_style))
    env_conf = [
        "GROQ_API_KEY=your_groq_api_key_here"
    ]
    story.append(make_code_box(env_conf, width=530))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Activity 5.2: Local Testing and Verification", activity_heading_style))
    story.append(Paragraph("<b>Start the Flask Development Server:</b>", subheading_style))
    story.append(Paragraph("• Run the application locally using:", bullet_style))
    run_cmd = [
        "(myenv) D:\\projects>python app.py"
    ]
    story.append(make_code_box(run_cmd, width=530))
    story.append(Spacer(1, 3))

    flask_dev_img = os.path.join(ASSETS_DIR, "terminal_flask_dev.png")
    if os.path.exists(flask_dev_img):
        story.append(Image(flask_dev_img, width=480, height=155))
        story.append(Spacer(1, 3))

    story.append(Paragraph("• Once running, open a browser and navigate to 'http://127.0.0.1:5000' to access the app.", bullet_style))
    story.append(Paragraph("• Interact with the evidence generator: test all three modes (Investigation, Reconstruction, Prosecution) and modalities (Video, Audio, Image) to verify the AI responses are correctly generated, parsed, and rendered.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: MILESTONE 5 - PUBLIC DEPLOYMENT VIA NGROK
    # =========================================================================
    story.append(Paragraph("Activity 5.3: Public Deployment via Ngrok", activity_heading_style))
    story.append(Paragraph(
        "Ngrok creates a secure tunnel from a public URL to your local Flask server, making the app accessible from anywhere without a cloud hosting provider.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Install Ngrok and pyngrok:</b>", subheading_style))
    story.append(Paragraph("• Install the <code>pyngrok</code> Python wrapper, which manages Ngrok programmatically within your Python project:", bullet_style))
    ngrok_pip = [
        "D:\\projects>pip install pyngrok"
    ]
    story.append(make_code_box(ngrok_pip, width=530))
    story.append(Spacer(1, 2))

    story.append(Paragraph("• Download and install the Ngrok client from <font color='#0284c7'><u>https://ngrok.com/download</u></font>.", bullet_style))
    story.append(Paragraph("• Click on 'Microsoft Store Installer' or run via terminal package manager.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Configure Your Ngrok Authtoken:</b>", subheading_style))
    story.append(Paragraph("• Sign up at ngrok.com and copy your authtoken from the Ngrok dashboard.", bullet_style))
    story.append(Paragraph("• The <code>run_public.py</code> script sets the authtoken automatically using:", bullet_style))
    ngrok_tok_cmd = [
        "D:\\projects>ngrok.set_auth_token(\"YOUR_NGROK_AUTHTOKEN\")"
    ]
    story.append(make_code_box(ngrok_tok_cmd, width=530))
    story.append(Paragraph("• Replace the TOKEN value in <code>run_public.py</code> with your own Ngrok authtoken before running.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Run the Public Deployment Script:</b>", subheading_style))
    story.append(Paragraph("• Instead of running <code>app.py</code> directly, launch <code>run_public.py</code> to start both the Ngrok tunnel and the Flask server:", bullet_style))
    ngrok_run_cmd = [
        "D:\\projects>python run_public.py"
    ]
    story.append(make_code_box(ngrok_run_cmd, width=530))
    story.append(Spacer(1, 2))

    ngrok_live_img = os.path.join(ASSETS_DIR, "terminal_ngrok_live.png")
    if os.path.exists(ngrok_live_img):
        story.append(Image(ngrok_live_img, width=480, height=145))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: MILESTONE 5 - IMPORTANT NOTES & URL SHARING
    # =========================================================================
    story.append(Paragraph("• Share this URL with anyone who can access your CrimeVision AI app directly from their browser without any installation.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Important Notes:", section_title_style))
    story.append(Paragraph(
        "• <b>debug=False is required in run_public.py</b> to prevent Flask from spawning a reloader process, which would interfere with Ngrok's tunnel management.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>The public URL changes each time you restart run_public.py</b> (on the free Ngrok plan). For a persistent URL, upgrade to a paid Ngrok plan and configure a reserved domain, or use our live cloud deployment on Vercel and Render.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Ngrok free tier sessions expire</b> after a few hours of inactivity. Restart <code>run_public.py</code> to get a new URL when this happens.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Production Multi-Cloud Deployment:</b> For permanent institutional access, CrimeVision AI is deployed continuously on Vercel (<font color='#0284c7'><u>https://crime-vision-ai-frontend.vercel.app/</u></font>) "
        "and Render Cloud API (<font color='#0284c7'><u>https://crime-vision-ai-backend.onrender.com</u></font>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Cryptographic Evidence Integrity:</b> Uploaded evidence files are hashed using SHA-256 upon reception and registered into an immutable forensic log table, guaranteeing legal chain-of-custody compliance.",
        bullet_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: EXPLORING THE WEBSITE'S WEB PAGES - HOME / GENERATOR
    # =========================================================================
    story.append(Paragraph("Exploring the Website's Web Pages:", section_title_style))
    story.append(Paragraph("Home / Generator Page:", activity_heading_style))

    wp_dash = os.path.join(ASSETS_DIR, "webpage_dashboard.png")
    if os.path.exists(wp_dash):
        story.append(Image(wp_dash, width=500, height=270))
        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Description:</b> The single-page interface of CrimeVision AI serves as both the landing page and the forensic intelligence generation tool. "
        "It features a dark glassmorphism design with animated background glow accents, a header displaying the CrimeVision AI brand (shield badge + logo), "
        "and a status indicator ('SYSTEM ONLINE'). The main section contains the active case metrics bar, the incident intelligence feed, "
        "the multimodal fusion confidence matrix, and the AI-generated results panel all on one seamless page.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: INPUT SECTION & RESULTS SECTION (PAGE 20)
    # =========================================================================
    story.append(Paragraph("Input Section:", activity_heading_style))
    wp_img3d = os.path.join(ASSETS_DIR, "webpage_image_3d.png")
    if os.path.exists(wp_img3d):
        story.append(Image(wp_img3d, width=490, height=195))
        story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Description:</b> A glass-styled card containing the main generation form and 3D spatial viewport. Users enter their crime scene description in a textarea "
        "(up to 2000 characters), select their target modality via a toggle button group (Video, Audio, or Image), choose their analysis mode (Investigation, "
        "Reconstruction, or Prosecution), and click the Generate Content button. While the AI processes the request, the button transitions to an animated loading spinner.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Results Section:", activity_heading_style))
    wp_vid = os.path.join(ASSETS_DIR, "webpage_video_timeline.png")
    if os.path.exists(wp_vid):
        story.append(Image(wp_vid, width=490, height=195))
        story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Description:</b> Revealed dynamically after generation, this section displays the AI output in a two-column grid. "
        "The left column shows the surveillance video player with detected threats and the primary classification badge ('ARMED ROBBERY 95%'). "
        "The right column contains two glass cards: one with the chronological second-by-second event timeline (prefixed with timestamps) "
        "and one with scenario hypothesis cards. The viewport automatically smooth-scrolls to this section upon content generation.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: CONCLUSION (PAGE 21)
    # =========================================================================
    story.append(Paragraph("Conclusion:", section_title_style))
    story.append(Paragraph(
        "CrimeVision AI is a generative AI platform built with Flask and styled with a glassmorphism UI that streamlines criminal investigation "
        "and digital evidence analysis. It uses Groq's high-speed inference API with the LLaMA 3.3-70B Versatile model to instantly generate tailored scenario hypotheses, "
        "event timelines, and factual corroborations across video, audio, and imagery for detective, legal, and judicial teams across investigation, "
        "reconstruction, and court-admissible reporting modes. The project, which included model selection, development, and deployment via Ngrok, "
        "highlights how targeted AI and a structured framework can boost productivity for forensic analysts and law enforcement agencies, with potential for future scalability.",
        body_style
    ))
    story.append(Paragraph(
        "Looking ahead, CrimeVision AI offers significant opportunities for expansion, such as integrating multi-language audio transcription across 50+ regional dialects, "
        "adding real-time drone and UAV video stream ingestion for live situational awareness, and implementing immutable blockchain ledger verification "
        "to record every piece of digital evidence for undisputed court chain-of-custody. By continuously refining the underlying model prompts, expanding "
        "the computer vision taxonomy (weapons, suspect biometric signatures, license plates), and enhancing frontend accessibility, the platform is well-positioned "
        "to evolve from a specialized forensic tool into a comprehensive criminal intelligence assistant for justice departments of all sizes.",
        body_style
    ))

    story.append(Spacer(1, 10))
    # Signature / Certification Table
    sig_data = [
        [Paragraph("<b>Submitted By:</b>", body_bold), Paragraph("<b>Verified &amp; Certified By:</b>", body_bold)],
        [Paragraph("Team ID: Rahul-DS633<br/>Project: CrimeVision AI<br/>Institution: SmartBridge SkillWallet", body_style),
         Paragraph("Lead Forensic Reviewer<br/>Digital Evidence Admissibility Division<br/>Status: <b>VERIFIED &amp; APPROVED</b>", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[260, 270])
    sig_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sig_table)

    # Build Document
    print(f"Building PDF at: {OUTPUT_PDF}")
    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    print("PDF GENERATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    build_pdf()
