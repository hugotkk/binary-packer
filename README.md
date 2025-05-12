## **Usage**

```bash
python3 pack.py --dest ./pack --binary /usr/sbin/tcpdump
```

Output:
```
Copied library: /lib/aarch64-linux-gnu/libpcap.so.0.8
Copied binary: /usr/sbin/tcpdump

Run with:
LD_LIBRARY_PATH=./pack/lib ./pack/bin/tcpdump
```