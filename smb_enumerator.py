#!/usr/bin/python

import sys
from smb.SMBConnection import SMBConnection

conn = SMBConnection(sys.argv[1],
    sys.argv[2],
    'MyApp',
    '192.168.5.128',
    '',
    use_ntlm_v2=True,
    sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
    is_direct_tcp=True)
connected = conn.connect('192.168.5.128',445)
Response = conn.listShares(timeout=30)

for i in range(len(Response)):
        print("Share[",i,"] =", Response[i].name)
