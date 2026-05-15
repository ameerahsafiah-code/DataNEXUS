import os
import subprocess
import pandas as pd
import streamlit as st
from playwright.sync_api import sync_playwright
from groq import Groq

def install_playwright_stuff():
    """Memastikan browser dipasang hanya jika perlu"""
    try:
        # Semak jika browser sudah ada, jika tidak, pasang.
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except:
        pass

def scrape_data():
    install_playwright_stuff()
    with sync_playwright() as p:
        try:
            # Gunakan chromium_headless_shell untuk lebih ringan di server
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()
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
            browser.close()
            return data
        except Exception as e:
            st.error(f"Ralat semasa melayar web: {e}")
            return []

def analyze_with_ai(data):
    api_key = os.getenv("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")
    if not api_key:
        st.error("Sila masukkan GROQ_API_KEY dalam Secrets!")
        return
    
    client = Groq(api_key=api_key)
    prompt = f"Analisis data harga ini dalam Bahasa Melayu: {str(data)}. Berikan rumusan strategi perniagaan yang kreatif."
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
        )
        result = chat.choices[0].message.content
        with open("laporan_ai.txt", "w", encoding="utf-8") as f:
            f.write(result)
        return result
    except Exception as e:
        st.error(f"Ralat AI: {e}")

def run_all():
    data = scrape_data()
    if data:
        analyze_with_ai(data)