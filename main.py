import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time

def initialize_browser_with_extension(extension_path):
    """
    Menginisialisasi browser dengan ekstensi tertentu untuk menyelesaikan CAPTCHA.
    """
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_extension(extension_path)  # Tambahkan ekstensi
    
    driver = uc.Chrome(options=options)
    return driver

def login_nodepay_with_captcha(driver, username, password):
    """
    Fungsi untuk login ke NodePay dengan menangani CAPTCHA jika diperlukan.
    """
    driver.get("https://app.nodepay.ai/login")
    time.sleep(3)  # Tunggu halaman selesai dimuat
    
    # Isi form login
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    
    # Handle CAPTCHA
    captcha_frame = driver.find_elements(By.TAG_NAME, "iframe")
    if captcha_frame:
        print("CAPTCHA ditemukan. Ekstensi akan mencoba menyelesaikannya...")
        time.sleep(15)  # Beri waktu ekstensi untuk menyelesaikan CAPTCHA
    
    # Klik tombol login
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(5)  # Tunggu respon dari server
    
    # Cek hasil login
    if "dashboard" in driver.current_url:
        print(f"Login berhasil untuk {username}!")
        return True
    else:
        print(f"Login gagal untuk {username}.")
        return False

def read_credentials(file_path):
    """
    Membaca file credential.txt dan mengembalikan daftar email dan password.
    """
    credentials = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                email, password = line.split(":")
                credentials.append((email, password))
    return credentials

if __name__ == "__main__":
    EXTENSION_PATH = "/path/to/extension/directory_or_crx_file"  # Path ke ekstensi CAPTCHA solver
    CREDENTIAL_FILE = "credential.txt"  # Path file credential.txt
    
    credentials = read_credentials(CREDENTIAL_FILE)
    
    driver = initialize_browser_with_extension(EXTENSION_PATH)
    try:
        for email, password in credentials:
            print(f"Memulai login untuk: {email}")
            success = login_nodepay_with_captcha(driver, email, password)
            if success:
                print(f"Berhasil login untuk: {email}")
            else:
                print(f"Gagal login untuk: {email}")
            time.sleep(2)  # Delay sebelum mencoba kredensial berikutnya
    finally:
        driver.quit()
