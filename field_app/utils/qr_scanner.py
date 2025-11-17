"""
QR code scanning utilities using streamlit-webrtc and pyzbar.
"""
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
from pyzbar import pyzbar
import numpy as np
import cv2
from typing import Optional


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class QRScanner:
    """QR code scanner using webcam."""
    
    def __init__(self):
        """Initialize QR scanner."""
        self.scanned_code = None
    
    def video_frame_callback(self, frame):
        """Process video frame and detect QR codes."""
        img = frame.to_ndarray(format="bgr24")
        
        # Decode QR codes in the frame
        decoded_objects = pyzbar.decode(img)
        
        for obj in decoded_objects:
            # Extract QR code data
            qr_data = obj.data.decode('utf-8')
            
            # Store in session state
            if 'scanned_asset_id' not in st.session_state or st.session_state.scanned_asset_id != qr_data:
                st.session_state.scanned_asset_id = qr_data
                st.session_state.scan_complete = True
            
            # Draw rectangle around QR code
            points = obj.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                pts = np.array(pts, dtype=np.int32)
                cv2.polylines(img, [pts], True, (0, 255, 0), 3)
            
            # Draw QR code data
            x, y, w, h = obj.rect
            cv2.putText(img, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    def start_scanner(self):
        """Start the QR code scanner."""
        # Initialize session state
        if 'scan_complete' not in st.session_state:
            st.session_state.scan_complete = False
        if 'scanned_asset_id' not in st.session_state:
            st.session_state.scanned_asset_id = None
        
        # Start webcam stream
        webrtc_ctx = webrtc_streamer(
            key="qr-scanner",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            video_frame_callback=self.video_frame_callback,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        return webrtc_ctx
