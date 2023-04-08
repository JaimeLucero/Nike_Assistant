import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from tkinter import messagebox

keyword = None
results = []
class scrapper:
    def __init__(self, keyword):
        self.keyword = keyword

    def __str__(self):
        return str(self.keyword)
    
    def check_internet_connection(self):
        try:
            requests.get('https://www.google.com/')
            return True
        except:
            return False

    def search_result(keyword):
        global results
        
        # Construct URL
        url = f"https://www.nike.com/ph/w?q={keyword}"
        
        try:
            # Send a GET request to the search result page
            response = requests.get(url)
        
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all the HTML elements that contain the search results
            search_results = soup.find_all('div', {'class': 'product-card__body'})
            
            # Extract the product name and link from the first 5 search results
            for i, result in enumerate(search_results):
                if i >= 5:
                    break
                product_name = result.find('div', {'class': 'product-card__title'}).text
                product_link = result.find('a', {'class': 'product-card__link-overlay'}).get('href')
                results.append((product_name, product_link))
                time.sleep(5)
            
            # Format the results as a string
            result_str = f"Here are the first 5 search results for '{str(keyword)}':\n"
            for i, result in enumerate(results):
                result_str += str(f"{i+1}. {result[0]}\n")
            
            return str(result_str)

        except requests.exceptions.RequestException as e:
            # Return an error message if there's a connection error
            return "Error: Could not connect to server"

    def pick_result(self, entry):
        global results

        selected_product = results[entry-1]

        webbrowser.open_new_tab(selected_product[1])