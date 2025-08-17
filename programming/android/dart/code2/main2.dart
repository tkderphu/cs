void main() {
  List<String> players = ["messi", "ronaldo"];

  // players.forEach((name) => {
  //   print(name)
  // });

  players.asMap().forEach((index, name) => {
    print("$index $name")
  });
}