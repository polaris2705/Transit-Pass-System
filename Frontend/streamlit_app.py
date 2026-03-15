import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None

st.title("Digital Transit Pass System")


if st.session_state.token is None:

    auth_mode = st.radio(
        "Authentication",
        ["Login", "Register"]
    )



    # Login
    if auth_mode == "Login":

        st.header("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            response = requests.post(
                f"{API_URL}/api/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.user_id = data["user_id"]
                st.session_state.role = data["role"]

                st.session_state.token = True

                st.success("Login successful")
                st.rerun()

            else:
                st.error("Invalid credentials")


    # Register
    elif auth_mode == "Register":

        st.header("Register New User")

        name = st.text_input("Name")
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            response = requests.post(
                f"{API_URL}/api/auth/register",
                json={
                    "name": name,
                    "mobile": mobile,
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                st.success("Registration successful. Please login.")

            else:
                st.error(response.json()["detail"])

    st.stop()



#role = st.sidebar.selectbox(
#    "Select Role",
#    ["Commuter", "Validator", "Admin"]
#)
role = st.session_state.role

headers = {"X-User-ID": str(st.session_state.user_id)}

# Commuter interface
if role == "Commuter":

    st.header("Commuter Dashboard")

    if st.button("View Pass Types"):

        response = requests.get(f"{API_URL}/api/passes/types",headers=headers)

        if response.status_code == 200:
            #pass_types = response.json()

            #for p in pass_types:
            #    st.write(
            #        f"{p['name']} | Price: {p['price']} | Validity: {p['validity_days']} days"
            #    )
            pass_types = response.json()
            df = pd.DataFrame(pass_types)

            st.table(df)

    st.subheader("Purchase Pass")

    pass_type_id = st.number_input("Pass Type ID", min_value=1)
    #user_id = st.number_input("User ID", min_value=1)

    if st.button("Purchase Pass"):

        response = requests.post(
            f"{API_URL}/api/passes/purchase",
            json={
                #"user_id": user_id,
                "pass_type_id": pass_type_id
            },
            headers=headers
        )

        #st.json(response.json())
        result = response.json()

        if response.status_code == 200:
            st.success("Pass Purchased Successfully")

            st.write("Pass Code:", result["pass_code"])
            st.write("Purchase Date", result["purchase_date"])
            st.write("Expiry Date:", result["expiry_date"])
        else:
            st.error(result["detail"])

    if st.button("View My Passes"):

        response = requests.get(
            f"{API_URL}/api/passes/my-passes",headers=headers
        )

        passes = response.json()
        df = pd.DataFrame(passes)
        st.table(df)

        #st.json(response.json())

    st.subheader("Journey History")

    if st.button("Load Trip History"):

        response = requests.get(
            f"{API_URL}/api/trips/history",headers=headers
        )

        #st.json(response.json())
        trips = response.json()
        df = pd.DataFrame(trips)
        st.table(df)


# Validator interface
elif role == "Validator":

    st.header("Validator Console")

    pass_code = st.text_input("Pass Code")

    transport_modes = {
        "Metro": "MET",
        "Bus": "BUS",
        "Train": "TRN"
    }

    selected_mode = st.selectbox(
        "Transport Mode",
        list(transport_modes.keys())
    )

    transport_mode = transport_modes[selected_mode]

    route_info = st.text_input("Route Info")

    if st.button("Validate Pass"):

        response = requests.post(
            f"{API_URL}/api/validate",
            json={
                "pass_code": pass_code,
                "transport_mode": transport_mode,
                "route_info": route_info
            },
            headers=headers
        )

        #st.json(response.json())
        #result = response.json()
        st.write(response.status_code)
        st.write(response.text)

        result = response.json()

        if response.status_code == 200:
            if result.get("valid"):
                st.success("Pass Valid")
            else:
                st.error("Pass Invalid")

            st.write("Message:", result.get("message"))
            st.write("Expiry Date:", result.get("expiry_date"))

            trip = result.get("trip")

            if trip:
                st.write("Transport Mode:", trip["transport_mode"])
                st.write("Validated At:", trip["validated_at"])
        else:
            st.error(result.get("detail"))



# Admin interface
elif role == "Admin":

    st.header("Admin Dashboard")

    if st.button("Load Statistics"):

        response = requests.get(
            f"{API_URL}/api/admin/dashboard",headers=headers
        )

        data = response.json()

        st.metric(
            "Total Passes Sold",
            data["total_passes_sold"]
        )

        st.write("Validations by Mode")

        st.table(data["validations_by_mode"])