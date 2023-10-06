import requests
from bs4 import BeautifulSoup

year = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]

for i in year:
    for j in range(10):
        # Define the URL
        url = f"https://www.emerald.com/insight/search?ipp=50&openAccess=true&q=knowledge+management&showAll=true&p={j+1}&fromYear={i}&toYear={i}"

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
            for element,pdf in zip(elements_with_class,pdfs):
                link = element['href']  # Extract the 'href' attribute (link)
                file = pdf['href']
                print(element.text.strip())
                print(link)
                print(file)
                print()

        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)
