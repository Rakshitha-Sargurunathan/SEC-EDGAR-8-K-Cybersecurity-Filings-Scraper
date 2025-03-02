# SEC-EDGAR-8-K-Cybersecurity-Filings-Scraper
This project is a Python-based web scraper designed to extract cybersecurity-related disclosures from 8-K filings. It automates the retrieval of filings for multiple companies and years, scans for Item 1.05 (Material Cybersecurity Incidents), and exports structured results into a CSV file.

## 🔍 Features
- **Fetches 8-K filings** from the SEC EDGAR database.
- **Scans filings** for cybersecurity-related disclosures (Item 1.05).
- **Processes multiple companies & years** from a CSV file.
- **Implements error handling & retry logic** for API requests.
- **Exports structured results** including filing dates into a new CSV.

## 🛠️ Setup & Installation
### Prerequisites
Ensure you have **Python 3.8+** installed. Install required dependencies:

pip install requests beautifulsoup4 pandas openpyxl

### **Configure SEC Headers**

Update the script with your email address for SEC API compliance:
HEADERS = {'User-Agent': 'Your Name (your_email@example.com)'}

### **Run the Script**
python sec_8k_scraper.py

📊 **How It Works**
* Reads CIK numbers & years from a CSV file.
* Fetches all 8-K filings for each company-year from the SEC.
* Scans filings for cybersecurity keywords (Item 1.05).
* Saves results (found/not found) with filing dates back to CSV.

📝 **Sample Output**

![image](https://github.com/user-attachments/assets/4996cee4-a73a-40e1-8c30-72a3b243201f)

🚀**Future Enhancements**
* Expand search to 10-K, 10-Q filings for broader cybersecurity insights.
* Improve parallel processing for faster execution.
* Add natural language processing (NLP) to refine keyword detection.




