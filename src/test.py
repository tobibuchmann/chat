import streamlit as st

# Function to toggle sidebar visibility
def toggle_sidebar():
    if "sidebar" not in st.session_state:
        st.session_state.sidebar = True
    else:
        st.session_state.sidebar = not st.session_state.sidebar
    st.experimental_rerun()

# Get sidebar visibility from session state
if "sidebar" in st.session_state:
    sidebar_visible = st.session_state.sidebar
else:
    sidebar_visible = True

# Set sidebar width based on visibility
if sidebar_visible:
    sidebar_width = "20%"
else:
    sidebar_width = "0%"

# Set sidebar style
st.markdown(
    f"""
    <style>
    .sidebar. {{
        width: {sidebar_width};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content
if sidebar_visible:
    st.sidebar.write("This is the sidebar content.")

# Button to toggle sidebar visibility
if st.button("Toggle Sidebar"):
    toggle_sidebar()

st.write("This is the main content.")
