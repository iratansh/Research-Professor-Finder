class QuickSort:
    def __init__(self, array, epsilon=1e-10):
        self.array = array
        self.epsilon = epsilon
        
    def is_less_or_equal(self, a, b):
        return a >= b - self.epsilon
        
    def is_greater(self, a, b):
        return a < b - self.epsilon
        
    def partition(self, low, high):
        mid = (low + high) // 2
        pivot_candidates = [
            (low, self.array[low][1]),
            (mid, self.array[mid][1]),
            (high, self.array[high][1])
        ]
        pivot_idx = sorted(pivot_candidates, key=lambda x: x[1], reverse=True)[1][0]
        self.array[pivot_idx], self.array[high] = self.array[high], self.array[pivot_idx]
        pivot = self.array[high][1]
        
        i = low - 1
        
        for j in range(low, high):
            if self.is_less_or_equal(self.array[j][1], pivot):
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1
    
    def insertion_sort(self, low, high):
        for i in range(low + 1, high + 1):
            key = self.array[i]
            j = i - 1
            while j >= low and self.is_greater(self.array[j][1], key[1]):
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key

    def quicksort(self, low, high, n):
        if low >= high or low >= n:
            return
            
        if high - low < 10:
            self.insertion_sort(low, high)
            return
            
        pivot = self.partition(low, high)
        
        if pivot >= n:
            self.quicksort(low, pivot - 1, n)
        else:
            self.quicksort(low, pivot - 1, n)
            self.quicksort(pivot + 1, high, n)

    def sort(self, n):
        if n <= 0:
            return []
        if n > len(self.array):
            n = len(self.array)
        
        if len(self.array) <= 1:
            return self.array
            
        self.quicksort(0, len(self.array) - 1, n)
        return self.array[:n]