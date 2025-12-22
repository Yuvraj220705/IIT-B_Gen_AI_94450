import streamlit as st

with st.form("registration_form"):
    st.header("Registration Form")
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.slider("Age",10,100,25,1)
    addr = st.text_area("Address")
    submit = st.form_submit_button("Submit")


if submit:

    err_msg = ""
    is_error = False

    if not name:
        is_error = True
        err_msg += "Enter the Name\n"

    if not email:
        is_error = True
        err_msg +="Enter the email\n"

    if not addr:
        is_error = True
        err_msg +="Enter the Address\n"

    if is_error:
        st.error(err_msg)


    else:
        print("successfully logged in!!!")




