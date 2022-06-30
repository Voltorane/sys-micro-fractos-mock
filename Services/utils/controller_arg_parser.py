import getopt

def arg_parser(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'zvn:', ["name="])
    except getopt.GetoptError:
        print(f"ERROR by parsing args: {argv}!")
    run_with_zookeeper = False
    verbose = False
    name = ""
    MAX_SERVERS = 10
    for opt, arg in opts:
        if opt in ('-z', '--zookeeper'):
            run_with_zookeeper = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-n', '--name'):
            try:
                name = arg
            except ValueError:
                pass
    return run_with_zookeeper, verbose, name