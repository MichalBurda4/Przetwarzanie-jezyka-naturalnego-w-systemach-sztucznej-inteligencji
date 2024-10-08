from flask import Flask, render_template, request
from collections import Counter
import os

app = Flask(__name__)

# Importujemy funkcje z plików w folderze functions
from functions.zlicz_slowa import zlicz_slowa
from functions.zlicz_unikalne_slowa import zlicz_unikalne_slowa
from functions.tabela_zipfa import tabela_zipfa
from functions.slowa_rozumienie import slowa_na_rozumienie_tekstu
from functions.graf import generuj_graf_polaczen_zipf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zlicz_slowa')
def zlicz_slowa_route():
    slowa = zlicz_slowa()
    return render_template('zlicz_slowa.html', slowa=slowa)

@app.route('/zlicz_unikalne_slowa')
def zlicz_unikalne_slowa_route():
    unikalne_slowa = zlicz_unikalne_slowa()
    return render_template('zlicz_unikalne_slowa.html', unikalne_slowa=unikalne_slowa)

@app.route('/tabela_zipfa')
def tabela_zipfa_route():
    tabela = tabela_zipfa()
    return render_template('tabela_zipfa.html', tabela=tabela)

@app.route('/rozumienie_tekstu', methods=['GET', 'POST'])
def rozumienie_tekstu_route():
    liczba_slow = 0
    slowa_rozumiane = 0
    wszystkie_slowa = 0
    procent = 10

    if request.method == 'POST':
        procent = int(request.form['procent'])
        liczba_slow, slowa_rozumiane, wszystkie_slowa = slowa_na_rozumienie_tekstu(procent)

    return render_template('rozumienie_tekstu.html', liczba_slow=liczba_slow, slowa_rozumiane=slowa_rozumiane, wszystkie_slowa=wszystkie_slowa, procent=procent)

@app.route('/graf_polaczen')
def graf_polaczen_route():
    generuj_graf_polaczen_zipf()  # Generowanie grafu
    return render_template('graf.html')  # Dodajemy nowy plik HTML dla grafu

if __name__ == '__main__':
    app.run(debug=True)
