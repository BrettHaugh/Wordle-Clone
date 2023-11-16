package wordle;

import java.io.*;
import java.net.*;
import java.util.*;
import java.util.stream.Collectors;

public class WordleServer {
    private static final int PORT = 1234;
    //private static final String[] WORDS = {"apple", "banjo", "crane", "dwarf", "eagle"};
    private static String secretWord;
    private static ServerSocket serverSocket;

    public static void main(String[] args) throws IOException {
        serverSocket = new ServerSocket(PORT);
        System.out.println("Server is listening on port " + PORT);

        try (Socket socket = serverSocket.accept();
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            
            System.out.println("Client connected");
            selectRandomWord();
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                String feedback = generateFeedback(inputLine.toLowerCase());
                out.println(feedback);
            }
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen on port " + PORT);
            System.out.println(e.getMessage());
        } finally {
            serverSocket.close();
        }
    }

    private static void selectRandomWord() {
        Random rand = new Random();
        File file = new File("Words.txt");
        secretWord = new Scanner(file);
    }

    private static String generateFeedback(String guess) {
        if (guess.length() != secretWord.length()) {
            throw new IllegalArgumentException("Guess and secret word must be the same length.");
        }

        StringBuilder feedback = new StringBuilder("XXXXX");
        Map<Character, Long> letterFrequency = secretWord.chars().boxed()
                .collect(Collectors.groupingBy(
                        k -> (char) k.intValue(),
                        Collectors.counting()
                ));

        for (int i = 0; i < secretWord.length(); i++) {
            if (guess.charAt(i) == secretWord.charAt(i)) {
                feedback.setCharAt(i, 'G');
                letterFrequency.put(guess.charAt(i), letterFrequency.get(guess.charAt(i)) - 1);
            }
        }

        for (int i = 0; i < guess.length(); i++) {
            if (feedback.charAt(i) != 'G' && letterFrequency.getOrDefault(guess.charAt(i), 0L) > 0) {
                feedback.setCharAt(i, 'Y');
                letterFrequency.put(guess.charAt(i), letterFrequency.get(guess.charAt(i)) - 1);
            } else if (feedback.charAt(i) != 'G') {
                feedback.setCharAt(i, 'X');
            }
        }

        return feedback.toString();
    }
}
