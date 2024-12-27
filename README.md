# xNodepayBot
This bot connects via multiple HTTP proxies to farm Nodepay using a multi account.

## Installation

1. Install ENV
   ```bash
   sudo apt update -y && apt install -y python3 python3-venv pip
   ```

2. Setup resources:
   ```bash
   git clone https://github.com/officialputuid/xNodepayBot && cd xNodepayBot
   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   python3 main.py
   python3 dailyclaim.py
   ```

## Token
- If you haven't registered, feel free to use my referral link: ([REGISTER NODEPAY)](https://app.nodepay.ai/register?ref=Sp9DUiMoAAw3MBv).
- How to Get Token?
  - Login and open https://app.nodepay.ai/dashboard
  - Open Developer Tools in your browser (F12) / Inspect Element.
  - In the "Console" tab, type:
   `localStorage.getItem('np_token')`
  - Copy the result without "" or '' and paste it into `tokens.txt`.
  - For multiple accounts, add each token on a new line, for example:
     ```
     token1
     token2
     token3
     ```

## Proxy  
- Fill in `proxy.txt` with the format `protocol://user:pass@host:port`.

## Need Proxy?
1. Sign up at [Proxies.fo](https://app.proxies.fo/ref/849ec384-ecb5-1151-b4a7-c99276bff848).
2. Go to [Plans](https://app.proxies.fo/plans) and only purchase the "ISP plan" (Residential plans don’t work).
3. Top up your balance, or you can directly buy a plan and pay with Crypto!
4. Go to the Dashboard, select your ISP plan, and click "Generate Proxy."
5. Set the proxy format to `protocol://username:password@hostname:port`
6. Choose any number for the proxy count, and paste the proxies into `proxy.txt`.


