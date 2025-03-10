import requests
from bs4 import BeautifulSoup

def crawl_website(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and return the text from the website
        text = soup.get_text(separator='\n', strip=True)
        return text

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def main():
    url = input("Enter the website URL to crawl: ")
    text_content = crawl_website(url)
    print("\nWebsite Text Content:\n")
    print(text_content)

if __name__ == "__main__":
    main()
