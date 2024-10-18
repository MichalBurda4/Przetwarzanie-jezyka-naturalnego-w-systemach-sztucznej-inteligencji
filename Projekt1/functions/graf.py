import os
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Użyj backendu bez GUI
import matplotlib.pyplot as plt
from collections import Counter

def generuj_graf_polaczen_zipf(folder_path='teksty', output_image='static/graf.png'):
    slowa = []

    # Odczyt plików z folderu
    for plik in os.listdir(folder_path):
        if plik.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, plik), 'r', encoding='utf-8') as f:
                    zawartosc = f.read()
                    slowa.extend(zawartosc.lower().split())  # Dodajemy słowa do listy
            except FileNotFoundError:
                print(f"Plik {plik} nie został znaleziony.")

    # Zliczanie unikalnych słów i ich częstotliwości
    licznik_slow = Counter(slowa)
    unikalne_slowa = list(licznik_slow.keys())[:500]  # Ograniczamy do pierwszych 500 unikalnych słów

    # Tworzenie grafu
    G = nx.Graph()

    # Iteracja przez pliki i zdania, aby zbudować graf połączeń
    for plik in os.listdir(folder_path):
        if plik.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, plik), 'r', encoding='utf-8') as f:
                    zdania = f.read().lower().split('.')  # Podział na zdania
                    for zdanie in zdania:
                        wyrazy = zdanie.split()  # Podział na wyrazy
                        # Dodajemy krawędzie między sąsiednimi wyrazami
                        for i in range(len(wyrazy) - 1):  # Iteracja do przedostatniego wyrazu
                            if wyrazy[i] in unikalne_slowa and wyrazy[i + 1] in unikalne_slowa:
                                G.add_edge(wyrazy[i], wyrazy[i + 1])  # Połączenie między sąsiednimi wyrazami

            except FileNotFoundError:
                print(f"Plik {plik} nie został znaleziony.")

    # Rysowanie grafu
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.5)  # Ustalanie pozycji węzłów
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=10, font_color='black')
    plt.title("Graf połączeń wyrazowych (do pierwszych 500 słów)")
    plt.savefig(output_image)
    plt.close()

# Wywołanie funkcji (można umieścić w aplikacji Flask lub wywołać niezależnie)
generuj_graf_polaczen_zipf()
