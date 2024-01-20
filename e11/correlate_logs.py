import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types, Row
import re
import math

#spark-submit correlate_logs.py nasa-logs-1

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred.
    Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        hostname = m.group(1)
        bytes_transferred = float(m.group(2))
        return Row(hostname=hostname, bytes_transferred=bytes_transferred)
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    log_lines = log_lines.map(line_to_row)
    log_lines = log_lines.filter(lambda row: row is not None)
    return log_lines


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    # TODO: calculate r.
    #print(logs)
    counts = logs.groupBy('hostname').count()
    counts = counts.cache()
    bytes = logs.groupBy('hostname').sum('bytes_transferred')
    bytes = bytes.cache()
    df = counts.join(bytes,'hostname')

    df = df.withColumnRenamed('count', 'xi')
    df = df.withColumnRenamed('sum(bytes_transferred)', 'yi')
    df = df.withColumn('xi_2', df['xi'] ** 2)
    df = df.withColumn('yi_2', df['yi'] ** 2)
    df = df.withColumn('xi_yi', df['xi'] * df['yi'])

    log = df.groupby().sum()
    n = df.count()
    log = log.first()
    xi = log[0]
    yi = log[1]
    xi_2 = log[2]
    yi_2 = log[3]
    xi_yi = log[4]

    r = (n * xi_yi - xi * yi) / math.sqrt((n * xi_2 - xi**2) * (n * yi_2 - yi**2))
    print(f"r = {r}\nr^2 = {r*r}")
    # Built-in function should get the same results.
    #print(totals.corr('count', 'bytes'))


if __name__=='__main__':
    in_directory = sys.argv[1]
    spark = SparkSession.builder.appName('correlate logs').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory)
