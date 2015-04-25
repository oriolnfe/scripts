import sys
from smb.SMBConnection import SMBConnection

print ("### Usage:  python smb_enumerator 'username' 'password' 'ip/systems file' 'domain'")

with open(sys.argv[3]) as f:
    for line in f:
        try:
            print('### Analyzing system: ' + line)
            # parameterize an smb connection with a system
            conn = SMBConnection(sys.argv[1],
                sys.argv[2],
                'enumerator',
                line,
                sys.argv[4],
                use_ntlm_v2=True,
                sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                is_direct_tcp=True)

            # establish the actual connection
            connected = conn.connect(sys.argv[3],445)

            try:
                Response = conn.listShares(timeout=30)  # obtain a list of shares
                print('Shares on: ' + sys.argv[3])
                for i in range(len(Response)):  # iterate through the list of shares
                    print("  Share[",i,"] =", Response[i].name)
                            
                    try:
                        # list the files on each share (recursivity?)
                        Response2 = conn.listPath(Response[i].name,'/',timeout=30)
                        print('    Files on: ' + sys.argv[3] + '/' + "  Share[",i,"] =",
                               Response[i].name)
                        for i in range(len(Response2)):
                            print("    File[",i,"] =", Response2[i].filename)
                    except:
                        print('### can not access the resource')

            except:
                print('### can not list shares')

        except:
            print('### can not access the system')
