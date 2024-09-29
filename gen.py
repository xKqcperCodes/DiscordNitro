import requests
import random
from faker import Faker
from colorama import Fore, Style, init
import datetime
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
import os
os.system('title UnlockNow bypasser / .xKq on discord')
fake = Faker()
init()

def log(tag, content, color):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"{Style.BRIGHT}{Fore.BLACK}[{ts}] {color}[{tag}] {Fore.WHITE}{content}{Style.RESET_ALL}")

def generate_account_and_promo(proxy):
    name = (fake.first_name() + fake.last_name()).lower()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.chess.com/friends?name=joseph",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    session = requests.Session()
    if '@' in proxy:
        ip_port, user_pass = proxy.split('@')
        session.proxies = {
            "http": "http://" + user_pass + "@" + ip_port,
            "https": "http://" + user_pass + "@" + ip_port,
        }
    else:
        session.proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy,
        }

    response = session.get("https://www.chess.com/member/" + name, headers=headers)
    try:
        uuid = response.text.split('data-user-uuid="')[1].split('"')[0]
        log("GENNED", f"Genned Account -> {uuid} ({name})", Fore.BLUE)
    except Exception as e:
        log("ERR", f"Failed to retrieve UUID: {e}", Fore.RED)
        return None

    promo_headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.chess.com",
        "priority": "u=1, i",
        "referer": "https://www.chess.com/play/computer/discord-wumpus?utm_source=partnership&utm_medium=article&utm_campaign=discord2024_bot",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    json_data = {
        "userUuid": uuid,
        "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce",
    }

    response = session.post(
        "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode",
        headers=promo_headers,
        json=json_data,
    )

    try:
        response_data = response.json()
        if response.status_code == 200 and "codeValue" in response_data:
            code = 'https://promos.discord.gg/' + response_data["codeValue"]
            log("PROMO", "Created Promo -> {}".format(code), Fore.GREEN)
            with open('codes.txt', 'a') as f:
                f.write(code + '\n')
        else:
            log("ERR", f"Error retrieving promo code: {response_data}", Fore.RED)
    except Exception as e:
        log("ERR", "Error occurred while processing the response -> {}".format(e), Fore.RED)


if not os.path.isfile('proxies.txt'):
    with open('proxies.txt', 'w') as f:
        f.write('# Add your proxies here, one per line\n')


if not os.path.isfile('codes.txt'):
    with open('codes.txt', 'w') as f:
        f.write('# This file will store generated promo codes\n')


with open('proxies.txt', 'r') as f:
    proxies = f.read().splitlines()


if not proxies or all(proxy.strip() == '' for proxy in proxies):
    log("ERR", "No proxies found. Please add proxies to proxies.txt.", Fore.RED)
else:
    
    user_input = input("Enter the number of promo codes to generate (press Enter to generate indefinitely): ")
    
    
    if user_input.strip() == "":
        num_codes = float("inf")
        log("INFO", "Generating promo codes indefinitely...", Fore.YELLOW)
    else:
        num_codes = int(user_input)

    num_threads = int(input("Enter the number of threads (recommended: 50-1000): "))

    generated_count = 0

    with ThreadPoolExecutor(max_workers=num_threads) as exc:
        while generated_count < num_codes:
            if proxies:  
                p = random.choice(proxies)
                exc.submit(generate_account_and_promo, p)
                generated_count += 1  
                time.sleep(0.001)
            else:
                log("ERR", "No valid proxies available to generate promo codes.", Fore.RED)
                break