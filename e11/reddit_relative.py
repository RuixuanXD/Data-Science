import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types

# spark-submit --conf spark.dynamicAllocation.enabled=false --num-executors=8 reddit_relative.py reddit-1 output

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)

    # TODO
    comments = comments.cache()
    group = comments.groupBy('subreddit')
    average = group.agg(functions.avg('score').alias('avg_score'))
    average = average.filter(functions.col('avg_score') > 0)
    average = average.cache()
    #comments_avg = comments.join(average, on='subreddit')
    comments_avg = comments.join(average.hint('broadcast'), on='subreddit')
    comments_rel = comments_avg.withColumn("rel_score", functions.col("score") / functions.col("avg_score"))
    comments_rel_max = comments_rel.groupBy('subreddit').agg(functions.max('rel_score').alias('rel_score'))
    best_comment = group.agg(functions.max('score').alias('score'))
    best_comment = best_comment.cache()
    #best_comment = comments.join(best_comment, on=['score', 'subreddit'])
    best_comment = comments.join(best_comment.hint('broadcast'), on=['score', 'subreddit'])
    best_comment_rel = best_comment.join(comments_rel_max, on='subreddit').select('subreddit', 'author', 'rel_score')
    best_comment_rel.write.json(out_directory, mode='overwrite')


    #print(best_comments_rel)
    #print(average)


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    spark = SparkSession.builder.appName('Reddit Relative Scores').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory, out_directory)
