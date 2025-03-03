#!/usr/bin/env python3
"""
AXON Jupyter Kernel kurulum betiği
"""

import os
import sys
import json
import argparse
from tempfile import TemporaryDirectory

def main():
    parser = argparse.ArgumentParser(description='AXON Jupyter Kernel kurulumu')
    parser.add_argument('--user', action='store_true', help='Kernel\'i sadece mevcut kullanıcı için kur')
    args = parser.parse_args()
    
    # Kernel JSON dosyası
    kernel_json = {
        "argv": [sys.executable, os.path.abspath("axon_kernel.py"), "-f", "{connection_file}"],
        "display_name": "AXON",
        "language": "axon"
    }
    
    try:
        from jupyter_client.kernelspec import KernelSpecManager
    except ImportError:
        print("Jupyter yüklü değil. Lütfen 'pip install jupyter' komutu ile yükleyin.")
        sys.exit(1)
    
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Jupyter requires this permission
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, indent=4)
        
        # Kernel logosu eklemek isterseniz:
        # logo_path = os.path.join(os.path.dirname(__file__), 'axon_logo.png')
        # if os.path.exists(logo_path):
        #     shutil.copy(logo_path, os.path.join(td, 'logo-64x64.png'))
        
        print('Kurulacak kernel spec dizini:', td)
        KernelSpecManager().install_kernel_spec(td, 'axon', user=args.user, replace=True)
        print('AXON kernel başarıyla kuruldu.')
        print('Jupyter Notebook veya Jupyter Lab\'ı başlatarak AXON kernel\'ini kullanabilirsiniz.')

if __name__ == '__main__':
    main() 