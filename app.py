import streamlit as st
import random
import pandas as pd
from PIL import Image
import io
import base64
import time

# Page configuration
st.set_page_config(
    page_title="A/B Voting Studio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .card {
        background: #1e1e2e;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
    }
    .card h2 {
        color: #fff;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    .option-card {
        background: #2d2d44;
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    .option-card:hover {
        border-color: #667eea;
    }
    .vote-btn {
        width: 100%;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .vote-btn-a {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .vote-btn-a:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    .vote-btn-b {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .vote-btn-b:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
    }
    .stats-box {
        background: #2d2d44;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    .spin-wheel {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            #667eea 0deg 60deg,
            #764ba2 60deg 120deg,
            #f093fb 120deg 180deg,
            #f5576c 180deg 240deg,
            #4facfe 240deg 300deg,
            #00f2fe 300deg 360deg
        );
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: none;
    }
    .spin-wheel.spinning {
        animation: spin 0.5s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        background: #2d2d44;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    .persona-card {
        background: #2d2d44;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'title_a' not in st.session_state:
    st.session_state.title_a = "Option A"
if 'title_b' not in st.session_state:
    st.session_state.title_b = "Option B"
if 'appeal_a' not in st.session_state:
    st.session_state.appeal_a = 50
if 'appeal_b' not in st.session_state:
    st.session_state.appeal_b = 50
if 'image_a' not in st.session_state:
    st.session_state.image_a = None
if 'image_b' not in st.session_state:
    st.session_state.image_b = None
if 'human_votes_a' not in st.session_state:
    st.session_state.human_votes_a = 0
if 'human_votes_b' not in st.session_state:
    st.session_state.human_votes_b = 0
if 'ai_votes_a' not in st.session_state:
    st.session_state.ai_votes_a = 0
if 'ai_votes_b' not in st.session_state:
    st.session_state.ai_votes_b = 0
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'last_spin' not in st.session_state:
    st.session_state.last_spin = "-"
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'persona_count' not in st.session_state:
    st.session_state.persona_count = 50
if 'persona_results' not in st.session_state:
    st.session_state.persona_results = []

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 A/B Voting Studio</h1>
    <p>Upload options, collect votes, spin for points, and run AI persona simulations</p>
</div>
""", unsafe_allow_html=True)

# Section 1: Set Up A vs B
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("1️⃣ Set Up A vs B")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    st.markdown("### 🅰️ Option A")
    st.session_state.title_a = st.text_input("Title", value=st.session_state.title_a, key="title_a_input")
    uploaded_a = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="uploader_a")
    if uploaded_a:
        st.session_state.image_a = Image.open(uploaded_a)
        st.image(st.session_state.image_a, use_container_width=True)
    st.session_state.appeal_a = st.slider("AI Appeal Score", 0, 100, st.session_state.appeal_a, key="appeal_a_slider")
    st.caption("Used by AI persona simulation to influence voting")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    st.markdown("### 🅱️ Option B")
    st.session_state.title_b = st.text_input("Title", value=st.session_state.title_b, key="title_b_input")
    uploaded_b = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="uploader_b")
    if uploaded_b:
        st.session_state.image_b = Image.open(uploaded_b)
        st.image(st.session_state.image_b, use_container_width=True)
    st.session_state.appeal_b = st.slider("AI Appeal Score", 0, 100, st.session_state.appeal_b, key="appeal_b_slider")
    st.caption("Used by AI persona simulation to influence voting")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Section 2: User Voting
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("2️⃣ User Voting")
st.caption("Cast your vote for Option A or Option B")

vcol1, vcol2, vcol3 = st.columns([2, 2, 1])

with vcol1:
    if st.button(f"🗳️ Vote {st.session_state.title_a}", key="vote_a", use_container_width=True):
        st.session_state.human_votes_a += 1
        st.success(f"Voted for {st.session_state.title_a}!")
        time.sleep(0.5)
        st.rerun()

with vcol2:
    if st.button(f"🗳️ Vote {st.session_state.title_b}", key="vote_b", use_container_width=True):
        st.session_state.human_votes_b += 1
        st.success(f"Voted for {st.session_state.title_b}!")
        time.sleep(0.5)
        st.rerun()

with vcol3:
    if st.button("🔄 Reset", key="reset_human"):
        st.session_state.human_votes_a = 0
        st.session_state.human_votes_b = 0
        st.rerun()

# Vote statistics with progress bars
total_human = st.session_state.human_votes_a + st.session_state.human_votes_b
if total_human > 0:
    pct_a = (st.session_state.human_votes_a / total_human) * 100
    pct_b = (st.session_state.human_votes_b / total_human) * 100
else:
    pct_a = pct_b = 0

scol1, scol2, scol3 = st.columns(3)
with scol1:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number'>{st.session_state.human_votes_a}</div>", unsafe_allow_html=True)
    st.caption(f"Votes for {st.session_state.title_a}")
    st.progress(pct_a / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with scol2:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number'>{st.session_state.human_votes_b}</div>", unsafe_allow_html=True)
    st.caption(f"Votes for {st.session_state.title_b}")
    st.progress(pct_b / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with scol3:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number'>{total_human}</div>", unsafe_allow_html=True)
    st.caption("Total Votes")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Spin Wheel
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("3️⃣ Spin Wheel (0-50 Points)")
st.caption("Spin the wheel to earn random points!")

wcol1, wcol2, wcol3 = st.columns([1, 2, 1])

with wcol2:
    wheel_class = "spinning" if st.session_state.spinning else ""
    st.markdown(f'''
    <div class="spin-wheel {wheel_class}" id="wheel">
        {st.session_state.last_spin if not st.session_state.spinning else "?"}
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("🎰 SPIN!", key="spin_btn", use_container_width=True, type="primary"):
        st.session_state.spinning = True
        # Simulate spinning animation
        progress_bar = st.progress(0)
        for i in range(20):
            time.sleep(0.05)
            progress_bar.progress((i + 1) * 5)
        
        result = random.randint(0, 50)
        st.session_state.last_spin = result
        st.session_state.total_points += result
        st.session_state.spinning = False
        progress_bar.empty()
        st.rerun()

pcol1, pcol2 = st.columns(2)
with pcol1:
    st.metric("Last Spin", st.session_state.last_spin)
with pcol2:
    st.metric("Total Points", st.session_state.total_points)

st.markdown('</div>', unsafe_allow_html=True)

# Section 4: AI Persona Test
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("4️⃣ AI Persona Test (Pool: 200 Personas)")
st.caption("Simulate AI personas voting based on appeal scores")

st.session_state.persona_count = st.slider(
    "Personas to simulate this run", 
    1, 100, 
    st.session_state.persona_count,
    key="persona_slider"
)

aicol1, aicol2 = st.columns(2)

with aicol1:
    if st.button("🤖 Run AI Test", key="run_ai", use_container_width=True, type="primary"):
        with st.spinner(f"Simulating {st.session_state.persona_count} AI personas..."):
            time.sleep(1)
            
            # Generate persona profiles
            personas = []
            first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery", 
                          "Sam", "Jamie", "Drew", "Cameron", "Reese", "Parker", "Sage", "Dakota"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                         "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"]
            preferences = ["Visual", "Practical", "Innovative", "Traditional", "Bold", "Subtle"]
            
            votes_a = 0
            votes_b = 0
            
            for i in range(st.session_state.persona_count):
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                pref = random.choice(preferences)
                
                # Calculate vote probability based on appeal scores
                total_appeal = st.session_state.appeal_a + st.session_state.appeal_b
                if total_appeal == 0:
                    prob_a = 0.5
                else:
                    prob_a = st.session_state.appeal_a / total_appeal
                
                # Add some randomness
                prob_a += random.uniform(-0.1, 0.1)
                prob_a = max(0.1, min(0.9, prob_a))
                
                voted_a = random.random() < prob_a
                if voted_a:
                    votes_a += 1
                    vote = st.session_state.title_a
                else:
                    votes_b += 1
                    vote = st.session_state.title_b
                
                personas.append({
                    "name": name,
                    "preference": pref,
                    "vote": vote,
                    "confidence": random.randint(60, 98)
                })
            
            st.session_state.ai_votes_a += votes_a
            st.session_state.ai_votes_b += votes_b
            st.session_state.persona_results = personas
            
        st.success(f"AI simulation complete! {votes_a} voted A, {votes_b} voted B")
        time.sleep(0.5)
        st.rerun()

with aicol2:
    if st.button("🔄 Reset AI Votes", key="reset_ai"):
        st.session_state.ai_votes_a = 0
        st.session_state.ai_votes_b = 0
        st.session_state.persona_results = []
        st.rerun()

# AI Vote Statistics
total_ai = st.session_state.ai_votes_a + st.session_state.ai_votes_b
if total_ai > 0:
    ai_pct_a = (st.session_state.ai_votes_a / total_ai) * 100
    ai_pct_b = (st.session_state.ai_votes_b / total_ai) * 100
else:
    ai_pct_a = ai_pct_b = 0

aistat1, aistat2, aistat3 = st.columns(3)
with aistat1:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number' style='color: #667eea'>{st.session_state.ai_votes_a}</div>", unsafe_allow_html=True)
    st.caption("AI Votes A")
    st.progress(ai_pct_a / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with aistat2:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number' style='color: #f5576c'>{st.session_state.ai_votes_b}</div>", unsafe_allow_html=True)
    st.caption("AI Votes B")
    st.progress(ai_pct_b / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with aistat3:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='stats-number'>{total_ai}</div>", unsafe_allow_html=True)
    st.caption("Total AI Votes")
    st.markdown('</div>', unsafe_allow_html=True)

# Show persona results if available
if st.session_state.persona_results:
    with st.expander(f"📋 View Last {len(st.session_state.persona_results)} Persona Details"):
        df = pd.DataFrame(st.session_state.persona_results)
        st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

# Section 5: Combined Results Chart
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Combined Voting Results")

# Prepare data for chart
chart_data = pd.DataFrame({
    'Category': ['Human Votes', 'AI Votes', 'Total'],
    st.session_state.title_a: [
        st.session_state.human_votes_a,
        st.session_state.ai_votes_a,
        st.session_state.human_votes_a + st.session_state.ai_votes_a
    ],
    st.session_state.title_b: [
        st.session_state.human_votes_b,
        st.session_state.ai_votes_b,
        st.session_state.human_votes_b + st.session_state.ai_votes_b
    ]
})

st.bar_chart(chart_data.set_index('Category'), use_container_width=True)

# Summary table
total_a = st.session_state.human_votes_a + st.session_state.ai_votes_a
total_b = st.session_state.human_votes_b + st.session_state.ai_votes_b
total_all = total_a + total_b

if total_all > 0:
    st.markdown("---")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric(
            f"🏆 {st.session_state.title_a}", 
            f"{total_a} votes",
            f"{((total_a/total_all)*100):.1f}%"
        )
    
    with summary_col2:
        st.metric(
            f"🏆 {st.session_state.title_b}", 
            f"{total_b} votes",
            f"{((total_b/total_all)*100):.1f}%"
        )
    
    with summary_col3:
        winner = st.session_state.title_a if total_a > total_b else st.session_state.title_b if total_b > total_a else "Tie"
        st.metric("Winner", winner)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🎯 A/B Voting Studio - Built with Streamlit")
