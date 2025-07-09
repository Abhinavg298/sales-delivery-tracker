
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales & Delivery Tracker", layout="wide")
st.title("📦 Sales & Delivery Tracker (Based on Google Sheet)")

# Initialize session state
if "sales_data" not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=[
        "Date", "Party", "Item", "Qty", "Delivered", "Balance",
        "Rate", "GST (%)", "Discount", "Freight", "Total",
        "Vehicle", "Dispatch Location", "Remarks"
    ])

# Add new order
with st.form("order_form", clear_on_submit=True):
    st.subheader("➕ Add New Sales Order")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date")
        party = st.text_input("Party")
        item = st.text_input("Item")
    with col2:
        qty = st.number_input("Order Quantity", min_value=0.0)
        rate = st.number_input("Rate", min_value=0.0)
        gst = st.number_input("GST (%)", min_value=0.0)
    with col3:
        discount = st.number_input("Discount", min_value=0.0)
        freight = st.number_input("Freight", min_value=0.0)
        delivered = st.number_input("Delivered Quantity", min_value=0.0)

    vehicle = st.text_input("Vehicle No.")
    dispatch = st.text_input("Dispatch Location")
    remarks = st.text_input("Remarks")

    submitted = st.form_submit_button("Add Order")
    if submitted:
        base = qty * rate
        gst_amt = (base * gst) / 100
        total = base + gst_amt - discount + freight
        balance = qty - delivered

        new_entry = {
            "Date": date, "Party": party, "Item": item, "Qty": qty,
            "Delivered": delivered, "Balance": balance,
            "Rate": rate, "GST (%)": gst, "Discount": discount,
            "Freight": freight, "Total": total,
            "Vehicle": vehicle, "Dispatch Location": dispatch,
            "Remarks": remarks
        }

        st.session_state.sales_data = pd.concat(
            [st.session_state.sales_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success("✅ Order added successfully!")

# View & filter section
st.subheader("📊 View & Filter Data")
filter_party = st.text_input("Filter by Party")
filtered_data = st.session_state.sales_data
if filter_party:
    filtered_data = filtered_data[filtered_data["Party"].str.contains(filter_party, case=False)]

st.dataframe(filtered_data, use_container_width=True)

# Download button
st.download_button(
    "📥 Download Excel",
    filtered_data.to_excel(index=False),
    file_name="Sales_Delivery_Tracker.xlsx"
)
