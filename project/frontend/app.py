import streamlit as st
import pandas as pd
from datetime import date
st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide"
)
st.markdown("""
<style>

/* Oswald Font */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Oswald', sans-serif;
}

/* Main Background */
.stApp {
    background-color: #001F54;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #002D72;
}

/* Text Color */
h1, h2, h3, h4, h5, h6,
label, p, span {
    color: white !important;
}

/* Title */
.main-title {
    text-align: center;
    color: white !important;
    font-size: 60px;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background-color: green;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    background-color: darkgreen;
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea {
    background-color: white;
    color: black;
    border-radius: 10px;
}

/* Table Styling */
[data-testid="stDataFrame"] {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)
if "users" not in st.session_state:
    st.session_state.users = {}

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None
def register():

    st.header("Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if not username or not email or not password:
            st.error("Please fill all fields")

        elif username in st.session_state.users:
            st.error("Username already exists")

        else:

            st.session_state.users[username] = {
                "email": email,
                "password": password
            }

            st.session_state.tasks[username] = []

            st.success("Registration Successful!")
def login():

    st.header("Login")

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button("Login"):

        if (
            username in st.session_state.users
            and
            st.session_state.users[username]["password"] == password
        ):

            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()

        else:
            st.error("Invalid Username or Password")
def dashboard():

    user = st.session_state.current_user

    st.markdown(
        "<h1 class='main-title'>TASK MANAGER</h1>",
        unsafe_allow_html=True
    )

    st.success(f"Welcome {user}")
    tasks = st.session_state.tasks[user]

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📋 Total Tasks", total_tasks)

    with col2:
        st.metric("✅ Completed", completed_tasks)

    with col3:
        st.metric("⏳ Pending", pending_tasks)

    st.divider()


    st.subheader("Create New Task")

    title = st.text_input("Task Title")

    description = st.text_area(
        "Task Description"
    )
    priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
    )
    due_date = st.date_input(
        "Due Date",
        min_value=date.today()
    )

    if st.button("Add Task"):

        if title:

            task_id = len(
                st.session_state.tasks[user]
            ) + 1

            st.session_state.tasks[user].append(
                {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "priority":priority,
                    "due_date": str(due_date),
                    "completed": False
                }
            )

            st.success("Task Added Successfully")
            st.rerun()

        else:
            st.error("Task Title is required")

    st.divider()

    st.subheader("My Tasks")

    tasks = st.session_state.tasks[user]

    if tasks:

        df = pd.DataFrame(
            [
                {
                    "ID": task["id"],
                    "Task Title": task["title"],
                    "Description": task["description"],
                    "Priority":
                "🟢 Low" if task["priority"] == "Low"
                else "🟡 Medium" if task["priority"] == "Medium"
                else "🔴 High",
                    "Due Date": task["due_date"],
                    "Completed": "✅ Yes"
                    if task["completed"]
                    else "❌ No"
                }
                for task in tasks
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "Update Task Status"
        )

        for index, task in enumerate(tasks):

            col1, col2, col3 = st.columns(
                [4, 2, 1]
            )

            with col1:
                st.write(
                    f"**{task['title']}**"
                )

            with col2:
               if task["completed"]:

                 st.success("✅ Completed")

               else:

                if st.button(
                    "Complete",
                    key=f"complete_{index}"
                ):
                 task["completed"] = True
                 st.rerun() 

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{index}"
                ):
                    st.session_state.tasks[user].pop(
                        index
                    )
                    st.rerun()

    else:
        st.info(
            "No Tasks Available"
        )

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
if st.session_state.logged_in:

    dashboard()

else:

    st.markdown(
        "<h1 class='main-title'>TASK MANAGER</h1>",
        unsafe_allow_html=True
    )

    option = st.sidebar.selectbox(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )

    if option == "Login":
        login()
    else:
        register()

