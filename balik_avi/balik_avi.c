#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define KART_SAYISI 24
#define OYUNCU_BASLANGIC 6
#define MAX_EL 30

void desteyi_hazirla(int deste[]);
void kartlari_dagit(int deste[], int *deste_indeksi,
                    int oyuncu_el[], int *oyuncu_kart_sayisi,
                    int bilgisayar_el[], int *bilgisayar_kart_sayisi);
void kartlari_yazdir(int el[], int adet);
void sirala(int el[], int adet);
int kart_sor(int el[], int adet, int hedef);
int kart_ver(int el[], int *adet, int hedef);
void kart_ekle(int el[], int *adet, int kart);
void kart_ekle_coklu(int el[], int *adet, int kart, int miktar);
int balik_kontrol(int el[], int *adet);

int main() {
    srand(time(NULL));

    int deste[KART_SAYISI];
    int deste_indeksi = 0;

    int oyuncu_el[MAX_EL];
    int bilgisayar_el[MAX_EL];
    int oyuncu_kart_sayisi = 0;
    int bilgisayar_kart_sayisi = 0;

    int oyuncu_balik = 0;
    int bilgisayar_balik = 0;
    int tur = 1;
    int oyuncu_sirasi = 1;

    desteyi_hazirla(deste);
    kartlari_dagit(deste, &deste_indeksi,
                   oyuncu_el, &oyuncu_kart_sayisi,
                   bilgisayar_el, &bilgisayar_kart_sayisi);

    printf("=== BALIK AVI KART OYUNU ===\n\n");
    printf("Kartlar dagitiliyor...\n\n");

    printf("Oyuncu kartlari: ");
    kartlari_yazdir(oyuncu_el, oyuncu_kart_sayisi);

    printf("Bilgisayar kartlari: [Gizli]\n");
    printf("Bilgisayar kart sayisi: %d\n", bilgisayar_kart_sayisi);
    printf("Masadaki kalan kart sayisi: %d\n\n", KART_SAYISI - deste_indeksi);

    while ((oyuncu_balik < 2 && bilgisayar_balik < 2) &&
           (deste_indeksi < KART_SAYISI)) {

        printf("--- TUR %d ---\n\n", tur);
        printf("Oyuncunun balik sayisi: %d | Bilgisayarin balik sayisi: %d\n",
               oyuncu_balik, bilgisayar_balik);

        if (oyuncu_sirasi) {
            int secim;
            int alinan;

            printf("Oyuncu kartlari: ");
            kartlari_yazdir(oyuncu_el, oyuncu_kart_sayisi);

            printf("Hangi kart numarasini sormak istiyorsunuz? ");
            scanf("%d", &secim);

            if (!kart_sor(oyuncu_el, oyuncu_kart_sayisi, secim)) {
                printf("Elinizde bu kart yok!\n");
                continue;
            }

            alinan = kart_ver(bilgisayar_el, &bilgisayar_kart_sayisi, secim);

            if (alinan > 0) {
                printf("\nBilgisayarda %d numarali kart(lar) var! ", secim);
                kart_ekle_coklu(oyuncu_el, &oyuncu_kart_sayisi, secim, alinan);
                printf("verildi.\n");

                if (balik_kontrol(oyuncu_el, &oyuncu_kart_sayisi)) {
                    oyuncu_balik++;
                }
            } else {
                printf("\nBilgisayarda %d numarali kart YOK.\n", secim);
                printf("Balik Avi ☹ Masadan bir kart cekiyorsunuz...\n");

                if (deste_indeksi < KART_SAYISI) {
                    int kart = deste[deste_indeksi++];
                    printf("Masadan cekilen kart: %d\n", kart);
                    kart_ekle(oyuncu_el, &oyuncu_kart_sayisi, kart);
                }

                oyuncu_sirasi = 0;
            }
        } else {
            int secim;
            int alinan;

            secim = bilgisayar_el[rand() % bilgisayar_kart_sayisi];
            printf("\nBilgisayar %d numarali karti soruyor...\n", secim);

            alinan = kart_ver(oyuncu_el, &oyuncu_kart_sayisi, secim);

            if (alinan > 0) {
                printf("Oyuncuda var! Bilgisayar aliyor.\n");
                kart_ekle_coklu(bilgisayar_el, &bilgisayar_kart_sayisi, secim, alinan);

                if (balik_kontrol(bilgisayar_el, &bilgisayar_kart_sayisi)) {
                    bilgisayar_balik++;
                }
            } else {
                printf("Oyuncuda YOK. Bilgisayar masadan cekiyor...\n");

                if (deste_indeksi < KART_SAYISI) {
                    kart_ekle(bilgisayar_el, &bilgisayar_kart_sayisi,
                              deste[deste_indeksi++]);
                }

                oyuncu_sirasi = 1;
            }
        }

        printf("\n");
        tur++;
    }

    printf("=== OYUN BITTI ===\n");

    if (oyuncu_balik > bilgisayar_balik)
        printf("Kazanan: OYUNCU!\n");
    else if (bilgisayar_balik > oyuncu_balik)
        printf("Kazanan: BILGISAYAR!\n");
    else
        printf("Sonuc: BERABERE!\n");

    printf("Oyuncunun toplam baligi: %d\n", oyuncu_balik);
    printf("Bilgisayarin toplam baligi: %d\n", bilgisayar_balik);
    printf("Masadaki kalan kart sayisi: %d\n", KART_SAYISI - deste_indeksi);

    return 0;
}

/* ================= FONKSIYONLAR ================= */

void desteyi_hazirla(int deste[]) {
    int i, j, k = 0;
    for (i = 1; i <= 6; i++) {
        for (j = 0; j < 4; j++) {
            deste[k++] = i;
        }
    }

    for (i = 0; i < KART_SAYISI; i++) {
        int r = rand() % KART_SAYISI;
        int tmp = deste[i];
        deste[i] = deste[r];
        deste[r] = tmp;
    }
}

void kartlari_dagit(int deste[], int *deste_indeksi,
                    int oyuncu_el[], int *oyuncu_kart_sayisi,
                    int bilgisayar_el[], int *bilgisayar_kart_sayisi) {
    int i;
    for (i = 0; i < OYUNCU_BASLANGIC; i++) {
        oyuncu_el[(*oyuncu_kart_sayisi)++] = deste[(*deste_indeksi)++];
        bilgisayar_el[(*bilgisayar_kart_sayisi)++] = deste[(*deste_indeksi)++];
    }
}

void kartlari_yazdir(int el[], int adet) {
    int i;
    for (i = 0; i < adet; i++) {
        printf("%d ", el[i]);
    }
    printf("\n");
}

int kart_sor(int el[], int adet, int hedef) {
    int i;
    for (i = 0; i < adet; i++) {
        if (el[i] == hedef) return 1;
    }
    return 0;
}

int kart_ver(int el[], int *adet, int hedef) {
    int i, j, sayac = 0;
    for (i = 0; i < *adet; ) {
        if (el[i] == hedef) {
            sayac++;
            for (j = i; j < *adet - 1; j++)
                el[j] = el[j + 1];
            (*adet)--;
        } else {
            i++;
        }
    }
    return sayac;
}

void kart_ekle(int el[], int *adet, int kart) {
    el[(*adet)++] = kart;
}

void kart_ekle_coklu(int el[], int *adet, int kart, int miktar) {
    int i;
    for (i = 0; i < miktar; i++) {
        el[(*adet)++] = kart;
    }
}

int balik_kontrol(int el[], int *adet) {
    int i, j, sayac;
    for (i = 0; i < *adet; i++) {
        sayac = 0;
        for (j = 0; j < *adet; j++) {
            if (el[j] == el[i]) sayac++;
        }
        if (sayac == 4) {
            printf("🎉 Tebrikler! %d numarali karttan 4 adet topladiniz. 1 balik kazandiniz.\n", el[i]);
            kart_ver(el, adet, el[i]);
            return 1;
        }
    }
    return 0;
}

