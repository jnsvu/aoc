import Foundation

let url = URL(fileURLWithPath: "data.txt")
let lines = try String(contentsOf: url, encoding: .utf8).components(separatedBy: .newlines)

struct Gems {
  let blue: Int
  let red: Int
  let green: Int
}

let bluePattern = #/(\d+ blue)/#
let redPattern = #/(\d+ red)/#
let greenPattern = #/(\d+ green)/#

func parseGems(_ pattern: Regex<(Substring, Substring)>, _ str: String) -> Int {
  let parts = str.firstMatch(of: pattern)?.output.0.components(separatedBy: " ")
  let strInt = parts?.first ?? "0"
  return Int(strInt) ?? 0
}

func parseLine(_ line: String) -> [Gems] {
  return line.split(separator: ":")[1].split(separator: ";").map {
    String($0)
  }.map { (str: String) -> Gems in
    let blue = parseGems(bluePattern, str)
    let red = parseGems(redPattern, str)
    let green = parseGems(greenPattern, str)
    return Gems(blue: blue, red: red, green: green)
  }

}

func resolve() -> Int {
  let results = lines.enumerated().map {
    let gameId = $0.offset + 1
    let gems = parseLine($0.element)
    let isBlue = gems.contains { $0.blue > 14 }
    let isRed = gems.contains { $0.red > 12 }
    let isGreen = gems.contains { $0.green > 13 }

    return (!isBlue && !isGreen && !isRed) ? gameId : 0
  }.reduce(0, +)

  return results
}

func resolveP2() -> Int {
  let results = lines.enumerated().map {
    let gameId = $0.offset + 1
    let gems = parseLine($0.element)
    let minBlue = gems.max { $0.blue < $1.blue }?.blue ?? 0
    let minRed = gems.max { $0.red < $1.red }?.red ?? 0
    let minGreen = gems.max { $0.green < $1.green }?.green ?? 0

    return minBlue * minRed * minGreen
  }.reduce(0, +)

  return results
}

print(resolve())
print(resolveP2())
