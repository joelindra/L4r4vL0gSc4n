#!/usr/bin/python3

import requests
import urllib3
from multiprocessing.dummy import Pool
from colorama import Fore, Style
from os import system, name, makedirs
from os.path import exists
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LaravelDebugScanner:
    def __init__(self):
        self.header = {
            "User-Agent": self.get_user_agent()
        }
        self.default_thread = 10
        self.result_folder = "results"
        self.vulnerable_file = f"{self.result_folder}/log.txt"

    def get_user_agent(self):
        user_agent = input("Enter User-Agent (Press Enter for default): ")
        if not user_agent:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        return user_agent

    def create_results_folder(self):
        if not exists(self.result_folder):
            makedirs(self.result_folder)

    def clear_screen(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def scan_site(self, site):
        try:
            response = requests.get(f"{site}/_ignition/health-check", timeout=10, headers=self.header, verify=False)
            if '{"can_execute_commands":true}' in response.text and response.status_code == 200:
                print(f"{Fore.GREEN + '[!]' + Style.RESET_ALL} {Fore.GREEN + response.url + Style.RESET_ALL} => FOUND DUDE!")
                self.log_result(site)
            else:
                print(f"{Fore.RED + '[=]' + Style.RESET_ALL} {site} => FUCK NOT FOUND!")
        except requests.exceptions.Timeout:
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Timeout accessing {site}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Error accessing {site}: {e}")
        except urllib3.exceptions.NewConnectionError as ne:
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Connection error for {site}: {ne}")
        except Exception as ex:
            error_msg = str(ex) if str(ex) else "Unknown error"
            print(f"{Fore.RED + '[!]' + Style.RESET_ALL} Error accessing {site}: {error_msg}")

    def log_result(self, site):
        with open(self.vulnerable_file, "a") as vuln_file:
            vuln_file.write(f"{site}\n")


    def main(self):
        self.create_results_folder()
        input_file = input("List: ")
        if exists(input_file):
            thread = input(f"Thread (Default: {self.default_thread}): ")
            if thread.isdigit():
                thread_count = int(thread)
            else:
                print("Using default thread count.")
                thread_count = self.default_thread

            with open(input_file, "r") as f:
                websites = f.read().split("\n")
                with Pool(thread_count) as pool:
                    pool.map(self.scan_site, websites)
                    pool.close()
                    pool.join()
        else:
            print("File not found")

if __name__ == "__main__":
    scanner = LaravelDebugScanner()
    scanner.clear_screen()
    scanner.main()
