import os
from collections import Counter

# Funkcja do zliczania słów potrzebnych do rozumienia tekstu
def slowa_na_rozumienie_tekstu(procent=10):
    folder_path = 'teksty'
    slowa = []

    for plik in os.listdir(folder_path):
        if plik.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, plik), 'r', encoding='utf-8') as f:
                    zawartosc = f.read()
                    slowa.extend(zawartosc.lower().split())
            except FileNotFoundError:
                print(f"Plik {plik} nie został znaleziony.")

    liczba_wszystkich_slow = len(slowa)
    licznik_slow = Counter(slowa)
    slowa_posortowane = sorted(licznik_slow.items(), key=lambda x: x[1], reverse=True)

    wymagane_slow = (procent / 100) * liczba_wszystkich_slow
    suma_wystapien = 0
    liczba_znanych_slow = 0

    for slowo, czestotliwosc in slowa_posortowane:
        suma_wystapien += czestotliwosc
        liczba_znanych_slow += 1
        if suma_wystapien >= wymagane_slow:
            break

    return liczba_znanych_slow, suma_wystapien, liczba_wszystkich_slow
