import streamlit as st

def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True
    
    st.title("ai ream time gym trainer")
    st.markdown("# welcome ! pls enter a username to start")

    with st.form("login_form",clear_on_submit=False):
        username=st.text_input("name",placeholder="princekhunt")
        submit_button = st.form_submit_button("start session",width="stretch")

    if submit_button:
        if not username:
            st.error("name cannot be empty")
            return False
        
        st.session_state["username"]=username
        st.session_state["user_id"]=1
        st.rerun()

    return False
    
