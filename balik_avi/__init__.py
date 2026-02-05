import check50
import check50.c
import re
import os

# ============================================================
# BALIK AVI OYUNU - AUTOGRADING TEST DOSYASI
# Toplam: 100 Puan
# ============================================================

# Oyunun tamamlanması için yeterli input dizisi
# Oyun 2 balık veya 12 masadan kart çekene kadar sürer
# En fazla 24 tur olabilir, her turda 1-6 arası seçim yapılabilir
GAME_INPUTS = ["1", "2", "3", "4", "5", "6"] * 10  # 60 input - oyun kesin biter


def get_output(prog):
    """MockRunner'dan çıktıyı güvenli şekilde al."""
    # Programı doğrudan çalıştır (pattern matching olmadan)
    if not prog.executed:
        prog._decide_and_run()
    
    # stdout_text üzerinden çıktıyı al
    return prog.stdout_text if hasattr(prog, 'stdout_text') else ""


@check50.check()
def exists():
    """balik_avi.c dosyası mevcut mu? (0 Puan - Zorunlu)"""
    check50.exists("balik_avi.c")


@check50.check(exists, points=5)
def syntax_check():
    """Yasaklı syntax kontrolü - C99 öncesi stil (5 Puan)"""
    with open("balik_avi.c", "r", encoding="utf-8") as f:
        content = f.read()
    
    # C99 öncesi stil zorunluluğu: for(int i=0) tespiti
    if re.search(r"for\s*\(\s*int\s+", content):
        raise check50.Failure(
            "Eksi 5 Puan: For döngüsü içinde 'int' tanımlaması yapılmış.\n"
            "Değişkeni döngüden önce tanımlayınız (Örn: int i; for(i=0...))"
        )
    
    # while(int x=...) kontrolü
    if re.search(r"while\s*\(\s*int\s+", content):
        raise check50.Failure(
            "Eksi 5 Puan: While döngüsü içinde değişken tanımlaması yapılmış.\n"
            "Değişkeni döngüden önce tanımlayınız."
        )


@check50.check(exists, points=40)
def compiles():
    """Kod derleniyor mu? (40 Puan)"""
    check50.c.compile("balik_avi.c", lcs50=False)


@check50.check(compiles, points=10)
def test_start():
    """Oyun başlangıç mesajları doğru mu? (10 Puan)"""
    prog = check50.run("./balik_avi")
    
    # Oyunun bitmesi için yeterli input gönder
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    
    output = get_output(prog)
    
    errors = []
    
    # Kontrol 1: Oyun başlığı
    if "BALIK AVI" not in output.upper():
        errors.append("Oyun başlığı '=== BALIK AVI KART OYUNU ===' bulunamadı.")
    
    # Kontrol 2: Kartlar dağıtılıyor mesajı
    if "dagitiliyor" not in output.lower() and "dağıtılıyor" not in output.lower():
        errors.append("'Kartlar dağıtılıyor...' mesajı eksik.")
    
    # Kontrol 3: Oyuncu kartları gösteriliyor mu
    if "oyuncu kart" not in output.lower():
        errors.append("Oyuncunun kartları yazdırılmamış.")
    
    # Kontrol 4: Bilgisayar kart sayısı
    if "bilgisayar kart" not in output.lower():
        errors.append("Bilgisayar kart sayısı gösterilmemiş.")
    
    # Kontrol 5: Masadaki kart sayısı
    if "masa" not in output.lower():
        errors.append("Masadaki kart sayısı gösterilmemiş.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=20)
def test_game_loop():
    """Oyun döngüsü ve kullanıcı girişi doğru mu? (20 Puan)"""
    prog = check50.run("./balik_avi")
    
    # Oyunun bitmesi için yeterli input gönder
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    
    output = get_output(prog)
    
    errors = []
    
    # Kontrol 1: TUR bilgisi
    if "TUR" not in output.upper():
        errors.append("Tur bilgisi (Örn: --- TUR 1 ---) ekrana yazdırılmalı.")
    
    # Kontrol 2: Balık sayısı gösteriliyor mu
    if "balik sayisi" not in output.lower() and "balık sayısı" not in output.lower():
        errors.append("Her turda balık sayıları gösterilmeli.")
    
    # Kontrol 3: Hangi kart numarasını sormak istiyorsunuz?
    if "hangi kart" not in output.lower():
        errors.append("'Hangi kart numarasını sormak istiyorsunuz?' sorusu eksik.")
    
    # Kontrol 4: Bilgisayarın cevabı (var/yok/balık avı)
    found_positive = "var" in output.lower() or "verildi" in output.lower()
    found_negative = "yok" in output.lower() or "balik avi" in output.lower() or "balık avı" in output.lower()
    
    if not (found_positive or found_negative):
        errors.append("Bilgisayarın cevabı (Var!/Yok/Balık Avı) algılanamadı.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=25)
def test_full_flow():
    """Oyun akışı ve format kontrolü (25 Puan)"""
    prog = check50.run("./balik_avi")
    
    # Oyunun bitmesi için yeterli input gönder
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    
    try:
        output = get_output(prog)
        
    except Exception as e:
        raise check50.Failure(f"Oyun ardışık girişler sırasında hata verdi: {e}")
    
    errors = []
    
    # Kontrol 1: Masa kartları gösteriliyor mu
    if "masadaki" not in output.lower() and "masa" not in output.lower():
        errors.append("Masadaki kalan kart sayısı gösterilmeli.")
    
    # Kontrol 2: Bilgisayar sırası var mı
    if "bilgisayar" not in output.lower():
        errors.append("Bilgisayar sırası oyun akışında eksik.")
    
    # Kontrol 3: Çoklu tur oynandı mı
    tur_matches = re.findall(r"TUR\s*\d+", output.upper())
    if len(tur_matches) < 2:
        errors.append("Oyun birden fazla tur oynamamış. Sıra geçişleri çalışmıyor olabilir.")
    
    # Kontrol 4: Kart çekme mesajı var mı (masadan veya transfer)
    if "cekilen" not in output.lower() and "çekilen" not in output.lower() and \
       "verildi" not in output.lower() and "aliyor" not in output.lower():
        errors.append("Kart çekme/transfer mesajları eksik.")
    
    # Kontrol 5: Oyun sonu mesajı var mı
    if "oyun bitti" not in output.lower() and "kazanan" not in output.lower():
        errors.append("Oyun sonu mesajı (=== OYUN BİTTİ === veya Kazanan:) eksik.")
    
    if errors:
        raise check50.Failure("\n".join(errors))

