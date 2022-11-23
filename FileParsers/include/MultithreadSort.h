#ifndef PETSYSPARSERS_MULTITHREADSORT_H
#define PETSYSPARSERS_MULTITHREADSORT_H

// CPP Program to implement merge sort using
// multi-threading
#include <iostream>
#include <ctime>
#include <vector>
#include <thread>


// merge function for merging two parts
void merge(std::vector<double> list, long low, long mid, long high) {
	auto *left  = new double[mid - low + 1];
	auto *right = new double[high - mid];
	
	// n1 is size of left part and n2 is size
	// of right part
	long n1 = mid - low + 1, n2 = high - mid, i, j;
	
	// storing values in left part
	for (i = 0; i < n1; i++)
		left[i] = list[i + low];
	
	// storing values in right part
	for (i = 0; i < n2; i++)
		right[i] = list[i + mid + 1];
	
	long k = low;
	i = j = 0;
	
	// merge left and right in ascending order
	while (i < n1 && j < n2) {
		if (left[i] <= right[j])
			list[k++] = left[i++];
		else
			list[k++] = right[j++];
	}
	
	// insert remaining values from left
	while (i < n1) {
		list[k++] = left[i++];
	}
	
	// insert remaining values from right
	while (j < n2) {
		list[k++] = right[j++];
	}
}

// merge sort function
//template<class T>
void merge_sort(const std::vector<double>& list, long low, long high) {
	// calculating mid point of array
	long mid = low + (high - low) / 2;
	if (low < high) {
		
		// calling first half
		merge_sort(list, low, mid);
		
		// calling second half
		merge_sort(list, mid + 1, high);
		
		// merging the two halves
		merge(list, low, mid, high);
	}
}

// thread function for multi-threading
void* merge_sort(const std::vector<double> list, int part, long MAX) {
	// which part out of 4 parts
	int thread_part = part++;
	
	// calculating low and high
	long low  = thread_part * (MAX / 4);
	long high = (thread_part + 1) * (MAX / 4) - 1;
	
	// evaluating mid point
	long mid = low + (high - low) / 2;
	if (low < high) {
		merge_sort(list, low, mid);
		merge_sort(list, mid + 1, high);
		merge(list, low, mid, high);
	}
}

// Driver Code
int main() {
	
	// number of threads
#define THREAD_MAX 4
	
	
	// array of size MAX
	std::vector<double> a;
	
	int part = 0;
	
	// generating random values in array
	for (int i = 0; i < 100; i++)
		a[i] = rand() % 100;
	
	// number of elements in array
	long MAX = a.size();
	
	// t1 and t2 for calculating time for
	// merge sort
	clock_t t1, t2;
	
	t1 = clock();
	
	std::vector<std::thread> threads;
	
	// creating 4 threads
	for (int i = 0; i < THREAD_MAX; i++) {
		std::thread newThread(merge_sort, a, part, MAX);
		threads.push_back(newThread);
	}
	
	
	// joining all 4 threads
	for (auto &thread: threads)
		thread.join();
	
	// merging the final 4 parts
	merge(a, 0, (MAX / 2 - 1) / 2, MAX / 2 - 1);
	merge(a, MAX / 2, MAX / 2 + (MAX - 1 - MAX / 2) / 2, MAX - 1);
	merge(a, 0, (MAX - 1) / 2, MAX - 1);
	
	t2 = clock();
	
	return 0;
}

#endif //PETSYSPARSERS_MULTITHREADSORT_H
