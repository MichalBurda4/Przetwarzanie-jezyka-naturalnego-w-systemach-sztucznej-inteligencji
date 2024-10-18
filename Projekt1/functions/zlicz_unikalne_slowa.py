import os

# Funkcja do zliczania unikalnych słów
def zlicz_unikalne_slowa():
    folder_path = 'teksty'
    unikalne_slowa = set()

    for plik in os.listdir(folder_path):
        if plik.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, plik), 'r', encoding='utf-8') as f:
                    zawartosc = f.read()
                    slowa = zawartosc.lower().split()
                    unikalne_slowa.update(slowa)
            except FileNotFoundError:
                print(f"Plik {plik} nie został znaleziony.")

    return len(unikalne_slowa)
