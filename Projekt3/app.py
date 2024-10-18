from flask import Flask, render_template, request
import os
import re

app = Flask(__name__)

# Słownik z czasownikami i ich formami
verbs = {
    "be": ["be", "was", "were", "been"],
    "have": ["have", "had", "had"],
    "do": ["do", "did", "done"],
    "say": ["say", "said", "said"],
    "go": ["go", "went", "gone"],
    "get": ["get", "got", "gotten"],
    "make": ["make", "made", "made"],
    "know": ["know", "knew", "known"],
    "think": ["think", "thought", "thought"],
    "take": ["take", "took", "taken"],
    "see": ["see", "saw", "seen"],
    "come": ["come", "came", "come"],
    "want": ["want", "wanted", "wanted"],
    "look": ["look", "looked", "looked"],
    "use": ["use", "used", "used"],
    "find": ["find", "found", "found"],
    "give": ["give", "gave", "given"],
    "tell": ["tell", "told", "told"],
    "work": ["work", "worked", "worked"],
    "call": ["call", "called", "called"],
    "try": ["try", "tried", "tried"],
    "ask": ["ask", "asked", "asked"],
    "need": ["need", "needed", "needed"],
    "feel": ["feel", "felt", "felt"],
    "become": ["become", "became", "become"],
    "leave": ["leave", "left", "left"],
    "put": ["put", "put", "put"],
    "mean": ["mean", "meant", "meant"],
    "keep": ["keep", "kept", "kept"],
    "let": ["let", "let", "let"],
    "begin": ["begin", "began", "begun"],
    "seem": ["seem", "seemed", "seemed"],
    "help": ["help", "helped", "helped"],
    "talk": ["talk", "talked", "talked"],
    "turn": ["turn", "turned", "turned"],
    "start": ["start", "started", "started"],
    "show": ["show", "showed", "shown"],
    "hear": ["hear", "heard", "heard"],
    "play": ["play", "played", "played"],
    "run": ["run", "ran", "run"],
    "move": ["move", "moved", "moved"],
    "like": ["like", "liked", "liked"],
    "live": ["live", "lived", "lived"],
    "believe": ["believe", "believed", "believed"],
    "hold": ["hold", "held", "held"],
    "bring": ["bring", "brought", "brought"],
    "happen": ["happen", "happened", "happened"],
    "write": ["write", "wrote", "written"],
    "provide": ["provide", "provided", "provided"],
    "sit": ["sit", "sat", "sat"],
    "stand": ["stand", "stood", "stood"],
    "lose": ["lose", "lost", "lost"],
    "pay": ["pay", "paid", "paid"],
    "meet": ["meet", "met", "met"],
    "include": ["include", "included", "included"],
    "continue": ["continue", "continued", "continued"],
    "set": ["set", "set", "set"],
    "learn": ["learn", "learned", "learned/learnt"],
    "change": ["change", "changed", "changed"],
    "lead": ["lead", "led", "led"],
    "understand": ["understand", "understood", "understood"],
    "watch": ["watch", "watched", "watched"],
    "follow": ["follow", "followed", "followed"],
    "eat": ["eat", "ate", "eaten"],
    "create": ["create", "created", "created"],
    "speak": ["speak", "spoke", "spoken"],
    "read": ["read", "read", "read"],
    "allow": ["allow", "allowed", "allowed"],
    "add": ["add", "added", "added"],
    "spend": ["spend", "spent", "spent"],
    "grow": ["grow", "grew", "grown"],
    "open": ["open", "opened", "opened"],
    "walk": ["walk", "walked", "walked"],
    "win": ["win", "won", "won"],
    "offer": ["offer", "offered", "offered"],
    "remember": ["remember", "remembered", "remembered"],
    "love": ["love", "loved", "loved"],
    "consider": ["consider", "considered", "considered"],
    "appear": ["appear", "appeared", "appeared"],
    "buy": ["buy", "bought", "bought"],
    "wait": ["wait", "waited", "waited"],
    "serve": ["serve", "served", "served"],
    "die": ["die", "died", "died"],
    "send": ["send", "sent", "sent"],
    "expect": ["expect", "expected", "expected"],
    "build": ["build", "built", "built"],
    "stay": ["stay", "stayed", "stayed"],
    "fall": ["fall", "fell", "fallen"],
    "cut": ["cut", "cut", "cut"],
    "reach": ["reach", "reached", "reached"],
    "kill": ["kill", "killed", "killed"],
    "remain": ["remain", "remained", "remained"],
    "suggest": ["suggest", "suggested", "suggested"],
    "raise": ["raise", "raised", "raised"],
    "pass": ["pass", "passed", "passed"],
    "sell": ["sell", "sold", "sold"],
    "require": ["require", "required", "required"],
    "report": ["report", "reported", "reported"],
    "decide": ["decide", "decided", "decided"],
    "drink": ["drink", "drank", "drunk"]
}

skip_words = {
    "a", "the", "in", "on", "at", "of", "for", "to", "with", "and", "but", "or", "so",
    "is", "was", "were", "are", "am", "been", "be", "it", "he", "me", "i",
    "that", "which", "who", "whom", "whose", "this", "those", "these", "there", "here",
    "by", "from", "over", "under", "between", "through", "into", "out", "up", "down", "about",
    "more", "less", "most", "least", "many", "few", "some", "any", "every", "each", "all", "no",
    "not", "only", "very", "just", "quite", "almost", "nearly", "too", "also", "enough", "still",
    "then", "now", "soon", "yesterday", "today", "tomorrow", "yes", "no", "you", "him", "its", "well", "her",
    "my", "had", "his", "em", "if", "youre", "lift", "dudley", "followed", "we",
    "perfect", "furious", "why", "easy", "full", "us", "won", "they", "their",
    "thats", "them", "never", "shooting", "strained", "right", "packed", "fire", "wear", "bargaining", "moved", "intolerable", "faster", "lookin", "refusing", "knocked", "free", "either", "spread", "scared", "fascinated", "fatiguing", "amazed", "while", "fairly", "giving", "liking", "brushed", "passing", "enjoying", "reined", "surrounded", "divided", "mentioned", "rather", "slammed", "explaining", "safely", "sounding", "lashing", "bothering", "blazing", "unwelcome", "flooding", "busy", "knew", "surplus", "startled", "overshadowed", "already", "displeased", "upset", "talked", "excitement", "conceited", "created", "stopped", "blow", "ruined", "renamed", "shock", "dribbling", "training", "chosen", "joining", "skimming", "clenched", "after", "shall", "ive", "until", "powerful", "proper", "hurrying", "liable", "because", "real", "saddled", "anxious", "off", "scraping", "makin", "dressed", "facing", "curious", "obliged", "convenient", "becoming", "awake", "stomping", "heavier", "coming", "extremely", "equally", "weirdos", "unbelievable", "strange", "away", "poured", "bobbing", "ripping", "fine", "rubbing", "lying", "recently", "drowned", "blinding", "nearest", "pale", "harnessed", "knocking", "looked", "prevented", "forced", "till", "remembering", "petted", "bound", "halfway", "growling", "mounted", "tied", "shaken", "drinking", "safeand", "kicked", "ringing", "crying", "thinned", "trusted", "troubled", "paid", "transformed", "drenched", "shattered", "reminded", "suffering", "resting", "wandered", "laughing", "injured", "kept", "galloping", "pushed", "drawn", "distracted", "raised", "smoking", "hiding", "seen", "surprised", "changeable", "used", "headless", "broken", "rooted", "shaking", "riding", "floating", "forgiven", "thrown",
    "worried", "stumped", "closer", "back", "remarkably", "ready", "terrible", "excited", "distinctly", "rummaged", "younger", "along", "called", "older", "frightened", "round", "dunno", "shocked", "murmured", "instead", "where", "flashy", "straight", "past", "burned", "upward", "pleased", "wildly", "puzzled", "awfully", "fit", "feeling", "simply", "will", "dumbfounded", "illtempered", "miffed", "even", "across", "intently", "likely", "stunned", "serious", "tearful", "taken", "forward", "though", "did", "handsome", "theyre", "suddenly", "horrified", "what", "convinced", "dreadfully", "behind", "cheerful", "desperate", "around", "strangely", "downhearted", "solid", "knows",
    "blemished", "turned", "jumped", "wooden", "cursed", "coalcarting", "drastically", "must", "lives",
    "your", "im", "bet", "didnt", "first", "blistering", "sure", "er", "next",
    "pointing", " oh", "img", "leading", "looking", "hoping", "shrilly", "little",
    "can", "heavily", "owing"


    # Przymiotniki
    "better", "best", "worse", "worst", "great", "small", "big", "large", "tiny", "huge",
    "good", "bad", "funny", "happy", "sad", "thankful", "thankfully", "careful", "carefully",
    "quick", "quickly", "slow", "slowly", "beautiful", "beautifully", "ugly", "strong", "weak",
    "new", "old", "young", "fast", "dangerous", "dangerously", "simple", "complex", "rich", "poor",
    "tall", "short", "wide", "narrow", "clean", "dirty", "expensive", "cheap", "soft", "hard",
    "bright", "dark", "calm", "nervous", "sharp", "blunt", "thin", "thick", "deep", "shallow",
    "dry", "wet", "hot", "cold", "warm", "cool", "strong", "weak", "safe", "unsafe", "happy",
    "unhappy", "loud", "quiet", "modern", "ancient", "recent", "early", "late", "famous", "unknown", "delicious",

    # Dodatkowe przymiotniki
    "heavy", "light", "polite", "rude", "kind", "cruel", "angry", "calm", "healthy", "sick",
    "interesting", "boring", "intelligent", "stupid", "brave", "cowardly", "friendly", "unfriendly",
    "noisy", "silent", "open", "closed", "bright", "dull", "lively", "dead", "beautiful", "ugly", "much"

    # Przysłówki
    "quickly", "slowly", "happily", "sadly", "easily", "barely", "hardly", "clearly", "badly",
    "carefully", "carelessly", "loudly", "quietly", "bravely", "cowardly", "gracefully", "angrily",
    "anxiously", "foolishly", "smartly", "sharply", "vividly", "warmly", "coldly", "nervously",
    "patiently", "impatiently", "calmly", "hastily", "excitedly", "enthusiastically", "politely",

    # Dodatkowe przysłówki
    "softly", "gently", "boldly", "weakly", "beautifully", "horribly", "terribly", "wonderfully",
    "naturally", "completely", "entirely", "partially", "slightly", "barely", "almost", "exactly",
    "perfectly", "briefly", "eagerly", "closely", "generously", "vigorously", "merrily", "reluctantly",

    # Czasowniki (dodane)
    "be", "have", "do", "say", "get", "make", "go", "know", "take", "see", "come", "think",
    "look", "want", "use", "find", "give", "tell", "work", "call", "try", "ask", "need",
    "feel", "become", "leave", "put", "mean", "keep", "let", "begin", "seem", "help",
    "talk", "turn", "start", "show", "hear", "play", "run", "move", "like", "live",
    "believe", "hold", "bring", "happen", "write", "provide", "sit", "stand", "lose",
    "pay", "meet", "include", "continue", "set", "learn", "change", "lead", "understand",
    "watch", "follow", "eat", "create", "speak", "read", "allow", "add", "spend", "grow",
    "open", "walk", "win", "offer", "remember", "love", "consider", "appear", "buy",
    "wait", "serve", "die", "send", "expect", "build", "stay", "fall", "cut", "reach",
    "kill", "remain", "suggest", "raise", "pass", "sell", "require", "report", "decide",
    "drink", "sleep", "hope", "gave", "disappear", "talking", "fresh", "greater", "together", "watched",
    "an", "before", "how", "our", "without", "as", "ill", "she", "hay", "'em", "much", "again", "said", "please",
    "mouthfuls", "since", "poorly", "processed", "when'", "when", "bit"

}


# Funkcja czyszcząca tekst z interpunkcji
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)  # Usuwa wszystkie znaki poza literami, cyframi i spacjami


# Funkcja, która wyszukuje słowa po czasownikach i pomija czasowniki spełniające warunki
def find_next_word_after_verb(text, verb_forms):
    text = remove_punctuation(text)  # Czyszczenie tekstu z interpunkcji
    words = text.split()  # Dzielenie tekstu na słowa
    results = []

    i = 0
    while i < len(words):
        word = words[i].lower()

        # Sprawdzanie, czy czasownik jest na końcu zdania
        if word in verb_forms:
            if i + 1 < len(words) and words[i + 1] == '.':
                i += 1  # Pomijamy czasownik, bo jest na końcu zdania
                continue

            # Sprawdzamy ile słów z listy skip_words występuje po czasowniku
            next_word_idx = i + 1
            skip_count = 0
            found_words = []

            while next_word_idx < len(words):
                next_word = words[next_word_idx].lower()
                if next_word in skip_words:
                    skip_count += 1
                else:
                    found_words.append(next_word)  # Zbieramy słowa, które nie są w skip_words
                    break
                next_word_idx += 1  # Pomijanie słów z listy skip_words


            if skip_count < 2:
                results.extend(found_words)

        i += 1

    return results

# Funkcja przeszukująca pliki w folderze i zbierająca wyniki
def search_in_books(folder_path, verb_forms):
    all_words = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                matches = find_next_word_after_verb(text, verb_forms)
                all_words.extend(matches)  # Dodanie znalezionych słów do listy
    return set(all_words)  # Zwraca zbiór unikalnych słów


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    verb1 = request.form['verb1'].lower()
    verb2 = request.form['verb2'].lower()

    if verb1 in verbs and verb2 in verbs:
        verb1_forms = verbs[verb1]  # Pobieranie form pierwszego czasownika
        verb2_forms = verbs[verb2]  # Pobieranie form drugiego czasownika

        folder_path = './teksty'  # Ścieżka do folderu z tekstami

        # Szukanie w plikach dla każdego czasownika
        words_after_verb1 = search_in_books(folder_path, verb1_forms)
        words_after_verb2 = search_in_books(folder_path, verb2_forms)

        # Liczenie sumy i części wspólnej
        union_words = words_after_verb1.union(words_after_verb2)
        intersection_words = words_after_verb1.intersection(words_after_verb2)

        result = {
            'words_after_verb1': list(words_after_verb1),
            'words_after_verb2': list(words_after_verb2),
            'union_words': list(union_words),
            'intersection_words': list(intersection_words)
        }
    else:
        result = {
            'words_after_verb1': [],
            'words_after_verb2': [],
            'union_words': [],
            'intersection_words': []
        }

    return result


if __name__ == '__main__':
    app.run(debug=True)