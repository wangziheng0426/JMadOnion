from __future__ import absolute_import
import sys
import subprocess
import os
import json
import traceback
from . import DeadlineSend

class ConnectionProperty:

    def __init__(self, address, useAuth=False, useTls =True, caCert=None, insecure=False):
        self.address = address
        self.useAuth = useAuth
        self.user = ""
        self.password = ""
        self.useTls = useTls
        self.caCert = caCert
        self.insecure = insecure
        
    def GetAddress(self):
        return self.address
        
    def SetAddress(self, address):
        self.address = address
        
    def GetAuthentication(self):
        return self.user, self.password
        
    def SetAuthentication(self, user, password):
        self.user = user
        self.password = password
        
    def AuthenticationEnabled(self):
        return self.useAuth
        
    def EnableAuthentication(self, enable):
        self.useAuth = enable
        
    def __get__(self, commandString):
        
        return DeadlineSend.send(self.address,commandString, "GET", None, self.useAuth, self.user, self.password, self.useTls, self.caCert, self.insecure)
        
    def __put__(self, commandString, body):
        
        return DeadlineSend.send(self.address, commandString, "PUT", body, self.useAuth, self.user, self.password, self.useTls, self.caCert, self.insecure)
        
    def __delete__(self, commandString):
        
        return DeadlineSend.send(self.address,commandString, "DELETE", None, self.useAuth, self.user, self.password, self.useTls, self.caCert, self.insecure)
        
    def __post__(self, commandString, body):
        
        return DeadlineSend.send(self.address, commandString, "POST", body, self.useAuth, self.user, self.password, self.useTls, self.caCert, self.insecure)
