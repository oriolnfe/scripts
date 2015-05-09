import sys
from optparse import OptionParser
from smb.SMBConnection import SMBConnection


def main(argv):

    parser = OptionParser()

    parser.add_option("-u", "--username", 
            help="Username that will be used for authentication")
    parser.add_option("-p", "--password", 
            help="Password that will be used for authentication")
    parser.add_option("-f", "--file", dest="filename",
                              help="Read systems list from file")
    parser.add_option("-d", "--domain", 
            help="Domain name that will be used for authentication")
    (options, args) = parser.parse_args()

    with open(options.filename) as f:
        for system_name in f:
            try:
                print('### Analyzing system: ' + system_name)
                # parameterize an smb connection with a system
                conn = SMBConnection(options.username,
                    options.password,
                    'enumerator',
                    system_name,
                    options.domain,
                    use_ntlm_v2=True,
                    sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                    is_direct_tcp=True)

                # establish the actual connection
                connected = conn.connect(system_name,445)

                try:
                    Response = conn.listShares(timeout=30)  # obtain a list of shares
                    print('Shares on: ' + system_name)
                    for i in range(len(Response)):  # iterate through the list of shares
                        print("  Share[",i,"] =", Response[i].name)
                                
                        try:
                            # list the files on each share (recursivity?)
                            Response2 = conn.listPath(Response[i].name,'/',timeout=30)
                            print('    Files on: ' + system_name + '/' + "  Share[",i,"] =",
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
