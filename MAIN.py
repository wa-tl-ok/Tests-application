import multiprocessing

def task1():
    import CHART

def task2():
    import TEST

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=task1)
    p2 = multiprocessing.Process(target=task2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
