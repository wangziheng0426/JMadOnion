import sys
import subprocess
import os
import json
import traceback
import DeadlineSend

class ConnectionProperty:

    def __init__(self, address, useAuth=False):
        self.address = address
        self.useAuth = useAuth
        self.user = ""
        self.password = ""
        
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
        
        return DeadlineSend.send(self.address,commandString, "GET", self.useAuth, self.user, self.password)
        
    def __put__(self, commandString, body):
        
        return DeadlineSend.pSend(self.address, commandString, "PUT", body, self.useAuth, self.user, self.password)
        
    def __delete__(self, commandString):
        
        return DeadlineSend.send(self.address,commandString, "DELETE", self.useAuth, self.user, self.password)
        
    def __post__(self, commandString, body):
        
        return DeadlineSend.pSend(self.address, commandString, "POST", body, self.useAuth, self.user, self.password)