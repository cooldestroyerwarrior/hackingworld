// CPP Program to check if a number can 
// be written as sum of three consecutive 
// integers. 
#include <bits/stdc++.h> 
using namespace std; 

// function to check if a number can be written as sum of 
// three consecutive integer. 
void checksum(int n) 
{ 
	// if n is 0 
	if (n == 0) { 
		cout << "-1 0 1" << endl; 
		return; 
	} 

	int inc; 

	// if n is positive, increment loop by 1. 
	if (n > 0) 
		inc = 1; 

	// if n is negative, decrement loop by 1. 
	else
		inc = -1; 

	// Running loop from 0 to n - 2 
	for (int i = 0; i <= n - 2; i += inc) { 

		// check if sum of three consecutive 
		// integer is equal to n. 
		if (i + i + 1 + i + 2 == n) { 
			cout << i << " " << i + 1 
				<< " " << i + 2; 
			return; 
		} 
	} 

	cout << "-1"; 
} 

// Driver Program 
int main() 
{ 
	int n = 6; 
	checksum(n); 
	return 0; 
} 
