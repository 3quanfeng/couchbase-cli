#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  listservers class

  This class implements methods that will list servers within a
  membase cluster

"""

import pprint
from membase_info import *
from restclient import *


class Listservers:

    def __init__(self):
        """
      constructor
    """

        self.rest_cmd = '/pools/default'
        self.method = 'GET'
        self.debug = False
        self.output = 'standard'
        self.user = ''
        self.password = ''

    def runCmd(
        self,
        cmd,
        server,
        port,
        user,
        password,
        opts,
        ):

        self.user = user
        self.password = password

        for (o, a) in opts:
            if o in  ('-o', '--output'):
                self.output = a
            if o in  ('-d', '--debug'):
                self.debug = 1

        data = self.getData(server,
                            port,
                            user,
                            password)

        if (self.output == 'json'):
            print data
        else:
            print 'List of servers within the server %s:%s' % (server, port)
            self.printNodes(self.getNodes(data))


    def getData(self,
                server,
                port,
                user='',
                password=''):
        """
        get the raw json output from the server
    """

        if not user and not password:
            user = self.user
            password = self.password

        self.rest = RestClient(server, port, {'debug':self.debug})
        response = self.rest.sendCmd(self.method,
                                     self.rest_cmd,
                                     user,
                                     password)

        if response.status == 200:
            data = response.read()
        else:
            data = '"Error! ' + response.status + response.reason + '"'

        return data

    def getNodes(self, data):
        """
        deserialize the raw json output and return just the nodes
    """

        json = self.rest.getJson(data)
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(json['nodes'])
        return json['nodes']

    def printNodes(self, nodes):
        """
        print the nodes
    """

        for node in nodes:
            print '\t%s\t%s\t%s' % (node['hostname'],
                node['otpNode'], node['status' ])
