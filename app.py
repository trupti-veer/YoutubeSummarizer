import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

##Load all environment variables
load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from youtube_transcript_api import YouTubeTranscriptApi

##Prompt to generate the summart
prompt1 ="""
            You are an expert Youtube video summarizer. You will take the video transcript text and
            summarize the entire video hightlighting the important points and takeaways in the video in summary format 
            using around 250-300 words. The transcript text will be appended here : 
        """

prompt2 ="""
            Summarize this text as bullets points of key information in around 250-300 words. The transcript text will be appended here :         
        """
        
## Get the transcript for a particular youtube video
def get_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text_list = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for transcript_text in transcript_text_list:
            transcript += " " +transcript_text["text"]

        return transcript
    except Exception as e:
        raise e


## Get the summary from Gemini Pro based on prompt given
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.set_page_config(page_title="Transcript to Notes Converter")
st.title("Transcript to Notes Converter")
video_link = st.text_input("Enter Youtube Video Link:")

if video_link:
    video_id = video_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Notes"):
    transcript_text = get_transcript_details(video_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt2)
        st.write(summary)


