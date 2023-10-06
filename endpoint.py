import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from config import CATEGORY_LIST  # Import the category list

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_data():
    # Get the search term from the query parameter, default to "knowledge management"
    search_term = request.args.get('q', 'knowledge management')

    # Get the start year and end year from the query parameters, default to a range of years
    start_year = int(request.args.get('start_year', '2023'))
    end_year = int(request.args.get('end_year', '2021'))

    # Generate the list of years based on user input
    years = list(range(start_year, end_year + 1))

    results = {category: [] for category in CATEGORY_LIST}  # Initialize results dictionary

    for year in years:
        for j in range(10):
            # Define the URL with the user-specified search term and year
            url = f"https://www.emerald.com/insight/search?ipp=50&openAccess=true&q={search_term}&showAll=true&p={j+1}&fromYear={year}&toYear={year}"

            # Send an HTTP GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all elements with class "intent_link font-serif"
                elements_with_class = soup.find_all(class_="intent_link font-serif")
                pdfs = soup.find_all(class_="d-flex align-items-center mb-2 intent_pdf_link")

                # Loop through the elements and find links
                for element, pdf in zip(elements_with_class, pdfs):
                    link = element['href']  # Extract the 'href' attribute (link)
                    file = pdf['href']
                    title = element.text.strip()

                    # Check if the title contains keywords for categorization
                    for category in CATEGORY_LIST:
                        if category.lower() in title.lower():
                            results[category].append({
                                'title': title,
                                'link': "https://www.emerald.com"+link,
                                'file': "https://www.emerald.com"+file
                            })
                print(year, j, "done")

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
