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
        selected_page = option_menu(
            menu_title="DD-AI Menu", 
            options=["Landing", "Theory", "Practice"], 
            icons=["house", "book", "pencil"], 
            menu_icon="cast", 
            default_index=["Landing", "Theory", "Practice"].index(st.session_state.page) 
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
    st.markdown("<h1 style='text-align: center;'>THEORETICAL GUIDE</h1>", unsafe_allow_html=True)
    st.divider()

    # Section 1: EDUs
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("<h2 style='text-align: center;'>1. Elementary Discourse Units (EDUs)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Every text is made of minimal building blocks called EDUs, which are typically single clauses.</p>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'>", unsafe_allow_html=True)
        annotated_text(
            ("She was willing to skip class", "EDU 1"),
            " ",
            ("to attend the opening exhibit.", "EDU 2"), 
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Section 2: Nucleus vs Satellite
    _, center_col_2, _ = st.columns([1, 2, 1])
    with center_col_2:
        st.markdown("<h2 style='text-align: center;'>2. Nucleus vs. Satellite</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Relations usually consist of an essential <b>Nucleus</b> and a supporting <b>Satellite</b>.</p>", unsafe_allow_html=True)

        nuc_col, sat_col = st.columns(2)
        with nuc_col:
            st.markdown("""
                <div style='background-color: #e6f4ea; padding: 15px; border-radius: 8px; text-align: center; min-height: 120px;'>
                    <span style='color: #1e8e3e; font-weight: bold;'>The Nucleus</span>
                    <p style='margin-top: 10px; color: black;'>Essential info that makes sense in isolation.</p>
                </div>
            """, unsafe_allow_html=True)

        with sat_col:
            st.markdown("""
                <div style='background-color: #e8f0fe; padding: 15px; border-radius: 8px; text-align: center; min-height: 120px;'>
                    <span style='color: #1a73e8; font-weight: bold;'>The Satellite</span>
                    <p style='margin-top: 10px; color: black;'>Supporting info that depends on the nucleus.</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Section 3: Rhetorical Relations
    st.markdown("<h2 style='text-align: center;'>3. Rhetorical Relations</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>There are 16 functional groups that act as the 'Glue' for cohesion.</p>", unsafe_allow_html=True)
    
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
                        if st.button(name, use_container_width=True, key=f"btn_{name}"):
                            st.session_state.active_rel = name

        # DYNAMIC RELATION CONTENT
        if st.session_state.active_rel == "Attribution":
            st.divider()
            st.markdown("<h4 style='text-align: center;'>Attribution</h4>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("**Definition:** Attribution is used for reported speech (direct or indirect) and cognitive acts (feelings, thoughts, hopes).")
            
            _, center_content, _ = st.columns([1, 4, 1])
            with center_content:
                st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
                annotated_text(("Mercedes officials said", "Satellite", "#ffd"), " ", ("they expect flat sales next year", "Nucleus", "#afa"))
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.graphviz_chart('digraph { graph [rankdir=TB, center=true] node [shape=box, style=filled, fontname="Helvetica"] Relation [label="ATTRIBUTION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse] Satellite [label="Satellite:\\nMercedes officials said", fillcolor="#fff3cd"] Nucleus [label="Nucleus:\\nthey expect flat sales next year", fillcolor="#d4edda"] Relation -> Nucleus [label="Nucleus", arrowhead=none] Relation -> Satellite [label="Satellite", style=dashed] }', use_container_width=True)
                st.info("The Satellite is the source and the Nucleus is the content of the message.")

        elif st.session_state.active_rel == "Background":
            st.divider()
            st.markdown("<h4 style='text-align: center;'>Background</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("**Definition:** The satellite establishes the context with respect to which the nucleus is to be interpreted.")
            st.write("Background content logic goes here...")

# --- PRACTICE PAGE CONTENT ---
elif st.session_state.page == "Practice":
    st.markdown("<h1 style='text-align: center;'>Practice Mode</h1>", unsafe_allow_html=True)
    st.divider()

    col_left, col_right = st.columns([2, 1])

    with col_right:
        diff_choice = st.radio("Select Difficulty:", ["Easy"], horizontal=True)
        
        if st.button("Generate Text", use_container_width=True):
            filtered_db = [ex for ex in EX_DATABASE if ex["difficulty"] == diff_choice]
            if filtered_db:
                st.session_state.current_ex = random.choice(filtered_db)
                st.session_state.user_edges = [] 
                st.session_state.active_relations = []
                st.session_state.checked = False
                st.rerun()

        if st.session_state.current_ex:
            curr = st.session_state.current_ex
            st.caption(f"**Source:** {curr['source']}")
            with st.container(border=True):
                st.write(" ".join(curr['edus']))

            st.divider()
            
            with st.container(border=True):
                st.write("**Graph Tools**")
                new_rel = st.selectbox("1. Pick Relation:", ["None"] + RELATION_GROUPS, key="rel_selector")
                if st.button("Add Relation Node", use_container_width=True):
                    if new_rel != "None":
                        rel_id = f"REL_{len(st.session_state.active_relations) + 1}"
                        st.session_state.active_relations.append({"id": rel_id, "name": new_rel})
                        st.rerun()

                st.write("---")
                del_col1, del_col2 = st.columns(2)
                with del_col1:
                    if st.button("Undo Edge", use_container_width=True):
                        if st.session_state.user_edges:
                            st.session_state.user_edges.pop()
                            st.rerun()
                with del_col2:
                    if st.button("Delete Relationship", use_container_width=True):
                        if st.session_state.active_relations:
                            removed_rel = st.session_state.active_relations.pop()
                            st.session_state.user_edges = [e for e in st.session_state.user_edges if e['from'] != removed_rel['id'] and e['to'] != removed_rel['id']]
                            st.rerun()

            if st.button("Reset Full Graph", use_container_width=True):
                st.session_state.user_edges = []
                st.session_state.active_relations = []
                st.session_state.checked = False
                st.rerun()

            if st.button("Check Answer", use_container_width=True, type="primary"):
                st.session_state.checked = True

    with col_left:
        if st.session_state.current_ex:
            curr = st.session_state.current_ex
            nodes = [Node(id=f"U{i+1}", label=curr['edus'][i], size=20, color="#e8f0fe", shape="box", font={"size": 12}) for i in range(len(curr['edus']))]
            for r in st.session_state.active_relations:
                nodes.append(Node(id=r['id'], label=r['name'].upper(), color="#ff4b4b", size=25, shape="diamond"))
            
            edges = [Edge(source=e['from'], target=e['to'], color="#ff4b4b") for e in st.session_state.user_edges]
            clicked_id = agraph(nodes=nodes, edges=edges, config=Config(width="100%", height=600, directed=True, physics=True))

            if clicked_id and st.session_state.active_relations:
                source_rel_id = st.session_state.active_relations[-1]['id']
                if (clicked_id.startswith("U") or clicked_id.startswith("REL_")) and clicked_id != source_rel_id:
                    if not any(e['to'] == clicked_id and e['from'] == source_rel_id for e in st.session_state.user_edges):
                        st.session_state.user_edges.append({"from": source_rel_id, "to": clicked_id})
                        st.rerun()

            if st.session_state.checked:
                st.divider()
                primary_rel_match = any(r['name'] == curr['relation'] for r in st.session_state.active_relations)
                connected_units = [e['to'] for e in st.session_state.user_edges if e['to'].startswith("U")]
                all_units_linked = all(f"U{i+1}" in connected_units for i in range(len(curr['edus'])))
                if primary_rel_match and all_units_linked:
                    st.success("Correct! ")
                else:
                    st.error("Wrong!")