import http.client
import threading
import time

end = time.time() + 240


def load_worker():
    while time.time() < end:
        try:
            conn = http.client.HTTPConnection(
                "voting-alb-1454407.us-east-1.elb.amazonaws.com", timeout=2
            )
            for _ in range(200):
                if time.time() >= end:
                    break
                conn.request("GET", "/")
                conn.getresponse().read()
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    threads = [threading.Thread(target=load_worker) for _ in range(25)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()