import streamlit as st
import requests
import pandas as pd
from datetime import datetime

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
        # date formartting
        date_columns = ["purchase_date", "expiry_date"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.strftime("%d %b %Y %H:%M")
        st.table(df)

        #st.json(response.json())

    st.subheader("Journey History")
    # Add date filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    if st.button("Load Trip History"):

        # Convert dates to string in ISO format (if needed)
        start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
        end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

        # Prepare query params
        params = {}
        if start_date_str:
            params["start_date"] = start_date_str
        if end_date_str:
            params["end_date"] = end_date_str

        response = requests.get(
            f"{API_URL}/api/trips/history",headers=headers, params=params
        )

        #trips = response.json()
        #df = pd.DataFrame(trips)
        #st.table(df)
        if response.status_code == 200:
            trips = response.json()
            if trips:
                df = pd.DataFrame(trips)
                # date formatting
                date_columns = ["purchase_date", "expiry_date", "validated_at"]

                for col in date_columns:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col]).dt.strftime("%d %b %Y %H:%M")
                st.table(df)
            else:
                st.info("No trips found for the selected date range.")
        else:
            st.error(f"Error loading trips: {response.status_code}")


# Validator interface
elif role == "Validator":

    st.header("Validator Console")

    pass_code = st.text_input("Pass Code")

    # TODO: automatic add code?
    transport_modes = {
        "Metro": "MET",
        "Bus": "BUS",
        "Train": "TRN",
        "One-way Bus": "OBUS"
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

    # Stats

    response = requests.get(
        f"{API_URL}/api/admin/dashboard",headers=headers
    )

    data = response.json()

    st.metric(
        "Total Passes Sold",
        data["total_passes_sold"]
    )

    #st.write("Validations by Mode")

    #st.table(data["validations_by_mode"])
    st.subheader("Validations by Transport Mode")

    df = pd.DataFrame(data["validations_by_mode"])

    st.table(df)

    st.bar_chart(
        df.set_index("transport_mode")
    )

    #ADMIN CRUD

    # Admin Create Pass
    st.subheader("Create Pass Type")

    name = st.text_input("Pass Name")

    validity_days = st.number_input(
        "Validity (days)",
        min_value=1,
        step=1
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=0.5
    )

    transport_modes = st.text_input(
        "Transport Modes (comma separated)",
        placeholder="BUS,MET"
    )

    max_trips = st.number_input(
        "Max Trips Per Day",
        min_value=0,
        step=1
    )

    if st.button("Create Pass Type"):

        payload = {
            "name": name,
            "validity_days": validity_days,
            "price": price,
            "transport_modes": transport_modes if transport_modes else None,
            "max_trips_per_day": max_trips if max_trips > 0 else None
        }

        response = requests.post(
            f"{API_URL}/api/admin/pass-types",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            st.success("Pass type created")
            st.rerun()
        else:
            st.error(response.text)

    # Admin Read Pass Types
    st.subheader("Existing Pass Types")

    response = requests.get(
        f"{API_URL}/api/admin/pass-types",
        headers=headers
    )

    if response.status_code == 200:
        pass_types = response.json()
        df = pd.DataFrame(pass_types)
        st.table(df)
    else:
        st.error("Failed to load pass types")

    # Admin Update Pass Types
    st.subheader("Update Pass Type")

    pass_type_id = st.number_input("Pass Type ID", min_value=1)

    new_name = st.text_input("New Name")
    new_validity = st.number_input("Validity Days", min_value=1)
    new_price = st.number_input("Price", min_value=0.0)
    new_transport_modes = st.text_input("Transport Modes")
    new_max_trips_per_day = st.number_input("Max Trips Per Day",min_value=1)

    if st.button("Update Pass Type"):

        payload = {
            "name": new_name,
            "validity_days": new_validity,
            "price": new_price,
            "transport_modes": new_transport_modes,
            "max_trips_per_day": new_max_trips_per_day
        }

        response = requests.put(
            f"{API_URL}/api/admin/pass-types/{pass_type_id}",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            st.success("Pass type updated")
            st.rerun()
        else:
            st.error(response.text)



    # Admin Delete Pass Types
    st.subheader("Delete Pass Type")

    delete_id = st.number_input("Pass Type ID to delete", min_value=1)

    if st.button("Delete Pass Type"):

        response = requests.delete(
            f"{API_URL}/api/admin/pass-types/{delete_id}",
            headers=headers
        )

        if response.status_code == 200:
            st.success("Pass type deleted")
            st.rerun()
        else:
            st.error(response.text)
