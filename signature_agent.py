import streamlit as st
import requests
# ✅ CORRECT ENDPOINT
API_URL = "https://signature-agent-production.up.railway.app/compare"
st.set_page_config(page_title="Signature Agent", page_icon="✍️")
st.title("✍️ AI Signature Verification Agent")
st.write("Upload a signature image and the agent will verify it.")
uploaded_file = st.file_uploader(
   "Upload Signature Image",
   type=["png", "jpg", "jpeg"]
)
if uploaded_file is not None:
   st.image(uploaded_file, caption="Uploaded Signature", use_container_width=True)
   if st.button("Verify Signature"):
       with st.spinner("Agent is analysing..."):
           # ✅ IMPORTANT: send as real file
           files = {
               "file": (
                   uploaded_file.name,
                   uploaded_file.getvalue(),
                   uploaded_file.type
               )
           }
           try:
               response = requests.post(API_URL, files=files)
               if response.status_code == 200:
                   result = response.json()
                   st.success("✅ Verification Completed")
                   st.write(result)
               else:
                   st.error(f"API Error: {response.text}")
           except Exception as e:
               st.error(f"Connection Error: {e}")