package inequality_joins
import scala.collection.mutable.ListBuffer

object Main {
    def main(args: Array[String]): Unit = {
      val arr1 = List(1, 2, 3)
      val arr2 = List(4, 5)

      val ineqjoin = IneqJoin;
      val output: org.apache.spark.sql.DataFrame = ineqjoin.list_to_df();
      output.show(10);
    }
}