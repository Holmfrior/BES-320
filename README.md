DD-AI: A New Way to Learn Discourse Analysis
DD-AI is a Streamlit-based application that teaches users how to identify and map the relationships between ideas in a text. By breaking down sentences into Elementary Discourse Units (EDUs), the app guides users through the process of diagramming discourse structures using interactive graphs.

Features
Interactive Landing Page: A modern, particle-animated interface to welcome users.

Theoretical Guide: Detailed explanations of RST concepts, including:

EDUs: The building blocks of text.

Nucleus vs. Satellite: Distinguishing between essential and supporting information.

16 Rhetorical Relations: Interactive deep dives into relations like Attribution, Cause, Contrast, Elaboration, and Temporal with visual Graphviz diagrams.

Practice Mode: A hands-on workspace where users can:

Generate practice texts sourced from the RST Discourse Treebank (RST-DT).

Build interactive discourse graphs by adding relation nodes and linking them to text units.

Check their answers against the database logic.

🛠️ Tech Stack
Frontend/App Framework: Streamlit

Visualizations: * streamlit-agraph (Interactive Practice Graphs)

Graphviz (Static Theory Diagrams)

Particles.js (Landing Page Animation)

UI Components: * streamlit-option-menu

st-annotated-text
