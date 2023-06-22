import av
import os
import sys
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)


from utils import get_mediapipe_pose
from process_frame import ProcessFrame
from thresholds import get_thresholds_beginner
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from streamlit_webrtc import (RTCConfiguration,VideoProcessorBase, WebRtcMode,webrtc_streamer,)
from PIL import Image


thresholds = None 
thresholds = get_thresholds_beginner()

live_process_frame = ProcessFrame(thresholds=thresholds, flip_frame=True)
# Initialize face mesh solution
pose = get_mediapipe_pose()


def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    frame, _ = live_process_frame.process(frame, pose)  # Process frame
    return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return BGR frame


#Streamlit
st.set_page_config(
   page_title="Ocalis Pose Analysis App",
   page_icon="🎈")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.set_option('deprecation.showfileUploaderEncoding', False)

image = Image.open(r'image/ocalis.png')
st.image(image)

ctx = webrtc_streamer(   
        key="deneme",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}], "sdpSemantics": "unified-plan"},
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True},
        async_processing=True,
        translations={
            "start": "👆 Start video recording",
            "stop": "Stop Analyze",})

with st.expander("See Analysis Section"):
        
    option = st.selectbox('Choose the sector name',('Automotive', 'Metal Production', 'Construction',"Plastic","Food"))
    analysis = st.button('📝 Show the analysis results')










    


