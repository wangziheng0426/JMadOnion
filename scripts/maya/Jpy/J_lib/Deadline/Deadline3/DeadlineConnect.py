from __future__ import absolute_import
import sys
import subprocess
import os
import json
import traceback
from . import Jobs
from . import SlavesRenderingJob
from . import JobReports
from . import TaskReports
from . import Limits
from . import Tasks
from . import Pulse
from . import Repository
from . import MappedPaths
from . import MaximumPriority
from . import Pools
from . import Groups
from . import Plugins
from . import Slaves
from . import Users
from . import Balancer
from .ConnectionProperty import ConnectionProperty

#http://docs.python.org/2/library/httplib.html

class DeadlineCon:
    """
        Object used by user to communicate with the web service.
        Host name of the Web Service, as well as the port number the
        Web Service is listening on are required for construction.
        Call other API functions through this object.
    """
    def __init__(self, host, port, useTls=False, caCert=None, insecure=False):
        """ Constructs an instance of DeadlineCon.
            Params: host name of the Web Service (string).
                    port number the Web Service is listening on (integer).
                    useTls specifies wether the webservice is listining on a TLS port or not.
                    caCert specifies the caCert to use to validate the response form the webservice.
                    insecure NOT RECOMMENDED, True specifies that we shouldn't validate the respone from the webservice.
        """
        
        #Builds the ConnectionProperty object used for sending requests.
        address = host+":"+str(port)
        self.connectionProperties = ConnectionProperty(address, False, useTls, caCert, insecure)
        
        #The different request groups use the ConnectionProperty object to send their requests.
        self.Jobs = Jobs.Jobs(self.connectionProperties)
        self.SlavesRenderingJob = SlavesRenderingJob.SlavesRenderingJob(self.connectionProperties)
        self.Tasks = Tasks.Tasks(self.connectionProperties)
        self.TaskReports = TaskReports.TaskReports(self.connectionProperties)
        self.JobReports = JobReports.JobReports(self.connectionProperties)
        self.LimitGroups = Limits.LimitGroups(self.connectionProperties)
        self.Pulse = Pulse.Pulse(self.connectionProperties)
        self.Repository = Repository.Repository(self.connectionProperties)
        self.MappedPaths = MappedPaths.MappedPaths(self.connectionProperties)
        self.MaximumPriority = MaximumPriority.MaximumPriority(self.connectionProperties)
        self.Pools = Pools.Pools(self.connectionProperties)
        self.Groups = Groups.Groups(self.connectionProperties)
        self.Plugins = Plugins.Plugins(self.connectionProperties)
        self.Slaves = Slaves.Slaves(self.connectionProperties)
        self.Users = Users.Users(self.connectionProperties)
        self.Balancer = Balancer.Balancer(self.connectionProperties)
        
    def EnableAuthentication(self, enable=True):
        """
            Toggles authentication mode. If enabled, requests sent through this DeadlineCon object will attempt authentication with the current user name and password credentials.
            If the authentication credentials have not been set, authentication will fail. Required to be enabled if the Web Service requires authentication.
            Params: whether to disable or enable authentication mode (enabled by default, bool).
        """
        self.connectionProperties.EnableAuthentication(enable)
        
    def SetAuthenticationCredentials(self, username, password, enable=True):
        """
            Sets the authentication credentials to be used when attempting authentication.
            Params: the username credential (string).
                    the password credential (string).
                    whether to enable authentication mode or not (enabled by default, bool).
        """
        self.connectionProperties.SetAuthentication(username, password)
        self.connectionProperties.EnableAuthentication(enable)
        
    def AuthenticationModeEnabled(self):
        """
            Returns whether authentication mode is enabled for this DeadlineCon or not. If not, then authentication will fail if the Web Service requires authentication.
        """
        return self.connectionProperties.AuthenticationEnabled()