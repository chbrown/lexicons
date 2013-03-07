package com.henrian

import com.codahale.jerkson.Json.parse
import scala.collection.JavaConverters._

object ScalaJson {
  def scalafy(entity: Any): Any = {
    // thanks: http://stackoverflow.com/questions/674713/converting-java-collection-into-scala-collection
    // import scala.collection.JavaConverters._ // asScala
    entity match {
      case obj: java.util.LinkedHashMap[_, _] =>
        obj.asScala.toMap.mapValues(scalafy)
      case arr: java.util.ArrayList[_] =>
        arr.asScala.toList.map(scalafy)
      case x => x
    }
  }

  def fromFile[A](path: String): A = {
    val raw = io.Source.fromFile(path).mkString
    scalafy(parse(raw)).asInstanceOf[A]
  }
}

object Liwc {
  val categories = List("funct", "pronoun", "ppron", "i", "we", "you", "shehe", "they", "ipron", "article", "verb", "auxverb", "past", "present", "future", "adverb", "preps", "conj", "negate", "quant", "number", "swear", "social", "family", "friend", "humans", "affect", "posemo", "negemo", "anx", "anger", "sad", "cogmech", "insight", "cause", "discrep", "tentat", "certain", "inhib", "incl", "excl", "percept", "see", "hear", "feel", "bio", "body", "health", "sexual", "ingest", "relativ", "motion", "space", "time", "work", "achieve", "leisure", "home", "money", "relig", "death", "assent", "nonfl", "filler")
  lazy val _trie = {
    ScalaJson.fromFile[Map[String, Any]]("/usr/local/data/liwc_2007.trie")
  }

  def _walk(token: String, index: Int, cursor: Map[String, Any]): List[String] = {
    if (cursor.contains("*")) {
      // assert cursor("*") = List[String]
      return cursor("*").asInstanceOf[List[String]]
    }
    else if (cursor.contains("$") && index == token.size) {
      return cursor("$").asInstanceOf[List[String]]
    }
    else if (index < token.size) {
      var letter = token(index).toString
      if (cursor.contains(letter)) {
        val nextCursor = cursor(letter).asInstanceOf[Map[String, Any]]
        return _walk(token, index + 1, nextCursor)
      }
    }
    return List()
  }

  // : Map[String, Int]
  def apply(tokens: Seq[String]) = {
    // returns a map from categories to counts
    val categories = tokens.map(_walk(_, 0, _trie))
    Map("Dic" -> categories.count(_.size > 0), "WC" -> tokens.size) ++
      categories.flatten.groupBy(identity).mapValues(_.size)
  }

  // : Seq[List[String]]
  def Tokenwise(tokens: Seq[String]) = {
    // returns a list of lists of categories, many of which might be empty
    tokens.map(_walk(_, 0, _trie))
  }
}
