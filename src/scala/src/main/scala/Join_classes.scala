package inequality_joins
import scala.collection.mutable.ListBuffer
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}

object IneqJoin {
  def pairs(arr1: List[Int], arr2: List[Int]): ListBuffer[Any] = {
    var output = new ListBuffer[Any]()
    for (i <- 0 until arr1.length;
        j <- 0 until arr2.length)
    output += ((arr1.apply(i), arr2.apply(j)))
    return output
  }

  case class Person(id: String, age: Int)
  case class Department(id: String, name: String)

  def list_to_df(): org.apache.spark.sql.DataFrame = {
    val conf = new SparkConf().setAppName("Spark Scala WordCount Example").setMaster("local[1]")
    val spark = SparkSession.builder().config(conf).appName("CsvExample").master("local").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    import spark.implicits._

    val department1 = Department("123456", "Computer Science")
    val department2 = Department("789012", "Mechanical Engineering")
    val department3 = Department("345678", "Theater and Drama")
    val department4 = Department("901234", "Indoor Recreation")
    val df: DataFrame = Seq(department1, department2, department3, department4).toDF
    return df
  } 
}