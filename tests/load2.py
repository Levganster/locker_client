import time,sys
loading = "Loading: [▒▒▒▒▒▒▒▒▒▒]"
for i in range(101):
    time.sleep(0.1)
    sys.stdout.write("\r"+loading+" %d%%" % i)
    if not (i+1) % 10:
        loading = loading.replace("▒","█",1)
    sys.stdout.flush()