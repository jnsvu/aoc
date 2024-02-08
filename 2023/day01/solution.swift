import Foundation

let url = URL(fileURLWithPath: "data.txt")
let lines = try String(contentsOf: url, encoding: .utf8).components(separatedBy: .newlines)

let valuesP1 = (1...9).map { String($0) }
let valuesP2 = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] + valuesP1
let reversedValuesP2 = valuesP2.map { String($0.reversed()) }
let numberMap = Dictionary(uniqueKeysWithValues: zip(valuesP2, valuesP1))

func indexOfSubstring(_ substring: String, in mainString: String) -> Int? {
  if let range = mainString.range(of: substring) {
    let index = mainString.distance(from: mainString.startIndex, to: range.lowerBound)
    return index
  } else {
    return nil
  }
}

func getFirstIndex(_ values: [String], _ line: String, substringClosure: (String) -> String) -> (
  Int?, String
)? {
  let sortedValues = values.map { (value) -> (Int?, String) in
    return (indexOfSubstring(substringClosure(value), in: line), value)
  }.sorted { ($0.0 ?? Int.max) < ($1.0 ?? Int.max) }

  return sortedValues.first
}

func resolve(_ values: [String]) -> Int {
  let results = lines.map { (line) -> Int in
    let reversedLine = String(line.reversed())
    let first = getFirstIndex(values, line) { $0 }
    let reversedFirst = getFirstIndex(values, reversedLine) { String($0.reversed()) }

    if let f = first?.1, let rf = reversedFirst?.1 {
      let numStr = (numberMap[f] ?? f) + (numberMap[rf] ?? rf)
      return Int(numStr) ?? 0
    } else {
      return 0
    }
  }

  return results.reduce(0, +)
}

print(resolve(valuesP1))
print(resolve(valuesP2))

