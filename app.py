import os
import sys
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
# Flask session secure rakhne ke liye zaroori key
app.secret_key = 'super-secret-key-change-this-later'

# Secret Admin Login Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123"

# --- ULTIMATE 75+ GLOBAL AI DIRECTORY SEEDER ---
def seed_ultimate_free_tools():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Core operational categories mapping
        categories = [
            (1, "Text & Writing", "text-writing"),
            (2, "Image & Art", "image-art"),
            (3, "Coding & Dev", "coding-dev"),
            (4, "Audio & Voice", "audio-voice"),
            (5, "Productivity & Research", "productivity-research"),
            (6, "Video & Motion", "video-motion"),
            (7, "3D & Design", "3d-design")
        ]
        for cat in categories:
            cursor.execute('INSERT OR IGNORE INTO categories (id, name, slug) VALUES (?, ?, ?)', cat)

        # Gigantic Dataset containing Global Famous AI Tools (A-Z)
        tools = [
            # --- TEXT, CHAT & WRITING (1) ---
            ("ChatGPT", "The world's most popular conversational AI by OpenAI", "https://chatgpt.com", 1, "Freemium", "1", 2100),
            ("Claude AI", "State-of-the-art intelligence for analysis and writing by Anthropic", "https://claude.ai", 1, "Freemium", "1", 1850),
            ("Copy.ai", "AI-powered copywriter for marketing campaigns and high-converting text", "https://copy.ai", 1, "Freemium", "0", 610),
            ("DeepL", "Gold-standard AI translation across multiple languages", "https://deepl.com", 1, "Freemium", "0", 280),
            ("DeepSeek R1", "Open-source reasoning model rivaling top proprietary chat layers", "https://deepseek.com", 1, "Free", "1", 1950),
            ("DuckDuckGo AI Chat", "100% Anonymous and secure open-source model chat", "https://duckduckgo.com", 1, "Free", "0", 350),
            ("Gemini AI", "Google's powerful multimodal assistant with massive context limits", "https://google.com", 1, "Freemium", "1", 1720),
            ("Grok 4", "Real-time search and information parsing built by xAI with X integration", "https://grok.com", 1, "Paid", "0", 1210),
            ("Grammarly AI", "Deeply embedded writing assistant correcting complex context structures", "https://grammarly.com", 1, "Freemium", "0", 810),
            ("HuggingChat", "The open-source community alternative to commercial LLMs", "https://huggingface.co", 1, "Free", "1", 420),
            ("Jasper AI", "Enterprise-grade copilot built for marketing teams", "https://jasper.ai", 1, "Free Trial", "0", 670),
            ("Notion AI", "Workspace assistant to brainstorm, write, and summarize directly", "https://notion.so", 1, "Paid", "0", 920),
            ("QuillBot", "Advanced paragraph paraphraser and summaries editing tool", "https://quillbot.com", 1, "Freemium", "0", 980),
            ("Rytr", "An affordable, fast AI writing assistant for blogs and captions", "https://rytr.me", 1, "Freemium", "0", 410),
            ("Text Cortex", "Personal writing assistant with flexible daily rewards", "https://textcortex.com", 1, "Freemium", "0", 150),
            ("TinyWow AI", "A completely free package of simple micro writing tools", "https://tinywow.com", 1, "Free", "0", 195),
            ("Wordtune", "Professional sentences tuner and thoughts capturing writing partner", "https://wordtune.com", 1, "Freemium", "0", 540),
            ("Writesonic", "Generate SEO-optimized articles, landing pages, and blogs instantly", "https://writesonic.com", 1, "Freemium", "0", 790),

            # --- IMAGE, DESIGN & GRAPHICS (2) ---
            ("Adobe Firefly", "Commercial-safe vector and image creation tool with web client", "https://adobe.com", 2, "Freemium", "0", 310),
            ("Bing Image Creator", "Generate hyper-realistic 3D scenes via DALL-E", "https://bing.com", 2, "Free", "1", 190),
            ("Canva Magic Studio", "Visual content suite packing smart canvas design adjustments", "https://canva.com", 2, "Freemium", "0", 1140),
            ("Civitai", "The global repository for open-source checkpoint models and stable matrices", "https://civitai.com", 2, "Free", "0", 720),
            ("Craiyon", "Free and unlimited prompt to image matrix for abstract brainstorming", "https://craiyon.com", 2, "Free", "0", 180),
            ("Flux.1", "Next-gen premier open-weights photorealistic image model", "https://github.com", 2, "Free", "1", 1340),
            ("Fooocus", "Local workspace offering Midjourney quality without limits", "https://github.com", 2, "Free", "1", 510),
            ("Leonardo AI", "Production grade assets framework with full generation pipelines", "https://leonardo.ai", 2, "Freemium", "1", 1430),
            ("Midjourney v6", "Industry standard for artistic rendering and conceptual visual style", "https://midjourney.com", 2, "Paid", "1", 1650),
            ("NightCafe Studio", "Community art canvas running dense text-to-image challenges daily", "https://nightcafe.studio", 2, "Freemium", "0", 490),
            ("Photoroom", "Studio level product displays photography remover and editor background", "https://photoroom.com", 2, "Freemium", "0", 630),
            ("PixAI", "Anime-centric asset creator with dense community configurations", "https://pixai.art", 2, "Free", "0", 240),
            ("Playground AI", "Stunning graphics canvas combining canvas scaling and model filters", "https://playground.com", 2, "Freemium", "0", 820),
            ("Recraft AI", "Vector canvas tool for crisp branded palettes and typography", "https://recraft.ai", 2, "Freemium", "0", 780),
            ("Remove.bg", "Automated background canvas deletion layer working in single click", "https://remove.bg", 2, "Free", "0", 890),
            ("TensorArt", "Daily rotating platform for hosting and generating custom weights", "https://tensor.art", 2, "Free", "1", 390),
            ("Upscayl", "Local application to instantly fix and sharpen low resolution assets", "https://upscayl.org", 2, "Free", "0", 295),

            # --- CODING & SOFTWARE ENGINEERING (3) ---
            ("Amazon Q", "AWS native secure infrastructure coding expert tracking enterprise clouds", "https://amazon.com", 3, "Freemium", "0", 520),
            ("AskCodi", "Quick multi-language coding assistant for testing blocks", "https://askcodi.com", 3, "Freemium", "0", 410),
            ("Blackbox AI", "Super fast programming query box index with live file reference features", "https://blackbox.ai", 3, "Freemium", "0", 610),
            ("Codeium", "Lightning fast free telemetry autocompletion extension built for major IDEs", "https://codeium.com", 3, "Free", "0", 940),
            ("CodePal AI", "Generate, translate, and explain chunks of code instantly", "https://codepal.ai", 3, "Freemium", "0", 185),
            ("Cursor", "An AI-first code editor tailored for hyper-productive builders", "https://cursor.com", 3, "Freemium", "1", 1421),
            ("Devin AI", "The premier autonomous system capable of complete engineering tasks", "https://cognition.ai", 3, "Paid", "0", 1),
            ("GitHub Copilot", "Autocompletion pair-programmer baked right into common editors", "https://github.com", 3, "Paid", "1", 1280),
            ("Google AI Studio", "Direct pipeline to experiment with Gemini Pro models natively", "https://google.com", 3, "Free", "1", 480),
            ("Jan.ai", "Transform normal desktop environments into offline private nodes", "https://jan.ai", 3, "Free", "0", 320),
            ("LM Studio", "Run and test open weights cleanly without network connections", "https://lmstudio.ai", 3, "Free", "1", 430),
            ("Replit Agent", "Prompt-to-deployment pipeline that sets up entire code stacks", "https://replit.com", 3, "Paid", "0", 890),
            ("Tabnine", "Secure context aware code assistant focusing heavily on enterprise privacy", "https://tabnine.com", 3, "Paid", "0", 720),
            ("v0 by Vercel", "Generative design interface outputting raw React and Tailwind components", "https://v0.dev", 3, "Freemium", "1", 1150),

            # --- AUDIO, VOICE & TRANSCRIPTION (4) ---
            ("Audacity OpenVINO", "Isolate noise and separate musical stems locally using AI features", "https://audacityteam.org", 4, "Free", "0", 190),
            ("Descript", "Audio and video editor that allows script adjustment via transcript text editing", "https://descript.com", 4, "Freemium", "0", 850),
            ("ElevenLabs", "Ultra-realistic text-to-speech engine and authentic voice replication", "https://elevenlabs.io", 4, "Freemium", "1", 1780),
            ("LALAL.AI", "High fidelity stem extractor separating vocals, drums, and bass layers", "https://lalal.ai", 4, "Paid", "0", 410),
            ("Murf AI", "Studio grade narrations and voiceovers for crisp presentations", "https://murf.ai", 4, "Freemium", "0", 620),
            ("Play.ht", "Massive repository of realistic narrative voices with rich conversational style", "https://play.ht", 4, "Freemium", "0", 530),
            ("Speechify", "Convert heavy books and documents into fluid narrative voiceovers", "https://speechify.com", 4, "Freemium", "0", 940),
            ("Suno v3.5", "Synthesize full musical compositions with rich instrumental and vocal tracks", "https://suno.com", 4, "Freemium", "1", 1410),
            ("TTSMP3", "Zero-signup voice rendering utility exporting direct into raw MP3 format", "https://ttsmp3.com", 4, "Free", "0", 145),
            ("Udio", "Professional audio generation architecture producing structured songs", "https://udio.com", 4, "Freemium", "1", 1120),
 .
