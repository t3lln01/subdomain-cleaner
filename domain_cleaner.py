#!/usr/bin/python3

import os
import sys
import subprocess
import requests

PSL_URL = "https://publicsuffix.org/list/public_suffix_list.dat"

def download_psl(url):
    """Download the Public Suffix List."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the Public Suffix List: {e}")
        sys.exit(1)

def extract_psl_domains(psl_data):
    """Extract second-level domains from the Public Suffix List."""
    lines = [line.strip() for line in psl_data.splitlines() if line and not line.startswith("//")]
    return set(lines)

def extract_slds_with_awk(input_file):
    """Use awk to extract second-level domains from the input file."""
    awk_command = f"awk -F'.' '{{ k[$(NF-1)\".\"$(NF)]++}}END{{for (i in k){{print i}}}}' {input_file}"
    try:
        result = subprocess.check_output(awk_command, shell=True, text=True)
        return {line.strip() for line in result.splitlines()}
    except subprocess.CalledProcessError as e:
        print(f"Error running awk: {e}")
        sys.exit(1)

def apply_sed_format(domains):
    """Apply sed-style replacement to format domains (replace '.' with '[.]')."""
    return [domain.replace('.', '[.]') for domain in domains]

def filter_domains(input_slds, psl_domains):
    """Filter input second-level domains by removing those present in the PSL."""
    return input_slds - psl_domains

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 filter_domains_with_sed.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    print("Downloading the Public Suffix List...")
    psl_data = download_psl(PSL_URL)

    print("Extracting domains from the Public Suffix List...")
    psl_domains = extract_psl_domains(psl_data)

    print("Extracting second-level domains from input file using awk...")
    input_slds = extract_slds_with_awk(input_file)

    print("Filtering domains...")
    filtered_slds = filter_domains(input_slds, psl_domains)

    print("Applying sed-style formatting to filtered domains...")
    formatted_slds = apply_sed_format(filtered_slds)

    print("Filtered and formatted domains:")
    for domain in sorted(formatted_slds):
        print(domain)

if __name__ == "__main__":
    main()


 
