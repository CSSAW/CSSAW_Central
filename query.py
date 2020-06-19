"""
Author: Luke Williams

CSSAW Python SQL helpers

(Will eventually become a command line program for executing sql scripts
in the python shell)

"""
from Session import *
import argparse
import json
import os
from pathlib import Path

def get_JSON_from_cursor(cursor):
    """ Return JSON string from cursor results """

    outS = ''
    for result in cursor:
        outS += json.dumps(result, JSONout, indent=4)

    return outS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Host IP for server')
    parser.add_argument('user', help='Database account for login')
    parser.add_argument('password', default=None, help='Password for database user')
    parser.add_argument('querypath', help='Path of query to execute')
    parser.add_argument('-outfile', default='./results/result.json', help='Filename of output json file')
    args = parser.parse_args()

    # connect to server using given user and pass
    cursor = connect(args.user, args.password, args.host)

    # execute external sql file
    execute_SQL(args.querypath, cursor)

    # create out path if needed
    outpath = os.path.dirname(args.outfile)
    Path(outpath).mkdir(parents=True, exist_ok=True)

    # write json file from query output
    with open(args.outfile, 'w+') as outfile:
        outfile.write(get_JSON_from_cursor(cursor))