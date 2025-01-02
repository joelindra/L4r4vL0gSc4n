
# Laravel Debug Mode Scanner

A simple Python-based scanner to check for the existence of Laravel Debug Mode vulnerabilities in web applications. The tool checks if a Laravel application exposes sensitive debugging information through the `_ignition/health-check` endpoint, which could indicate the application is in debug mode and vulnerable to exploits.

## Features
- Checks if the `/ _ignition/health-check` endpoint is exposed by Laravel applications.
- Detects if the response includes the string `{"can_execute_commands":true}`, indicating the presence of Laravel Debug Mode.
- Logs the result in either `txt` or `json` format.
- Supports scanning multiple targets concurrently with configurable thread count.

## Prerequisites

- Python 3.x
- `requests` and `colorama` libraries

You can install the required libraries using the following:

```bash
pip install requests colorama
```

## Usage

### Single Target Scan

To scan a single target, run:

```bash
python3 laravlog.py -t https://example.com
```

### Multiple Target Scan

To scan a list of targets from a file, create a text file with each target on a new line and use the `-l` option:

```bash
python3 laravlog.py -l targets.txt
```

### Log Format

You can choose between two log formats: `txt` or `json`. The default is `txt`. You can specify the format using the `-f` option:

```bash
python3 laravlog.py -t https://example.com -f json
```

### Thread Count

You can also configure the number of threads for concurrent scanning using the `-th` option:

```bash
python3 laravlog.py -t https://example.com -th 20
```

### Example of Combined Usage

```bash
python3 laravlog.py -l targets.txt -th 20 -f json
```

## Logging Results

The scanner will log the results to a file located in the `results` folder:

- `log.txt` or `log.json` based on the chosen format.

Each log entry will indicate whether the site is "VULNERABLE" or "NOT VULNERABLE."

## Output

- If the target is vulnerable, it will be logged with the status `VULNERABLE`.
- If the target is not vulnerable, it will be logged with the status `NOT VULNERABLE`.
- In case of errors or timeouts, they will also be displayed in the terminal.

## Example Output

```
[!] https://example.com/_ignition/health-check => FOUND PATH
[=] https://anotherexample.com => FVCK OFF
```

## License

This tool is released under the MIT License. Feel free to modify, distribute, or use it for your own purposes.
