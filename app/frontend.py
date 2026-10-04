import streamlit as st
import requests

st.set_page_config(page_title="Autonomous Content Engine", page_icon="🚀", layout="wide")

st.title("🚀 Autonomous Multi-Agent Content Engine")
st.write("Generate viral LinkedIn posts with matching custom graphics powered entirely by Google Gemini.")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("Enter your topic:", placeholder="e.g., Why multi-agent systems are the future of software engineering")
    
    # Clean and direct options in the dropdown
    output_format = st.selectbox(
        "Select Output Format", 
        [
            "LinkedIn Post", 
            "Blog Post", 
            "Research Brief", 
            "Technical Article"
        ]
    )
    generate_btn = st.button("Generate Post & Graphic", type="primary")

if generate_btn:
    if not topic.strip():
        st.warning("Please enter a valid topic.")
    else:
        with st.spinner("🤖 Agents are researching and Gemini is rendering your graphic... (takes ~30 seconds)"):
            try:
                response = requests.post(
                    "http://content-engine:8000/generate",
                    json={"topic": topic, "output_format": output_format}
                )
                if response.status_code == 200:
                    data = response.json()
                    
                    with col2:
                        st.markdown(f"### 📝 Generated Content")
                        st.text_area("Ready to copy:", value=data["content"], height=550)
                        
                        if data.get("image_url"):
                            st.markdown("### 🎨 AI-Generated Gemini Graphic")
                            st.image(data["image_url"], caption="Custom Visual generated via Gemini", use_container_width=True)
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")