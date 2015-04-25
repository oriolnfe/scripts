import sys
import getopt
from smb.SMBConnection import SMBConnection



def usage():
    print ("### Usage:  python smb_enumerator -u 'username' -p 'password' -f 'ip/systems file' -d 'domain'")

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:p:f:d:", ["help","user=","password=","file=","domain="])
    
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-d", "--domain"):
            domain = arg

    with open(filename) as f:
        for line in f:
            try:
                print('### Analyzing system: ' + line)
                # parameterize an smb connection with a system
                conn = SMBConnection(username,
                    password,
                    'enumerator',
                    line,
                    domain,
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


if __name__ == "__main__":
    main(sys.argv[1:])
