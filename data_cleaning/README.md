## Data Cleaning
Data cleaning is performed in New York University’s Peel node cluster, specifically within the Hadoop distributed file system, using Hadoop MapReduce. 

### Transfering files
* transfering file from local machine to Peel cluster

	`scp -r /Users/huzijia/Desktop/reddit zh1130@peel.hpc.nyu.edu:~/`

* transfer file from Peel cluster to HDFS

	`hdfs dfs -put /home/zh1130/reddit /user/zh1130`

### Preparation
* check your java version

	`java -version`

* check your yarn version

	`yarn classpath`

### MapReduce
* compile the mapper and reducer file

		javac -classpath \`yarn classpath\` -d . RedditMapper.java
		javac -classpath \`yarn classpath\` -d . RedditReducer.java 
		javac -classpath \`yarn classpath\`:. -d . Reddit.java

* create the .jar file
	
	`jar -cvf reddit.jar *.class`

* create a directory in HDFS
	
	`hdfs dfs -mkdir /user/zh1130/reddit`

* move the to-be-cleaned dataset into the directory we just created
	
	`hdfs dfs -put 500_Reddit_users_posts_labels.csv /user/zh1130/reddit`

* run MapReduce
	
	`hadoop jar reddit.jar Reddit /user/zh1130/reddit/500_Reddit_users_posts_labels.csv /user/zh1130/reddit/output`

### Output
* checkout the output
	
	`hdfs dfs -ls /user/zh1130/reddit/output`
	`hdfs dfs -cat /user/zh1130/reddit/output/part-m-00000`

* convert the output into a csv file
	
	`hdfs dfs -cat /user/zh1130/reddit/output/* | hdfs dfs -put - /user/zh1130/reddit/Reddit_Cleaned.csv`


### To move a file from HDFS to your laptop, there are two steps:
	
1. Open a terminal window, log into Peel, and get the file from HDFS into the local file system using this command: 
	
	`hdfs dfs -get /user/zh1130/reddit/Reddit_Cleaned.csv`
	
2. Open a second terminal window on your laptop and use scp (or sftp) to copy the file from Peel to your laptop (you can also use Fugu): 
		
	`scp zh1130@peel.hpc.nyu.edu:/home/zh1130/reddit/Reddit_Cleaned.csv .`
