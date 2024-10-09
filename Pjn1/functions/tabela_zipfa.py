import os
from collections import Counter

# Funkcja do tworzenia tabeli Zipfa
def tabela_zipfa():
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

    licznik_slow = Counter(slowa)
    slowa_posortowane = sorted(licznik_slow.items(), key=lambda x: x[1], reverse=True)
    stala_zipfa = slowa_posortowane[0][1]

    tabela = []
    for numer, (slowo, czestotliwosc) in enumerate(slowa_posortowane, start=1):
        ranga = round(stala_zipfa / czestotliwosc)
        iloczyn_zipfa = ranga * czestotliwosc
        tabela.append({
            'numer': numer,
            'slowo': slowo,
            'ranga': ranga,
            'czestotliwosc': czestotliwosc,
            'iloczyn_zipfa': iloczyn_zipfa
        })

    return tabela
