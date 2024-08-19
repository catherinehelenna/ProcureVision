import streamlit as st
import eda
from deployment import prediction

# url= 'https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/FINALFOTO.png'
st.sidebar.markdown("### RM. Hati Tenteram")
st.sidebar.markdown(
        """
        <div style="text-align:center; margin-bottom: 30px;">
            <img src="https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/OutlinedLogo.png" alt="Logo" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )
page = st.sidebar.selectbox(label="Choose Menu", options=["HOME", "EDA", "PREDICTION"])

if page == 'HOME':
    st.write("# FINAL PROJECT")
    st.write("## FTDS-RMT-027")
    st.write("### Group 1")
    st.write("#### <--- Exploratory Data Analysis & Prediction")
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center'>Meet our Rangers</h2>", unsafe_allow_html=True)

    # Custom CSS for the LinkedIn buttons
    button_css = """
    <style>
    .linkedin-btn {
        display: inline-block;
        background: #005db5;
        color: #F26634;
        padding: 10px 15px;
        margin: 10px 0px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 14px;
        text-align: center;
        vertical-align: middle;
    }
    </style>
    """
    
    # Render the custom CSS with the HTML
    st.markdown(button_css, unsafe_allow_html=True)
    
    def linkedin_button(profile_url, button_text="LinkedIn Profile"):
        return f'<a href="{profile_url}" target="_blank" class="linkedin-btn">{button_text}</a>'
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.image('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/Foto%20Satuan/Foto_0004_Bagus.png')
        st.markdown(linkedin_button("https://www.linkedin.com/in/bagusprasetyo21/"), unsafe_allow_html=True)
    
    with col2:
        st.image('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/Foto%20Satuan/Foto_0003_Qais.png')
        st.markdown(linkedin_button("https://www.linkedin.com/in/qais-ahmad-45b36280/"), unsafe_allow_html=True)
    
    with col3:
        st.image('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/Foto%20Satuan/Foto_0002_Ardi.png')
        st.markdown(linkedin_button("https://www.linkedin.com/in/rahardiansyah-fatoni-688777185/"), unsafe_allow_html=True)
    
    with col4:
        st.image('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/Foto%20Satuan/Foto_0001_Catherine.png')
        st.markdown(linkedin_button("https://www.linkedin.com/in/catherine-helenna-mulyadi/"), unsafe_allow_html=True)
    
    with col5:
        st.image('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-group-01-ftds-rmt-27/main/img/Foto%20Satuan/Foto_0000_Aqila.png')
        st.markdown(linkedin_button("https://www.linkedin.com/in/aqila-ratna-dhiyaa/"), unsafe_allow_html=True)

elif page == 'EDA':
    eda.run()
else:
    prediction.run()