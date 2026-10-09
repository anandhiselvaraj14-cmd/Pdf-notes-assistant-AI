import streamlit as st
import pymupdf
from google import genai

st.set_page_config(page_title="AI PDF Notes Assistant", page_icon="📚")
st.title("📚 AI PDF Notes Assistant")
st.write("Upload study notes; AI can summarize, explain, and create quiz questions from the PDF text.")

pdf = st.file_uploader("Choose a text-based PDF", type=["pdf"])
if pdf:
    try:
        doc = pymupdf.open(stream=pdf.getvalue(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc).strip()
        st.caption(f"Pages: {len(doc)}")
        if not text:
            st.warning("Selectable text illa. Scanned PDF-ku OCR innum add pannala.")
        else:
            task = st.selectbox("AI enna seyyanum?", ["Summary", "Key points", "Quiz questions", "Explain simply"])
            if st.button("Generate with AI"):
                try:
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                    prompts = {
                        "Summary": "Summarize these study notes in clear simple language. Use only the provided content. Mention uncertainty rather than inventing facts.",
                        "Key points": "Extract the 8 most important study points from these notes. Use concise bullets and only provided content.",
                        "Quiz questions": "Create 5 revision questions from these notes, followed by a separate answer key. Use only provided content.",
                        "Explain simply": "Explain these notes in simple student-friendly language. Keep technical terms and define them. Use only provided content."
                    }
                    prompt = prompts[task] + "\n\nNOTES:\n" + text[:18000]
                    with st.spinner("AI notes-ai process pannudhu..."):
                        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    st.subheader(task)
                    st.write(response.text)
                    st.caption("AI output-la thappu irukkalaam; original PDF-oda compare panni verify pannunga.")
                except KeyError:
                    st.error("GEMINI_API_KEY set pannala. Streamlit app Secrets-la API key add pannunga.")
                except Exception as e:
                    st.error(f"AI request fail aachu: {e}")
            with st.expander("Extracted text preview"):
                st.text(text[:6000])
    except Exception as e:
        st.error(f"PDF read panna mudiyala: {e}")
