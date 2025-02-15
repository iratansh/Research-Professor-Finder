class QuickSort:
    def __init__(self, array):
        self.array = array
        
    def partition(self, low, high):

        mid = (low + high) // 2
        pivot_candidates = [
            (low, self.array[low][1]),
            (mid, self.array[mid][1]),
            (high, self.array[high][1])
        ]
        pivot_idx = sorted(pivot_candidates, key=lambda x: x[1])[1][0]
        self.array[pivot_idx], self.array[high] = self.array[high], self.array[pivot_idx]
        pivot = self.array[high][1]
        
        i = low - 1
        
        for j in range(low, high):
            if self.array[j][1] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1
    
    def insertion_sort(self, low, high):
        for i in range(low + 1, high + 1):
            key = self.array[i]
            j = i - 1
            while j >= low and self.array[j][1] > key[1]:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key

    def quicksort(self, low, high):
        while low < high:
            if high - low < 10:
                self.insertion_sort(low, high)
                return
                
            pivot = self.partition(low, high)
            
            if pivot - low < high - pivot:
                self.quicksort(low, pivot - 1)
                low = pivot + 1
            else:
                self.quicksort(pivot + 1, high)
                high = pivot - 1

    def sort(self):
        if len(self.array) <= 1:
            return self.array
        self.quicksort(0, len(self.array) - 1)
        return self.array
