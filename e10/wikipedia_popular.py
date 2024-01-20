import sys
import re
from pyspark.sql import SparkSession, functions as F, types

#  spark-submit wikipedia_popular.py pagecounts-1 output

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8)  # make sure we have Python 3.8+
assert spark.version >= '3.2'  # make sure we have Spark 3.2+

wikipedia_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('datetime', types.LongType()),
    types.StructField('bytes', types.LongType()),
])

def file2date(pathname):
    result = re.search('([0-9]{8}\-[0-9]{2})', pathname)
    return result.group(1)

def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema=wikipedia_schema, sep=' ').withColumn('filename', F.input_file_name())
    data = data.filter((F.col('language') == 'en') & (F.col('title') != 'Main_page') & ~F.col('title').startswith('Special:'))

    path2hour = F.udf(file2date, types.StringType())
    data = data.withColumn('date', path2hour(data['filename']))
    data = data.cache()

    most_viewed = data.groupBy("date").agg(F.max(data["datetime"]).alias("datetime"))
    result = data.join(most_viewed, on=["date", "datetime"], how="inner").select('date', 'title', 'datetime')
    result = result.sort('date', 'title')

    result.write.csv(out_directory + '-wikipedia', mode='overwrite')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: wikipedia_popular.py <input_directory> <output_directory>")
        sys.exit(1)
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
