import requests
from bs4 import BeautifulSoup
import re
import pdfplumber
import pandas as pd

#function to retrieve the urls themselves
def retrieve_urls_and_get_pdf(url):

    # get data from the homepage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # parse html return
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # find html tags in code
        links = soup.find_all('a')

        # extract urls, append pdf extension
        urls = [link.get('href') for link in links if link.get('href')]
        new_urls = [url + i for i in urls if 'pdf' in i]
        
        # return data structure
        return new_urls
        
    else:
        print(f"Failed to retrieve the webpage: {response.status_code}")

# download pdf
def download_pdf(pdf_url, idx):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_prefix = pdf_url.split('.pdf')[0]
        with open(f'case_{idx}.pdf', 'wb') as f:
            f.write(response.content)
        return f'case_{idx}.pdf'
    else:
        print("Failed to download PDF.")
        return None

# use regular expression (RegEx) to match email common expression
def extract_emails_from_pdf(pdf_path):
    emails = set()  # Use a set to avoid duplicates
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                found_emails = re.findall(email_pattern, text)
                emails.update(found_emails)

    return emails

# driver code
if __name__ == '__main__':
    
    # using popular machine learning journal
    url = 'https://www.jmlr.org'

    # retrieve PDF and read into local memory - using only a test set of 70 for now..
    file_paths = retrieve_urls_and_get_pdf(url)[:70]
    emails = []

    # extract emails and iterate over all pdf urls
    for idx in range(len(file_paths)):
        pdf = download_pdf(file_paths[idx],idx)
        email = extract_emails_from_pdf(pdf)
        emails.append(email)
        # Print the extracted emails

    # output results to csv
    final_output = pd.DataFrame({
        'id':range(len(emails)),
        'email_list':emails
    })

    final_output.to_csv('ML_emails',index=False)