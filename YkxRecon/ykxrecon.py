#!/usr/bin/env python3

def logo():
    print(r"""
 __     __  _             _____                                
 \ \   / / | |           |  __ \                               
  \ \_/ /  | | __ __  __ | |__) |   ___    ___    ___    _ __  
   \   /   | |/ / \ \/ / |  _  /   / _ \  / __|  / _ \  | '_ \ 
    | |    |   <   >  <  | | \ \  |  __/ | (__  | (_) | | | | |
    |_|    |_|\_\ /_/\_\ |_|  \_\  \___|  \___|  \___/  |_| |_|

""")
logo()

import subprocess
import argparse
import os

def argument():
    parser = argparse.ArgumentParser(description="Created by Ykx999 (:")
    parser.add_argument(
        "-d", "--domains", nargs="+",
        help="List of domains to add. Separate multiple domains with spaces.",
        required=False
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to a file containing domains (one per line).",
        required=False
    )
    parser.add_argument(
        "-v", "--version", action="version", version="1.0",
        help="Display the script version and exit."
    )
    parser.add_argument(
        "--stdout", action="store_true",
        help="Display the subdomain enumeration result directly in the terminal."
    )
    return parser.parse_args()

def remove_duplicates(file_path):
    """Remove duplicates from the given file"""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove duplicates by converting to a set and then back to a list
        unique_lines = list(set(line.strip() for line in lines))

        with open(file_path, 'w') as file:
            for line in unique_lines:
                file.write(line + "\n")

        print(f"check {file_path}.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred while removing duplicates: {e}")

def main():
    args = argument()

    # Check if no arguments are passed (i.e., neither -d nor -f)
    if not args.domains and not args.file:
        print("Error: No domains specified. Please provide domains using -d or -f & for --help use -h")
        exit(1)  # Exit the script if no domains are provided

    # Ensure the hidden '.domains.txt' file exists
    subprocess.run("touch .domains.txt", shell=True)

    # Add domains from command-line arguments
    if args.domains:
        with open(".domains.txt", "a") as file:
            for domain in args.domains:
                file.write(domain.strip() + "\n")
        print(f"Added {len(args.domains)} domains to '.domains.txt'.")

    # Add domains from a file
    if args.file:
        try:
            with open(args.file, "r") as f:
                domains_from_file = f.read().splitlines()
                with open(".domains.txt", "a") as file:
                    for domain in domains_from_file:
                        file.write(domain.strip() + "\n")
                print(f"Added {len(domains_from_file)} domains from '{args.file}' to '.domains.txt'.")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")

    # Step 1: Remove 'www.' from the start of the domains
    try:
        with open(".domains.txt", "r") as domains, open(".clean-domains.txt", "w") as domains2:
            for domain in domains:
                cleaned_domain = domain.lstrip('www.').strip()
                domains2.write(cleaned_domain + "\n")
    except FileNotFoundError:
        print("Error: '.domains.txt' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Remove duplicates from both '.domains.txt' and '.clean-domains.txt'
    remove_duplicates(".domains.txt")
    remove_duplicates(".clean-domains.txt")

    # Step 2: Subdomain enumeration using Amass or Subfinder
    if os.path.exists(".clean-domains.txt"):
        with open(".clean-domains.txt", "r") as domains:
            for domain in domains:
                domain = domain.strip()  # Remove newline and extra spaces
                if not domain:
                    continue
                print(f"Enumerating subdomains for: {domain}")

                # Debug: Print out the domain being processed
                print(f"Processing domain: {domain}")

                if args.stdout:
                    # Display results directly in the terminal
                    try:
                        subprocess.run(f"subfinder -d {domain} -silent", shell=True, timeout=60)
                    except subprocess.TimeoutExpired:
                        print(f"Subdomain enumeration for {domain} timed out.")
                    except Exception as e:
                        print(f"An error occurred while enumerating subdomains for {domain}: {e}")
                else:
                    # Default behavior: Write results to a file
                    try:
                        subdomain_file = f"{domain}_subdomains.txt"
                        counter = 2
                        while os.path.exists(subdomain_file):
                            subdomain_file = f"{domain}_subdomains-{counter}.txt"
                            counter += 1

                        # Run subfinder and set a timeout
                        result = subprocess.run(f"subfinder -d {domain} -silent -o {subdomain_file}", shell=True, capture_output=True, text=True, timeout=60)
                        if result.returncode != 0:
                            print(f"Error occurred while running subfinder for {domain}: {result.stderr}")
                        else:
                            print(f"Subdomain enumeration complete for {domain}, results saved to {subdomain_file}.")
                    except subprocess.TimeoutExpired:
                        print(f"Subdomain enumeration for {domain} timed out.")
                    except Exception as e:
                        print(f"An error occurred while enumerating subdomains for {domain}: {e}")
    else:
        print("Error: 'something went wrong. Please type ./ykxrecon -h'")

if __name__ == "__main__":
    main()
