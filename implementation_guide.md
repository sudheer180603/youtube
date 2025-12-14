# Step-by-Step Implementation & Run Guide

Follow these steps to set up and run the YouTube-to-Blog + Podcast Automation project on your local machine.

## 1. Prerequisites
- **Python 3.10+**: Ensure Python is installed and added to your PATH.
- **Chrome Browser**: Required for the Selenium-based Spotify uploader.
- **Git** (Optional): If you want to version control the code.

## 2. API Keys & Credentials
You need to gather the following credentials before running the app:

### Essential
- **Google Gemini API Key**:
  - Go to [Google AI Studio](https://aistudio.google.com/).
  - Create a new API key.
- **Spotify Account**:
  - You need a regular Spotify account.
  - **Important**: If you have 2-Factor Authentication (2FA) enabled, the automation script might get stuck. It is recommended to use an App Password if supported or a separate account without 2FA for automation.

### Integrations (Optional but Recommended)
- **Tavily API Key** (for Fact Checking):
  - Sign up at [Tavily](https://tavily.com/).
- **WordPress Credentials**:
  - URL of your WordPress site (e.g., `https://mysite.com`).
  - Username.
  - **App Password**: Go to `Users > Profile` in WordPress admin, scroll down to "Application Passwords", and create a new one. Do **not** use your main login password.
- **Twilio Credentials** (for WhatsApp):
  - Sign up at [Twilio](https://www.twilio.com/).
  - Get Account SID and Auth Token.
  - Set up the WhatsApp Sandbox.

## 3. Project Setup

1.  **Open Terminal/Command Prompt** in the project folder:
    ```cmd
    cd "c:/Users/Venkata Sudheer.P/Documents/Temp/youtube-to-blog"
    ```

2.  **Create Virtual Environment** (Recommended):
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```cmd
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    - Open the `.env` file in the project root.
    - Paste your keys after the `=` signs.
    - Example:
      ```env
      GEMINI_API_KEY=AIzaSy...
      WORDPRESS_URL=https://myblog.com
      WORDPRESS_USERNAME=admin
      WORDPRESS_APP_PASSWORD=abcd-efgh-ijkl-mnop
      ```

## 4. Running the Application

You need two separate terminal windows running simultaneously.

### Terminal 1: Backend
Start the FastAPI server.
```cmd
uvicorn backend.main:app --reload
```
- You should see: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Frontend
Start the Streamlit UI.
```cmd
streamlit run frontend/streamlit_app.py
```
- Your browser should automatically open `http://localhost:8501`.

## 5. Using the App

1.  **Fetch Transcript**:
    - Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
    - Click **Fetch Transcript**.
    - Verify the transcript loads in the preview.

2.  **Generate Blog**:
    - Modify the "Custom Prompt" if you want specific tone/style.
    - Click **Generate Blog**.
    - Wait a few seconds for Gemini to generate the content.

3.  **Publish & Repurpose**:
    - Edit the generated blog if needed.
    - **Publish to WordPress**: Click to post immediately.
    - **Run Fact Check**: Verifies claims against the web using Tavily.
    - **Post Podcast**:
        - Check "Create & Upload Podcast".
        - Click "Process Extras".
        - **Watch your computer**: A Chrome window will open. Do not click anything; let the bot log in to Spotify and upload the MP3.

## 6. Troubleshooting
- **Browser crashes immediately**: Ensure you have Chrome installed. `webdriver-manager` should handle the driver automatically.
- **Connection Error**: Ensure the backend (Terminal 1) is running.
- **Authentication Error**: Check your keys in `.env`.
