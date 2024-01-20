import string, re
import sys
from pyspark.sql import SparkSession, functions
from pyspark.sql.functions import split, explode, lower, col

#spark-submit wordcount.py wordcount-1 output

spark = SparkSession.builder.appName('wordcount').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8)
assert spark.version >= '3.2'

def main(input_dir, output_dir):
    lines = spark.read.text(input_dir)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
    words = lines.select(explode(split(lines.value, wordbreak)).alias('word'))
    #print(words)
    words = words.select(lower(col('word')).alias('word'))
    words = words.filter(words.word != '')
    word_count = words.groupBy('word').agg(functions.count('*').alias('count'))
    word_count = word_count.orderBy(['count', 'word'], ascending=[False, True])
    word_count.write.csv(output_dir, mode="overwrite")



if __name__ =='__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main(input_dir, output_dir)