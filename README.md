**subdomain-cleaner.py** clears up subdomains from lists until 2nd level domain is reached and fangs the remaining domains (avoids matches for legit domains like co.uk or com.co etc..). Small util useful for domain blocklists clearup, host files clearup, etc..

**domain_cleaner.py** downloads the Mozilla's Publix Suffix List  then extracts 2nd level domains from an input list and removes known bening entries  (ex: co[.]uk, com[.]co, gov[.]us, edu[.]in, etc...) using the PSL and fangs the malicious 2nd level domains.  
