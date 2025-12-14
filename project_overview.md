# Project Overview & Tech Stack Deep Dive

## 🚀 Project Overview

**YouTube-to-Blog + Podcast Automation** is a local-first, AI-powered content repurposing engine. It solves the problem of manually converting video content into written and audio formats. By simply pasting a YouTube link, the application orchestrates a complex pipeline that extracts content, synthesizes a blog post, fact-checks it, publishes it to a CMS, and even produces and uploads a podcast episode.

### Core Capabilities
1.  **Ingestion**: Extracts video metadata and transcripts from YouTube.
2.  **Synthesis**: Uses Google's Gemini AI to transform raw transcripts into engaging, SEO-optimized blog posts.
3.  **Verification**: Cross-references generated content with live web data using Tavily to ensure accuracy.
4.  **Distribution**:
    -   **Web**: Auto-publishes to WordPress.
    -   **Social**: Sends notifications via WhatsApp.
    -   **Audio**: Converts text to speech and automates the upload to Spotify for Creators.

---

## 🛠️ Technology Stack & Rationale

We chose a "Python-native" stack to ensure ease of development, maintainability, and high performance for local automation tasks.

### 1. Frontend: **Streamlit**
-   **Why**: Streamlit allows for rapid UI development without writing HTML/CSS/JS. It is data-centric and Python-native, making it the perfect choice for building internal tools and AI prototypes.
-   **Role**: Handles user input (URLs, prompts), displays previews (transcripts, markdown), and triggers backend processes.

### 2. Backend: **FastAPI**
-   **Why**: FastAPI is modern, fast (high-performance), and easy to use. It supports asynchronous operations natively (`async/await`), which is crucial when handling I/O bound tasks like calling OpenAI/Gemini APIs or scraping data.
-   **Role**: Serves as the orchestration layer, exposing endpoints for each step of the pipeline (transcript fetch, blog gen, publishing).

### 3. AI Intelligence: **Google Gemini 1.5 Flash**
-   **Why**:
    -   **Speed**: Flash is optimized for high-volume, low-latency tasks.
    -   **Context Window**: It has a massive context window (1M+ tokens), making it superior for processing very long video transcripts that would crash other models.
    -   **Cost**: Significantly more cost-effective than GPT-4 for this use case.
-   **Role**: Understands context, follows style instructions, and generates the final blog post and summaries.

### 4. Search & Fact-Checking: **Tavily AI**
-   **Why**: Unlike generic search APIs (like Google Serper), Tavily is built specifically for AI agents. It returns clean, parsed text chunks rather than raw HTML, reducing noise for the LLM.
-   **Role**: Validates claims in the generated blog against real-time web search results.

### 5. Content Extraction: **yt-dlp** & **youtube-transcript-api**
-   **Why**:
    -   `yt-dlp` is the industry standard for robust video metadata extraction.
    -   `youtube-transcript-api` uses undocumented internal APIs to fetch captions without requiring official OAuth credentials, making it lighter and easier to set up.
-   **Role**: The raw data layer.

### 6. Podcast Automation: **gTTS** & **Selenium**
-   **Why**:
    -   **gTTS (Google Text-to-Speech)**: A simple, free interface to Google's TTS API for generating decent quality MP3s.
    -   **Selenium**: Spotify for Creators (formerly Anchor) does not provide a public API for file uploads. We use Browser Automation (Selenium) to mimic a human user logging in and uploading the file.
-   **Role**: Converts text to audio and handles the "last mile" delivery to the podcast platform.

### 7. Notifications: **Twilio**
-   **Why**: The most reliable enterprise-grade API for WhatsApp and SMS.
-   **Role**: Pushes the final published URL to the user's phone, closing the feedback loop.

### 8. Integrations: **WordPress REST API**
-   **Why**: WordPress powers >40% of the web. Its REST API is mature and allows for full CRUD operations on posts relative to the user's site.
-   **Role**: Final destination for the written content.

---

## 📂 Architecture

The project follows a modular **Service-Oriented Architecture (SOA)**, even though it runs locally.

-   **`frontend/`**: View Layer. Dumb components that just display data.
-   **`backend/api/`**: Controller Layer. Routes that handle specific business domains (YouTube, Blog, Podcast).
-   **`backend/utils/`**: Service Layer. Heavy lifting logic (Selenium scripts, TTS conversion).
-   **`backend/models/`**: Data Layer. Pydantic models ensuring type safety across the app.

This separation ensures that if you want to swap Streamlit for a React app later, or swap Gemini for GPT-4, you only need to touch specific isolated modules.
