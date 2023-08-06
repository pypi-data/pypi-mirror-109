import threading
import time
import concurrent.futures

from threading import Thread
import subprocess


def single_thread(t, num_threads):
    bashCommand = "./computedis.out " + str(t) + " " + str(num_threads) + " true_swap_10x50 288 50 10 swap "
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)

    print("Thread " + str(t) + " is ready :)")


if __name__ == "__main__":

    num_threads = 80

    threads = [None for _ in range(num_threads)]

    for t in range(num_threads):
        print('thread: ', t)

        threads[t] = Thread(target=single_thread, args=(t, num_threads))
        threads[t].start()

    for t in range(num_threads):
        threads[t].join()

    print("All threads are ready :) :) :)")
