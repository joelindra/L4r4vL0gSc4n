#!/usr/bin/python3

import argparse
import requests
import urllib3
from multiprocessing.dummy import Pool
from colorama import Fore, Style
from os import makedirs
from os.path import exists
import json
import sys
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LaravelDebugScanner:
    def __init__(self, targets, threads, log_format):
        self.targets = [self.clean_url(target) for target in targets]  # Membersihkan URL dari trailing slashes
        self.threads = threads
        self.log_format = log_format
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        }
        self.result_folder = "results"
        self.vulnerable_file = f"{self.result_folder}/log.{log_format}"
        self.create_results_folder()

    def clean_url(self, url):
        # Pastikan hanya ada satu slash di akhir domain
        if url.endswith('/'):
            return url.rstrip('/')
        return url

    def create_results_folder(self):
        if not exists(self.result_folder):
            makedirs(self.result_folder)

    def scan_site(self, site):
        try:
            response = requests.get(f"{site}/_ignition/health-check", timeout=10, headers=self.header, verify=False)
            if '{"can_execute_commands":true}' in response.text and response.status_code == 200:
                print(f"{Fore.GREEN + '[!]' + Style.RESET_ALL} {Fore.GREEN + response.url + Style.RESET_ALL} => FOUND PATH")
                self.log_result(site, True)
            else:
                print(f"{Fore.RED + '[=]' + Style.RESET_ALL} {site} => FVCK OFF")
                self.log_result(site, False)
        except requests.exceptions.Timeout:
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Timeout accessing {site}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Error accessing {site}: {e}")
        except Exception as ex:
            error_msg = str(ex) if str(ex) else "Unknown error"
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Error accessing {site}: {error_msg}")

    def log_result(self, site, is_vulnerable):
        if self.log_format == "txt":
            with open(self.vulnerable_file, "a") as vuln_file:
                vuln_file.write(f"{site} => {'VULNERABLE' if is_vulnerable else 'NOT VULNERABLE'}\n")
        elif self.log_format == "json":
            result = {"site": site, "status": "VULNERABLE" if is_vulnerable else "NOT VULNERABLE"}
            with open(self.vulnerable_file, "a") as vuln_file:
                vuln_file.write(json.dumps(result) + "\n")

    def run(self):
        with Pool(self.threads) as pool:
            pool.map(self.scan_site, self.targets)
            pool.close()
            pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}Laravel Debug Mode Scanner{Style.RESET_ALL}",
        epilog=f"{Fore.GREEN}Example usage:{Style.RESET_ALL}\n"
               f"  {Fore.YELLOW}Single target:{Style.RESET_ALL} python3 laravlog.py -t https://example.com\n"
               f"  {Fore.YELLOW}Multiple targets:{Style.RESET_ALL} python3 laravlog.py -l targets.txt\n"
    )

    parser.add_argument(
        "-t", "--target", type=str, help=f"{Fore.CYAN}Single target domain (e.g., https://example.com){Style.RESET_ALL}"
    )
    parser.add_argument(
        "-l", "--list", type=str, help=f"{Fore.CYAN}Path to a file containing a list of targets{Style.RESET_ALL}"
    )
    parser.add_argument(
        "-th", "--threads", type=int, default=10, help=f"{Fore.CYAN}Number of threads (default: 10){Style.RESET_ALL}"
    )
    parser.add_argument(
        "-f", "--format", type=str, choices=["txt", "json"], default="txt", 
        help=f"{Fore.CYAN}Log format (default: txt){Style.RESET_ALL}"
    )

    args = parser.parse_args()

    if not args.target and not args.list:
        parser.error(f"{Fore.RED}You must specify a single target (-t) or a list of targets (-l){Style.RESET_ALL}")

    targets = []
    if args.target:
        targets.append(args.target.strip())
    if args.list:
        if exists(args.list):
            with open(args.list, "r") as f:
                targets.extend([line.strip() for line in f if line.strip()])
        else:
            print(f"{Fore.RED}[!] List file not found: {args.list}{Style.RESET_ALL}")
            exit(1)

    scanner = LaravelDebugScanner(targets, args.threads, args.format)
    scanner.run()
