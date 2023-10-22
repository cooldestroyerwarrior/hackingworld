#include <iostream>
#include <ctime>
#include <cstdlib>
#include <chrono>
using namespace std;
using namespace std::chrono;

#define size 25000

int main()
{
    int i, j, a[size], t ,min;
    high_resolution_clock::time_point start, end;
    duration<double, std::micro> cpu_microseconds;

    // Fill the array with random integers
    for (i = 0; i < size; i++)
        a[i] = rand() % 100;

    start = high_resolution_clock::now();

    for (i = 0; i < size; i++)
        a[i] = rand() % 100;

    start = high_resolution_clock::now();
    for (i = 0; i < (size - 1); i++)
    {
        min = i;
        for (j = i + 1; j < size; j++)
        {
            if (a[min] > a[j])
            {
                min = j;
            }
        }
        if (min != i)
        {
            t = a[i];
            a[i] = a[min];
            a[min] = t;
        }
    }
    end = high_resolution_clock::now();
    cpu_microseconds = duration_cast<duration<double, std::micro>>(end - start);

    cout << "\nSELECTION SORT  ";
    cout << "\nTime is " << cpu_microseconds.count() << " microseconds" << endl;
    cout << "\nSorted data  \n";

    for (i = 0; i < size; i++)
        cout << a[i] << " ";

    return 0;
}
