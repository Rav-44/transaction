import streamlit as st
import pandas as pd
from datetime import date
from models import create_table, add_transaction, get_all_transactions

# Ensure table exists
create_table()

st.set_page_config(page_title="Office Transactions", layout="wide")

menu = ["Office Transactions", "Add Transaction"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Office Transactions":
    st.title("📊 Office Transactions")

    transactions = get_all_transactions()

    if transactions:
        df = pd.DataFrame(transactions)
        # Create Credit and Debit columns
        df['Credit'] = df.apply(lambda x: x['amount'] if x['type'] == 'Credit' else '', axis=1)
        df['Debit'] = df.apply(lambda x: x['amount'] if x['type'] == 'Debit' else '', axis=1)

        # Calculate running balance (oldest to newest)
        running_bal = 0
        balance_list = []
        for _, row in df[::-1].iterrows():
            if row['type'] == 'Credit':
                running_bal += float(row['amount'])
            else:
                running_bal -= float(row['amount'])
            balance_list.append(running_bal)
        df['Running Balance'] = balance_list[::-1]

        # Reorder columns & rename headers
        df = df[['date', 'description', 'Credit', 'Debit', 'Running Balance']]
        df.columns = ['Date', 'Description', 'Credit', 'Debit', 'Running Balance']

        # Show dataframe
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No transactions found.")

elif choice == "Add Transaction":
    st.title("➕ Add Transaction")

    txn_type = st.selectbox("Transaction Type", ["Credit", "Debit"])
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    description = st.text_input("Description")
    txn_date = st.date_input("Date", value=date.today())

    if st.button("Save"):
        if description and amount > 0:
            add_transaction(str(txn_date), description, txn_type, amount)
            st.success("Transaction saved successfully!")
            st.rerun()
        else:
            st.error("Please fill all fields correctly.")
