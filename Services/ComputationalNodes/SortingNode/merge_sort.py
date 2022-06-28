def merge_sort(arr):
    merge_sort_helper(arr)
    return arr

def merge_sort_helper(arr):
	if len(arr) > 1:

		m = len(arr) // 2

		left_copy = arr[:m]
		right_copy = arr[m:]

		merge_sort_helper(left_copy)
		merge_sort_helper(right_copy)

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
	# arr = [19, 27, 6, 8, 1]
	arr = [19, 27, 6, 8, 1, 23]
	print(merge_sort(arr))
 
