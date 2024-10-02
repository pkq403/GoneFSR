/**
 * Producto de listas PARALELIZADO con OpenMP, Implementacion en la cual cada combinacion ocupa un entero por lo que 0001, seria 1
 * autor: Pedro Castro
 */
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <omp.h>
#include <math.h>
#include <sys/time.h>
#include <time.h>


int* mult_by_itself(int len_V, int times);

int main(int argc, char* argv[])
{
    if (argc != 3) printf("[*] Help \n mal uso, usalo asi ./list_product.c <tam_lista> <repeats>\n");
    clock_t start, end;
    start = clock();
    mult_by_itself(atoi(argv[1]), atoi(argv[2]));
    end = clock();
	double diferencia = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("product en C: %.10f\n", diferencia);
}

/**
 * Multiply a vector by itself n times. 
 * Making all the combinations of the values possible
 * so if V = [0,1] and times = 2
 * It will return
 * {{0,0},{0,1},{1,0},{1,1}}
 *
 */
int* mult_by_itself(int len_V, int times)
{
    int real_rows = (int) pow(len_V, times);
    int num_combs_per_row = (int) pow(len_V, times - 1); // cols
    int virt_rows = len_V;
    int virt_cols = num_combs_per_row;
    int *R;
    int len_R = real_rows; // Total Length
    R = (int *) malloc(len_R * sizeof(int));
    int row_offset, col_offset;
#pragma omp 
{
    omp_set_num_threads(omp_get_max_threads());
    int *combs = (int *)malloc((times - 1) * sizeof(int));
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < len_V; i++) {
        for (int z = 0; z < times-1; z++) combs[z] = 0;
        for (int j = 0; j < num_combs_per_row; j++) {
            row_offset = i * virt_cols;
            col_offset = j;
            R[row_offset+col_offset] = i * (int) pow(10, times-1);
            for (int k = 1; k < times; k++) {
                R[row_offset + col_offset] += combs[k-1] * (int) pow(10, times - 1 - k);
            }
            for (int x = times - 1 -1; x >= 0; x--) {
                if (j % (int) pow(len_V, x) == 0) {
                        combs[x] = (combs[x] + 1) % len_V;
                }
            }
        }
    }
}
    /* Imprimir todas las combinaciones
    for (int i = 0; i < len_R; i++)
    {
        printf("%d, ", R[i]);
    }
    printf("\n"); */

    return R;
}
