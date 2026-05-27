# Maildir Email Parser & CSV Exporter

A lightweight Python script for parsing raw Maildir email files and exporting useful metadata into a structured CSV report.

This tool is useful for:
- Email triage
- Mailbox analysis
- DFIR / forensic workflows
- Bulk email review
- Parsing archived Maildir datasets

---

# Features

- Parses raw Maildir email files
- Extracts:
  - Sender
  - Recipient
  - Subject
  - Date
  - Message-ID
  - File size
- Detects attachments
- Extracts attachment filenames
- Generates a body text excerpt
- Exports everything into a CSV file
- Handles multipart emails
- Supports plain text and HTML fallback extraction

---

# Example Output

| File Name | From | Subject | Has Attachments |
|---|---|---|---|
| 1420900801.H532906P176699 | john@example.com | Meeting Notes | True |

---

# Requirements

Python 3.x

No external dependencies are required.

Uses only Python standard libraries:
- `csv`
- `email`
- `os`

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/maildir-parser.git
cd maildir-parser
```

---

# Usage

## 1. Place Email Files

Put your Maildir email files inside a folder.

Example:

emails/
├── 1420900801.H5565775176699.lh230.example.com,S=1026
├── 1420900802.H5322415176700.lh230.example.com,S=2048
```
## 2. Configure the Script

Edit the configuration section at the bottom of the script:

```python
if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Change target folder path if the files are not running from the local script directory
    TARGET_FOLDER = "."
    OUTPUT_CSV = "email_triage_summary.csv"
    EXCERPT_CHARACTER_LIMIT = 200
    # ---------------------

    parse_maildir_to_csv(
        TARGET_FOLDER, OUTPUT_CSV, excerpt_length=EXCERPT_CHARACTER_LIMIT
    )
```
### Configuration Options

| Variable | Description |
|---|---|
| `TARGET_FOLDER` | Folder containing the Maildir email files |
| `OUTPUT_CSV` | Name/path of the generated CSV report |
| `EXCERPT_CHARACTER_LIMIT` | Maximum number of characters extracted from the email body |

---

## 3. Run the Script

```bash
python3 parser.py
```

---

# Output

The script generates a CSV file containing:

| Column | Description |
|---|---|
| File Name | Original Maildir filename |
| Date | Email date header |
| From | Sender address |
| To | Recipient address |
| Subject | Email subject |
| Excerpt | Short preview of the email body |
| Has Attachments | Indicates if attachments exist |
| Attachment Names | Attachment filenames |
| Message-ID | Email Message-ID header |
| Size (Bytes) | Original file size |

---

# Attachment Handling

The script:
- Detects attachments automatically
- Decodes encoded attachment filenames
- Handles multipart MIME structures
- Supports unnamed attachments

---

# Body Extraction Logic

The parser:
1. Searches for `text/plain`
2. Falls back to `text/html`
3. Cleans whitespace/newlines
4. Truncates output to a configurable length

---

# Error Handling

If a file cannot be parsed, the script continues processing remaining files and prints an error message:

```text
Error processing file example.msg: <error details>
```

---

# Example Workflow

```text
Maildir Files
      ↓
Python Parser
      ↓
Structured CSV Report
      ↓
Excel / SIEM / DFIR Analysis
```

---

# Use Cases

- Digital forensics
- Incident response
- Email investigations
- Mailbox auditing
- Threat hunting
- Bulk email indexing
- Migration analysis

---

# License

MIT License

---

# Disclaimer

This tool is intended for educational, administrative, and authorized forensic purposes only.
Use responsibly and only on systems/data you are authorized to analyze.
