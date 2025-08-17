

enum Weather{sunny, snowny}

void main() {
  String name = "quang pdhu";

  /**
   * If-else
   */
  if(name == "quang phu") {
    print("ok");
  } else if(name is int) {
    print("fuck");
  } 
  else {
    print("condition failed");
  }

  int numb = 2;

/**
 * Switch
 */
  switch(numb) {
      case 1:
        print("mot");
      case 2:
        print("2");
      default:
        print("default");
  }

  const weather = Weather.snowny;

  switch(weather) {
    case Weather.snowny:
      print("sunny");
    default:
      print("default");
  }



  /**
   * Assert: raise err when condition false
   */


  int age =25;

  // assert(age > 25, "age must less than 25");


  /**
   * Ternary: condition ? exprIfTrue : exprIfFlase
   */

  int high = 170;

  String x = high >= 170 ? "Tall" : "Low";

  print("x: $x");
}