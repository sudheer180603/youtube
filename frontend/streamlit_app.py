import streamlit as st
import requests
import json

# Setup
st.set_page_config(page_title="YouTube to Blog & Podcast", layout="wide", initial_sidebar_state="expanded")

# Backend URL
API_URL = "http://127.0.0.1:8000"

# Custom CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("frontend/static/style.css")

st.title("🎥 YouTube to Blog + 🎙️ Podcast Automation")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info("Ensure the Backend is running on port 8000.")
    run_all = st.button("🚀 Run All Steps", type="primary")

# Session State
if 'transcript_data' not in st.session_state:
    st.session_state.transcript_data = None
if 'generated_blog' not in st.session_state:
    st.session_state.generated_blog = None
if 'blog_title' not in st.session_state:
    st.session_state.blog_title = ""

# 1. Input & Transcript
st.subheader("1. 📥 Fetch Content")
url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Fetch Transcript"):
    if url:
        with st.spinner("Fetching transcript..."):
            try:
                response = requests.get(f"{API_URL}/transcript", params={"url": url})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.transcript_data = data
                    st.success("Transcript fetched!")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is it running?")

if st.session_state.transcript_data:
    data = st.session_state.transcript_data
    video = data.get('video_info', {})
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if video.get('thumbnail'):
            st.image(video['thumbnail'], use_column_width=True)
        st.write(f"**{video.get('title')}**")
        st.caption(f"Channel: {video.get('channel')}")
    
    with col2:
        with st.expander("Show Transcript Preview"):
            st.text_area("Transcript", data['full_text'], height=200)

    # 2. Blog Generation
    st.subheader("2. ✍️ Generate Blog")
    
    default_prompt = "Convert this YouTube transcript into a well-structured, SEO-friendly blog post in a friendly, informative tone. Use H2 and H3 headings. Include a catchy intro and a conclusion."
    prompt = st.text_area("Custom Prompt", value=default_prompt, height=100)
    
    if st.button("Generate Blog") or (run_all and not st.session_state.generated_blog):
        with st.spinner("Generating blog with LLM..."):
            req_data = {
                "transcript": data['full_text'],
                "prompt": prompt,
                "video_info": video
            }
            res = requests.post(f"{API_URL}/generate-blog", json=req_data)
            if res.status_code == 200:
                blog_res = res.json()
                st.session_state.generated_blog = blog_res['content']
                st.session_state.blog_title = blog_res['title']
                st.session_state.blog_summary = blog_res['summary'] # Assuming backend returns this
                st.success("Blog Generated!")
            else:
                st.error("Failed to generate blog.")

# 3. Operations
if st.session_state.generated_blog:
    st.subheader("3. 🛠️ Edit & Publish")
    
    blog_title_input = st.text_input("Blog Title", value=st.session_state.blog_title)
    blog_content_input = st.text_area("Blog Content (Markdown)", value=st.session_state.generated_blog, height=400)
    
    st.markdown("### Preview")
    st.markdown(blog_content_input)
    
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    
    # Checkbox options
    send_wa = st.checkbox("Send to WhatsApp")
    post_podcast = st.checkbox("Create & Upload Podcast")

    if st.button("Publish to WordPress") or run_all:
        with st.spinner("Publishing to WordPress..."):
            wp_data = {
                "title": blog_title_input,
                "content": blog_content_input,
                "excerpt": st.session_state.get('blog_summary', ''),
                "tags": ["Automated", "YouTube"]
            }
            res = requests.post(f"{API_URL}/publish-wordpress", json=wp_data)
            if res.status_code == 200:
                wp_res = res.json()
                st.success(f"Published! [View Post]({wp_res['url']})")
                st.session_state.wp_url = wp_res['url']
            else:
                st.error("WordPress publish failed.")

    if st.button("Run Fact Check"):
         with st.spinner("Checking facts..."):
             res = requests.post(f"{API_URL}/check-facts", json={"content": blog_content_input})
             if res.status_code == 200:
                 st.info(res.json()['analysis'])
             else:
                 st.error("Fact check failed.")

    # Post-generation actions (WhatsApp & Podcast)
    if run_all or st.button("Process Extras (WA/Podcast)"):
        # WhatsApp
        if send_wa:
            with st.spinner("Sending WhatsApp..."):
                msg = f"New Post: {blog_title_input}\n\n{st.session_state.get('blog_summary', '')}\n\nLink: {st.session_state.get('wp_url', 'pending...')}"
                res = requests.post(f"{API_URL}/send-whatsapp", json={"message": msg})
                if res.status_code == 200:
                    st.success("WhatsApp Sent!")
                else:
                    st.error("WhatsApp failed.")
        
        # Podcast
        if post_podcast:
            with st.spinner("Creating & Uploading Podcast... (This may take a minute)"):
                pod_data = {
                    "text": blog_content_input,
                    "title": blog_title_input,
                    "description": st.session_state.get('blog_summary', 'Generated podcast')
                }
                res = requests.post(f"{API_URL}/create-and-upload-podcast", json=pod_data)
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error("Podcast creation failed.")

