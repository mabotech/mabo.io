

# pip install python-etcd --no-deps
# pip install urllib3 --no-deps

import etcd

client = etcd.Client()

print client.read('/mi/tag').value