import scala.io.Source

object Main {

  def solve1(it: Iterator[String]) = {
    val (horizontal, depth) = it.foldLeft((0, 0)) {
      case ((horizontal, depth), command) =>
        command.split(" ") match {
          case Array("forward", x) =>
            (horizontal + x.toInt, depth)
          case Array("up", x) =>
            (horizontal, depth - x.toInt)
          case Array("down", x) =>
            (horizontal, depth + x.toInt)
        }
    }
    horizontal * depth
  }

  def solve2(it: Iterator[String]) = {
    val (horizontal, depth, _) = it.foldLeft((0, 0, 0)) {
      case ((horizontal, depth, aim), command) =>
        command.split(" ") match {
          case Array("forward", x) =>
            (horizontal + x.toInt, depth + aim * x.toInt, aim)
          case Array("up", x) =>
            (horizontal, depth, aim - x.toInt)
          case Array("down", x) =>
            (horizontal, depth, aim + x.toInt)
        }

    }
    horizontal * depth
  }

  def main(args: Array[String]): Unit = {
    var it = Source.fromFile("1.in").getLines
    println(solve1(it))

    it = Source.fromFile("1.in").getLines
    println(solve2(it))
  }
}
