package org.example;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;

public class CSVReader {

    public ArrayList<String> getWords(String fileName) {
        ArrayList<String> words = new ArrayList<>();
        File file = new File(fileName);
        try(BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while((line = br.readLine()) != null){
                String[] lineWords = line.split(",");
                words.addAll(Arrays.asList(lineWords));

            }
        } catch (IOException e) {}
        return words;
    }

}
