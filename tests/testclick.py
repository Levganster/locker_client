import click, requests

@click.command()
@click.option('--host', '-h', default="212.193.27.248", help='Host ip.')
@click.option('--port', '-p', default="443", help='Host port')
def post(host, port):
    response = requests.get(f"http://{host}:{port}/log/get_logs", cookies={"access_token_cookie": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiMTIzIiwiYWRtaW4iOnRydWUsImdyb3VwIjpudWxsfSwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTcyODQ2NDY0NywiaWF0IjoxNzI3ODU5ODQ3LCJqdGkiOiI2YmQxYWI3NS1iOGRhLTQ5MmEtYjVjMS02NTA2OTY0YmYxMjQifQ.r7A7mHB83CFAoIgJyJ6wcjNwde4Wj9iv0L4KfH2Smhc"})
    print(response.content)
if __name__ == '__main__':
    post()