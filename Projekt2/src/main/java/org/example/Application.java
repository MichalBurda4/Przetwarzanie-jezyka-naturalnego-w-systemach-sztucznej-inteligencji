package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class Application {
    public static void main(String[] args) {
        Words.readWords();

        JFrame frame = new JFrame("Generator zdań");
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));

        JComboBox<String> nounList = new JComboBox<>();
        JComboBox<String> verbList = new JComboBox<>();
        JComboBox<String> complementList = new JComboBox<>();
        JComboBox<String> tenseList = new JComboBox<>();
        JComboBox<String> numberList = new JComboBox<>();
        JComboBox<String> formList = new JComboBox<>();
        JLabel numberLabel = new JLabel("Wybierz Liczbę:");


        for (Pronoun pronoun : Words.pronouns) {
            nounList.addItem(pronoun.FirstForm);
        }
        for (Noun noun : Words.nouns) {
            nounList.addItem(noun.singular);
        }

        for (Verb verb : Words.verbs) {
            verbList.addItem(verb.FirstForm);
        }

        for (Noun noun : Words.nouns) {
            complementList.addItem(noun.singular);
        }

        tenseList.addItem("Present Simple");
        tenseList.addItem("Past Simple");
        tenseList.addItem("Past Perfect");
        numberList.addItem("Liczba pojedyncza");
        numberList.addItem("Liczba mnoga");
        formList.addItem("Tryb oznajmujacy");
        formList.addItem("Tryb przeczacy");
        formList.addItem("Tryb pytajacy");
        numberList.setVisible(false);
        numberLabel.setVisible(false);


        verbList.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String selectedVerb = (String) verbList.getSelectedItem();
                complementList.setVisible(true);
                if ("be".equals(selectedVerb)) {
                    for (String adjective : Words.adjectives) {
                        complementList.addItem(adjective);
                    }
                } else {
                    complementList.removeAllItems();
                    for (Noun noun : Words.nouns) {
                        complementList.addItem(noun.singular);
                    }
                }
            }
        });

        nounList.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String selectedNoun = (String) nounList.getSelectedItem();
                if (selectedNoun.equals("I") || selectedNoun.equals("You") || selectedNoun.equals("He") || selectedNoun.equals("She") || selectedNoun.equals("It") || selectedNoun.equals("We") || selectedNoun.equals("They")) {
                    numberList.setVisible(false);
                    numberLabel.setVisible(false);
                    numberList.setSelectedItem("Liczba pojedyncza");
                } else {
                    numberList.setVisible(true);
                    numberLabel.setVisible(true);

                }
            }
        });

        JButton button = new JButton("Generuj");
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String selectedNoun = (String) nounList.getSelectedItem();
                String selectedVerb = (String) verbList.getSelectedItem();
                String selectedAdjective = (String) complementList.getSelectedItem();
                String selectedTense = (String) tenseList.getSelectedItem();
                String selectedNumber = (String) numberList.getSelectedItem();
                String selectedForm = (String) formList.getSelectedItem();

                Noun selectedNounObject = Words.findNoun(selectedNoun);
                boolean heSheIt = selectedNoun.equals("He") || selectedNoun.equals("She") || selectedNoun.equals("It");
                boolean iYouWeThey = selectedNoun.equals("I") || selectedNoun.equals("You") || selectedNoun.equals("We") || selectedNoun.equals("They");
                boolean youWeThey = selectedNoun.equals("You") || selectedNoun.equals("We") || selectedNoun.equals("They");

                if (selectedNumber.equals("Liczba mnoga")) {
                    selectedNoun = selectedNounObject.plural;
                }
                if (selectedTense.equals("Present Simple") && !selectedVerb.equals("be") && (heSheIt || selectedNumber.equals("Liczba pojedyncza"))) {
                    Verb verb = Words.findVerb(selectedVerb);
                    selectedVerb = verb.PresentSimple;
                }
                if (selectedTense.equals("Past Simple") && !selectedVerb.equals("be")) {
                    Verb verb = Words.findVerb(selectedVerb);
                    selectedVerb = verb.SecondForm;
                }
                if (selectedTense.equals("Past Perfect")) {
                    Verb verb = Words.findVerb(selectedVerb);
                    selectedVerb = "had " + verb.ThirdForm;
                }
                if (selectedVerb.equals("be")) {
                    if (selectedTense.equals("Present Simple")) {
                        if (selectedNoun.equals("I")) {
                            selectedVerb = "am";
                        } else if ((heSheIt || selectedNumber.equals("Liczba pojedyncza")) && !iYouWeThey ) {
                            selectedVerb = "is";
                        } else if (youWeThey || selectedNumber.equals("Liczba mnoga")) {
                            selectedVerb = "are";
                        }
                    }
                    if (selectedTense.equals("Past Simple")) {
                        if ((heSheIt || selectedNoun.equals("I") || selectedNumber.equals("Liczba pojedyncza")) && !youWeThey) {
                            selectedVerb = "was";
                        } else if (youWeThey || selectedNumber.equals("Liczba mnoga")) {
                            selectedVerb = "were";
                        }
                    }
                }

                String message = "";
                if (selectedForm.equals("Tryb oznajmujacy")) {
                    message = selectedNoun + " " + selectedVerb + " " + selectedAdjective;
                } else if (selectedForm.equals("Tryb przeczacy")) {
                    if (selectedTense.equals("Present Simple")){
                        if(selectedVerb.equals("am")){
                            message = selectedNoun + "'m not " + selectedAdjective;
                        }
                        else if(selectedVerb.equals("are") || selectedVerb.equals("is")){
                            message = selectedNoun + " " + selectedVerb + "n't " + selectedAdjective;
                        }
                        else if((heSheIt || selectedNumber.equals("Liczba pojedyncza") && !iYouWeThey)){
                            Verb verb = Words.findVerb(selectedVerb);
                            message = selectedNoun + " doesn't " + verb.FirstForm + " " + selectedAdjective;
                        }
                        else{
                            message = selectedNoun + " don't " + selectedVerb + " " + selectedAdjective;
                        }
                    }
                    else if (selectedTense.equals("Past Simple")) {
                        if(selectedVerb.equals("was") || selectedVerb.equals("were")){
                            message = selectedNoun + " " + selectedVerb + "n't " + selectedAdjective;
                        }
                        else {
                            Verb verb = Words.findVerb(selectedVerb);
                            message = selectedNoun + " didn't " + verb.FirstForm + " " + selectedAdjective;
                        }
                    }
                    else if(selectedTense.equals("Past Perfect")) {
                        selectedVerb = selectedVerb.replaceAll("had ", "");
                        message = selectedNoun + " hadn't " + selectedVerb + " " + selectedAdjective;
                    }
                } else if (selectedForm.equals("Tryb pytajacy")) {
                    if (selectedTense.equals("Present Simple")){
                        if (selectedVerb.equals("am") || selectedVerb.equals("are") || selectedVerb.equals("is")) {
                            message = selectedVerb + " " + selectedNoun + " " + selectedAdjective + "?";
                        } else if ((heSheIt || selectedNumber.equals("Liczba pojedyncza") && !iYouWeThey)) {
                            Verb verb = Words.findVerb(selectedVerb);
                            message = "Does " + selectedNoun + " " + verb.FirstForm + " " + selectedAdjective + "?";
                        } else {
                            message = "Do " + selectedNoun + " " + selectedVerb + " " + selectedAdjective + "?";
                        }
                    }
                    else if (selectedTense.equals("Past Simple")){
                        if (selectedVerb.equals("was") || selectedVerb.equals("were")) {
                            message = selectedVerb + " " + selectedNoun + " " + selectedAdjective + "?";
                        }
                        else {
                            Verb verb = Words.findVerb(selectedVerb);
                            message = "Did " + selectedNoun + " " + verb.FirstForm + " " + selectedAdjective + "?";
                        }
                    }
                    else if (selectedTense.equals("Past Perfect")) {
                        selectedVerb = selectedVerb.replaceAll("had ", "");
                        message = "Had " + selectedNoun + " " + selectedVerb + " " + selectedAdjective + "?";
                    }

                }
                JOptionPane.showMessageDialog(frame, message);
            }
        });


        panel.add(new JLabel("Wybierz Podmiot:"));
        panel.add(nounList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(numberLabel);
        panel.add(numberList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(new JLabel("Wybierz Orzeczenie:"));
        panel.add(verbList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(new JLabel("Wybierz Dopełnienie:"));
        panel.add(complementList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(new JLabel("Wybierz Czas:"));
        panel.add(tenseList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(new JLabel("Wybierz Tryb Zdania:"));
        panel.add(formList);

        panel.add(Box.createRigidArea(new Dimension(0, 10)));
        panel.add(button);

        frame.getContentPane().add(panel);

        frame.setVisible(true);
    }
}
