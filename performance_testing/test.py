import requests
import time
#performance_testing
with open('test_paragraph.txt', 'r') as f:
  data = f.read()
  t1 = time.time()
  resp = requests.post('http://localhost:5000/getspeech', json={'text_message': data})
  t2 = time.time()
  print('Response Time={} seconds'.format(t2-t1))
  

