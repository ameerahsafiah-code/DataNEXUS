import os
import subprocess
import pandas as pd
from playwright.sync_api import sync_playwright
from groq import Groq

def install_playwright_stuff():
    """Memaksa pemasangan sistem dependencies di server"""
    try:
        # Pasang browser dan dependencies sistem secara paksa
        subprocess.run(["playwright", "install", "chromium"], check=True)
        subprocess.run(["playwright", "install-deps", "chromium"], check=True)
    except:
        pass

def scrape_data():
    install_playwright_stuff()
    with sync_playwright() as p:
        # Argumen 'args' ditambah untuk mengelakkan ralat sandbox di server Linux
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        try:
            page.goto("http://books.toscrape.com/", timeout=60000)
            titles = page.locator("h3 a").all_inner_texts()
            prices = page.locator(".price_color").all_inner_texts()
            
            data = []
            for i in range(min(10, len(titles))):
                data.append({
                    "Nama Produk": titles[i],
                    "Harga": prices[i].replace("Â", ""),
                })
            df = pd.DataFrame(data)
            df.to_csv("data_buku_besar.csv", index=False)
            return data
        except Exception as e:
            print(f"Ralat: {e}")
            return []
        finally:
            browser.close()

def analyze_with_ai(data):
    api_key = os.getenv("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")
    if not api_key: return "API Key tidak dijumpai."
    client = Groq(api_key=api_key)
    prompt = f"Analisis data harga produk ini dalam Bahasa Melayu secara profesional: {str(data)}. Berikan produk termahal, termurah dan cadangan perniagaan."
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
        )
        result = chat.choices[0].message.content
        with open("laporan_ai.txt", "w", encoding="utf-8") as f:
            f.write(result)
        return result
    except:
        return "Ralat semasa menjana ulasan AI."

def run_all():
    data = scrape_data()
    if data:
        analyze_with_ai(data)