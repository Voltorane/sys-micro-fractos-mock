# Python program for implementation of MergeSort
def mergeSort(arr):
	if len(arr) > 1:

		m = len(arr) // 2

		left_copy = arr[:m]
		right_copy = arr[m:]

		mergeSort(left_copy)
		mergeSort(right_copy)

		i = j = sort = 0

		# Copy data to temp arrays L[] and R[]
		while i < len(left_copy) and j < len(right_copy):
			if left_copy[i] < right_copy[j]:
				arr[sort] = left_copy[i]
				i += 1
			else:
				arr[sort] = right_copy[j]
				j += 1
			sort += 1

		# Checking if any element was left
		while i < len(left_copy):
			arr[sort] = left_copy[i]
			i += 1
			sort += 1

		while j < len(right_copy):
			arr[sort] = right_copy[j]
			j += 1
			sort += 1

if __name__ == '__main__':
	arr = [12, 11, 13, 5, 6, 7]
	# print(mergeSort(arr))
