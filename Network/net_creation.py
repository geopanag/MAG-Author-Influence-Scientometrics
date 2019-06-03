from pyspark.sql.functions import count, avg

with open('names.txt', 'r') as f:
	filenames = [line.replace("\n", "") for line in f]

authors = spark.read.csv(''hdfs:///user/clean_paper_authors.txt', header=False)
authors = authors.selectExpr("_c0 as Paper", "_c1 as PapAuthor")


start = 0
step = 10
for batch in range(start, len(filenames), step):
	df1 = spark.read.csv(filenames[batch], header=False)
	concat = df1.selectExpr("_c0 as Author", "_c1 as Paper")
	for name in filenames[batch+1:batch+step]:
		df2 = spark.read.csv(name, header=False)
		concat = concat.union(df2.selectExpr("_c0 as Author", "_c1 as Paper"))
	print("Batch: ", batch)
	joined = authors.join(concat, "Paper")
	joined = joined.drop("Paper")
	joined.groupBy("Author", "PapAuthor").agg(count("*")).repartition(1).write.csv("hdfs:///user/citationsOutput/" + str(batch))