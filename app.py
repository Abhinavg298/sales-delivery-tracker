
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales & Delivery Tracker", layout="wide")
st.title("📦 Sales & Delivery Tracker")

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Date', 'Party Name', 'Item Name', 'Quantity', 'Rate', 'GST', 'Total Value',
        'Discount', 'Freight', 'Remarks', 'Vehicle No.', 'Dispatch Location'
    ])

# Input form
with st.form("entry_form", clear_on_submit=True):
    st.subheader("➕ New Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date")
        party = st.text_input("Party Name")
        item = st.text_input("Item Name")
    with col2:
        qty = st.number_input("Quantity", min_value=0.0)
        rate = st.number_input("Rate", min_value=0.0)
        gst = st.number_input("GST (%)", min_value=0.0)
    with col3:
        total = st.number_input("Total Value", min_value=0.0)
        discount = st.number_input("Discount", min_value=0.0)
        freight = st.selectbox("Freight", ["Included", "Excluded"])
    
    remarks = st.text_input("Remarks")
    vehicle = st.text_input("Vehicle No.")
    dispatch = st.text_input("Dispatch Location")
    
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        new_entry = {
            'Date': date, 'Party Name': party, 'Item Name': item,
            'Quantity': qty, 'Rate': rate, 'GST': gst, 'Total Value': total,
            'Discount': discount, 'Freight': freight, 'Remarks': remarks,
            'Vehicle No.': vehicle, 'Dispatch Location': dispatch
        }
        st.session_state.data = st.session_state.data.append(new_entry, ignore_index=True)
        st.success("Entry added successfully!")

# Display table and export option
st.subheader("📊 All Entries")
st.dataframe(st.session_state.data, use_container_width=True)
st.download_button("📥 Download as Excel", st.session_state.data.to_excel(index=False), "Sales_Tracker.xlsx")
