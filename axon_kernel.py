#!/usr/bin/env python3
"""
AXON Jupyter Kernel
"""
import sys
import os
import json
import re
from ipykernel.kernelbase import Kernel
from axon import AxonInterpreter

class AxonKernel(Kernel):
    implementation = 'AXON'
    implementation_version = '1.0'
    language = 'AXON'
    language_version = '1.0'
    language_info = {
        'name': 'axon',
        'mimetype': 'text/plain',
        'file_extension': '.axon',
    }
    banner = "AXON Kernel - Eğitim amaçlı programlama dili"

    def __init__(self, **kwargs):
        super(AxonKernel, self).__init__(**kwargs)
        self.interpreter = AxonInterpreter()
        self.output_history = []

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """
        AXON kodunu çalıştır ve sonuçları döndür
        """
        if not silent:
            # Çıktıları yakalamak için
            original_stdout = sys.stdout
            from io import StringIO
            captured_stdout = StringIO()
            sys.stdout = captured_stdout

            try:
                # Kodu satır satır çalıştır
                lines = code.split('\n')
                line_number = 0
                
                while line_number < len(lines):
                    line = lines[line_number]
                    line_number += 1
                    
                    # Boş satırları ve yorumları atla
                    if not line.strip() or line.strip().startswith('#'):
                        continue
                    
                    # Satırı çalıştır
                    self.interpreter.current_line = line_number
                    result = self.interpreter.parse_line(line)
                    
                    # Kontrol akışını yönet
                    if isinstance(result, dict) and 'jump' in result:
                        line_number = result['jump']
                
                # Çıktıyı al
                output = captured_stdout.getvalue()
                
                if output:
                    # Çıktıyı stream olarak gönder
                    self.send_response(self.iopub_socket, 'stream', {
                        'name': 'stdout',
                        'text': output
                    })
                
                # Eğer bir sonuç varsa, onu da gönder
                if result is not None and result != "None" and not isinstance(result, dict):
                    self.send_response(self.iopub_socket, 'execute_result', {
                        'execution_count': self.execution_count,
                        'data': {'text/plain': str(result)},
                        'metadata': {}
                    })
                
            except Exception as e:
                # Hata mesajını gönder
                error_msg = f"Error: {str(e)}"
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stderr',
                    'text': error_msg
                })
                
                return {
                    'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': [error_msg]
                }
            
            finally:
                # stdout'u eski haline getir
                sys.stdout = original_stdout

        # Başarılı çalıştırma durumunda
        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {}
        }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=AxonKernel) 