# Makwa — implementacja biblioteki algorytmu przechowywania haseł

Projekt realizowany w ramach przedmiotu **Bezpieczeństwo Danych (BDAN)** na Politechnice Warszawskiej (WEiTI).

**Autorzy:** Maciej Krupa, Wojciech Sondej

## Opis

Implementacja algorytmu **Makwa** — funkcji przechowywania haseł opartej na trudności faktoryzacji dużych liczb całkowitych (liczby Bluma). Projekt zrealizowany na podstawie oficjalnej dokumentacji algorytmu.

Makwa jest algorytmem zaprojektowanym tak, aby obliczanie hashy było kosztowne obliczeniowo — co utrudnia ataki brute-force i słownikowe. Wspiera dwa tryby obliczania:

- **Normal path** — bez znajomości faktoryzacji modułu N (wolniejszy)
- **Quick path** — ze znajomością czynników pierwszych p i q, z wykorzystaniem Chińskiego Twierdzenia o Resztach (szybszy)

## Struktura projektu

```
src/
├── Makwa.py                     # Główna implementacja algorytmu Makwa
├── ArytmetykaModularna.py       # Normal path i Quick path (CRT), NWD, odwrotność modularna
├── KDF.py                       # Key Derivation Function (HMAC_DRBG + SHA-256)
├── TestDictionaryAttack.py      # Test odporności na atak słownikowy
├── TestyDlaWektorówTestowych.py # Testy zgodności z oficjalnymi wektorami testowymi
├── hashesNormal.txt             # Wyniki hashowania — tryb normalny
├── hashesQuick.txt              # Wyniki hashowania — tryb szybki (CRT)
└── passwords.txt                # Dane testowe
```

## Wymagania

- Python 3.x
- Brak zewnętrznych bibliotek — wyłącznie biblioteka standardowa (`hashlib`, `hmac`, `secrets`)


## Testy

```bash
# Testy zgodności z oficjalnymi wektorami testowymi algorytmu Makwa
python TestyDlaWektorówTestowych.py

# Test odporności na atak słownikowy
python TestDictionaryAttack.py
```

## Algorytm

### Format modułu
Makwa używa modułu Bluma — iloczynu dwóch liczb pierwszych p i q, gdzie `p ≡ 3 (mod 4)` i `q ≡ 3 (mod 4)`.

### KDF
Funkcja wyprowadzania klucza oparta na **HMAC_DRBG z SHA-256** — używana zarówno do pre-hashingu wiadomości jak i post-hashingu wyniku.

### Dwa tryby obliczeń

**Normal path** — oblicza `x^(2^mcost) mod N` wprost za pomocą szybkiego potęgowania:
```
x^(2^roundNumber) mod N
```

**Quick path** — wykorzystuje Chińskie Twierdzenie o Resztach (CRT) dla przyspieszenia obliczeń przy znajomości p i q:
```
e_p = 2^roundNumber mod (p-1)
e_q = 2^roundNumber mod (q-1)
wynik = CRT(x^e_p mod p, x^e_q mod q)
```

### Parametry hashowania
- `mcost` — koszt obliczeniowy (liczba iteracji)
- `preHashing` — opcjonalne wstępne hashowanie wiadomości (KDF, 64 bajty)
- `postHashingLength` — długość wyjścia po końcowym hashowaniu KDF (`-1` = brak)
- `salt` — 16 losowych bajtów generowanych przez `secrets.token_bytes(16)`

## Źródła

- Dokumentacja algorytmu Makwa: https://www.bolet.org/makwa/
