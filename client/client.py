import json
import urllib3


def get_data_from_file(js_file):
    try:
        js_string = ''
        for line in open(js_file, "r").readlines():
            line = line.replace('\n', '')
            line = line.replace('\'', '"')
            js_string = js_string + line
        js_dict = json.loads(js_string)
    except Exception as e:
        print(f"Error opening json file: {e}")
        exit()
    return js_dict


data_dict = get_data_from_file('example.json')

http = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=2.0, read=2.0),
    retries=urllib3.Retry(3, redirect=1)
)

url = 'http://127.0.0.1:5000/json'
encoded_data = json.dumps(data_dict).encode('utf-8')

try:
    resp = http.request('POST',
                        url,
                        body=encoded_data,
                        headers={'Content-Type': 'application/json'})
    print(resp.status)
    print(resp.headers)
    print(resp.data.decode("utf-8"))
except Exception as e:
    print(f"Error of POST-request: {e}")