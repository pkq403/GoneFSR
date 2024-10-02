/* gonert.c

   This file contains runtime support functions for the Gone language 
   as well as boot-strapping code related to getting the main program
   to run.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// __declspec(dllexport)      // Uncomment on Windows
void _print_int(int x) {
  printf("%i\n", x);
}

// __declspec(dllexport)     // Uncomment on Windows
void _print_float(double x) {
  printf("%f\n", x);
}


// __declspec(dllexport)    // Uncomment on Windows
void _print_byte(char c) {
  printf("%c", c);
  fflush(stdout);
}

/* Bootstrapping code for a stand-alone executable */
// ---- Custom built in functions  ----
void _print_string(char *c) {
  printf("%s", c);
  fflush(stdout);
}

void _coder_nlfsr(char *i, char *o) {
  execlp("coder_nlfsr", "coder_nlfsr", i, o, (char *) NULL);
  perror("[x] Error en ejecución de coder nlfsr");
}

void _decoder_nlfsr(char *i, char*o) {
  execlp("decoder_nlfsr", "decoder_nlfsr", i, o, (char *) NULL);
  perror("[x] Error en ejecución de coder nlfsr");
}
#ifdef NEED_MAIN
extern void __init(void);
extern int _gone_main(void);

int main() {
  __init();
  return _gone_main();
}
#endif
