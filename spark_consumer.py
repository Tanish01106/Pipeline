from pyspark.sql import SparkSession 
from pyspark.sql.types import  StructField , IntegerType , StringType , FloatType , StructType , TimestampType
from pyspark.sql.functions import from_json


spark = SparkSession.builder \
    .appName("PipelineConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1")\
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "100.77.136.82:9092") \
    .option("subscribe", "login") \
    .option("startingOffsets", "earliest") \
    .load()

parsed_df=df.selectExpr("CAST(value as string) as json_data")

login_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("address", StringType(), True),
    StructField("ip_address", StringType(), True),
    StructField("device", StringType(), True),
    StructField("user_type", StringType(), True),
    StructField("login_status", IntegerType(), True),
    StructField("failed_attempts", IntegerType(), True),
    StructField("session_duration", FloatType(), True),
    StructField("login_time", TimestampType(), True),
    StructField("is_new_user", IntegerType(), True),
    StructField("loyalty_score", IntegerType(), True)
])

final_df= parsed_df.select(from_json(col=("json_data"),schema=login_schema).alias("data")).select("data.*")


query = final_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()
query.awaitTermination()