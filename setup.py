#!/usr/bin/env python3

from setuptools import setup
import os
import sys
import json
from tempfile import TemporaryDirectory

kernel_json = {
    "argv": [sys.executable, "-m", "axon_kernel", "-f", "{connection_file}"],
    "display_name": "AXON",
    "language": "axon"
}

def install_kernel_spec():
    user = '--user' in sys.argv
    try:
        from jupyter_client.kernelspec import KernelSpecManager
    except ImportError:
        raise ImportError('Jupyter is not installed. Install it via pip install jupyter.')
    
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Jupyter requires this permission
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, indent=4)
        
        # Kernel logosu eklemek isterseniz:
        # logo_path = os.path.join(os.path.dirname(__file__), 'axon_logo.png')
        # if os.path.exists(logo_path):
        #     shutil.copy(logo_path, os.path.join(td, 'logo-64x64.png'))
        
        print('Kurulacak kernel spec dizini:', td)
        KernelSpecManager().install_kernel_spec(td, 'axon', user=user, replace=True)
        print('AXON kernel başarıyla kuruldu.')

setup(
    name="axon_kernel",
    version="1.0",
    description="AXON Jupyter Kernel",
    author="AXON Team",
    py_modules=['axon_kernel'],
    install_requires=[
        'jupyter',
        'ipykernel',
    ],
    classifiers=[
        'Framework :: Jupyter',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
    ],
)

if 'install' in sys.argv or 'develop' in sys.argv:
    install_kernel_spec() 