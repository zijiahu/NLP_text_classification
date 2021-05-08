import java.io.IOException;
import java.util.Arrays;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class RedditMapper extends Mapper<LongWritable, Text, Text, Text>{

  @Override
  public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{

    String[] line = value.toString().split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",-1);
    String userID = line[0];
    String post = line[1];
    String label = line[2];
    String newPost = "";

    // String p = "[a-zA-Z]+";
    String p = "([a-z]+)|([A-Z]{1}[a-z]*)|([A-Z]+)";
	  Pattern pattern = Pattern.compile(p);
  	Matcher matcher = pattern.matcher(post);
    	
    while(matcher.find()){
      String str = matcher.group();
      
      newPost += str + " ";
	  }

    context.write( new Text(" "), new Text(userID + "," + newPost + "," + label));
  }

}