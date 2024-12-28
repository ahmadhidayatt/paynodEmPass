import asyncio
import aiohttp
import time
import uuid
import random
import re
from fake_useragent import UserAgent
import pyfiglet
from loguru import logger

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=''),
    format=(
        "<green>{time:DD/MM/YY HH:mm:ss}</green> | "
        "<level>{level:8} | {message}</level>"
    ),
    colorize=True
)

# main.py
def print_header():
    cn = pyfiglet.figlet_format("xNodepayBot")
    print(cn)
    print("🌟 Season 2")
    print("🔗 by \033]8;;https://github.com/officialputuid\033\\officialputuid\033]8;;\033\\")
    print("✨ Credits: IDWR2016, im-hanzou, AirdropFamilyIDN")
    print('💰 \033]8;;https://paypal.me/IPJAP\033\\Paypal.me/IPJAP\033]8;;\033\\ — \033]8;;https://trakteer.id/officialputuid\033\\Trakteer.id/officialputuid\033]8;;\033\\')

# Initialize the header
print_header()

# Read Credentials and Proxy count
def read_credentials_and_proxy():
    with open('credentials.txt', 'r') as file:
        credentials_content = sum(1 for line in file)

    with open('proxy.txt', 'r') as file:
        proxy_count = sum(1 for line in file)

    return credentials_content, proxy_count

credentials_content, proxy_count = read_credentials_and_proxy()

print()
print(f"🔑 Credentials: {credentials_content}.")
print(f"🌐 Loaded {proxy_count} proxies.")
print(f"🔒 Nodepay limits only 3 connections per account.")
print()

# Constants
PING_INTERVAL = 60
RETRIES_LIMIT = 60
PROXIES_PER_CREDENTIAL = 5

# API Endpoints
DOMAIN_API_ENDPOINTS = {
    "LOGIN": [
        "https://api.nodepay.ai/api/auth/login"
    ],
    "PING": [
        "https://nw.nodepay.ai/api/network/ping"
    ]
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NO_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NO_CONNECTION"]
browser_id = None
account_info = {}
last_ping_time = {}

def truncate_proxy(proxy):
    return f"{proxy[:6]}--{proxy[-10:]}"

def generate_uuid():
    return str(uuid.uuid4())

def validate_response(response):
    if not response or "code" not in response or response["code"] < 0:
        raise ValueError("Invalid response received from the server.")
    return response

async def initialize_profile(proxy, username, password):
    global browser_id, account_info
    await asyncio.sleep(random.uniform(1.0, 3.0))
    try:
        session_info = load_session_info(proxy)

        if not session_info:
            browser_id = generate_uuid()
            payload = {
                "username": username,
                "password": password
            }
            response = await send_request(DOMAIN_API_ENDPOINTS["LOGIN"][0], payload, proxy)
            validate_response(response)
            account_info = response["data"]

            if account_info.get("uid"):
                save_session_info(proxy, account_info)
                await start_ping_loop(proxy, username, password)
            else:
                handle_logout(proxy)
        else:
            account_info = session_info
            await start_ping_loop(proxy, username, password)
    except Exception as e:
        error_message = str(e)
        if "keepalive ping timeout" in error_message or "500 Internal Server Error" in error_message:
            remove_proxy(proxy)
        else:
            logger.error(f"Error: {error_message}")
            return proxy

async def send_request(url, payload, proxy):
    headers = {
        "Content-Type": "application/json",
        "User -Agent": UserAgent().random,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers, proxy=proxy, timeout=60) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Token: {truncate_token(token)} | API request failed, Error: {str(e)[:32]}**")
            raise ValueError(f"API request failed")

async def start_ping_loop(proxy, token):
    try:
        while True:
            await asyncio.sleep(random.uniform(1.0, 3.0))
            await send_ping(proxy, token)
            await asyncio.sleep(PING_INTERVAL)
    except asyncio.CancelledError:
        pass
    except Exception:
        pass

async def send_ping(proxy, token):
    global last_ping_time, RETRIES_LIMIT, status_connect
    last_ping_time[proxy] = time.time()

    try:
        ping_url = DOMAIN_API_ENDPOINTS["PING"][0]

        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time())
        }

        response = await send_request(ping_url, data, proxy, token)
        if response["code"] == 0:
            ip_address = "Not Used/Direct" if not proxy else re.search(r'(?<=@)[^:]+', proxy).group()
            logger.success(f"Token: {truncate_token(token)} | Ping: {response.get('msg')} | IP Score: {response['data'].get('ip_score')}% | Proxy: {ip_address}")
            RETRIES_LIMIT = 0
            status_connect = CONNECTION_STATES["CONNECTED"]
        else:
            handle_ping_failure(proxy, response)
    except Exception:
        handle_ping_failure(proxy, None)

def handle_ping_failure(proxy, response):
    global RETRIES_LIMIT, status_connect
    RETRIES_LIMIT += 1
    if response and response.get("code") == 403:
        handle_logout(proxy)
    else:
        logger.error(f"Token: {truncate_token(token)} | Ping failed for proxy {truncate_proxy(proxy)}.")
        remove_proxy(proxy)
        status_connect = CONNECTION_STATES["DISCONNECTED"]

def handle_logout(proxy):
    global status_connect, account_info
    status_connect = CONNECTION_STATES["NO_CONNECTION"]
    account_info = {}
    save_status(proxy, None)

def load_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except Exception:
        logger.error(f"Failed to load proxy list. Exiting.")
        raise SystemExit()

def save_session_info(proxy, data):
    pass

def load_session_info(proxy):
    return {}

def remove_proxy(proxy):
    pass

def ask_user_for_proxy():
    user_input = ""
    while user_input not in ['yes', 'no']:
        user_input = input("🔵 Do you want to use proxy? (yes/no)? ").strip().lower()
        if user_input not in ['yes', 'no']:
            print("🔴 Invalid input. Please enter 'yes' or 'no'.")
    print(f"🔵 You selected: {'Yes' if user_input == 'yes' else 'No'}, ENJOY!\n")
    return user_input == 'yes'

async def main():
    use_proxy = ask_user_for_proxy()

    proxies = load_proxies('proxy.txt') if use_proxy else []

    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        logger.error(f"tokens.txt not found. Ensure the file is in the correct directory.")
        exit()

    if not tokens:
        logger.error(f"No tokens provided. Exiting.")
        exit()

    if use_proxy and len(proxies) < len(tokens) * PROXIES_PER_TOKEN:
        logger.error(f"Insufficient proxies. You need at least {len(tokens) * PROXIES_PER_TOKEN} proxies for {len(tokens)} tokens.")
        exit()

    while True:
        logger.info("Starting a new cycle of tasks.")
        token_proxy_pairs = []

        if use_proxy:
            for i, token in enumerate(tokens):
                assigned_proxies = proxies[i * PROXIES_PER_TOKEN:(i + 1) * PROXIES_PER_TOKEN]
                if len(assigned_proxies) < PROXIES_PER_TOKEN:
                    logger.error(f"Not enough proxies assigned for token {truncate_token(token)}. Skipping this token.")
                    continue

                for proxy in assigned_proxies:
                    token_proxy_pairs.append((token, proxy))
        else:
            token_proxy_pairs = [(token, "") for token in tokens]

        tasks = []

        for token, proxy in token_proxy_pairs:
            tasks.append(asyncio.create_task(initialize_profile(proxy, token)))
            await asyncio.sleep(random.uniform(1.0, 3.0))

        await asyncio.gather(*tasks)

        logger.info("All tasks completed. Waiting before starting a new cycle.")
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info(f"Program terminated by user. ENJOY!\n")
