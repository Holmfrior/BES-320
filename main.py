import streamlit as st
import streamlit.components.v1 as component
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config
import random


# 1. PAGE CONFIGURATION
st.set_page_config(layout="wide", page_title="BES-320")

# 2. INITIALIZE SESSION STATES
# This ensures all necessary variables exist before the app runs its logic
if "page" not in st.session_state:
    st.session_state.page = "Landing"

if "active_rel" not in st.session_state:
    st.session_state.active_rel = None

if "current_ex" not in st.session_state:
    st.session_state.current_ex = None
if "user_edges" not in st.session_state:
    st.session_state.user_edges = []
if "active_relations" not in st.session_state:
    st.session_state.active_relations = []
if "checked" not in st.session_state:
    st.session_state.checked = False

# --- DATA: EXERCISE DATABASE ---
EX_DATABASE = [
    {
        "text": "Mercedes officials said they expect flat sales next year.",
        "edus": ["Mercedes officials said", "they expect flat sales next year"],
        "relation": "Attribution",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The manual treats complements of attribution verbs as separate EDUs, even if they form one grammatical sentence."
    },
    {
        "text": "The explosions began when a seal blew out.",
        "edus": ["The explosions began", "when a seal blew out"],
        "relation": "Cause",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The causal connection is identified between two clausal units within the same sentence."
    },
    {
        "text": "The government said the consumer price index rose 0.5% in September.",
        "edus": ["The government said", "the consumer price index rose 0.5% in September."],
        "relation": "Attribution",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The first unit attributes the information in the second unit to an official source."
    },
    {
        "text": "Analysts estimated that sales at U.S. stores declined in the quarter.",
        "edus": ["Analysts estimated", "that sales at U.S. stores declined in the quarter."],
        "relation": "Attribution",
        "difficulty": "Easy",
         "source": "RST-DT (News)",
        "logic": "Used with a cognitive predicate ('estimated') to separate the source from the estimate."
    },
    {
        "text": "The budget deficit widened because tax receipts fell.",
        "edus": ["The budget deficit widened", "because tax receipts fell."],
        "relation": "Cause",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides the direct cause for the situation described in the first unit."
    },
    {
        "text": "The airline is limiting the programs to reduce its high costs.",
        "edus": ["The airline is limiting the programs", "to reduce its high costs."],
        "relation": "Cause",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit (the goal) is the reason for the action taken in the first unit."
    },
    {
        "text": "The company's earnings fell, but its revenue rose 10%.",
        "edus": ["The company's earnings fell,", "but its revenue rose 10%."],
        "relation": "Contrast",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A multinuclear relation where two opposing facts about the company's performance are compared."
    },
    {
        "text": "Although the economy is slowing, consumer spending remains high.",
        "edus": ["Although the economy is slowing,", "consumer spending remains high."],
        "relation": "Contrast",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A concession relation where the 'although' clause raises an expectation that is countered by the second unit."
    },
    {
        "text": "S.A. Brewing would make a takeover offer if it exercises the option.",
        "edus": ["S.A. Brewing would make a takeover offer", "if it exercises the option."],
        "relation": "Condition",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The truth or realization of the first unit depends on the fulfillment of the condition in the second."
    },
    {
        "text": "Unless the board approves the deal, the merger will fail.",
        "edus": ["Unless the board approves the deal,", "the merger will fail."],
        "relation": "Condition",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A negative condition where the second unit's outcome is tied to the first unit not happening."
    },
    {
        "text": "The company announced a new product, a high-speed computer.",
        "edus": ["The company announced a new product,", "a high-speed computer."],
        "relation": "Elaboration",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides additional detail (Object-Attribute) about the product mentioned in the first."
    },
    {
        "text": "The firm hired a new CEO, who was formerly at Apple.",
        "edus": ["The firm hired a new CEO,", "who was formerly at Apple."],
        "relation": "Elaboration",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit is a relative clause providing more information about the subject in the first."
    },
    {
        "text": "The index rose 5 points before closing at 2500.",
        "edus": ["The index rose 5 points", "before closing at 2500."],
        "relation": "Temporal",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "Establishes a clear chronological sequence between the two events using 'before'."
    },
    {
        "text": "The dollar fell when the news reached the market.",
        "edus": ["The dollar fell", "when the news reached the market."],
        "relation": "Temporal",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "Specifies the time at which the main event occurred."
    },
    {
        "text": "Investors are selling shares to lock in recent profits.",
        "edus": ["Investors are selling shares", "to lock in recent profits."],
        "relation": "Enablement",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit describes the goal (purpose) that the first unit is intended to achieve."
    },
    {
        "text": "Earnings were flat, compared with a profit a year ago.",
        "edus": ["Earnings were flat,", "compared with a profit a year ago."],
        "relation": "Comparison",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides a specific point of comparison to contextualize the first unit."
    }
]

RELATION_GROUPS = ["Attribution", "Background", "Cause", "Comparison", "Condition", "Contrast", 
                   "Elaboration", "Enablement", "Evaluation", "Explanation", "Joint", 
                   "Manner-Means", "Topic-Comment", "Summary", "Temporal", "Topic Change"]

if st.session_state.page != "Landing":
    with st.sidebar:
        # Custom CSS for the Sidebar Container itself
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {
                    background-color: #11141a !important; /* Slightly darker than main app */
                    border-right: 1px solid rgba(255, 255, 255, 0.05);
                }
                [data-testid="stSidebarNav"] {
                    background-color: transparent !important;
                }
            </style>
        """, unsafe_allow_html=True)

        selected_page = option_menu(
            menu_title="DD-AI Menu", 
            options=["Landing", "Theory", "Practice"], 
            icons=["house", "book", "pencil"], 
            menu_icon="cpu", # Changed to 'cpu' for a more techy feel
            default_index=["Landing", "Theory", "Practice"].index(st.session_state.page),
            styles={
                "container": {"padding": "5px!", "background-color": "transparent"},
                "icon": {"color": "#8b92a5", "font-size": "18px"}, 
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "5px", 
                    "color": "#d1d5db",
                    "--hover-color": "rgba(224, 108, 117, 0.1)" # Faint rose glow on hover
                },
                "nav-link-selected": {
                    "background-color": "#e06c75", # Matches your Practice Title gradient
                    "font-weight": "bold",
                    "color": "white"
                },
                "menu-title": {
                    "color": "#8b92a5",
                    "font-weight": "700",
                    "text-transform": "uppercase",
                    "letter-spacing": "1px"
                }
            }
        )

        # If they click a different menu item, update and rerun
        if st.session_state.page != selected_page:
            st.session_state.page = selected_page
            st.rerun()

# CASE 1: LANDING PAGE
if st.session_state.page == "Landing":
    
    # 1. Particles.js Background via HTML Component
    # We use a CDN so you don't have to manage local JS files
    particles_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                /* Background color for the particle canvas */
                background-color: #0e1117; 
            }
            #particles-js {
                width: 100vw;
                height: 100vh;
                position: absolute;
                top: 0;
                left: 0;
            }
        </style>
    </head>
    <body>
        <div id="particles-js"></div>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            particlesJS("particles-js", {
              "particles": {
                "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#ff4b4b" }, /* Matches your button! */
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5, "random": false },
                "size": { "value": 3, "random": true },
                "line_linked": { 
                    "enable": true, 
                    "distance": 150, 
                    "color": "#ff4b4b", /* Matches your button! */
                    "opacity": 0.4, 
                    "width": 1 
                },
                "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
              },
              "interactivity": {
                "detect_on": "canvas",
                "events": {
                  "onhover": { "enable": true, "mode": "grab" }, /* Creates lines to mouse on hover */
                  "onclick": { "enable": true, "mode": "push" }, /* Adds more particles on click */
                  "resize": true
                },
                "modes": {
                  "grab": { "distance": 140, "line_linked": { "opacity": 1 } },
                  "push": { "particles_nb": 4 }
                }
              },
              "retina_detect": true
            });
        </script>
    </body>
    </html>
    """
    
    # Inject the HTML component
    component.html(particles_html, height=0, width=0)

    # 2. Advanced CSS for Branding, Interactivity, Centering, and making the Background work
    st.markdown("""
        <style>
        /* --- PARTICLES BACKGROUND FIX --- */
        /* Forces the component iframe to act as a full-screen background */
        iframe {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw !important;
            height: 100vh !important;
            z-index: -1; /* Puts it behind everything */
            border: none;
        }

        /* Makes the default Streamlit background transparent so we can see the particles */
        .stApp {
            background-color: transparent !important;
        }
        /* --- END PARTICLES FIX --- */

        /* 1. Hero Text Gradient */
        .hero-title {
            font-size: 6rem !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, #ff4b4b, #ff8a8a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0px !important;
            padding-bottom: 10px !important;
        }

        /* 2. Professional Subtitles */
        .hero-subtitle {
            font-size: 2.2rem !important;
            font-weight: 300 !important;
            color: #FAFAFA; /* Changed to white/light for dark mode particle background */
            text-align: center;
            margin-top: -15px !important;
        }
        
        /* 3. Description */
        .hero-desc {
            font-size: 1.3rem !important;
            color: #A0A5B5; /* Lightened for contrast */
            text-align: center;
            margin-bottom: 30px !important; 
        }

        /* 4. Get Started Button Styling */
        div[data-testid="stButton"] > button {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 0.8rem !important; 
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 10px 25px rgba(255, 75, 75, 0.5) !important;
            background-color: #ff3333 !important;
        }

        /* 5. Layout Container */
        .landing-hero {
            padding-top: 150px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            width: 100%; 
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Branding Header Section
    st.markdown('<div class="landing-hero">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">DD-AI</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="hero-subtitle">A New Way to Learn.</h2>', unsafe_allow_html=True)
    st.markdown('<p class="hero-desc">Learn How to Link Ideas together.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) 
    
    # 4. Main Entry Action - Centered via Streamlit Columns
    col1, col2, col3 = st.columns([1, 1.5, 1]) 
    
    with col2:
        if st.button("🚀 Get Started", type="primary", use_container_width=True):
            st.session_state.page = "Theory"
            st.rerun()



# --- THEORY PAGE CONTENT ---
if st.session_state.page == "Theory":
    
# 1. Inject Custom CSS for the Theory Page to match the Landing Page styling
    st.markdown("""
        <style>
        /* Force dark background to match landing page */
        .stApp {
            background-color: #0e1117 !important;
        }
        
        .theory-title {
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, #ff4b4b, #ff8a8a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px !important;
        }
        .section-title {
            font-size: 2rem !important;
            font-weight: 300 !important;
            color: #FAFAFA !important;
            text-align: center;
            margin-top: 10px !important;
        }
        .section-desc {
            font-size: 1.1rem !important;
            color: #A0A5B5 !important;
            text-align: center;
            margin-bottom: 25px !important;
        }
        .concept-box {
            background-color: rgba(255, 255, 255, 0.03); 
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px; 
            border-radius: 12px; 
            text-align: center; 
            min-height: 130px;
            transition: all 0.3s ease;
        }
        .concept-box:hover {
            transform: translateY(-5px);
            background-color: rgba(255, 255, 255, 0.05); 
        }
        .concept-title {
            font-weight: 700;
            font-size: 1.3rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .concept-text {
            margin-top: 12px; 
            color: #A0A5B5;
            font-size: 1rem;
        }
        .definition-box {
            background: rgba(255, 255, 255, 0.03); 
            border-left: 4px solid #ff4b4b; 
            padding: 15px 20px; 
            margin-bottom: 20px;
            border-radius: 0 8px 8px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='theory-title'>THEORETICAL GUIDE</h1>", unsafe_allow_html=True)
    st.divider()

    # Section 1: EDUs
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("<h2 class='section-title'>1. Elementary Discourse Units (EDUs)</h2>", unsafe_allow_html=True)
        st.markdown("<p class='section-desc'>Every text is made of minimal building blocks called EDUs, which are typically single clauses.</p>", unsafe_allow_html=True)
        
# Replaced annotated_text with raw HTML to enforce centering and background wrapper
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px; padding: 25px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                    She was willing to skip class 
                    <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>EDU 1</span>
                </span>
                <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                    to attend the opening exhibit. 
                    <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>EDU 2</span>
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Section 2: Nucleus vs Satellite
    _, center_col_2, _ = st.columns([1, 2, 1])
    with center_col_2:
        st.markdown("<h2 class='section-title'>2. Nucleus vs. Satellite</h2>", unsafe_allow_html=True)
        st.markdown("<p class='section-desc'>Relations usually consist of an essential <b>Nucleus</b> and a supporting <b>Satellite</b>.</p>", unsafe_allow_html=True)

        nuc_col, sat_col = st.columns(2)
        with nuc_col:
            st.markdown("""
                <div class='concept-box' style='border-color: rgba(255, 75, 75, 0.3);'>
                    <div class='concept-title' style='color: #ff4b4b;'>The Nucleus</div>
                    <div class='concept-text'>Essential info that makes sense in isolation.</div>
                </div>
            """, unsafe_allow_html=True)

        with sat_col:
            st.markdown("""
                <div class='concept-box' style='border-color: rgba(255, 138, 138, 0.3);'>
                    <div class='concept-title' style='color: #ff8a8a;'>The Satellite</div>
                    <div class='concept-text'>Supporting info that depends on the nucleus.</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Section 3: Rhetorical Relations
    st.markdown("<h2 class='section-title'>3. Rhetorical Relations</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>There are 16 functional groups that act as the 'Glue' for cohesion.</p>", unsafe_allow_html=True)
    
    other_relations = {
        "Background": "background, circumstance",
        "Cause": "cause, result, consequence",
        "Comparison": "comparison, preference, analogy",
        "Condition": "condition, hypothetical, contingency",
        "Contrast": "contrast, concession, antithesis",
        "Elaboration": "elaboration-additional, example, definition",
        "Enablement": "purpose, enablement",
        "Evaluation": "evaluation, interpretation, comment",
        "Explanation": "evidence, argumentative, reason",
        "Joint": "list, disjunction",
        "Manner-Means": "manner, means",
        "Topic-Comment": "problem-solution, question-answer",
        "Summary": "summary, restatement",
        "Temporal": "temporal-before, sequence",
        "Topic Change": "topic-shift, topic-drift",
    }

    col_left, col_center, col_right = st.columns([1, 5, 1])
    with col_center:
        all_names = ["Attribution"] + list(other_relations.keys())
        
        # Button grid (Centered)
        for i in range(0, len(all_names), 4):
            btn_cols = st.columns(4)
            for j in range(4):
                if i + j < len(all_names):
                    name = all_names[i+j]
                    with btn_cols[j]:
                        # Make the active button distinct
                        btn_type = "primary" if st.session_state.active_rel == name else "secondary"
                        if st.button(name, use_container_width=True, key=f"btn_{name}", type=btn_type):
                            st.session_state.active_rel = name
                            st.rerun()

        # DYNAMIC RELATION CONTENT
        if st.session_state.active_rel == "Attribution":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Attribution</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>Attribution is used for reported speech (direct or indirect) and cognitive acts (feelings, thoughts, hopes).</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                    <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                        Mercedes officials said 
                        <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                    </span>
                    <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                        they expect flat sales next year 
                        <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="ATTRIBUTION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nMercedes officials said", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nthey expect flat sales next year", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite is the source and the Nucleus is the content of the message.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Background":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Background</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite establishes the context or history with respect to which the nucleus is to be interpreted.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Tension has been brewing for months. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Yesterday, the workers finally went on strike. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Background
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="BACKGROUND", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nTension has been brewing for months.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nYesterday, the workers finally went on strike.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite provides the historical or contextual setup necessary to fully understand the main event in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Cause":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Cause</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite presents a situation that is the direct cause, reason, or consequence of the situation presented in the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The budget deficit widened 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            because tax receipts fell. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Cause
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="CAUSE", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nbecause tax receipts fell.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe budget deficit widened", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite provides the direct reason or cause for the situation described in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Comparison":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Comparison</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite provides a specific point of comparison to contextualize the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Earnings were flat, 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            compared with a profit a year ago. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Comparison
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="COMPARISON", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\ncompared with a profit a year ago.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nEarnings were flat,", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite highlights a similarity or difference to give the main point in the Nucleus more context.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Condition":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Condition</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The truth or realization of the nucleus depends on the fulfillment of the condition in the satellite.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            S.A. Brewing would make a takeover offer 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            if it exercises the option. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Condition
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="CONDITION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nif it exercises the option.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nS.A. Brewing would make a takeover offer", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite ("if...") acts as the requirement for the Nucleus to happen.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Contrast":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Contrast</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>Highlights opposing facts. When structured as a Nucleus-Satellite (like a Concession), the satellite raises an expectation that is countered by the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Although the economy is slowing, 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            consumer spending remains high. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Contrast
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="CONTRAST", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nAlthough the economy is slowing,", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nconsumer spending remains high.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite sets up a premise, but the Nucleus contradicts the expected outcome.
                </div>
                """, unsafe_allow_html=True)


        elif st.session_state.active_rel == "Evaluation":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Evaluation</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite provides an assessment, interpretation, or opinion of the situation presented in the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The stock market surged 500 points today. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            It was a remarkable recovery. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="EVALUATION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nIt was a remarkable recovery.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe stock market surged 500 points today.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite offers a subjective judgment or evaluation of the objective event in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Explanation":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Explanation</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite provides reasoning, evidence, or argumentative support for the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The CEO was forced to resign 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            because he repeatedly violated company policies. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="EXPLANATION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nbecause he repeatedly violated company policies.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe CEO was forced to resign", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite explains the "why" or provides evidence to justify the statement in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Joint":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Joint</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>A multinuclear relation where the units form a list or a disjunction (e.g., connected by "and" or "or") with equal weight.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Apple released a new phone, 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus 1</span>
                        </span>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            and Microsoft updated its operating system. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus 2</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Joint uses TWO nuclei, no satellite
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="JOINT", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Nucleus1 [label="Nucleus 1:\\nApple released a new phone,", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Nucleus2 [label="Nucleus 2:\\nand Microsoft updated its operating system.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus1 [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Nucleus2 [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    Because this is a list of independent, equal facts, both units are considered a Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Manner-Means":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Manner-Means</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite specifies the method, manner, or means by which the action in the nucleus is achieved.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The company cut costs 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            by laying off 10% of its workforce. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="MANNER-MEANS", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nby laying off 10% of its workforce.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe company cut costs", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite answers the question of "how" the Nucleus was accomplished.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Topic-Comment":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Topic-Comment</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite introduces a general topic or problem, and the nucleus provides a specific comment, solution, or answer to it.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            As for the new tax legislation, 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            it will likely pass next week. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="TOPIC-COMMENT", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nAs for the new tax legislation,", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nit will likely pass next week.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite merely sets the stage (the topic), while the Nucleus delivers the actual news (the comment).
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Summary":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Summary</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite provides a concise summary or restatement of the information presented in the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Sales plummeted, costs skyrocketed, and morale was low. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            In short, it was a disastrous year. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="SUMMARY", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nIn short, it was a disastrous year.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nSales plummeted, costs skyrocketed...", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite wraps up the complex information of the Nucleus into a single, easily digestible point.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Topic Change":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Topic Change</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>A multinuclear relation indicating a major shift or drift in the topic being discussed. Both units carry equal weight but address completely different subjects.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The corporate merger was finalized yesterday. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus 1</span>
                        </span>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            In other news, inflation dropped to 2%. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus 2</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Topic Change uses TWO nuclei, no satellite
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="TOPIC\\nCHANGE", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Nucleus1 [label="Nucleus 1:\\nThe corporate merger was finalized...", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Nucleus2 [label="Nucleus 2:\\nIn other news, inflation dropped to 2%.", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus1 [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Nucleus2 [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    Since there is an abrupt shift in subject matter, both events are independent Nuclei.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Elaboration":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Elaboration</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite provides additional details, examples, or definitions about the subject mentioned in the nucleus.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The company announced a new product, 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            a high-speed computer. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Elaboration
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="ELABORATION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\na high-speed computer.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe company announced a new product,", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite adds specific details to flesh out the entity or concept introduced in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Enablement":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Enablement</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite describes the goal or purpose that the action in the nucleus is intended to achieve.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            Investors are selling shares 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            to lock in recent profits. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Enablement
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="ENABLEMENT", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nto lock in recent profits.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nInvestors are selling shares", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite sets the underlying goal or purpose for the action described in the Nucleus.
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_rel == "Temporal":
            st.divider()
            st.markdown("<h4 class='section-title' style='color: #ff4b4b !important;'>Temporal</h4>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='definition-box'>
                    <span style='color: #FAFAFA; font-weight: bold;'>Definition:</span> 
                    <span style='color: #A0A5B5;'>The satellite establishes a clear chronological sequence or specifies the time at which the main event occurred.</span>
                </div>
                """, unsafe_allow_html=True)
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("""
                    <div style='text-align: center; margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 10px; line-height: 2.5;'>
                        <span style='background: #ff4b4b; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            The index rose 5 points 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Nucleus</span>
                        </span>
                        <span style='background: #ff8a8a; color: white; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin: 0 0.2rem;'>
                            before closing at 2500. 
                            <span style='font-size: 0.75em; font-weight: 700; opacity: 0.8; margin-left: 0.3rem; text-transform: uppercase;'>Satellite</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Darkened Graphviz chart for Temporal
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true, bgcolor=transparent] node [shape=box, style="filled,rounded", fontname="Helvetica", color="#333333", penwidth=1] Relation [label="TEMPORAL", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse, color="#ff4b4b"] Satellite [label="Satellite:\\nbefore closing at 2500.", fillcolor="#1e1e24", fontcolor="#FAFAFA"] Nucleus [label="Nucleus:\\nThe index rose 5 points", fillcolor="#2b2d35", fontcolor="#FAFAFA"] Relation -> Nucleus [label="Nucleus", arrowhead=none, color="#ff4b4b", fontcolor="#ff4b4b"] Relation -> Satellite [label="Satellite", style=dashed, color="#ff8a8a", fontcolor="#ff8a8a"] }', use_container_width=True)
                
                st.markdown("""
                <div style='text-align: center; color: #A0A5B5; font-size: 0.95rem; margin-top: 10px; font-style: italic;'>
                    The Satellite tells us exactly when the event in the Nucleus took place or its relative order in time.
                </div>
                """, unsafe_allow_html=True)

# --- PRACTICE PAGE CONTENT ---
elif st.session_state.page == "Practice":

    # 1. Inject Softer Dark Mode & Custom Styling
    st.markdown("""
        <style>
        /* Force dark background */
        .stApp {
            background-color: #151821 !important; 
        }
        
        /* Practice Page Title */
        .practice-title {
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, #e06c75, #e59299); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px !important;
        }

        /* BRIGHTNESS FIX for Radio Buttons */
        div[data-testid="stRadio"] label p {
            color: #FFFFFF !important; 
            font-weight: 700 !important;   
            font-size: 1.1rem !important;  
            text-shadow: 0px 0px 5px rgba(255, 255, 255, 0.2) !important;
        }

        /* Additional Radio Label Styling */
        div[data-testid="stRadio"] label {
            color: #FAFAFA !important; 
            font-weight: 500 !important;
            font-size: 1rem !important;
        }

        /* Container Styling */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #1e222d !important; 
        }

        .edu-text {
            color: #d1d5db; 
            font-size: 1.1rem;
            line-height: 1.6;
            text-align: center;
            padding: 10px;
        }
                
                /* Reduce overall brightness and add a soft fade */
        .stApp {
            filter: contrast(0.95) brightness(0.9);
        }

        /* Make the graph container look integrated, not floating */
        iframe {
            border-radius: 15px;
            opacity: 0.85; /* Slight transparency so it isn't a harsh block */
            transition: opacity 0.3s ease;
        }

        iframe:hover {
            opacity: 1.0;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("<h1 class='practice-title'>Practice Mode</h1>", unsafe_allow_html=True)
    st.divider()

    col_left, col_right = st.columns([2, 1])

    # --- RIGHT COLUMN: CONTROLS & SETUP ---
    with col_right:
        st.markdown("<h3 style='color: #d1d5db; font-weight: 300; font-size: 1.5rem; margin-bottom: 0;'>Setup</h3>", unsafe_allow_html=True)
        
        # Difficulty selection
        diff_choice = st.radio("Select Difficulty:", ["Easy"], horizontal=True, label_visibility="collapsed")
        
        if st.button("🚀 Generate Text", use_container_width=True):
            filtered_db = [ex for ex in EX_DATABASE if ex["difficulty"] == diff_choice]
            if filtered_db:
                st.session_state.current_ex = random.choice(filtered_db)
                st.session_state.user_edges = [] 
                st.session_state.active_relations = []
                st.session_state.checked = False
                st.rerun()

        if st.session_state.current_ex:
            curr = st.session_state.current_ex
            st.markdown(f"<span style='color: #8b92a5; font-size: 0.9rem;'><b>Source:</b> {curr['source']}</span>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"<div class='edu-text'>{' '.join(curr['edus'])}</div>", unsafe_allow_html=True)

            st.divider()
            
            with st.container(border=True):
                st.markdown("<h4 style='color: #e06c75; margin-bottom: 15px;'>Graph Tools</h4>", unsafe_allow_html=True)
                new_rel = st.selectbox("1. Pick Relation:", ["None"] + RELATION_GROUPS, key="rel_selector")
                
                if st.button("➕ Add Relation Node", use_container_width=True, type="primary"):
                    if new_rel != "None":
                        rel_id = f"REL_{len(st.session_state.active_relations) + 1}"
                        st.session_state.active_relations.append({"id": rel_id, "name": new_rel})
                        st.rerun()

                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
                del_col1, del_col2 = st.columns(2)
                with del_col1:
                    if st.button("↩️ Undo Edge", use_container_width=True):
                        if st.session_state.user_edges:
                            st.session_state.user_edges.pop()
                            st.rerun()
                with del_col2:
                    if st.button("🗑️ Delete Rel", use_container_width=True):
                        if st.session_state.active_relations:
                            removed_rel = st.session_state.active_relations.pop()
                            # Clean up edges connected to the deleted relation
                            st.session_state.user_edges = [e for e in st.session_state.user_edges if e['from'] != removed_rel['id'] and e['to'] != removed_rel['id']]
                            st.rerun()

            if st.button("🔄 Reset Full Graph", use_container_width=True):
                st.session_state.user_edges = []
                st.session_state.active_relations = []
                st.session_state.checked = False
                st.rerun()

            if st.button("✅ Check Answer", use_container_width=True, type="primary"):
                st.session_state.checked = True

    # --- LEFT COLUMN: GRAPH VISUALIZATION ---
    with col_left:
        if st.session_state.current_ex:
            curr = st.session_state.current_ex
            
# --- SOFTER GRAPH VISUALS ---
            nodes = []
            for i in range(len(curr['edus'])):
                nodes.append(Node(
                    id=f"U{i+1}", 
                    label=curr['edus'][i], 
                    size=20, # Slightly smaller nodes
                    color={
                        "background": "#2d3436", # Muted Charcoal
                        "border": "#636e72",     # Soft Silver
                        "highlight": {"background": "#636e72", "border": "#dfe6e9"}
                    }, 
                    shape="box", 
                    margin=10,
                    font={"size": 13, "color": "#b2bec3"} # Dimmed white text
                ))
                
            for r in st.session_state.active_relations:
                nodes.append(Node(
                    id=r['id'], 
                    label=r['name'].upper(), 
                    color={
                        "background": "#764348", # Muted Dusty Rose (low saturation)
                        "border": "#a29bfe",     # Soft Lavender border
                        "highlight": {"background": "#a29bfe", "border": "#ffffff"}
                    }, 
                    size=22, 
                    shape="diamond",
                    font={"color": "#fab1a0", "size": 12} # Peach-toned text (lower blue light)
                ))

            edges = [Edge(
                source=e['from'], 
                target=e['to'], 
                color="#4a4e58", # Darker, thinner lines
                width=1,         # Thinner lines are less "noisy"
                smooth={'type': 'curvedCW', 'roundness': 0.2} # Curved lines look more organic
            ) for e in st.session_state.user_edges]

            # Render with Physics OFF for eye comfort
            clicked_id = agraph(
                nodes=nodes, 
                edges=edges, 
                config=Config(
                    width="100%", 
                    height=600, 
                    directed=True, 
                    physics=False, # THIS IS KEY: Stops the nodes from vibrating/moving
                    nodeSpacing=200
                )
            )

            # Edge Creation Logic
            if clicked_id and st.session_state.active_relations:
                source_rel_id = st.session_state.active_relations[-1]['id']
                if (clicked_id.startswith("U") or clicked_id.startswith("REL_")) and clicked_id != source_rel_id:
                    if not any(e['to'] == clicked_id and e['from'] == source_rel_id for e in st.session_state.user_edges):
                        st.session_state.user_edges.append({"from": source_rel_id, "to": clicked_id})
                        st.rerun()

            # Result Checking Logic
            if st.session_state.checked:
                st.divider()
                primary_rel_match = any(r['name'] == curr['relation'] for r in st.session_state.active_relations)
                connected_units = [e['to'] for e in st.session_state.user_edges if e['to'].startswith("U")]
                all_units_linked = all(f"U{i+1}" in connected_units for i in range(len(curr['edus'])))
                
                if primary_rel_match and all_units_linked:
                    st.success("Correct! Well done.")
                else:
                    st.error("Not quite! Try checking your relation type and connections.")