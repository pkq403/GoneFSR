// Function definition
func add(x int, y int) int {
     return x+y;
}

// Function definition
func fibonacci(n int) int {
     print MAXFIB; // should be ok
     print x; // error?
     if n > 1 {
        return fibonacci(n-1) + fibonacci(n-2);     // Return
     } else {
        return 1;    // Return
     }
     return 2;
 }

 const MAXFIB = 5;       // Global

 // Function definition (entry point)
 func main() int {
      print y;
      print add(2,3);            // Function call
      var n int = 0;
      while n < MAXFIB {
          print fibonacci(n);    // Function call
          n = n + 1;
      }
      return 0;
 }
