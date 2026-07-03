from pyspark.sql import SparkSession
import json
spark = SparkSession.builder \
    .appName("PipelineConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "100.77.136.82:9092") \
    .option("subscribe", "login,order,payment") \
    .option("startingOffsets", "earliest") \
    .load()

query = json_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()