from collections import defaultdict, Counter
import heapq
def nth_lowest_selling(sales, n):
    """
    :param elements: (list) List of book sales.
    :param n: (int) The n-th lowest selling element the function should return.
    :returns: (int) The n-th lowest selling book id in the book sales list.
    """
     
    book_sales = defaultdict(int)
    for book_id in sales:
        book_sales[str(book_id)]+=1

    return heapq.nsmallest(n, book_sales, key=book_sales.get)[-1]

    
    #return sort_book_sales[n-1][0]

    #return Counter(sales).most_common()[-n][0]

if __name__ == "__main__":
    print(nth_lowest_selling([5, 4, 3, 2, 1, 5, 4, 3, 2, 5, 4, 3, 5, 4, 5], 2))