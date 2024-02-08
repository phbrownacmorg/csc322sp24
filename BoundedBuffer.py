from threading import Thread, Semaphore, BoundedSemaphore
from time import sleep
import random

def main(args: list[str]) -> int:
    # Shared resources
    NUM_VALUES: int = 10
    CAPY: int = 4
    buffer: list[int] = [-1] * CAPY

    # Semaphores (also shared)
    mutex: BoundedSemaphore = BoundedSemaphore()
    spaces: BoundedSemaphore = BoundedSemaphore(CAPY)
    items: Semaphore = Semaphore(0) # Bad if value > CAPY

    # Define the kinds of threads I aim to run

    class Producer(Thread):
        def __init__(self, num_items: int, nap: int):
            # Pre:
            assert num_items > 0 and nap > 0
            self.num_items = num_items
            self.nap = nap
            super().__init__()

        def run(self) -> None:
            for i in range(self.num_items):
                spaces.acquire()
                with mutex: # Actually a monitor
                    buffer[i % CAPY] = i
                items.release()
                sleep(self.nap * random.random())

    class Consumer(Thread):
        def __init__(self, num_items: int, nap: int):
            # Pre:
            assert num_items > 0 and nap > 0
            self.num_items = num_items
            self.nap = nap
            super().__init__()

        def run(self) -> None:
            for i in range(self.num_items):
                items.acquire()
                with mutex: # Actually a monitor
                    print(i % CAPY, buffer[i % CAPY])
                spaces.release()
                sleep(self.nap * random.random())

    # Make threads
    prod = Producer(NUM_VALUES, 2)
    cons = Consumer(NUM_VALUES, 1)

    # Start threads
    prod.start()
    cons.start()

    # Threads run

    # Let threads finish
    prod.join()
    cons.join()

    return 0



if __name__ == '__main__':
    import sys
    sys.exit(main([]))