# AXON Programming Language

AXON, eğitim amaçlı geliştirilmiş bir programlama dilidir. Python ile yazılmış bir yorumlayıcı kullanarak çalışır.

## Özellikler

- Değişken tanımlama ve atama
- Koşullu ifadeler (if)
- Döngüler (while)
- Fonksiyonlar
- Bellek yönetimi
- İş parçacığı (thread) yönetimi
- Görev (task) zamanlama
- Süreç (process) yönetimi
- Nesne yönelimli programlama
- Hata ayıklama özellikleri
- Standart kütüphane

## Standart Kütüphane

AXON, aşağıdaki kategorilerde standart kütüphane fonksiyonları sunar:

- Matematik fonksiyonları (`math.*`)
- String işlemleri (`string.*`)
- Zaman işlemleri (`time.*`)
- Sistem işlemleri (`system.*`)
- Dosya işlemleri (`file.*`)
- JSON işlemleri (`json.*`)
- Rastgele sayı üretimi (`random.*`)

## Kullanım

AXON programını çalıştırmak için:

```bash
python run_axon.py dosya_adi.axon
```

Etkileşimli mod için:

```bash
python run_axon.py
```

## Örnek Programlar

`examples/` dizininde çeşitli örnek programlar bulunmaktadır:

- `examples/hello_world.axon`: Basit bir "Merhaba Dünya" programı
- `examples/factorial.axon`: Faktöriyel hesaplayan bir program
- `examples/fibonacci.axon`: Fibonacci dizisi üreten bir program
- `examples/oop.axon`: Nesne yönelimli programlama örneği
- `examples/memory.axon`: Bellek yönetimi örneği
- `examples/threading.axon`: İş parçacığı örneği
- `examples/debugging.axon`: Hata ayıklama özellikleri örneği
- `examples/stdlib_demo.axon`: Standart kütüphane fonksiyonları örneği
- `examples/simple_stdlib.axon`: Basit standart kütüphane örneği

## Dil Sözdizimi

### Değişken Tanımlama

```
x = 10
name = "AXON"
```

### Koşullu İfadeler

```
if x > 5
    print("x is greater than 5")
```

### Döngüler

```
while i < 10
    print(i)
    i = i + 1
```

### Fonksiyonlar

```
function factorial(n)
    if n <= 1
        return 1
    return n * factorial(n - 1)
```

### Bellek Yönetimi

```
memory allocate arr 10
memory write arr 0 42
value = memory read arr 0
memory free arr
```

### Hata Ayıklama

```
debug on
breakpoint set 15
# ... kod ...
debug off
```

### Standart Kütüphane Kullanımı

```
sqrt_result = math.sqrt(16)
upper_text = string.upper("hello")
current_time = time.now()
random_number = random.int(1, 10)
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 