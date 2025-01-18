import streamlit as st
import random
import numpy as np
import pandas as pd

def generate_sales_data():
    return [random.randint(50, 200) for _ in range(100)]

def analyze_sales_data(sales_data):
    sales_array = np.array(sales_data)
    return {
        "Average Sales": np.mean(sales_array),
        "Median Sales": np.median(sales_array),
        "Standard Deviation": np.std(sales_array),
    }

def create_sales_dataframe(sales_data):
    return pd.DataFrame({
        'Day': list(range(1, 101)),
        'Sales': sales_data,
        'Sales Growth Rate (%)': [0] + [((sales_data[i] - sales_data[i - 1]) / sales_data[i - 1]) * 100 for i in range(1, 100)],
    })

def add_sales_category(df):
    df['Category'] = df['Sales'].apply(lambda x: 'High' if x > 150 else 'Low')
    return df

def main():
    st.title("Sales Data Analysis Dashboard")

    if "sales_data" not in st.session_state:
        st.session_state.sales_data = []

    menu = [
        "Generate Sales Data",
        "View Statistical Analysis",
        "View Sales Data",
        "View Last 30 Days",
        "Filter Sales Above Threshold",
        "Add Sales Category",
        "Save Data to CSV",
    ]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Generate Sales Data":
        if st.button("Generate Data"):
            st.session_state.sales_data = generate_sales_data()
            st.success("Sales data has been generated.")

    elif choice == "View Statistical Analysis":
        if st.session_state.sales_data:
            analysis = analyze_sales_data(st.session_state.sales_data)
            st.subheader("Statistical Analysis")
            st.write(analysis)
        else:
            st.warning("Please generate sales data first.")

    elif choice == "View Sales Data":
        if st.session_state.sales_data:
            df = create_sales_dataframe(st.session_state.sales_data)
            st.subheader("Sales Data")
            st.dataframe(df.head(15))
        else:
            st.warning("Please generate sales data first.")

    elif choice == "View Last 30 Days":
        if st.session_state.sales_data:
            df = create_sales_dataframe(st.session_state.sales_data)
            st.subheader("Last 30 Days of Sales Data")
            st.dataframe(df.tail(30))
        else:
            st.warning("Please generate sales data first.")

    elif choice == "Filter Sales Above Threshold":
        if st.session_state.sales_data:
            threshold = st.number_input("Enter threshold value", min_value=0, value=100)
            if st.button("Filter Data"):
                df = create_sales_dataframe(st.session_state.sales_data)
                filtered_df = df[df['Sales'] > threshold]
                st.subheader(f"Sales Above {threshold} Units")
                st.dataframe(filtered_df)
        else:
            st.warning("Please generate sales data first.")

    elif choice == "Add Sales Category":
        if st.session_state.sales_data:
            df = create_sales_dataframe(st.session_state.sales_data)
            categorized_df = add_sales_category(df)
            st.subheader("Sales Data with Categories")
            st.dataframe(categorized_df.head(15))
        else:
            st.warning("Please generate sales data first.")

    elif choice == "Save Data to CSV":
        if st.session_state.sales_data:
            df = create_sales_dataframe(st.session_state.sales_data)
            df.to_csv("sales_data.csv", index=False)
            st.success("Data saved to 'sales_data.csv'.")
        else:
            st.warning("Please generate sales data first.")

if __name__ == "__main__":
    main()
