package org.example;

import java.util.ArrayList;

public class Words {

    public static ArrayList<Pronoun> pronouns = new ArrayList<>();
    public static ArrayList<Verb> verbs = new ArrayList<>();
    public static ArrayList<Noun> nouns = new ArrayList<>();
    public static ArrayList<String> adjectives = new ArrayList<>();

    public static void readWords() {

        ArrayList<String> words = new ArrayList<>();
        CSVReader CSVReader = new CSVReader();
        words = CSVReader.getWords("pronouns.txt");
        for (int i = 0; i < words.size(); i = i + 5) {
            Pronoun pronoun = new Pronoun();
            pronoun.FirstForm = words.get(i);
            pronoun.SecondForm = words.get(i + 1);
            pronoun.ThirdForm = words.get(i + 2);
            pronoun.FourthForm = words.get(i + 3);
            pronoun.FifthForm = words.get(i + 4);
            pronouns.add(pronoun);
        }

        words = CSVReader.getWords("verbs.txt");
        for (int i = 0; i < words.size(); i = i + 4) {
            Verb verb = new Verb();
            verb.FirstForm = words.get(i);
            verb.PresentSimple = words.get(i + 1);
            verb.SecondForm = words.get(i + 2);
            verb.ThirdForm = words.get(i + 3);
            verbs.add(verb);
        }
        words = CSVReader.getWords("nouns.txt");
        for (int i = 0; i < words.size(); i = i + 2) {
            Noun noun = new Noun();
            noun.singular = words.get(i);
            noun.plural = words.get(i + 1);
            nouns.add(noun);
        }

        adjectives = CSVReader.getWords("adjectives.txt");


    }

    public static void printWords(){
        System.out.println("pronouns:\n");
        for (Pronoun pronoun : pronouns) {
            System.out.print(pronoun.FirstForm + " " + pronoun.SecondForm + " " + pronoun.ThirdForm + " " + pronoun.FourthForm + " " + pronoun.FifthForm + "\n");
        }
        System.out.println("\nverbs:\n");
        for (Verb verb : verbs) {
            System.out.print(verb.FirstForm + " " + verb.PresentSimple + " " + verb.SecondForm + " " + verb.ThirdForm + "\n");
        }
        System.out.println("\nnouns:\n");
        for(Noun noun : nouns) {
            System.out.print(noun.singular + " " + noun.plural + "\n");
        }
        System.out.println("\nadjectives:\n");
        for(String adjective : adjectives) {
            System.out.println(adjective);
        }
    }

    public static Verb findVerb(String word) {
        for(Verb verb : verbs) {
            if(verb.FirstForm.equals(word) || verb.SecondForm.equals(word) || verb.ThirdForm.equals(word) || verb.PresentSimple.equals(word)) {
                return verb;
            }
        }
        return null;
    }

    public static Noun findNoun(String word) {
        for(Noun noun : nouns) {
            if(noun.singular.equals(word)) {
                return noun;
            }
        }
        return null;
    }

}