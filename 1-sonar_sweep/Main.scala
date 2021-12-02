import scala.io.Source

object Main {

  def solve(it: Iterator[Int], size: Int = 1, step: Int = 1) =
    it.sliding(size + 1, step)
      .count(xs => xs.head < xs.last)

  def main(args: Array[String]): Unit = {
    val filename = "1.in"

    var it = Source.fromFile(filename).getLines.map((s: String) => s.toInt)
    println(solve(it, 1, 1))

    it = Source.fromFile(filename).getLines.map((s: String) => s.toInt)
    println(solve(it, 3, 1))
  }
}
