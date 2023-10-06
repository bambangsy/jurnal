import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define the Flask API endpoint URL
API_ENDPOINT = "http://localhost:5000/scrape"  # Replace with your Flask app's URL

st.title("Search")

# Create a sidebar for user input
search_term = st.sidebar.text_input("Enter search term", "knowledge management")

# Create input fields for the year range
start_year = st.sidebar.number_input("Start Year", value=2022)
end_year = st.sidebar.number_input("End Year", value=2023)

# Create a sidebar widget for selecting the category
category_options = ['All', 'literature review', 'systematic review', 'bibliomatic review', 'syntetic review', 'other']
selected_category = st.sidebar.selectbox("Filter by Category", category_options)

# Create a button to trigger the search
if st.sidebar.button("Search"):
    # Cache the API URL
    @st.cache_resource
    def cache_api_url(api_endpoint, search_term, start_year, end_year):
        return f"{api_endpoint}?q={search_term}&start_year={start_year}&end_year={end_year}"

    # Cache the API response
    @st.cache_data
    def cache_api_response(api_url):
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Get the API URL using the cached function
    api_url = cache_api_url(API_ENDPOINT, search_term, start_year, end_year)

    # Get the API response using the cached function
    data = cache_api_response(api_url)

    if data:
        st.header("Search Results")

        # Filter results based on the selected category
        if selected_category == "All":
            # Display all results without categorization
            for category, results in data.items():
                for result in results:
                    st.write(f"[{result['title']}]({result['link']})")
        elif selected_category == "other":
            # Display results for all categories except the specified ones
            for category, results in data.items():
                if category not in ['literature review', 'systematic review', 'bibliomatic review', 'syntetic review']:
                    for result in results:
                        st.write(f"[{result['title']}]({result['link']})")
        else:
            # Display results for the selected category
            if selected_category in data:
                for result in data[selected_category]:
                    st.write(f"[{result['title']}]({result['link']})")
            else:
                st.write("No results for the selected category.")
    else:
        st.error("Failed to retrieve data. Please check your Flask API.")
