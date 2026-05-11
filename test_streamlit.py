import streamlit as st

st.title("Hello World")
st.write("This is my first streamlit app")

name = st.text_input("Enter your name")
st.write(f"Hello {name}")

if st.button("Click me"):
    st.write("Button was clicked")