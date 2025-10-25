# **Automated Credential Exposure Scanner**

## **Project Overview**

The **Automated Credential Exposure Scanner** is a **security automation tool** developed to detect **exposed or leaked credentials** from public sources such as breach data APIs, GitHub repositories, or Pastebin dumps.  

This project was created as part of the **CYB 333 – Security Automation** course at **National University** by **Yamariki Toukou**. It demonstrates how **automation and Python scripting** can be used to strengthen an organization’s security posture by identifying compromised credentials before attackers exploit them.

The tool automates the process of querying data sources, parsing returned results for credential-like patterns (emails, usernames, or passwords), and generating a structured report of any findings. It helps **reduce manual workload** for cybersecurity teams while providing **faster detection and response** capabilities.

---

## **Objectives and Features**

### **Objectives**
- Automate the detection of leaked or exposed credentials.  
- Query public data sources (e.g., breach data APIs).  
- Use **regular expressions (regex)** to identify emails and passwords.  
- Log all activity and findings for traceability.  
- Generate a structured JSON report for security analysis and remediation planning.  

### **Key Features**
- **Automated Scanning:** Queries APIs and parses results for credential patterns.  
- **Regex-Based Detection:** Identifies potential emails and passwords using pattern matching.  
- **Logging and Reporting:** Records all activities in `exposure_scanner.log` and produces a `exposure_report.json` summary.  
- **Configurable Targets:** Allows customization of monitored domains or user patterns via `targets.txt`.  
- **Error Handling:** Robust exception management for failed API calls or malformed data.  
- **Extensible Architecture:** Designed for easy integration of new data sources or alerting systems (e.g., email or Slack notifications).

---

## **Project Structure**

```
.
├── exposure_scanner.py          # Main Python script
├── exposure_scanner.log         # Log file (auto-generated)
├── exposure_report.json         # Output report (auto-generated)
├── targets.txt                  # Optional file containing domains/emails to monitor
├── README.md                    # Documentation file
```

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.8 or higher  
- Internet connection (for API queries)  
- Basic familiarity with command-line execution  

### **Dependencies**
Install the required Python modules using `pip`:
```bash
pip install requests
```

The script uses the following built-in or standard libraries:
- `re` – for pattern matching (regex)
- `requests` – for HTTP API calls
- `logging` – for event logging
- `json` – for report generation
- `datetime` – for timestamp handling

---

## **Usage Instructions**

1. **Clone or Download the Project**
   ```bash
   git clone https://github.com/Yamariki93/Toukou-Yamariki.git
   cd Toukou-Yamariki
   ```

2. **Prepare the Target List**  
   Create a file named `targets.txt` in the same directory, containing one email or domain pattern per line.  
   Example:
   ```
   admin@example.com
   user1@example.org
   ```

   If no file is found, the scanner defaults to the predefined patterns in the script (`@example.com`, `user\d+@example.org`).

3. **Run the Scanner**
   Execute the script from your terminal:
   ```bash
   python3 exposure_scanner.py
   ```

4. **View the Results**
   - Log file: `exposure_scanner.log` – contains details of each scan and any errors encountered.  
   - Report file: `exposure_report.json` – stores all detected exposures with timestamps.

   Example console output:
   ```
   [+] Exposures found. Report saved as exposure_report.json.
   ```
   or  
   ```
   [-] No exposures detected.
   ```

---

## **How It Works**

The script loads target patterns (either from a file or predefined list) and iterates through each target to query a breach API for possible credential leaks. The response data is then parsed using regular expressions to identify valid email and password strings.  

If any credentials are detected, they are stored as structured JSON data in `exposure_report.json`. The process is fully logged, ensuring transparency and traceability of all actions.

---

## **Code Documentation**

The source code is thoroughly documented for clarity and maintenance. Each major section and function includes descriptive comments. Below is a summary of the key components:

- **Configuration Section:**  
  Defines target patterns, API endpoints, and logging configuration.  

- **Utility Functions:**  
  - `load_targets()` loads monitored patterns or domains from a text file.  
  - `fetch_data_from_api()` retrieves potential breach data via HTTP requests.  
  - `parse_credentials()` extracts emails and passwords using regex expressions.  

- **Core Logic:**  
  - `scan_for_exposures()` handles the main scanning and data parsing loop.  
  - `generate_report()` writes all findings into a structured JSON file.  

- **Main Execution:**  
  The `main()` function initializes the logging system, loads targets, runs the scan, and generates a final report.
