import json
import threading
import time
from stream_example.stream_prices import PriceStreamer
from stream_example.stream_processor import PriceProcessor
from queue import Queue
from stream_example.stream_worker import WorkProcessor

def load_settings():
    with open("./bot/settings.json", "r") as f:
        return json.loads(f.read())
    

def run_streamer():
    
    settings = load_settings()
    
    shared_prices = {}
    shared_prices_events = {}
    shared_prices_lock = threading.Lock()
    work_queue = Queue()
    
    for p in settings['pairs'].keys():
        shared_prices_events[p] = threading.Event()
        shared_prices[p] = {}
    
    threads = []
    
    price_stream_t = PriceStreamer(shared_prices, shared_prices_lock, shared_prices_events)
    price_stream_t.daemon = True
    threads.append(price_stream_t)
    price_stream_t.start()
    
    worker_t = WorkProcessor(work_queue)
    worker_t.daemon = True
    threads.append(worker_t)
    worker_t.start()
    
    for p in settings['pairs'].keys():
        processing_t = PriceProcessor(shared_prices, shared_prices_lock, shared_prices_events, f"PriceProcessor_{p}", p , work_queue)
        processing_t.daemon =True
        threads.append(processing_t)
        processing_t.start()
    
    # Tells you therad when to wait. KeyboardInterupt does not work here... We need the windows api libary to listen to correct handlers for windows. we instead use a whiile and a sleep. 
    
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    
    
    # for t in threads:
    #     t.join()
        
    print("All Done")