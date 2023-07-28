from pathlib import Path

import streamlit as st
from PIL import Image
from streamlit_timeline import timeline

# --- PATH SETTINGS ---
css_file = "assets/main.css"
resume_file = "assets/CV.pdf"
profile_pic = "assets/img/profile-picture.png"
job_history = "assets/job-history.json"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Dominik Golebiewski"
PAGE_ICON = ":workshop:"
NAME = "Dominik Golebiewski"
DESCRIPTION = """
Detail-oriented Database Developer with a passion for data integrity and system optimization. 
"""

EMAIL = "dominik.golebiewski@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/dominik-golebiewski-229460b0/",
    "GitHub": "https://github.com/DominikGolebiewski"
}


PROJECTS = {
    "🏆 Streamlit Multi Thread Database Migration Tool - Comparing sales across three stores": "https://youtu.be/Sb0A9i6d320",
    "🏆  - Web app with NoSQL database": "https://youtu.be/3egaMfE9388",
    "🏆 Desktop Application - Excel2CSV converter with user settings & menubar": "https://youtu.be/LzCfNanQ_9c",
    "🏆 MyToolBelt - Custom MS Excel add-in to combine Python & Excel": "https://pythonandvba.com/mytoolbelt/",
}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label=" 📃 Download Resume",
        data=PDFbyte,
        file_name=resume_file,
        mime="application/octet-stream",
    )
    st.write("📮", EMAIL)

# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")




# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qulifications")
st.write("---")
st.write(
    """
- ✔️ 5 years experience with Snowflake Data Warehouse in the Cloud
- ✔️ Strong hands on experience and knowledge in Snowflake, SQL and DBT
- ✔️ [SnowPro Core Certified](https://www.credly.com/badges/d53c78cd-f188-4466-ae41-c4c765a1dd1b/linked_in_profile)
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)
#
#
# --- SKILLS ---
st.write('\n')
st.subheader("Hard Skills")
st.write("---")
st.write(
    """
- 👩‍💻 Programming: Python (Streamlit, Pandas), SQL, DBT
- 📊 Data Visulization: Altair, Snowflake Dashboards
- 🗄️ Databases: Snowflake
"""
)


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# load data
with open(job_history, "r") as f:
    data = f.read()

# render timeline
timeline(data, height=950)

# # --- JOB 1
# st.write("🚧", "**Database Developer | Atheon Analytics | Fully Remote, UK**")
# st.write("10/2019 - Present")
# st.write(
#     """
# - ► Developed effective modular SQL and Jinja scripts utilising DBT and Snowflake, resulting in enhanced performance
# - ► Designed internal database tools utilising Snowflake, Streamlit, and Python to enhance productivity and cycle time
# - ► Developed a testing framework and an internal DBT package to facilitate case tests for data pipelines
# - ► Refactored transformation architecture resulting in a ~70% performance increase and ~60% Snowflake credits reduction
# - ► Designed and implemented the back-end database that provides data to the BI tool Tableau and the end user
# - ► Supported junior developers and customer support with database-related questions, resulting in increased productivity and quicker delivery
# - ► Achieved Snowflake SnowPro Core accreditation
# """
# )
#
# # --- JOB 2
# st.write('\n')
# st.write("🤝🏻", "**Junior Database Developer | <font color='blue'>Atheon Analytics</font> | Cranfield, UK**", unsafe_allow_html=True)
# st.write("01/2018 - 02/2022")
# st.write(
#     """
# - ► Enhanced customer satisfaction and expedited delivery by assisting customer support with database queries
# - ► Participated in the redesign and implementation of ETL processes for legacy customer data outside of normal business hours to ensure timely and error-free data migration
# - ► Improved understanding of the most recent technologies, Python, and the Snowflake data warehouse in the Cloud
# """
# )
#
# # --- JOB 3
# st.write('\n')
# st.write("🚧", "**Data Analyst | Chegg**")
# st.write("04/2015 - 01/2018")
# st.write(
#     """
# - ► Devised KPIs using SQL across company website in collaboration with cross-functional teams to achieve a 120% jump in organic traﬃc
# - ► Analyzed, documented, and reported user survey results to improve customer communication processes by 18%
# - ► Collaborated with analyst team to oversee end-to-end process surrounding customers' return data
# """
# )
#
#
# # --- Projects & Accomplishments ---
# st.write('\n')
# st.subheader("Projects & Accomplishments")
# st.write("---")
# for project, link in PROJECTS.items():
#     st.write(f"[{project}]({link})")