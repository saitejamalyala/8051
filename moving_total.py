from typing import Deque, List
import time

def check_time_complexity(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken by {func.__name__} is {end - start} seconds\n")
        return result
    return wrapper

def check_memory_complexity(func):
    def wrapper(*args, **kwargs):
        import psutil
        import os
        process = psutil.Process(os.getpid())
        start = process.memory_info().rss
        result = func(*args, **kwargs)
        end = process.memory_info().rss
        print(f"Memory taken by {func.__name__} is {end - start} bytes,  ~ {(end - start)/1024/1024/1024} GB  \n")

        return result
    return wrapper


class MovingTotal:
       
    def __init__(self, window_size: int=3):
        self.numbers = []
        self.window = Deque([])
        self.moving_total = set()
        self.window_size = window_size

    @check_time_complexity
    @check_memory_complexity
    def append_time_efficient(self, numbers: List[int]):
        """
        :param numbers: (list) The list of numbers.
        """
        # append the numbers to the list
        """
        if len(self.numbers) == 0:
            self.numbers = numbers
            # calculate moving sum of three numbers in the list
            for i in range(len(self.numbers)-2):
                self.moving_total.add(sum(self.numbers[i:i+3]))

        else:
            last_len = len(self.numbers)
            self.numbers.extend(numbers)
            for i in range(last_len-2, len(self.numbers)-2):
                self.moving_total.add(sum(self.numbers[i:i+3]))
        """

        if len(self.numbers) == 0:
            self.numbers = numbers
            # calculate moving sum of three numbers in the list
            for i in range(len(self.numbers)-self.window_size+1):
                self.moving_total.add(sum(self.numbers[i:i+self.window_size]))

        else:
            last_len = len(self.numbers)
            self.numbers.extend(numbers)
            for i in range(last_len-2, len(self.numbers)-self.window_size+1):
                self.moving_total.add(sum(self.numbers[i:i+self.window_size]))


    @check_time_complexity
    @check_memory_complexity
    def append_space_efficient(self, numbers: List[int]):
        """
        :param numbers: (list) The list of numbers.
        """
        for number in numbers:
            self.window.append(number)
            if len(self.window) > self.window_size:
                self.window.popleft()
            if len(self.window) == self.window_size:
                self.moving_total.add(sum(self.window))

    @check_time_complexity
    @check_memory_complexity
    def contains(self, total:int) -> bool:
        """
        :param total: (int) The total to check for.
        :returns: (bool) If MovingTotal contains the total.
        """

        # check if the total exists in the list moving_total with less than O(n) time complexity
        return total in self.moving_total
        #return 

if __name__ == "__main__":
    movingtotal = MovingTotal(window_size=3)
    
    movingtotal.append_time_efficient([1, 2, 3, 4])
    movingtotal.append_space_efficient([1, 2, 3, 4])
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))
    
    movingtotal.append_time_efficient([5])
    movingtotal.append_space_efficient([5])
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))


    # append very very long list of numbers
    print("\nAppending very very long list of numbers to check time complexity of contains method\n")
    movingtotal.append_time_efficient(list(range(10**7)))
    movingtotal.append_space_efficient(list(range(10**7)))
    # check time complexity of contains
    
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))
    
