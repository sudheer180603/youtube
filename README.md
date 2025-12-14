# YouTube-to-Blog + Podcast Automation

A local-only, end-to-end automation app that converts YouTube videos into SEO-friendly blog posts and podcasts.

## Features
- **YouTube Extraction**: Fetches video stats and transcripts.
- **AI Blog Generation**: Uses Gemini 1.5 Flash to write blog posts.
- **Fact Checking**: Uses Tavily AI to verify content.
- **WordPress Publishing**: Posts directly to your WP site.
- **Podcast Creation**: Converts text to MP3 and uploads to Spotify for Creators via Selenium automation.
- **WhatsApp Notifications**: Sends updates via Twilio.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env`.
   - Fill in your API keys and credentials.
   - **Note for Spotify**: 2FA might block automation. Use an app password or disable 2FA if possible for this account.

3. **Run the App**

   **Backend (Terminal 1)**
   ```bash
   uvicorn backend.main:app --reload
   ```
   *Runs on http://127.0.0.1:8000*

   **Frontend (Terminal 2)**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
   *Runs on http://localhost:8501*

## Usage
1. Paste a YouTube URL.
2. Click **Fetch Transcript**.
3. Edit the prompt if needed and **Generate Blog**.
4. Review/Edit the blog.
5. Click **Publish to WordPress** or **Run All** to automate publishing, WhatsApp notification, and Podcast upload.

## Notes
- The "Post Podcast" feature uses Selenium to control a Chrome browser. Do not interact with this browser window while it runs.
- Fact checking and Blog generation require valid API keys.
