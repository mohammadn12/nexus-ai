import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'ai_tools.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE,
            icon TEXT NOT NULL,
            description TEXT,
            color TEXT NOT NULL
        )
    ''')

    # Create tools table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            tagline TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            website_url TEXT NOT NULL,
            logo_url TEXT NOT NULL,
            pricing_type TEXT NOT NULL,
            pricing_details TEXT,
            rating REAL DEFAULT 4.8,
            upvotes INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            is_verified INTEGER DEFAULT 1,
            tags TEXT NOT NULL,
            features TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tools_category ON tools(category_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tools_pricing ON tools(pricing_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tools_featured ON tools(is_featured)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tools_upvotes ON tools(upvotes)')

    # Check if categories already exist
    cursor.execute('SELECT COUNT(*) as count FROM categories')
    if cursor.fetchone()['count'] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    categories = [
        ("Coding & Dev", "coding-dev", "code", "AI coding assistants, code generation, and developer IDEs", "#3b82f6"),
        ("Text & Writing", "text-writing", "pen-tool", "AI copywriters, creative writing, and LLM assistants", "#8b5cf6"),
        ("Image & Art", "image-art", "image", "AI image generators, editors, and artistic stylizers", "#ec4899"),
        ("Video & Motion", "video-motion", "video", "Generative video, AI avatars, and video editing suites", "#f43f5e"),
        ("Audio & Voice", "audio-voice", "mic", "Voice cloning, AI music synthesis, and audio transcription", "#eab308"),
        ("Productivity & Research", "productivity-research", "sparkles", "Research engines, document analysis, and smart workflow automation", "#10b981"),
        ("3D & Design", "3d-design", "box", "3D mesh generation, UI design automation, and spatial computing", "#06b6d4")
    ]

    for cat in categories:
        cursor.execute(
            'INSERT INTO categories (name, slug, icon, description, color) VALUES (?, ?, ?, ?, ?)',
            cat
        )

    # Get category ID map
    cursor.execute('SELECT id, slug FROM categories')
    cat_map = {row['slug']: row['id'] for row in cursor.fetchall()}

    tools = [
        # Coding & Dev
        {
            "name": "Cursor",
            "slug": "cursor",
            "tagline": "The AI-first Code Editor built for hyper-productive engineers",
            "description": "Cursor is a fork of VS Code engineered from the ground up for AI pair programming. It understands your entire codebase, generates multi-file diffs, and seamlessly edits complex projects.",
            "category_id": cat_map["coding-dev"],
            "website_url": "https://cursor.com",
            "logo_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free tier available. Pro starts at $20/month with unlimited fast AI completions.",
            "rating": 4.9,
            "upvotes": 1420,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["IDE", "Code Generation", "Codebase Chat", "VS Code Fork"]),
            "features": json.dumps([
                "Full-codebase semantic indexing & intelligent context retrieval",
                "Composer mode for multi-file code editing & refactoring",
                "Instant AI fix recommendations for terminal & syntax errors",
                "Privacy mode ensures zero telemetry and code retention"
            ])
        },
        {
            "name": "GitHub Copilot",
            "slug": "github-copilot",
            "tagline": "Your AI pair programmer integrated directly inside your IDE",
            "description": "GitHub Copilot turns natural language prompts into code across dozens of programming languages. Features Copilot Chat for conversational debugging and explanation.",
            "category_id": cat_map["coding-dev"],
            "website_url": "https://github.com/features/copilot",
            "logo_url": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Paid",
            "pricing_details": "$10/month for Individuals, $19/user/month for Business with enterprise security.",
            "rating": 4.8,
            "upvotes": 1280,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Code Completion", "GitHub", "Copilot Chat", "Multi-Language"]),
            "features": json.dumps([
                "Real-time code autocompletion and snippet generation",
                "Pull request summaries and automated unit test generation",
                "Support for VS Code, Visual Studio, JetBrains, and Neovim",
                "Integrated vulnerability filter and security scanner"
            ])
        },
        {
            "name": "v0 by Vercel",
            "slug": "v0-vercel",
            "tagline": "Generative UI system powered by AI and React / Tailwind CSS",
            "description": "v0 is an AI-powered generative user interface tool by Vercel that converts natural language prompts into fully functional, accessible React, Next.js, and Tailwind CSS components.",
            "category_id": cat_map["coding-dev"],
            "website_url": "https://v0.dev",
            "logo_url": "https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free credits renewed monthly. Premium at $20/month with 5,000 credits.",
            "rating": 4.9,
            "upvotes": 1150,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["React", "Tailwind CSS", "UI Design", "Frontend AI"]),
            "features": json.dumps([
                "Instant production-ready React component generation",
                "Copy-paste code directly into Next.js & shadcn/ui projects",
                "Interactive live preview with dark/light mode toggle",
                "Figma-to-code and image-to-UI replication capabilities"
            ])
        },
        {
            "name": "Replit Agent",
            "slug": "replit-agent",
            "tagline": "Autonomous AI software engineer that builds apps from scratch",
            "description": "Replit Agent creates full-stack applications from simple natural language prompts. It plans architecture, sets up database schemas, installs packages, and deploys live to the cloud.",
            "category_id": cat_map["coding-dev"],
            "website_url": "https://replit.com",
            "logo_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Paid",
            "pricing_details": "Included with Replit Core subscription ($25/month).",
            "rating": 4.7,
            "upvotes": 890,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Autonomous Agent", "Fullstack", "Deployment", "Cloud IDE"]),
            "features": json.dumps([
                "End-to-end full-stack app creation from a single prompt",
                "Automated database provisioning and environment configuration",
                "Autonomous debugging with error self-healing",
                "One-click instant serverless deployment"
            ])
        },

        # Text & Writing
        {
            "name": "Claude 3.5 Sonnet",
            "slug": "claude-3-5-sonnet",
            "tagline": "State-of-the-art intelligence for coding, analysis, and nuanced writing",
            "description": "Anthropic's flagship model Claude 3.5 Sonnet sets industry benchmarks in reasoning, coding, and natural language communication. Features Artifacts for real-time interactive app rendering.",
            "category_id": cat_map["text-writing"],
            "website_url": "https://claude.ai",
            "logo_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free access available with limits. Claude Pro is $20/month with 5x usage.",
            "rating": 5.0,
            "upvotes": 1850,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["LLM", "Reasoning", "Artifacts", "Coding", "Anthropic"]),
            "features": json.dumps([
                "200K token context window for processing entire books & codebases",
                "Interactive Artifacts window for running HTML/React apps live",
                "Superior graduate-level reasoning and nuanced creative writing",
                "High precision vision and chart analysis"
            ])
        },
        {
            "name": "ChatGPT",
            "slug": "chatgpt",
            "tagline": "The world's most versatile conversational AI assistant by OpenAI",
            "description": "ChatGPT powered by GPT-4o offers multimodal intelligence with voice conversation, image analysis, web browsing, data analysis, and custom GPT ecosystem.",
            "category_id": cat_map["text-writing"],
            "website_url": "https://chatgpt.com",
            "logo_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free version with GPT-4o mini. Plus subscription at $20/month.",
            "rating": 4.9,
            "upvotes": 2100,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Conversational AI", "GPT-4o", "OpenAI", "Multimodal"]),
            "features": json.dumps([
                "Real-time voice mode with human-like low latency conversation",
                "Advanced Data Analysis for Python execution and chart plotting",
                "Web browsing with live citation generation",
                "Custom GPT store with specialized community agents"
            ])
        },
        {
            "name": "Jasper AI",
            "slug": "jasper-ai",
            "tagline": "Enterprise AI marketing platform built for high-performing teams",
            "description": "Jasper is an AI copilot for marketing teams that creates high-converting brand-aligned content across blogs, social media, ad campaigns, and SEO briefs.",
            "category_id": cat_map["text-writing"],
            "website_url": "https://jasper.ai",
            "logo_url": "https://images.unsplash.com/photo-1542744094-3a31f272c490?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Free Trial",
            "pricing_details": "7-day free trial. Creator plan starts at $39/month billed annually.",
            "rating": 4.6,
            "upvotes": 670,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Marketing", "Copywriting", "Brand Voice", "SEO"]),
            "features": json.dumps([
                "Company Brand Voice and Knowledge Base integration",
                "Multi-channel campaign asset generator",
                "Built-in plagiarism checking and SEO optimization mode",
                "Team collaboration and workflow review workflows"
            ])
        },
        {
            "name": "Notion AI",
            "slug": "notion-ai",
            "tagline": "Connected workspace intelligence that searches, writes, and organizes",
            "description": "Notion AI connects all your documents, wikis, and projects. It answers questions using your company knowledge base, drafts content, and automates database workflows.",
            "category_id": cat_map["text-writing"],
            "website_url": "https://notion.so/product/ai",
            "logo_url": "https://images.unsplash.com/photo-1517842645767-c639042777db?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Paid",
            "pricing_details": "$10/user/month add-on to existing Notion workspace plans.",
            "rating": 4.8,
            "upvotes": 920,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Productivity", "Knowledge Base", "Notes", "Wiki AI"]),
            "features": json.dumps([
                "Universal search across Slack, Google Drive, and Notion workspace",
                "Instant summaries of long meeting notes and project specs",
                "Automated database autofill and sentiment extraction",
                "Tone shifting, translation into 15+ languages, and grammar fixing"
            ])
        },

        # Image & Art
        {
            "name": "Midjourney v6",
            "slug": "midjourney",
            "tagline": "Photorealistic generative AI imagery and artistic visual storytelling",
            "description": "Midjourney generates astonishingly detailed, cinematic visuals and art styles from natural language descriptions. Accessible via Discord and the new web generation interface.",
            "category_id": cat_map["image-art"],
            "website_url": "https://midjourney.com",
            "logo_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Paid",
            "pricing_details": "Basic plan starts at $10/month, Standard at $30/month with unlimited relax hours.",
            "rating": 4.9,
            "upvotes": 1650,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Art", "Photorealism", "Text-to-Image", "Generative Art"]),
            "features": json.dumps([
                "Cinematic photorealism with fine texture and lighting rendering",
                "Accurate text spelling rendering inside images",
                "Vary Region (Inpainting) and Pan/Zoom out capabilities",
                "Character consistency and style reference parameters"
            ])
        },
        {
            "name": "Flux.1 by Black Forest Labs",
            "slug": "flux-1",
            "tagline": "Next-generation open-weights image generation foundation model",
            "description": "Flux.1 delivers state-of-the-art visual quality, prompt following, and typography. Available in Schnell (fast), Dev (open-weights), and Pro (enterprise API) variants.",
            "category_id": cat_map["image-art"],
            "website_url": "https://blackforestlabs.ai",
            "logo_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Free",
            "pricing_details": "Open-source non-commercial weights on HuggingFace. Paid API per megapixel.",
            "rating": 4.9,
            "upvotes": 1340,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Open Source", "Text-to-Image", "Typography", "Flux"]),
            "features": json.dumps([
                "Unmatched typographic accuracy and complex text rendering",
                "Extremely high anatomical accuracy with human hands and faces",
                "12B parameter hybrid architecture with flow matching",
                "Available for local inference on consumer GPUs"
            ])
        },
        {
            "name": "Recraft AI",
            "slug": "recraft-ai",
            "tagline": "Infinite AI canvas for vector graphics, 3D icons, and brand palettes",
            "description": "Recraft is a graphic design studio that generates editable SVGs, 3D illustrations, and brand style systems with strict color palette adherence.",
            "category_id": cat_map["image-art"],
            "website_url": "https://recraft.ai",
            "logo_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free plan with daily credits. Pro at $20/month with commercial vector downloads.",
            "rating": 4.8,
            "upvotes": 780,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Vector", "SVG", "Iconography", "Design Studio"]),
            "features": json.dumps([
                "Native vector (SVG) export with clean editable paths",
                "Custom brand color palette locking across all assets",
                "Mockup generator for apparel, print, and digital devices",
                "Infinite visual canvas with layered element control"
            ])
        },

        # Video & Motion
        {
            "name": "Runway Gen-3 Alpha",
            "slug": "runway-gen-3",
            "tagline": "Major breakthrough in high-fidelity video generation and simulation",
            "description": "Runway Gen-3 Alpha generates hyper-realistic video clips with expressive character motion, cinematic camera controls, and precise keyframing.",
            "category_id": cat_map["video-motion"],
            "website_url": "https://runwayml.com",
            "logo_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free tier with starter credits. Standard plan at $12/month per user.",
            "rating": 4.8,
            "upvotes": 1290,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Text-to-Video", "Cinematic", "VFX", "Camera Control"]),
            "features": json.dumps([
                "High-speed generation of 4K cinematic video clips",
                "Motion Brush and Director Mode camera trajectory control",
                "Image-to-video animating static concepts into motion",
                "Act-One for expressive human facial animation from webcam footage"
            ])
        },
        {
            "name": "Kling AI",
            "slug": "kling-ai",
            "tagline": "Generative video model simulating real-world physical laws",
            "description": "Kling AI produces up to 2-minute long video clips at 1080p 30fps with advanced physics simulation, dynamic lighting, and complex action choreography.",
            "category_id": cat_map["video-motion"],
            "website_url": "https://klingai.com",
            "logo_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Daily free credits granted. VIP memberships from $10/month.",
            "rating": 4.7,
            "upvotes": 870,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Video Simulation", "1080p", "Physics Engine", "Text-to-Video"]),
            "features": json.dumps([
                "Video length up to 2 minutes with continuous narrative",
                "3D space temporal attention mechanism",
                "End frame and starting frame trajectory interpolation",
                "Realistic simulation of fluid mechanics and cloth dynamics"
            ])
        },
        {
            "name": "HeyGen",
            "slug": "heygen",
            "tagline": "AI video creation platform with lifelike avatars and voice cloning",
            "description": "HeyGen enables effortless production of studio-quality spokesperson videos, marketing presentations, and localized international training videos without cameras.",
            "category_id": cat_map["video-motion"],
            "website_url": "https://heygen.com",
            "logo_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "1 free credit to try. Creator plan starting at $29/month.",
            "rating": 4.8,
            "upvotes": 950,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["AI Avatar", "Spokesperson", "Video Localization", "Lip Sync"]),
            "features": json.dumps([
                "100+ hyper-realistic digital human avatars",
                "Video translation with automatic multilingual lip-syncing",
                "Custom instant avatar creation from phone camera",
                "Zapier and Canva deep integrations"
            ])
        },

        # Audio & Voice
        {
            "name": "ElevenLabs",
            "slug": "elevenlabs",
            "tagline": "Industry standard for ultra-realistic AI voice synthesis & audio",
            "description": "ElevenLabs generates human-grade expressive voiceovers in 32 languages with emotional nuance, pitch dynamics, voice cloning, and sound effects generation.",
            "category_id": cat_map["audio-voice"],
            "website_url": "https://elevenlabs.io",
            "logo_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free tier with 10,000 chars/mo. Starter plan is $5/month.",
            "rating": 5.0,
            "upvotes": 1780,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Voice Cloning", "Text-to-Speech", "Sound Effects", "Dubbing"]),
            "features": json.dumps([
                "Instant Voice Cloning with as little as 1 minute of sample audio",
                "AI Sound Effects generator from text prompts",
                "Automatic video dubbing preserving original speaker voice & tone",
                "Reader app for narrating articles, PDFs, and e-books on mobile"
            ])
        },
        {
            "name": "Suno v3.5",
            "slug": "suno-ai",
            "tagline": "Create full songs with vocals, instruments, and lyrics from any prompt",
            "description": "Suno AI generates radio-ready 4-minute songs in any genre, complete with full acoustic arrangements, harmonized vocals, and structured verses.",
            "category_id": cat_map["audio-voice"],
            "website_url": "https://suno.com",
            "logo_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "50 daily credits free (5 songs). Pro plan is $10/month for 500 songs.",
            "rating": 4.9,
            "upvotes": 1410,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Music AI", "Song Generation", "Vocals", "Composition"]),
            "features": json.dumps([
                "Generates full 4-minute songs with custom song structure",
                "Custom lyrics input and automated rhyming lyricist mode",
                "Wide spectrum of genres from EDM and Jazz to Classical & Metal",
                "Commercial ownership of tracks for Pro subscribers"
            ])
        },
        {
            "name": "Whisper by OpenAI",
            "slug": "whisper-openai",
            "tagline": "Robust automatic speech recognition (ASR) and language translation",
            "description": "Whisper is an open-weights speech recognition model trained on 680,000 hours of multilingual supervised data. Provides robust transcription across heavy accents and noisy backgrounds.",
            "category_id": cat_map["audio-voice"],
            "website_url": "https://github.com/openai/whisper",
            "logo_url": "https://images.unsplash.com/photo-1589254065878-42c9da997008?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Free",
            "pricing_details": "100% Free and open-source under MIT License. Hosted API at $0.006 / minute.",
            "rating": 4.9,
            "upvotes": 1120,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["Open Source", "Transcription", "Speech-to-Text", "ASR"]),
            "features": json.dumps([
                "High accuracy transcription in 99+ world languages",
                "Automatic translation from any spoken language to English text",
                "Resilience to background noise and technical vocabulary",
                "Zero cloud dependency when run locally via whisper.cpp"
            ])
        },

        # Productivity & Research
        {
            "name": "Perplexity AI",
            "slug": "perplexity-ai",
            "tagline": "Where knowledge begins: AI-powered conversational search engine",
            "description": "Perplexity delivers direct answers to complex queries backed by real-time web citations, multi-step Pro Search reasoning, and structured computational research.",
            "category_id": cat_map["productivity-research"],
            "website_url": "https://perplexity.ai",
            "logo_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free unlimited Quick Searches. Perplexity Pro is $20/month with 300+ Pro queries.",
            "rating": 4.9,
            "upvotes": 1920,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Search Engine", "Research", "Citations", "Pro Search"]),
            "features": json.dumps([
                "Interactive follow-up questions and step-by-step reasoning",
                "Model selector toggle between Claude 3.5, GPT-4o, and Sonar",
                "Perplexity Pages for publishing formatted research reports",
                "File and document analysis for PDF, CSV, and code repositories"
            ])
        },
        {
            "name": "Gamma App",
            "slug": "gamma-app",
            "tagline": "AI design partner for generating presentations, documents & webpages",
            "description": "Gamma builds beautiful, on-brand presentations, briefs, and interactive slide decks in seconds from a single text outline or document.",
            "category_id": cat_map["productivity-research"],
            "website_url": "https://gamma.app",
            "logo_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "400 free signup credits. Plus plan at $10/user/month.",
            "rating": 4.8,
            "upvotes": 1050,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["Presentations", "Slides", "Websites", "Design Automation"]),
            "features": json.dumps([
                "Generates complete styled decks from raw text notes or URLs",
                "Interactive cards with embedded web widgets and videos",
                "One-click aesthetic restyling and automated layout restructuring",
                "Export to PDF and PPTX PowerPoint files"
            ])
        },
        {
            "name": "ChatPDF",
            "slug": "chatpdf",
            "tagline": "Chat with any PDF document to extract insights and summaries",
            "description": "ChatPDF turns research papers, legal contracts, textbooks, and financial reports into conversational knowledge partners with verified line citations.",
            "category_id": cat_map["productivity-research"],
            "website_url": "https://chatpdf.com",
            "logo_url": "https://images.unsplash.com/photo-1568667256549-094345857637?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free for 2 PDFs/day up to 120 pages. Plus plan is $5/month.",
            "rating": 4.7,
            "upvotes": 790,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["PDF", "Research Assistant", "Document AI", "Summaries"]),
            "features": json.dumps([
                "Instant semantic indexing of complex multi-hundred page documents",
                "Direct source page references for every extracted fact",
                "Multilingual translation and synthesis of foreign research papers",
                "API available for enterprise batch document processing"
            ])
        },

        # 3D & Design
        {
            "name": "Spline AI",
            "slug": "spline-ai",
            "tagline": "Generate, edit, and animate 3D scenes in the browser with AI",
            "description": "Spline AI allows designers to generate 3D objects, apply procedural textures, and craft physics-based interactive 3D web experiences using natural language.",
            "category_id": cat_map["3d-design"],
            "website_url": "https://spline.design",
            "logo_url": "https://images.unsplash.com/photo-1633493106185-5085c8ecff2d?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free starter tier. Super plan starts at $9/month billed annually.",
            "rating": 4.9,
            "upvotes": 1260,
            "is_featured": 1,
            "is_verified": 1,
            "tags": json.dumps(["3D Web", "Three.js", "Spatial Design", "Interactive"]),
            "features": json.dumps([
                "Prompt-to-3D mesh and texture generation in real-time",
                "Export directly to React Three Fiber, WebGL, and Three.js",
                "Real-time team collaboration in an infinite 3D workspace",
                "Physics simulations with gravity, collision, and scroll triggers"
            ])
        },
        {
            "name": "Meshy",
            "slug": "meshy-ai",
            "tagline": "Generative 3D foundation model for game assets and spatial computing",
            "description": "Meshy transforms text prompts and reference 2D images into textured, production-ready 3D game assets with clean quad topology in under 60 seconds.",
            "category_id": cat_map["3d-design"],
            "website_url": "https://meshy.ai",
            "logo_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "200 free credits monthly. Pro plan is $16/month with high-poly exports.",
            "rating": 4.7,
            "upvotes": 810,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["3D Assets", "Game Dev", "Text-to-3D", "PBR Textures"]),
            "features": json.dumps([
                "Text to 3D and Image to 3D conversion in under a minute",
                "Full PBR texture map generation (albedo, roughness, normal, metallic)",
                "Support for GLTF, FBX, OBJ, and USDZ exports",
                "Clean quad wireframe re-meshing for Unreal Engine & Unity"
            ])
        },
        {
            "name": "Uizard",
            "slug": "uizard-io",
            "tagline": "AI-powered UI/UX design tool that turns wireframes into Figma prototypes",
            "description": "Uizard enables anyone to design mobile apps, websites, and wireframes in minutes. Scan hand-drawn sketches or screenshots to convert them into editable digital designs.",
            "category_id": cat_map["3d-design"],
            "website_url": "https://uizard.io",
            "logo_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=128&auto=format&fit=crop&q=80",
            "pricing_type": "Freemium",
            "pricing_details": "Free plan with 2 projects. Pro plan is $12/month per creator.",
            "rating": 4.6,
            "upvotes": 730,
            "is_featured": 0,
            "is_verified": 1,
            "tags": json.dumps(["UI Design", "Wireframing", "Figma", "Sketch to App"]),
            "features": json.dumps([
                "Autodesigner 2.0 creates complete multi-screen apps from text prompts",
                "Screenshot-to-editable design reverse engineering",
                "Paper wireframe sketch digitization via smartphone camera",
                "Heatmap predictor for user attention analysis"
            ])
        }
    ]

    for tool in tools:
        cursor.execute('''
            INSERT INTO tools (
                name, slug, tagline, description, category_id, website_url,
                logo_url, pricing_type, pricing_details, rating, upvotes,
                is_featured, is_verified, tags, features
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tool["name"], tool["slug"], tool["tagline"], tool["description"],
            tool["category_id"], tool["website_url"], tool["logo_url"],
            tool["pricing_type"], tool["pricing_details"], tool["rating"],
            tool["upvotes"], tool["is_featured"], tool["is_verified"],
            tool["tags"], tool["features"]
        ))

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, COUNT(t.id) as tool_count 
        FROM categories c 
        LEFT JOIN tools t ON c.id = t.category_id 
        GROUP BY c.id 
        ORDER BY c.id ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_tools(query=None, category_slug=None, pricing=None, featured=None, sort_by="popular"):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = '''
        SELECT t.*, c.name as category_name, c.slug as category_slug, c.color as category_color, c.icon as category_icon
        FROM tools t
        JOIN categories c ON t.category_id = c.id
        WHERE 1=1
    '''
    params = []

    if query:
        q_wildcard = f"%{query.strip()}%"
        sql += " AND (t.name LIKE ? OR t.tagline LIKE ? OR t.description LIKE ? OR t.tags LIKE ?)"
        params.extend([q_wildcard, q_wildcard, q_wildcard, q_wildcard])

    if category_slug and category_slug != "all":
        sql += " AND c.slug = ?"
        params.append(category_slug)

    if pricing and pricing != "all":
        sql += " AND LOWER(t.pricing_type) = LOWER(?)"
        params.append(pricing)

    if featured is not None and featured == "1":
        sql += " AND t.is_featured = 1"

    # Sorting
    if sort_by == "popular":
        sql += " ORDER BY t.upvotes DESC"
    elif sort_by == "rating":
        sql += " ORDER BY t.rating DESC, t.upvotes DESC"
    elif sort_by == "newest":
        sql += " ORDER BY t.id DESC"
    elif sort_by == "name":
        sql += " ORDER BY t.name ASC"
    else:
        sql += " ORDER BY t.upvotes DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        item = dict(row)
        try:
            item['tags'] = json.loads(item['tags'])
        except Exception:
            item['tags'] = [t.strip() for t in item['tags'].split(',') if t.strip()]
        try:
            item['features'] = json.loads(item['features'])
        except Exception:
            item['features'] = [f.strip() for f in item['features'].split('\n') if f.strip()]
        results.append(item)

    return results

def get_tool_by_id(tool_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, c.name as category_name, c.slug as category_slug, c.color as category_color, c.icon as category_icon
        FROM tools t
        JOIN categories c ON t.category_id = c.id
        WHERE t.id = ?
    ''', (tool_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    item = dict(row)
    try:
        item['tags'] = json.loads(item['tags'])
    except Exception:
        item['tags'] = [t.strip() for t in item['tags'].split(',') if t.strip()]
    try:
        item['features'] = json.loads(item['features'])
    except Exception:
        item['features'] = [f.strip() for f in item['features'].split('\n') if f.strip()]
    return item

def upvote_tool(tool_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tools SET upvotes = upvotes + 1 WHERE id = ?', (tool_id,))
    conn.commit()
    cursor.execute('SELECT upvotes FROM tools WHERE id = ?', (tool_id,))
    row = cursor.fetchone()
    conn.close()
    return row['upvotes'] if row else None

def submit_tool(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    slug = data['name'].lower().replace(" ", "-").replace(".", "-").replace("/", "-")
    # check slug collision
    cursor.execute('SELECT id FROM tools WHERE slug = ?', (slug,))
    if cursor.fetchone():
        import random
        slug = f"{slug}-{random.randint(100, 999)}"

    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    tags_json = json.dumps(tags)

    features = data.get('features', [])
    if isinstance(features, str):
        features = [f.strip() for f in features.split('\n') if f.strip()]
    features_json = json.dumps(features)

    cursor.execute('''
        INSERT INTO tools (
            name, slug, tagline, description, category_id, website_url,
            logo_url, pricing_type, pricing_details, rating, upvotes,
            is_featured, is_verified, tags, features
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        slug,
        data['tagline'],
        data.get('description', data['tagline']),
        int(data['category_id']),
        data['website_url'],
        data.get('logo_url') or 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80',
        data.get('pricing_type', 'Freemium'),
        data.get('pricing_details', 'Free trial / Freemium options available.'),
        float(data.get('rating', 4.8)),
        1, # starting upvote
        0, # not featured by default
        1, # verified submission
        tags_json,
        features_json
    ))

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_tool_by_id(new_id)

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total_tools, SUM(upvotes) as total_upvotes FROM tools')
    row = cursor.fetchone()
    total_tools = row['total_tools']
    total_upvotes = row['total_upvotes'] or 0

    cursor.execute("SELECT COUNT(*) as free_tools FROM tools WHERE pricing_type IN ('Free', 'Freemium')")
    free_tools = cursor.fetchone()['free_tools']

    cursor.execute('SELECT COUNT(*) as total_cats FROM categories')
    total_cats = cursor.fetchone()['total_cats']

    conn.close()
    return {
        "total_tools": total_tools,
        "total_upvotes": total_upvotes,
        "free_tools": free_tools,
        "total_categories": total_cats
    }
