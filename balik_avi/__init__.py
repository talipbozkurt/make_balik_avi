import check50
import check50.c
import re
import os

# ============================================================
# BALIK AVI OYUNU - AUTOGRADING TEST DOSYASI
# Toplam: 100 Puan
# Deterministik Test: SEED=49
# 
# SEED=49 Beklenen Değerler:
# - Başlangıç kartları: 2 1 1 4 5 2
# - Tur 13: 2 numaralı karttan balık
# - Tur 14: 1 numaralı karttan balık  
# - Sonuç: OYUNCU 2 balık ile kazanır
# ============================================================

# Input dizisi - Seed=49 için optimize edilmiş
# [2,2,2,2,2,1,5] → bu sırayla sorarak oyuncu 2 balık yapar
GAME_INPUTS = ["2", "2", "2", "2", "2", "1", "5"] + ["1"] * 10


def get_output(prog):
    """MockRunner'dan çıktıyı güvenli şekilde al."""
    if not prog.executed:
        prog._decide_and_run()
    return prog.stdout_text if hasattr(prog, 'stdout_text') else ""


@check50.check()
def exists():
    """balik_avi.c dosyası mevcut mu? (0 Puan - Zorunlu)"""
    check50.exists("balik_avi.c")


@check50.check(exists, points=5)
def syntax_check():
    """C99 öncesi syntax kontrolü (5 Puan)"""
    with open("balik_avi.c", "r", encoding="utf-8") as f:
        content = f.read()
    
    if re.search(r"for\s*\(\s*int\s+", content):
        raise check50.Failure(
            "For döngüsü içinde 'int' tanımlaması yapılmış.\n"
            "Değişkeni döngüden önce tanımlayınız."
        )


@check50.check(exists, points=40)
def compiles():
    """Kod derleniyor mu? (40 Puan)"""
    check50.c.compile("balik_avi.c", lcs50=False)


@check50.check(compiles, points=10)
def test_start():
    """Başlangıç durumu - SEED=49 kontrolü (10 Puan)"""
    prog = check50.run("./balik_avi")
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    output = get_output(prog)
    
    errors = []
    
    # SEED=49 ile başlangıç kartları: 2 1 1 4 5 2
    if "Oyuncu kartlari: 2 1 1 4 5 2" not in output[output.index("Oyuncu"):output[output.index("Oyuncu"):].index("\n")]:
        errors.append("SEED=49 ile başlangıç kartları '2 1 1 4 5 2' olmalı.")
    
    # Masadaki kart sayısı: 12
    if "Masadaki kalan kart sayisi: 12" not in output:
        errors.append("Başlangıçta masada 12 kart olmalı.")
    
    # Bilgisayar kart sayısı: 6
    if "Bilgisayar kart sayisi: 6" not in output:
        errors.append("Başlangıçta bilgisayarda 6 kart olmalı.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=15)
def test_game_loop():
    """Oyun döngüsü ve tur mekaniği (15 Puan)"""
    prog = check50.run("./balik_avi")
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    output = get_output(prog)
    
    errors = []
    
    # TUR 1 kontrolü
    if "--- TUR 1 ---" not in output:
        errors.append("TUR 1 gösterilmemiş.")
    
    # Balık sayısı gösterimi
    if "Oyuncunun balik sayisi: 0 | Bilgisayarin balik sayisi: 0" not in output:
        errors.append("Başlangıçta balık sayıları 0|0 olmalı.")
    
    # Kart sorma prompt'u
    if "Hangi kart numarasini sormak istiyorsunuz?" not in output:
        errors.append("Kart sorma prompt'u eksik.")
    
    # Bilgisayar sırası
    if "Bilgisayar" not in output or "karti soruyor" not in output:
        errors.append("Bilgisayar sırası mesajı eksik.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=15)
def test_card_transfer():
    """Kart transferi ve Balık Avı mekaniği (15 Puan)"""
    prog = check50.run("./balik_avi")
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    output = get_output(prog)
    
    errors = []
    
    # SEED=49, TUR 1: Bilgisayarda 2 yok
    if "Bilgisayarda 2 numarali kart YOK" not in output:
        errors.append("TUR 1'de '2 numaralı kart YOK' mesajı eksik.")
    
    
    # Balık Avı mesajı
    if "Balik Avi" not in output:
        errors.append("Balık Avı mesajı eksik.")
    
    # Masadan kart çekme
    if "Masadan cekilen kart:" not in output:
        errors.append("Masadan çekilen kart mesajı eksik.")
    
    # Kart var durumu (TUR 13'te bilgisayarda 1 var)
    if "kart(lar) var! verildi" not in output:
        errors.append("Kart transfer mesajı ('var! verildi') bulunamadı.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=15)
def test_fish_creation():
    """Balık oluşturma - 4 aynı kart (15 Puan)"""
    prog = check50.run("./balik_avi")
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    output = get_output(prog)
    
    errors = []
    
    # SEED=49: TUR 13'te 2 numaralı karttan balık
    if "Tebrikler! 2 numarali karttan 4 adet topladiniz" not in output:
        errors.append("2 numaralı karttan balık oluşturma mesajı eksik.")
    
    # SEED=49: TUR 14'te 1 numaralı karttan balık
    if "Tebrikler! 1 numarali karttan 4 adet topladiniz" not in output:
        errors.append("1 numaralı karttan balık oluşturma mesajı eksik.")
    
    # Balık sayısı artışı - 1. balık sonrası
    if "Oyuncunun balik sayisi: 1" not in output:
        errors.append("1. balık sonrası sayı artmamış.")
    
    if errors:
        raise check50.Failure("\n".join(errors))


@check50.check(compiles, points=0)
def test_game_end():
    """Oyun sonu kontrolü - SEED=49 (Bonus - 0 Puan)"""
    prog = check50.run("./balik_avi")
    for inp in GAME_INPUTS:
        prog.stdin(inp)
    output = get_output(prog)
    
    errors = []
    
    # SEED=49: Oyuncu 2 balık ile kazanır
    if "=== OYUN BITTI ===" not in output:
        errors.append("Oyun sonu mesajı eksik.")
    
    if "Kazanan: OYUNCU!" not in output:
        errors.append("SEED=49 ile oyuncu kazanmalı.")
    
    if "Oyuncunun toplam baligi: 2" not in output:
        errors.append("Oyuncunun toplam balığı 2 olmalı.")
    
    if "Bilgisayarin toplam baligi: 0" not in output:
        errors.append("Bilgisayarın toplam balığı 0 olmalı.")
    
    if "Masadaki kalan kart sayisi: 2" not in output:
        errors.append("Masada 2 kart kalmalı.")
    
    if errors:
        raise check50.Failure("\n".join(errors))
