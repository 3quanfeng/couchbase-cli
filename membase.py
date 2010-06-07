#!/usr/bin/env python
"""
  membase.py

  This program is the top level source file for the Membase Command Line Tools

"""
import getopt,sys
from membase_cli_listservers import *
from membase_cli_buckets import *
from membase_info import *



if __name__ == "__main__":
  (cluster, user, password) = ('','','')
  try:
    opts, args = getopt.getopt(sys.argv[2:], 'b:c:e:gdp:c:hp:s',
                                             ['help',
                                              'cluster=',
                                              'password=',
                                              'user=',
                                              'stats'])
    cmd = sys.argv[1]
    if cmd == "--help" or cmd == "help":
      usage()
  except  getopt.GetoptError, err:
    usage()


  # check if usage specified
  for o, a in opts:
    if o == "-h" or o == "--help":
      cmd == "help"
      usage()
    if o == "-c" or o == "--cluster":
      cluster = a
    if o == "-u" or o == "--user":
      user = a
    if o == "-p" or o == "--password":
      password = a

  if (not cluster and cmd != "help"):
    usage("You must specify at least two things: command, and cluster (--cluster)")
  if not user:
     user = ''
  if not password:
     password = ''

  # need to make this dynamic
  commands = { 
                'listservers' : Listservers,
                'listbuckets' : Buckets, 
                'bucketinfo' : Buckets, 
                'bucketstats' : Buckets, 
                'bucketcreate' : Buckets, 
                'bucketdelete' : Buckets, 
                'bucketflush' : Buckets, 
                }

  # make sure the command is defined
  if cmd not in commands:
    err_message= "command: '%s' not found" % cmd
    usage(err_message)

  # instantiate
  taskrunner = commands[cmd]()
  # call runCmd method
  taskrunner.runCmd(cmd, cluster, user, password, opts)


