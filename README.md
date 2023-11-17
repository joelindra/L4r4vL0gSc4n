# Laravel Debug Scanner

This Python script is a tool designed for scanning Laravel applications for potential debug mode exposure. It utilizes multiprocessing to concurrently check multiple URLs for the presence of Laravel debug mode vulnerability.

## Features

- **Multiprocessing:** Uses Python's `multiprocessing` for concurrent scanning of multiple URLs.
- **Error Handling:** Comprehensive error handling to manage various exceptions during the scanning process.
- **Keyboard Interrupt Handling:** Gracefully stops the scanning process on keyboard interrupt (Ctrl+C).
- **Result Logging:** Logs potentially vulnerable URLs to a `vuln.txt` file in a `results` folder.

## Requirements

Ensure you have Python 3.x installed along with the necessary dependencies listed in `requirements.txt`.

## Usage

1. Clone the repository or download the script.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the script by executing `python3 laravlog.py`.
4. Follow the prompts to provide the list of URLs for scanning and thread count for multiprocessing.

## How it Works

The script sends a request to each URL appended with `/_ignition/health-check` to detect if Laravel's debug mode is exposed. If found, the script logs the vulnerable URLs in the `vuln.txt` file within a `results` directory.

Feel free to contribute, report issues, or suggest improvements!

**Note:** Use responsibly and only on URLs that you have permission to test.
