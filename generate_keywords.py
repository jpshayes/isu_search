import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import csv
import string
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def read_urls_from_file(file_path):
    """
    Reads a list of URLs from a given file.

    Parameters:
    file_path (str): The path to the file containing URLs.

    Returns:
    list: A list of URLs.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def fetch_page_content(url):
    """
    Fetches the HTML content of a given URL.

    Parameters:
    url (str): The URL to fetch content from.

    Returns:
    str: The HTML content of the page.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: Status code {response.status_code}")
            return ""
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def read_common_words(file_path):
    """
    Reads a list of common words to be excluded from keyword extraction.

    Parameters:
    file_path (str): The path to the file containing common words.

    Returns:
    list: A list of common words.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading common words file: {e}")
        return []

def extract_keywords(text, num_keywords=60):
    """
    Extracts a specified number of keywords from text.

    Parameters:
    text (str): The text to extract keywords from.
    num_keywords (int): The number of keywords to extract.

    Returns:
    list: A list of keywords.
    """
    words = word_tokenize(text.lower())
    custom_stopwords = set(stopwords.words('english') + list(string.punctuation) + common_words)
    words = [word for word in words if word not in custom_stopwords]
    freq_dist = FreqDist(words)
    return [word for (word, _) in freq_dist.most_common(num_keywords)]

def process_url(url):
    """
    Processes a URL to extract keywords from its content.

    Parameters:
    url (str): The URL to process.

    Returns:
    list: A list of extracted keywords.
    """
    print(f"Processing URL: {url}")
    html_content = fetch_page_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return extract_keywords(text)

# Main script execution
if __name__ == "__main__":
    # Load URLs from a file
    urls_file_path = 'urls.txt'
    urls = read_urls_from_file(urls_file_path)

    if not urls:
        print("No URLs found. Please check the file path and contents.")
    else:
        print(f"Found {len(urls)} URLs to process.")

        # Load common words from a file
        common_words_file_path = 'common_words.txt'
        common_words = read_common_words(common_words_file_path)

        # Output file for keywords
        output_file = 'keywords.csv'

        # Writing keywords to a CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Keywords'])

            for url in urls:
                keywords = process_url(url)
                writer.writerow([url, ', '.join(keywords)])
                print(f"Processed {url}")

        print(f"Keyword extraction complete. Data written to {output_file}")
