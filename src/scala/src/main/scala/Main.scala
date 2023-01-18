package inequality_joins
import scala.collection.mutable.ListBuffer
import scala.util.Random
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{Row, DataFrame, Dataset, SparkSession}
import org.apache.spark.sql.types.{IntegerType, StructField, StructType}

object Main {
  def df(rows: Int, cols: Int, spark: SparkSession): DataFrame = {
         val data = (1 to rows).map(_ => Seq.fill(cols)(Random.nextInt(100)))
         val colNames = (1 to cols).mkString(",")
         val sch = StructType(colNames.split(",").map(fieldName => StructField(fieldName, IntegerType, true)))
         val rdd = spark.sparkContext.parallelize(data.map(x => Row(x:_*)))
         val df = spark.sqlContext.createDataFrame(rdd, sch)
         return df
         //spark.stop()
    }
    
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Spark Scala WordCount Example").setMaster("local[1]")
    val spark = SparkSession.builder().config(conf).appName("CsvExample").master("local").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    import spark.implicits._

    val n_tuples = 100
    val predicate_len = 3

    val ineqjoin = IneqJoin;
    val output: DataFrame = df(100, 3, spark)
      //val output: org.apache.spark.rdd.RDD[List[Int]] = df
    println(output.show(10))
  }
}