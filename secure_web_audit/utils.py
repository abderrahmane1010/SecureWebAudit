class darkcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def colorize(string, alert):
    bcolors = darkcolours
    color = {
        'error':    bcolors.FAIL + string + bcolors.ENDC,
        'warning':  bcolors.WARNING + string + bcolors.ENDC,
        'ok':       bcolors.OKGREEN + string + bcolors.ENDC,
        'info':     bcolors.OKBLUE + string + bcolors.ENDC,
        'magenta':  bcolors.MAGENTA + string + bcolors.ENDC,
        "blue": "\033[94m" + string + "\033[94m",
        "green": "\033[92m" + string + "\033[92m",
        "yellow": "\033[93m" + string + "\033[93m",
        "red": "\033[91m" + string + "\033[91m",
        "end": "\033[0m" + string + "\033[0m",
        'cyan' : bcolors.CYAN + string + bcolors.ENDC,
        'High': bcolors.FAIL + string + bcolors.ENDC,
        'Medium': bcolors.WARNING + string + bcolors.ENDC,
        'Low': bcolors.OKBLUE + string + bcolors.ENDC,
        'Information Leak': bcolors.HEADER + string + bcolors.ENDC,
        'deprecated': string # No color for deprecated headers or not-an-issue ones
    }
    return color[alert] if alert in color else string

def banner_headers(url):
    print("")
    print(colorize("===" * 24, "green"))
    print(colorize("   >>> HTTP Headers Security Assessment <<<   ", "yellow"))
    print(colorize("---" * 24, "green"))
    print("This tool assesses HTTP headers of a website for security compliance and")
    print("potential vulnerabilities. It offers insights into header configurations")
    print("and provides recommendations for enhancing header security.")
    print(colorize("---" * 24, "green"))
    print(f' Analyzed URL: {colorize(url, "blue")}')
    print(colorize("===" * 24, "green"))
    print("")
    
def banner_xss(url):
    print("\n")
    print(colorize("===" * 24, "green"))
    print(colorize("   >>> XSS Analysis <<<   ", "yellow"))
    print(colorize("---" * 24, "green"))
    print("This tool assesses XSS vulnerabilities of a website.")
    print("It offers insights into possible XSS vulnerabilities")
    print("and provides recommendations for enhancing web security.")
    print(colorize("---" * 24, "green"))
    print(f' Analyzed URL: {colorize(url, "blue")}')
    print(colorize("===" * 24, "green"))
    print("\n")

    
def banner(url):
    print("")
    print("=" * 72)
    print(colorize("                           SecureWebAudit","cyan"))
    print("-" * 72)
    print("""SecureWebAudit is a tool designed for conducting comprehensive website """)
    print("security audits. These audits involve a detailed analysis of various")
    print("aspects of a website to identify and address potential vulnerabilities.")
    print("-" * 72)
    print(f' {colorize("URL : "+url,"magenta")}')
    print("=" * 72)
    print("")
    
    
def is_packet_suspicious(packet):
    # Logique simplifiée pour déterminer si un paquet est suspect
    return "suspicious" in packet