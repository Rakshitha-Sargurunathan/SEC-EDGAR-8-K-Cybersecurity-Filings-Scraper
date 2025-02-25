import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

# File path for the dataset
file_path = r"C:\Users\raksh\Downloads\TA - Financial Analytics\ojr2gqcpibyiqxad.csv"
output_file_path = r"C:\Users\raksh\Downloads\TA - Financial Analytics\First10000.csv"  # Save results
  
# SEC API details
SEC_BASE_URL = "https://data.sec.gov/submissions/CIK{}.json"
SEC_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data/{}/{}"
HEADERS = {'User-Agent': 'Raksh (vigneshsarr@vcu.edu)'}

# Keywords for cybersecurity
CYBERSECURITY_KEYWORDS = ["1.05."]
 
def get_all_8k_filings(cik, year, max_retries=5, delay=5):
    """Fetch all 8-K filings for the given CIK and year with retry logic."""
    url = SEC_BASE_URL.format(cik)
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                data = response.json()
                filings = data.get("filings", {}).get("recent", {})
                
                return [
                    {"filing_id": filings["accessionNumber"][i].replace("-", ""), "filing_date": filings["filingDate"][i]}
                    for i, form in enumerate(filings["form"])
                    if form == "8-K" and filings["filingDate"][i].startswith(str(year))
                ]

            print(f"⚠️ Attempt {attempt}/{max_retries}: Received status code {response.status_code}. Retrying...")
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Attempt {attempt}/{max_retries}: Connection Error. Retrying in {delay} seconds...")
            time.sleep(delay)
        except requests.exceptions.Timeout:
            print(f"⏳ Attempt {attempt}/{max_retries}: Request Timed Out. Retrying in {delay} seconds...")
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt}/{max_retries}: Unexpected error: {e}. Retrying...")
            time.sleep(delay)

    print(f"❌ ERROR: Failed to fetch data from SEC API after {max_retries} attempts.")
    return []

def check_filing_for_section_105(cik, filing_id, filing_date):
    """Check if an 8-K filing contains Section 1.05 or cybersecurity mentions."""
    filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{filing_id}/index.json"
    response = requests.get(filing_url, headers=HEADERS)

    if response.status_code != 200:
        return False

    try:
        filing_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return False

    document_urls = [doc["name"] for doc in filing_data["directory"]["item"] if doc["name"].endswith(".txt")]

    if not document_urls:
        return False

    filing_text_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{filing_id}/{document_urls[0]}"
    response = requests.get(filing_text_url, headers=HEADERS)

    if response.status_code != 200:
        return False

    content_type = response.headers.get("Content-Type", "").lower()
    if "text" not in content_type:
        return False

    try:
        text = response.text
    except UnicodeDecodeError:
        return False

    # ✅ Check for Section 1.05 or cybersecurity keywords
    found_keywords = [keyword for keyword in CYBERSECURITY_KEYWORDS if keyword.lower() in text.lower()]

    return filing_date if found_keywords else False

# ✅ Read only the required rows from the dataset
#df = pd.read_csv(file_path, dtype={'cik': str})
df = pd.read_csv(file_path, dtype={'cik': str}, skiprows=range(1, 1), nrows=10000)  

# ✅ Ensure CIK is a 10-digit number with leading zeros
df['cik'] = df['cik'].apply(lambda x: str(x).zfill(10))

# ✅ Create a new column "8-K Filing Date" (initially empty)
df["8-K Filing Date"] = ""

# ✅ Iterate over each row and update filing dates
for index, row in df.iterrows():
    cik = row['cik']
    year = str(row['fyear'])  # Ensure year is string
    
    filing_details = get_all_8k_filings(cik, year)

    found_date = None
    for filing in filing_details:
        filing_date = check_filing_for_section_105(cik, filing["filing_id"], filing["filing_date"])
        if filing_date:
            found_date = filing_date
            df.at[index, "8-K Filing Date"] = filing_date  # ✅ Write filing date back to CSV
            break  # Stop checking after the first valid match

    # ✅ Print result in terminal
    if found_date:
        print(f"\n✅ CIK {cik} ({year}): Section 1.05 found in filing dated {found_date}.")
    else:
        print(f"\n❌ CIK {cik} ({year}): No Section 1.05 found in any 8-K filings.")

# ✅ Save the updated CSV file
df.to_csv(output_file_path, index=False)
print(f"\n✅ Updated dataset saved at: {output_file_path}")
