import scala.io.Source
import scala.collection.mutable.HashMap

object Main {

  def count(it: Iterator[String]) = {
    val initial =
      it.next.toList.map((char) => MisraGries.init(char.toString.toInt))

    it.foldLeft(initial) {
      case (mgs, input) => {
        (mgs zip input.toList) map { case (mg, char) =>
          mg feed char.toString.toInt
          mg
        }
      }
    }.map(mg => mg.current.keySet.toArray.head)
  }

  def solve(it: Iterator[String]) = {
    val binaryString = count(it).mkString
    val gamma = Integer.parseInt(binaryString, 2)
    val epsilon =
      gamma ^ Integer.parseInt("".padTo(binaryString.length, "1").mkString, 2)
    gamma * epsilon
  }

  def main(args: Array[String]): Unit = {
    var it = Source.fromFile("1.in").getLines

    println(solve(it))
  }
}

object MisraGries {
  def init(value: Int, k: Int = 2) = {
    val mg = new MisraGries()
    mg feed value
    mg
  }
}

class MisraGries(k: Int = 2) {
  val a: HashMap[Int, Int] = new HashMap()

  def feed(str: Int): MisraGries = {
    if (a contains str)
      a(str) = (((a(str)) + 1))
    else if (a.size < k - 1)
      a(str) = (1)
    else
      a.iterator.foreach {
        case (key, value) => {
          a(key) = value - 1
          if (value == 0)
            a remove key
        }
      }
    this
  }

  def current = a
}
