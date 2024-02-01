import streamlit as st
import pandas as pd
import os

# Importing functions from the script
from bookbot_statistics import (
    count_bookbot_only_providers,
    count_outliers_bookbot_prices,
    average_deviation_from_lowest_price,
    calculate_foreign_offers_representation,
    lower_priced_providers_than_bookbot
)

# Function to load data
def load_data():
    csv_file_path = os.path.join(os.getcwd(), "1000_ISBNs_all.csv")
    return pd.read_csv(csv_file_path)

# Main function to run the app
def main():    
    # Centering the logo
    logo_path = os.path.join(os.getcwd(), "bookbot_logo.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, width=200)

    # Centering the header and logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Data Analysis")
    
    # Load the data
    data = load_data()
    data = data.loc[:, ~data.columns.isin(["Scanned_Page"])]


    # Display a sample of the data
    st.subheader("Sample of the Data")
    st.write(data.head(10))  # Displaying the first 5 rows

    # Display a selectbox to choose the analysis
    analysis_choice = st.selectbox(
        "Select an analysis",
        [
            "Count Bookbot Only Provider",
            "Count Outliers in Bookbot Prices",
            "Providers having a lower price than BookBot",
            "Average Deviation from Lowest Price",
            "Calculate Foreign Offers Representation",
        ],
    )

    # Perform the selected analysis
    if analysis_choice == "Count Bookbot Only Provider":
        result = count_bookbot_only_providers(data)
        st.write("Total occurrences where 'Bookbot' is the only provider:", result)
    elif analysis_choice == "Count Outliers in Bookbot Prices":
        result = count_outliers_bookbot_prices(data)
        st.write("Number of outliers found in Bookbot prices:", result)
    elif analysis_choice == "Providers having a lower price than BookBot":
        result = lower_priced_providers_than_bookbot(data)
        st.write("List of providers having a lower price than BookBot:", result)
    elif analysis_choice == "Average Deviation from Lowest Price":
        result = average_deviation_from_lowest_price(data)
        st.write("Average deviation of Bookbot's offers from the lowest price :", result, "EUR")
    elif analysis_choice == "Calculate Foreign Offers Representation":
        country = st.text_input("Enter the home country:", value="Tschechien")
        if country:
            result = calculate_foreign_offers_representation(country, data)
            st.write(
                f"Relative representation of foreign offers (excluding): {result:.2f}%"
            )
        else:
            st.warning("Please enter the name of your home country.")

if __name__ == "__main__":
    main()
