import java.util.List;
import java.util.ArrayList;
import java.util.Dictionary;
import java.util.Map;
import java.util.HashMap;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Autocorrect{
    final static Counter<String> dictionary = new Counter<>();
    static int total;
    static int max_word_length;

    public Autocorrect() throws Exception{
        instantiate_dict();
        max_word_length = find_max_word_length();
        ArrayList<String> result = viterbi_segment("supportiveOkay".toLowerCase());
        System.out.println(result.toString());

    }

    public static int find_max_word_length(){
        int max = Integer.MIN_VALUE;
        for(String word: dictionary.counts.keySet()){
            max = Math.max(max, word.length());
        }
        return max;
    }

    public static ArrayList<String> viterbi_segment(String text){
        ArrayList<Double> probs = new ArrayList<>();
        ArrayList<Integer> lasts = new ArrayList<>();
        probs.add(1.0);
        probs.add(0.0);
        lasts.add(0);

        for(int i = 1; i < text.length()+1; i++){
            for(int j = Math.max(0, i-max_word_length); j >= i; j--){
                double prob_k = Math.max(probs.get(j) * word_prob(text.substring(j,i+1)), j);
                int k = i;
                probs.add(prob_k);
                lasts.add(k);
            }
        }
        ArrayList<String> words = new ArrayList<>();
        int i = text.length();
        while(0 < i){
            words.add(text.substring(lasts.get(i), i));
            i = lasts.get(i);
        }
        ArrayList<String> output = new ArrayList<>();
        for(int k = words.size()-1; k >=0; k--){
            output.add(words.get(k));
        }
        return output;

    }

    public static List<String> words(String text){
        List<String> allwords = new ArrayList<>();
        Pattern pattern = Pattern.compile("[a-z]+");
        Matcher matcher = pattern.matcher(text.toLowerCase());
        while(matcher.find()){
            allwords.add(matcher.group());
        }
        return allwords;
    }

    public static void find_total(){
        total = dictionary.find_total();
    }

    public static double word_prob(String word){
        return dictionary.get(word) / total;
    }

    public static void instantiate_dict() throws Exception{
        BufferedReader br = new BufferedReader(new FileReader("bid.txt"));
        String input = "";
        Pattern pattern = Pattern.compile("[a-z]+");

		while ((input = br.readLine()) != null) {
            Matcher matcher = pattern.matcher(input.toLowerCase());
            while(matcher.find()){
                String word = matcher.group();
                dictionary.add(word);
            }
        }
        br.close();
    }

}

class Counter<T> {
    final Map<T, Integer> counts = new HashMap<>();

    public void add(T t) {
        counts.merge(t, 1, Integer::sum);
    }

    public int count(T t) {
        return counts.getOrDefault(t, 0);
    }

    public int get(T t){
        return counts.get(t);
    }

    public int find_total(){
        int total = 0;
        for(T t: this.counts.keySet()){
            total += this.counts.get(t);
        }
        return total;
    }
}