import streamlit as st
import speedtest
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import psutil
import threading

# Page configuration
st.set_page_config(
    page_title="NetPulse - Speed Test",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0D0F14 0%, #13161E 100%);
    }
    .metric-card {
        background: #1A1E2A;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #2A2F3E;
    }
    .title-text {
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #00D4FF, #00FF88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .subtitle-text {
        color: #6B7280;
        text-align: center;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'speed_history' not in st.session_state:
    st.session_state.speed_history = []
if 'test_count' not in st.session_state:
    st.session_state.test_count = 0

# Title
st.markdown('<p class="title-text">⚡ NetPulse</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Premium Speed Test Monitor</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Statistics")
    
    if st.session_state.speed_history:
        avg_download = sum([x['download'] for x in st.session_state.speed_history]) / len(st.session_state.speed_history)
        avg_upload = sum([x['upload'] for x in st.session_state.speed_history]) / len(st.session_state.speed_history)
        max_download = max([x['download'] for x in st.session_state.speed_history])
        max_upload = max([x['upload'] for x in st.session_state.speed_history])
        
        st.metric("Total Tests", len(st.session_state.speed_history))
        st.metric("Avg Download", f"{avg_download:.1f} Mbps")
        st.metric("Avg Upload", f"{avg_upload:.1f} Mbps")
        st.metric("Peak Download", f"{max_download:.1f} Mbps")
        st.metric("Peak Upload", f"{max_upload:.1f} Mbps")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    **NetPulse** is a professional speed test tool that helps you monitor your internet connection quality.
    
    Features:
    - Download/Upload Speed Test
    - Ping/Latency Measurement
    - Speed History Tracking
    - Real-time Monitoring
    """)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.speed_history = []
        st.session_state.test_count = 0
        st.rerun()

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📡 Speed Test", "📊 History", "🖧 Network Info"])

# Tab 1: Speed Test
with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🚀 Run Speed Test")
        
        if st.button("▶ START TEST", use_container_width=True, type="primary"):
            with st.spinner("Testing your internet connection..."):
                try:
                    # Initialize speedtest
                    st_test = speedtest.Speedtest()
                    
                    # Show progress
                    progress_bar = st.progress(0)
                    
                    # Find best server
                    st.markdown("📡 Finding best server...")
                    st_test.get_best_server()
                    progress_bar.progress(30)
                    
                    # Test download
                    st.markdown("📥 Testing download speed...")
                    download_speed = st_test.download() / 1_000_000
                    progress_bar.progress(60)
                    
                    # Test upload
                    st.markdown("📤 Testing upload speed...")
                    upload_speed = st_test.upload() / 1_000_000
                    progress_bar.progress(90)
                    
                    # Get ping
                    ping = st_test.results.ping
                    
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    
                    # Save to history
                    st.session_state.speed_history.append({
                        'timestamp': datetime.now(),
                        'download': download_speed,
                        'upload': upload_speed,
                        'ping': ping,
                        'test_no': len(st.session_state.speed_history) + 1
                    })
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### ✅ Test Complete!")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.markdown("""
                        <div class="metric-card" style="text-align:center">
                            <h3 style="color: #00D4FF; margin:0">📥 Download</h3>
                            <h1 style="margin:0">{:.1f}</h1>
                            <p style="color:#6B7280">Mbps</p>
                        </div>
                        """.format(download_speed), unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown("""
                        <div class="metric-card" style="text-align:center">
                            <h3 style="color: #00FF88; margin:0">📤 Upload</h3>
                            <h1 style="margin:0">{:.1f}</h1>
                            <p style="color:#6B7280">Mbps</p>
                        </div>
                        """.format(upload_speed), unsafe_allow_html=True)
                    
                    with col_c:
                        st.markdown("""
                        <div class="metric-card" style="text-align:center">
                            <h3 style="color: #FFD600; margin:0">⏱ Ping</h3>
                            <h1 style="margin:0">{:.0f}</h1>
                            <p style="color:#6B7280">ms</p>
                        </div>
                        """.format(ping), unsafe_allow_html=True)
                    
                    # Network Quality indicator
                    st.markdown("---")
                    quality = "🟢 Excellent" if download_speed > 50 else "🟡 Good" if download_speed > 20 else "🔴 Poor"
                    st.markdown(f"**Network Quality:** {quality}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure you have internet connection and speedtest-cli is installed")

# Tab 2: History
with tab2:
    if st.session_state.speed_history:
        # Create dataframe for history
        df_history = pd.DataFrame(st.session_state.speed_history)
        df_history['timestamp'] = pd.to_datetime(df_history['timestamp'])
        df_history = df_history.sort_values('timestamp')
        
        # Create interactive graph
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Download Speed History', 'Upload Speed History'),
            vertical_spacing=0.15
        )
        
        fig.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['download'],
                      mode='lines+markers', name='Download',
                      line=dict(color='#00D4FF', width=3),
                      marker=dict(size=8, color='#00D4FF')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['upload'],
                      mode='lines+markers', name='Upload',
                      line=dict(color='#00FF88', width=3),
                      marker=dict(size=8, color='#00FF88')),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            showlegend=True,
            plot_bgcolor='#13161E',
            paper_bgcolor='#13161E',
            font=dict(color='#E8EAF0')
        )
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Speed (Mbps)", row=1, col=1)
        fig.update_yaxes(title_text="Speed (Mbps)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show history table
        st.markdown("### 📋 Test History")
        display_df = df_history[['test_no', 'timestamp', 'download', 'upload', 'ping']].round(2)
        display_df.columns = ['Test #', 'Time', 'Download (Mbps)', 'Upload (Mbps)', 'Ping (ms)']
        display_df = display_df.sort_values('Test #', ascending=False)
        st.dataframe(display_df, use_container_width=True)
        
    else:
        st.info("📭 No tests performed yet. Go to the Speed Test tab to run your first test!")

# Tab 3: Network Info
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌐 Network Interfaces")
        
        # Get network interfaces info
        try:
            interfaces = psutil.net_if_stats()
            addresses = psutil.net_if_addrs()
            
            for iface, stats in interfaces.items():
                if stats.isup:
                    with st.expander(f"🔗 {iface}"):
                        st.metric("Speed", f"{stats.speed} Mbps" if stats.speed > 0 else "Unknown")
                        st.metric("MTU", stats.mtu)
                        st.metric("Duplex", stats.duplex)
                        
                        # Show IP addresses
                        for addr in addresses.get(iface, []):
                            if addr.family == 2:  # IPv4
                                st.write(f"📡 IPv4: `{addr.address}`")
                            elif addr.family == 23:  # IPv6
                                st.write(f"🌍 IPv6: `{addr.address}`")
        except Exception as e:
            st.warning("Could not fetch network interface information")
    
    with col2:
        st.markdown("### 💻 System Info")
        
        # System information
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            st.metric("CPU Usage", f"{cpu_percent}%")
            st.metric("RAM Usage", f"{memory.percent}%")
            st.metric("Available RAM", f"{memory.available / (1024**3):.1f} GB")
            
            # Network stats
            net_io = psutil.net_io_counters()
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Bytes Sent", f"{net_io.bytes_sent / (1024**3):.1f} GB")
            with col_b:
                st.metric("Bytes Received", f"{net_io.bytes_recv / (1024**3):.1f} GB")
                
        except Exception as e:
            st.warning("Could not fetch system information")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6B7280; font-size: 12px;'>"
    "© 2024 NetPulse | Premium Speed Test Monitor</p>",
    unsafe_allow_html=True
)
