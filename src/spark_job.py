from pyspark.sql import SparkSession
from scraper import scrape

def run_spark_scraper(urls):
    spark = SparkSession.builder \
        .appName("DistributedWebScraper") \
        .master("local[*]") \
        .getOrCreate()

    sc = spark.sparkContext
    url_rdd = sc.parallelize(urls)

    results = url_rdd.map(scrape).collect()
    for result in results:
        print(result)

    spark.stop()
