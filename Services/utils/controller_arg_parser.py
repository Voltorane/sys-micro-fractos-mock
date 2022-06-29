import getopt

def arg_parser(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'zvs:', ["servers="])
    except getopt.GetoptError:
        print(f"ERROR by parsing args: {argv}!")
    run_with_zookeeper = False
    verbose = False
    servers = 1
    MAX_SERVERS = 10
    for opt, arg in opts:
        if opt in ('-z', '--zookeeper'):
            run_with_zookeeper = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-s', '--servers'):
            try:
                servers = int(arg)
                servers = min(MAX_SERVERS, servers)
            except ValueError:
                pass
    return run_with_zookeeper, verbose, servers