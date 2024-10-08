import os

# Funkcja do zliczania wszystkich słów w plikach
def zlicz_slowa():
    folder_path = 'teksty'
    liczba_slow = 0

    for plik in os.listdir(folder_path):
        if plik.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, plik), 'r', encoding='utf-8') as f:
                    zawartosc = f.read()
                    slowa = zawartosc.split()
                    liczba_slow += len(slowa)
            except FileNotFoundError:
                print(f"Plik {plik} nie został znaleziony.")

    return liczba_slow
