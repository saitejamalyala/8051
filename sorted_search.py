def count_numbers(sorted_list, less_than):
    """
    :param sorted_list: (list) The list of numbers.
    :param less_than: (int) The number to compare with.
    :returns: (int) The number of elements in the list that are less than the given number.
    """
    # apply binary search to find the index of the first element that is greater than or equal to less_than
    """
    # if the first element is greater than or equal to less_than, return 0
    if sorted_list[0] >= less_than:
        return 0

    # if the last element is less than less_than, return the length of the list
    if sorted_list[-1] < less_than:
        return len(sorted_list)

    # if the first element is less than less_than and the last element is greater than or equal to less_than, apply binary search
    left = 0
    right = len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] < less_than:
            left = mid + 1
        else:
            right = mid - 1
    
    return left
    """

    # add element to list and sort the list
    sorted_list.append(less_than)
    sorted_list.sort()

    sorted_set = set(sorted_list)
    sorted_list = list(sorted_set).sort()

    # return the index of less_than
    return sorted_list.index(less_than)

if __name__ == "__main__":
    #sorted_list = [1, 3, 5, 7]
    #print(count_numbers(sorted_list, 4)) # should print 2

    sorted_list = list(range(1000000))
    print(count_numbers(sorted_list, 400000)) # should print 2