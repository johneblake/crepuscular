import sys
from datastore import datacontext
from reader import quandl_reader, etf_reader

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == "help":
        print("historical, daily, help")
    elif command == "historical":
        pass
    elif command == "daily":
        pass
    else:
        print("Unknown command {command}".format(command = command))