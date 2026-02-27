import streamlit as st
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config
import random

# Page Config
st.set_page_config(layout="wide", page_title="BES-320")

# Sidebar
with st.sidebar:
    selected = option_menu(
        "Main Menu", ["Theory", "Practice"], 
        icons=['house', 'pencil-fill'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

# --- THEORY PAGE ---
if selected == "Theory":
    st.markdown("<h1 style='text-align: center;'>A GUIDE FOR COHESION</h1>", unsafe_allow_html=True)
    st.divider()

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown("<h2 style='text-align: center;'>1. Elementary Discourse Units (EDUs)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Every text is made of minimal building blocks called EDUs, which are typically single clauses.</p>", unsafe_allow_html=True)
        
        spacer_l, text_col, spacer_r = st.columns([1, 6, 1])
        with text_col:
            # FIXED: Removed the leading comma that caused the SyntaxError
            annotated_text(
                ("She was willing to skip class", "EDU 1"),
                ("to attend the opening exhibit.", "EDU 2"), 
            )

        st.divider()

        st.markdown("<h2 style='text-align: center;'>2. Nucleus vs. Satellite</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Relations usually consist of an essential <b>Nucleus</b> and a supporting <b>Satellite</b>.</p>", unsafe_allow_html=True)

        nuc_col, sat_col = st.columns(2)
        with nuc_col:
            st.markdown("""
                <div style='background-color: #e6f4ea; padding: 15px; border-radius: 8px; text-align: center;'>
                    <span style='color: #1e8e3e; font-weight: bold;'>The Nucleus</span>
                </div>
                <p style='text-align: center; margin-top: 10px;'>Essential info that makes sense in isolation.</p>
            """, unsafe_allow_html=True)

        with sat_col:
            st.markdown("""
                <div style='background-color: #e8f0fe; padding: 15px; border-radius: 8px; text-align: center;'>
                    <span style='color: #1a73e8; font-weight: bold;'>The Satellite</span>
                </div>
                <p style='text-align: center; margin-top: 10px;'>Supporting info that depends on the nucleus.</p>
            """, unsafe_allow_html=True)

        st.divider()

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

        all_names = ["Attribution"] + list(other_relations.keys())
        attr_clicked = False

        for i in range(0, len(all_names), 4):
            btn_cols = st.columns(4)
            for j in range(4):
                if i + j < len(all_names):
                    name = all_names[i+j]
                    with btn_cols[j]:
                        if name == "Attribution":
                            attr_clicked = st.button("Attribution", use_container_width=True, key="main_attr")
                        else:
                            st.button(name, help=other_relations[name], use_container_width=True, key=f"btn_{name}")

        if attr_clicked:
            st.divider()
            st.markdown("<h4 style='text-align: center;'>Attribution</h4>", unsafe_allow_html=True)
            _, inner_mid, _ = st.columns([1, 4, 1])
            with inner_mid:
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                annotated_text(
                    "[ ", ("Mercedes officials said", "Satellite", "#ffd"), " ] [ ",
                    ("they expect flat sales next year", "Nucleus", "#afa"), " ]"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                st.graphviz_chart('''
                    digraph {
                        node [shape=box, style=filled, fontname="Helvetica"]
                        edge [fontname="Helvetica", fontsize=10]
                        Relation [label="ATTRIBUTION", fillcolor="#ff4b4b", fontcolor=white, shape=ellipse]
                        Satellite [label="Satellite:\\nMercedes officials said", fillcolor="#fff3cd"]
                        Nucleus [label="Nucleus:\\nthey expect flat sales next year", fillcolor="#d4edda"]
                        Relation -> Nucleus [label="Nucleus", arrowhead=none]
                        Relation -> Satellite [label="Satellite", style=dashed]
                    }
                ''')
                st.info("The **Satellite** is the source of the attribution and the **Nucleus** is the content of the reported message.")

# --- PRACTICE PAGE DATA ---

# --- CUSTOM CSS FOR MODERN LOOK ---
#st.markdown("""
#    <style>
#    /* Main Background */
#    .stApp {
#        background-color: #f8f9fa;
#    }
#    
#    /* Card-style containers */
#    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
#        background-color: white;
#        padding: 20px;
#        border-radius: 15px;
#        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#        margin-bottom: 20px;
#    }
#    
#    /* Custom Header */
#    .main-header {
#        font-family: 'Inter', sans-serif;
#        font-weight: 800;
#        color: #1e293b;
#        text-align: center;
#        margin-bottom: 0px;
#    }
#    
#    /* Score Badge */
#    .score-badge {
#        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
#        color: white;
#        padding: 10px 20px;
#        border-radius: 50px;
#        font-weight: bold;
#        text-align: center;
#        display: inline-block;
#    }
#    </style>
#""", unsafe_allow_html=True)

# --- EASY MODE DATABASE ---

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
    # --- ATTRIBUTION ---
    {
        "text": "The government said the consumer price index rose 0.5% in September.",
        "edus": ["The government said", "the consumer price index rose 0.5% in September."],
        "relation": "Attribution",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The first unit attributes the information in the second unit to an official source[cite: 693]."
    },
    {
        "text": "Analysts estimated that sales at U.S. stores declined in the quarter.",
        "edus": ["Analysts estimated", "that sales at U.S. stores declined in the quarter."],
        "relation": "Attribution",
        "difficulty": "Easy",
         "source": "RST-DT (News)",
        "logic": "Used with a cognitive predicate ('estimated') to separate the source from the estimate[cite: 693]."
    },
    
    # --- CAUSE / RESULT ---
    {
        "text": "The budget deficit widened because tax receipts fell.",
        "edus": ["The budget deficit widened", "because tax receipts fell."],
        "relation": "Cause",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides the direct cause for the situation described in the first unit[cite: 696]."
    },
    {
        "text": "The airline is limiting the programs to reduce its high costs.",
        "edus": ["The airline is limiting the programs", "to reduce its high costs."],
        "relation": "Cause",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit (the goal) is the reason for the action taken in the first unit[cite: 82, 696]."
    },

    # --- CONTRAST ---
    {
        "text": "The company's earnings fell, but its revenue rose 10%.",
        "edus": ["The company's earnings fell,", "but its revenue rose 10%."],
        "relation": "Contrast",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A multinuclear relation where two opposing facts about the company's performance are compared[cite: 701]."
    },
    {
        "text": "Although the economy is slowing, consumer spending remains high.",
        "edus": ["Although the economy is slowing,", "consumer spending remains high."],
        "relation": "Contrast",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A concession relation where the 'although' clause raises an expectation that is countered by the second unit[cite: 701]."
    },

    # --- CONDITION ---
    {
        "text": "S.A. Brewing would make a takeover offer if it exercises the option.",
        "edus": ["S.A. Brewing would make a takeover offer", "if it exercises the option."],
        "relation": "Condition",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The truth or realization of the first unit depends on the fulfillment of the condition in the second[cite: 700]."
    },
    {
        "text": "Unless the board approves the deal, the merger will fail.",
        "edus": ["Unless the board approves the deal,", "the merger will fail."],
        "relation": "Condition",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "A negative condition where the second unit's outcome is tied to the first unit not happening[cite: 700]."
    },

    # --- ELABORATION ---
    {
        "text": "The company announced a new product, a high-speed computer.",
        "edus": ["The company announced a new product,", "a high-speed computer."],
        "relation": "Elaboration",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides additional detail (Object-Attribute) about the product mentioned in the first[cite: 703]."
    },
    {
        "text": "The firm hired a new CEO, who was formerly at Apple.",
        "edus": ["The firm hired a new CEO,", "who was formerly at Apple."],
        "relation": "Elaboration",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit is a relative clause providing more information about the subject in the first[cite: 703]."
    },

    # --- TEMPORAL ---
    {
        "text": "The index rose 5 points before closing at 2500.",
        "edus": ["The index rose 5 points", "before closing at 2500."],
        "relation": "Temporal",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "Establishes a clear chronological sequence between the two events using 'before'[cite: 710]."
    },
    {
        "text": "The dollar fell when the news reached the market.",
        "edus": ["The dollar fell", "when the news reached the market."],
        "relation": "Temporal",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "Specifies the time at which the main event occurred[cite: 710]."
    },

    # --- ENABLEMENT ---
    {
        "text": "Investors are selling shares to lock in recent profits.",
        "edus": ["Investors are selling shares", "to lock in recent profits."],
        "relation": "Enablement",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit describes the goal (purpose) that the first unit is intended to achieve[cite: 704]."
    },

    # --- COMPARISON ---
    {
        "text": "Earnings were flat, compared with a profit a year ago.",
        "edus": ["Earnings were flat,", "compared with a profit a year ago."],
        "relation": "Comparison",
        "difficulty": "Easy",
        "source": "RST-DT (News)",
        "logic": "The second unit provides a specific point of comparison to contextualize the first unit[cite: 698]."
    }
]

# Standard functional groups [cite: 691, 693-710]
RELATION_GROUPS = ["Attribution", "Background", "Cause", "Comparison", "Condition", "Contrast", 
                   "Elaboration", "Enablement", "Evaluation", "Explanation", "Joint", 
                   "Manner-Means", "Topic-Comment", "Summary", "Temporal", "Topic Change"]

# Initialize state
if "current_ex" not in st.session_state:
    st.session_state.current_ex = None
if "user_edges" not in st.session_state:
    st.session_state.user_edges = []
if "active_relations" not in st.session_state:
    st.session_state.active_relations = []
if "checked" not in st.session_state:
    st.session_state.checked = False

if selected == "Practice":
    st.markdown("<h1 style='text-align: center;'>Practice Mode</h1>", unsafe_allow_html=True)
    st.divider()

    col_left, col_right = st.columns([2, 1])

    # --- RIGHT COLUMN: CONTROLS & CLEAN TEXT ---
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
                            # Clean up edges connected to this relation (either as source or target)
                            st.session_state.user_edges = [
                                e for e in st.session_state.user_edges 
                                if e['from'] != removed_rel['id'] and e['to'] != removed_rel['id']
                            ]
                            st.rerun()

            if st.button("Reset Full Graph", use_container_width=True):
                st.session_state.user_edges = []
                st.session_state.active_relations = []
                st.session_state.checked = False
                st.rerun()

            if st.button("Check Answer", use_container_width=True, type="primary"):
                st.session_state.checked = True

    # --- LEFT COLUMN: GRAPH VISUALIZATION ---
    with col_left:
        if st.session_state.current_ex:
            curr = st.session_state.current_ex
            nodes = []
            
            for i in range(len(curr['edus'])):
                nodes.append(Node(id=f"U{i+1}", label=curr['edus'][i], size=20, color="#e8f0fe", shape="box", font={"size": 12}))
            
            for r in st.session_state.active_relations:
                nodes.append(Node(id=r['id'], label=r['name'].upper(), color="#ff4b4b", size=25, shape="diamond"))
            
            edges = [Edge(source=e['from'], target=e['to'], color="#ff4b4b") for e in st.session_state.user_edges]
            
            config = Config(width="100%", height=600, directed=True, physics=True, hierarchical=False)
            clicked_id = agraph(nodes=nodes, edges=edges, config=config)

            # --- UPDATED INTERACTION LOGIC (Connect to EDU OR another Relation) ---
            if clicked_id and st.session_state.active_relations:
                # The 'source' is always the most recently added relation
                source_rel_id = st.session_state.active_relations[-1]['id']
                
                # Check if we clicked an EDU OR a DIFFERENT relation node
                is_edu = clicked_id.startswith("U")
                is_other_rel = clicked_id.startswith("REL_") and clicked_id != source_rel_id
                
                if is_edu or is_other_rel:
                    # Prevent duplicate edges
                    if not any(e['to'] == clicked_id and e['from'] == source_rel_id for e in st.session_state.user_edges):
                        st.session_state.user_edges.append({"from": source_rel_id, "to": clicked_id})
                        st.rerun()

            # --- VALIDATION ---
            if st.session_state.checked:
                st.divider()
                primary_rel_match = any(r['name'] == curr['relation'] for r in st.session_state.active_relations)
                connected_units = [e['to'] for e in st.session_state.user_edges if e['to'].startswith("U")]
                all_units_linked = all(f"U{i+1}" in connected_units for i in range(len(curr['edus'])))

                if primary_rel_match and all_units_linked:
                    st.success("Correct! ")
                else:
                    st.error("Wrong!")
