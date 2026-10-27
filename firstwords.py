import time
import pandas as pd
import trafilatura
from trafilatura import metadata

N_WORDS = 200

URL_FILE = "urls.txt"
OUTPUT_FILE = "scraped.xlsx"

def read_pasted():
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            return "\n".join(lines)
        if not lines and line.strip().lower() == "q":
            return None
        lines.append(line)

def read_urls():
    urls = []
    with open(URL_FILE, "r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()
            if url != "" and not url.startswith("#"):
                if url not in urls:
                    urls.append(url)
    return urls


def scrape_article(url):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Could not download article.")
    text = trafilatura.extract(downloaded)
    if not text:
        raise ValueError("Could not extract article text.")
    article_metadata = metadata.extract_metadata(downloaded)
    headline = ""
    date = ""
    publication = ""
    if article_metadata:
        if article_metadata.title:
            headline = article_metadata.title
        if article_metadata.date:
            date = article_metadata.date
        if article_metadata.sitename:
            publication = article_metadata.sitename
    return headline, date, publication, text

def process_article(text, headline, date, publication, article_id):
    words = text.split()
    if not words:
        print("Nothing to process.")
        return None
    result = " ".join(words[:N_WORDS])
    note = ""
    if len(words) < N_WORDS:
        note = " (article was shorter than 200 words)"
    print("\n----- first 200 words -----")
    print(result)
    print("---------------------------")
    print(str(min(len(words), N_WORDS)) +
          " of " + str(len(words)) + " words" + note)
    article = {
        "article_id": article_id,
        "date": date,
        "publication": publication,
        "headline": headline,
        "body": result,
        "lead_text": headline + ": " + result
    }
    return article

print("Choose input method:")
print("1. Paste article text into the terminal")
print("2. Scrape articles from urls.txt")
input_choice = input("Enter 1 or 2: ")
print("\nChoose output method:")
print("1. Print results to the terminal")
print("2. Write results to Excel")
output_choice = input("Enter 1 or 2: ")
articles = []
if input_choice == "1":
    article_number = 1
    while True:
        print("\nPaste article text, then type END on its own line.")
        print("Type q on the first line to finish.")
        text = read_pasted()
        if text is None:
            break
        print("\nEnter the article headline (or leave blank):")
        headline = input()
        print("Enter the publication (or leave blank):")
        publication = input()
        print("Enter the publication date (or leave blank):")
        date = input()
        article_id = str(article_number)
        article = process_article(text, headline, date, publication, article_id)
        if article is not None:
            articles.append(article)
            article_number += 1
        if output_choice == "1":
            print("\nResults printed above!")
elif input_choice == "2":
    urls = read_urls()
    for i in range(len(urls)):
        url = urls[i]
        print("\nScraping article", i + 1, "of", len(urls))
        try:
            headline, date, publication, text = scrape_article(url)
            article_id = str(i + 1)
            article = process_article(
                text, headline, date, publication, article_id
            )
            if article is not None:
                articles.append(article)
        except Exception as error:
            print("Failed to scrape:", url)
            print("Reason:", error)
        time.sleep(2)
else:
    print("Invalid input choice.")
if output_choice == "2":
    if articles:
        df = pd.DataFrame(articles)
        df = df[["article_id","date","publication","headline","body","lead_text"]]
        df.to_excel(OUTPUT_FILE, index=False)
        print("\nSaved", len(articles), "articles to", OUTPUT_FILE)
    else:
        print("\nNo articles to save.")
elif output_choice != "1":
    print("Invalid output choice.")