import streamlit as st
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config
import random

# Page Config
st.set_page_config(layout="wide", page_title="RST Master")

# Sidebar
with st.sidebar:
    selected = option_menu(
        "Main Menu", ["Home", "Practice"], 
        icons=['house', 'pencil-fill'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

# --- HOME PAGE ---
if selected == "Home":
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
EX_DATABASE = [
    {
        "text": "Mercedes officials said they expect flat sales next year.",
        "edus": ["Mercedes officials said", "they expect flat sales next year"],
        "relation": "Attribution",
        "correct_roles": ["Satellite", "Nucleus"],
        "logic": "The first unit is a reporting clause (Satellite) and the second is the message (Nucleus)."
    },
    {
        "text": "Although Mr. Freeman is retiring, he will continue to work as a consultant.",
        "edus": ["Although Mr. Freeman is retiring", "he will continue to work as a consultant"],
        "relation": "Contrast",
        "correct_roles": ["Satellite", "Nucleus"],
        "logic": "The 'Although' clause is a Satellite that concedes a point to the Nucleus."
    },
    {
        "text": "More people are remaining independent longer because they are better off.",
        "edus": ["More people are remaining independent longer", "because they are better off"],
        "relation": "Explanation",
        "correct_roles": ["Nucleus", "Satellite"],
        "logic": "The second unit provides the justification or reason for the first."
    }
]

RELATION_GROUPS = ["Attribution", "Background", "Cause", "Comparison", "Condition", "Contrast", 
                   "Elaboration", "Enablement", "Evaluation", "Explanation", "Joint", 
                   "Manner-Means", "Topic-Comment", "Summary", "Temporal", "Topic Change"]

# --- PRACTICE PAGE LOGIC ---
if selected == "Practice":
    st.markdown("<h1 style='text-align: center;'>Practice Mode</h1>", unsafe_allow_html=True)
    st.divider()

    col_left, col_right = st.columns([2.5, 1])

    with col_right:
        st.markdown("### 📋 Controls")
        if st.button("Generate Paragraph", use_container_width=True):
            st.session_state.current_ex = random.choice(EX_DATABASE)
            st.session_state.checked = False
            st.rerun()

        if "current_ex" in st.session_state:
            curr = st.session_state.current_ex
            st.markdown("#### Segmented Sentence")
            with st.container(border=True):
                annotated_text((curr['edus'][0], "Unit 1", "#e8f0fe"), " ", (curr['edus'][1], "Unit 2", "#e8f0fe"))
            
            st.divider()
            with st.expander("➕ Add Relation & Connect", expanded=True):
                selected_rel = st.selectbox("Relation Type:", ["None"] + RELATION_GROUPS)
                c1, c2 = st.columns(2)
                role_u1 = c1.selectbox("Unit 1 Role:", ["Satellite", "Nucleus"], key="u1_p")
                role_u2 = c2.selectbox("Unit 2 Role:", ["Satellite", "Nucleus"], key="u2_p")

            if st.button("Check Answer", use_container_width=True):
                st.session_state.checked = True

    with col_left:
        st.markdown("### Interactive Discourse Graph")
        if "current_ex" in st.session_state:
            curr = st.session_state.current_ex
            nodes = [
                Node(id="U1", label=curr['edus'][0], size=15, color="#e8f0fe", shape="box"),
                Node(id="U2", label=curr['edus'][1], size=15, color="#e8f0fe", shape="box")
            ]
            edges = []
            if selected_rel != "None":
                nodes.append(Node(id="REL", label=selected_rel.upper(), color="#ff4b4b", size=10))
                edges.append(Edge(source="REL", target="U1", label=role_u1, dashItems=[5, 5] if role_u1 == "Satellite" else None))
                edges.append(Edge(source="REL", target="U2", label=role_u2, dashItems=[5, 5] if role_u2 == "Satellite" else None))

            with st.container(border=True):
                config = Config(width="100%", height=500, directed=True, physics=True, hierarchical=False)
                agraph(nodes=nodes, edges=edges, config=config)

            if st.session_state.get("checked", False):
                st.divider()
                # Validate Relation and Roles
                is_rel_correct = (selected_rel == curr['relation'])
                is_roles_correct = (role_u1 == curr['correct_roles'][0] and role_u2 == curr['correct_roles'][1])

                if is_rel_correct and is_roles_correct:
                    st.success(f"🎯 Perfect! This is a/an **{curr['relation']}** relation with the correct roles.")
                elif is_rel_correct:
                    st.warning(f"✅ Correct Relation (**{curr['relation']}**), but check your Nucleus/Satellite assignments.")
                else:
                    st.error(f"❌ Incorrect. The manual categorizes this as **{curr['relation']}**.")
                
                st.markdown("#### Correct Discourse Structure")
                with st.container(border=True):
                    # Reveal the "Gold Standard" using actual EDU text and proper RST styling
                    c_nodes = [
                        Node(id="CU1", label=curr['edus'][0], color="#fff3cd" if curr['correct_roles'][0] == "Satellite" else "#d4edda", shape="box"),
                        Node(id="CU2", label=curr['edus'][1], color="#fff3cd" if curr['correct_roles'][1] == "Satellite" else "#d4edda", shape="box"),
                        Node(id="CREL", label=curr['relation'].upper(), color="#ff4b4b")
                    ]
                    c_edges = [
                        Edge(source="CREL", target="CU1", label=curr['correct_roles'][0], dashItems=[5, 5] if curr['correct_roles'][0] == "Satellite" else None),
                        Edge(source="CREL", target="CU2", label=curr['correct_roles'][1], dashItems=[5, 5] if curr['correct_roles'][1] == "Satellite" else None)
                    ]
                    agraph(nodes=c_nodes, edges=c_edges, config=config)
                st.info(f"**Manual Logic:** {curr['logic']}")