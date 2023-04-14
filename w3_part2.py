
import time
import os
import multiprocessing
from multiprocessing import Process, Pool
import logging


def factorize(*number):
    result_list = []
    el_list = []
    int_number = []
    
    for el in number:
        el_list.append(el)
        
    logging.debug('List Starting ')
    for el in el_list:
        for i in range(1, el+1):
            if el % i == 0:
                int_number.append(i)
        result_list.append(int_number)
        int_number = []
    logging.debug('List Finidhing ')
    return result_list
    
if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG,
                        format='%(threadName)s %(message)s')
    
    # Визначаємо кількість процесорів = кількість Процесів
    number_cpu = multiprocessing.cpu_count()
    pool = Pool(number_cpu)
    
    #Запускаємо Процеси 
    start = time.time()
    result = pool.map(factorize, [128, 255, 99999, 10651060] )
    end = time.time() - start 

    #Послідовний розрахунок
    start_1 = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_1 = time.time() - start_1 
    
    print("Number of cpu : ", number_cpu)
    
    print(f'Total time: {end} c')
    print(f'Total process time: {end_1} ')
    
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    
    
