# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


@st.cache_data
def load_data():
    return pd.read_csv("train.csv")  

df = load_data()

# Helper functions for analysis
def calculate_male_percentage():
    male_count = df[df['Sex'] == 'male'].shape[0]
    total_count = df.shape[0]
    percentage = (male_count / total_count) * 100
    return f"Approximately {percentage:.1f}% of passengers were male."

def get_age_histogram():
    fig, ax = plt.subplots()
    sns.histplot(df['Age'].dropna(), bins=20, ax=ax)
    ax.set_title("Distribution of Passenger Ages")
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    return fig

def calculate_average_fare():
    avg_fare = df['Fare'].mean()
    return f"The average ticket fare was £{avg_fare:.2f}."

def get_embarkation_counts():
    embark_counts = df['Embarked'].value_counts()
    response = "Passengers embarked from these ports:\n"
    for port, count in embark_counts.items():
        response += f"- {port}: {count} passengers\n"
    return response


def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    return img_str

def process_question(question):
    if "percentage of passengers were male" in question.lower():
        return calculate_male_percentage(), None
    elif "histogram of passenger ages" in question.lower():
        response = "Here's a histogram showing the distribution of passenger ages."
        fig = get_age_histogram()
        img_str = plot_to_base64(fig)
        return response, img_str
    elif "average ticket fare" in question.lower():
        return calculate_average_fare(), None
    elif "embarked from each port" in question.lower():
        return get_embarkation_counts(), None
    else:
        return "I'm not sure how to answer that. Try asking about passenger demographics, fares, or embarkation ports!", None


st.title("Titanic Dataset Chat Agent")
st.write("Ask me anything about the Titanic passengers!")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "image" in message and message["image"]:
            st.image(f"data:image/png;base64,{message['image']}")

if question := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        response, img_str = process_question(question)
        st.write(response)
        if img_str:
            st.image(f"data:image/png;base64,{img_str}")
            st.session_state.messages.append({"role": "assistant", "content": response, "image": img_str})
        else:
            st.session_state.messages.append({"role": "assistant", "content": response, "image": None})