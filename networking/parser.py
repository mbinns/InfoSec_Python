def parse(data, port, origin):
    if port==3333:
        return
    if origin == 'server':
        return
    print "[{}({})] {}".format(origin, port, data.encode('hex'))


def hexdump(src, source, length=32):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text))
    if "server" in source:
        print "[<=] Server response with {bytes:d} bytes".format(bytes=len(src))
    elif "client" in source:
        print "[=>] Client response with {bytes:d} bytes".format(bytes=len(src))

    print b'\n'.join(result)
