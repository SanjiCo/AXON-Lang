# AXON Jupyter Kernel

Bu belge, AXON programlama dili için Jupyter Notebook kernel'inin nasıl kurulacağını ve kullanılacağını açıklamaktadır.

## Gereksinimler

- Python 3.6 veya üzeri
- Jupyter Notebook veya JupyterLab
- AXON programlama dili yorumlayıcısı

## Kurulum

### 1. Gerekli Python paketlerini yükleyin

```bash
pip install jupyter notebook ipykernel
```

### 2. AXON Jupyter Kernel'ini kurun

```bash
python install_kernel.py --user
```

Bu komut, AXON kernel'ini mevcut kullanıcı için kuracaktır. Sistem genelinde kurmak için `--user` parametresini kaldırın.

## Kullanım

### 1. Jupyter Notebook'u başlatın

```bash
jupyter notebook
```

### 2. Yeni bir notebook oluşturun

Jupyter Notebook arayüzünde "New" düğmesine tıklayın ve açılan menüden "AXON" seçeneğini seçin.

### 3. AXON kodunu çalıştırın

Artık notebook hücrelerinde AXON kodunu yazabilir ve çalıştırabilirsiniz. Örnek:

```
var x = 10
var y = 20
print("Toplam: " + (x + y))
```

## Örnek Notebook

`examples/axon_jupyter_demo.axon` dosyasında AXON dilinin Jupyter Notebook'ta nasıl kullanılacağına dair bir örnek bulabilirsiniz. Bu örneği Jupyter'de açmak için:

1. Jupyter Notebook'u başlatın
2. Dosya gezgininde `examples` klasörüne gidin
3. `axon_jupyter_demo.axon` dosyasını açın

## Sorun Giderme

### Kernel başlatılamıyor

Eğer kernel başlatılamıyorsa:

1. Kernel kurulumunu kontrol edin:
   ```bash
   jupyter kernelspec list
   ```

2. AXON yorumlayıcısının doğru konumda olduğundan emin olun.

3. Kernel log dosyalarını kontrol edin:
   ```bash
   jupyter troubleshoot
   ```

### Kernel çöküyor

Eğer kernel çalışma sırasında çöküyorsa:

1. Terminal'de Jupyter'i başlatın ve hata mesajlarını kontrol edin.
2. `axon_kernel.py` dosyasındaki hata yakalama mekanizmalarını kontrol edin.

## Özelleştirme

Kernel davranışını özelleştirmek için `axon_kernel.py` dosyasını düzenleyebilirsiniz. Örneğin:

- Çıktı formatını değiştirme
- Ek komutlar ekleme
- Hata mesajlarını özelleştirme

## Katkıda Bulunma

AXON Jupyter Kernel'ini geliştirmek için önerileriniz veya katkılarınız varsa, lütfen bir pull request gönderin veya bir issue açın.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. 