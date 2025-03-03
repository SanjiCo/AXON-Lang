#!/usr/bin/env python3
"""
AXON Jupyter Notebook başlatma betiği
"""

import os
import sys
import subprocess
import argparse
import webbrowser
import time

def check_jupyter_installed():
    """Jupyter'in yüklü olup olmadığını kontrol eder."""
    try:
        import jupyter
        return True
    except ImportError:
        return False

def check_kernel_installed():
    """AXON kernel'inin yüklü olup olmadığını kontrol eder."""
    try:
        result = subprocess.run(
            ["jupyter", "kernelspec", "list"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return "axon" in result.stdout.lower()
    except subprocess.CalledProcessError:
        return False

def install_kernel():
    """AXON kernel'ini yükler."""
    print("AXON Jupyter Kernel kuruluyor...")
    try:
        subprocess.run(
            ["python", "install_kernel.py", "--user"], 
            check=True
        )
        print("Kernel başarıyla kuruldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Kernel kurulumu başarısız oldu: {e}")
        return False

def start_jupyter(notebook_dir=None, open_browser=True):
    """Jupyter Notebook'u başlatır."""
    cmd = ["jupyter", "notebook"]
    
    if notebook_dir:
        cmd.extend(["--notebook-dir", notebook_dir])
    
    if not open_browser:
        cmd.append("--no-browser")
    
    print("Jupyter Notebook başlatılıyor...")
    try:
        process = subprocess.Popen(cmd)
        
        if open_browser:
            # Jupyter'in başlaması için biraz bekle
            time.sleep(2)
            # Tarayıcıyı aç
            webbrowser.open("http://localhost:8888/tree")
        
        return process
    except Exception as e:
        print(f"Jupyter başlatılamadı: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="AXON Jupyter Notebook başlatma aracı")
    parser.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma")
    parser.add_argument("--notebook-dir", type=str, help="Notebook dizini")
    args = parser.parse_args()
    
    # Jupyter'in yüklü olup olmadığını kontrol et
    if not check_jupyter_installed():
        print("Jupyter yüklü değil. Lütfen 'pip install jupyter notebook ipykernel' komutunu çalıştırın.")
        return 1
    
    # AXON kernel'inin yüklü olup olmadığını kontrol et
    if not check_kernel_installed():
        print("AXON Jupyter Kernel bulunamadı.")
        install = input("Kernel'i şimdi kurmak ister misiniz? (e/h): ")
        if install.lower() in ["e", "evet", "y", "yes"]:
            if not install_kernel():
                return 1
        else:
            print("Kernel kurulmadan devam ediliyor. AXON kernel'i kullanılamayabilir.")
    
    # Notebook dizinini belirle
    notebook_dir = args.notebook_dir
    if not notebook_dir:
        # Varsayılan olarak examples klasörünü kullan
        examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
        if os.path.exists(examples_dir):
            notebook_dir = examples_dir
    
    # Jupyter'i başlat
    process = start_jupyter(notebook_dir, not args.no_browser)
    if not process:
        return 1
    
    try:
        # Jupyter çalışırken bekle
        print("Jupyter çalışıyor. Çıkmak için Ctrl+C tuşlarına basın...")
        process.wait()
    except KeyboardInterrupt:
        print("\nJupyter kapatılıyor...")
        process.terminate()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 