import requests


def isConnected():
    url = "https://attendanceproject1-default-rtdb.firebaseio.com/"
    timeout = 5
    try:
        # requesting URL
        request = requests.get(url, timeout = timeout)
        print(request)
        return True

    # catching exception
    except (requests.ConnectionError, requests.Timeout) or Exception as exception:
        return False


if __name__ == "__main__":
    isConnected()
