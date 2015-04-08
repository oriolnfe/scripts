import sys
from smb.SMBConnection import SMBConnection

print ("### Usage:  python smb_enumerator 'username' 'password' 'system' 'domain'")

conn = SMBConnection(sys.argv[1],
    sys.argv[2],
    'enumerator',
    sys.argv[3],
    sys.argv[4],
    use_ntlm_v2=True,
    sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
    is_direct_tcp=True)

connected = conn.connect(sys.argv[3],445)
Response = conn.listShares(timeout=30)

for i in range(len(Response)):
    print("Share[",i,"] =", Response[i].name)
