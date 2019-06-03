var authors = spark.read.format("csv").option("header", "false").load("hdfs:///user/clean_paper_authors.txt")
authors = authors.selectExpr("_c0 as Paper", "_c1 as Author")
# tmp1 = authors.group_by(Paper).count(Authors)
# tmp1 is Paper1, 3 ; Paper2, 10 etc... paper and number of coauthors
# reverse second column (1/3, 1/10)
# authors = authors.join(tmp1,"Paper") # gives Paper, AuthorCount, Author 
var references = spark.read.format("csv").option("header", "false").load("hdfs:///user/references.txt")
references = references.selectExpr("_c0 as Paper", "_c1 as Reference")
var tmp = references.join(authors, "Paper")
tmp = tmp.drop("Paper")


tmp = tmp.selectExpr("Author as AuthorID", "Reference as ReferencedPaper")
tmp = tmp.orderBy($"AuthorID")
tmp.write.format("csv").save("hdfs:///user/sorted.csv")
