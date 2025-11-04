from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class LimitGroups:
    """
        Class used by DeadlineCon to send Limit Group requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetLimitGroupNames(self):
        """ Gets all the limit group names.
            Returns: The list of user group names.
        """
        return self.connectionProperties.__get__("/api/limitgroups?NamesOnly=true")
    
    def GetLimitGroup(self,name):
        """ Gets a limit group.
            Input: name: The limit group name.
            Returns: The limit group.
        """
        result = self.connectionProperties.__get__("/api/limitgroups?Name="+name.replace(' ', '+'))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def GetLimitGroups(self, names = None):
        """ Gets a list of limit groups.
            Input: Names: A list of limit group names, gets all limit groups if left as None.
            Returns: The list of limit groups.
        """
        if names is not None:
            
            script = "/api/limitgroups?Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
            
        else:
            script = "/api/limitgroups"
            
        return self.connectionProperties.__get__(script)

    def SetLimitGroup(self, name, limit=None, slaveList=None, WhitelistFlag=None, progress = None, excludedSlaves = None):
        """ Creates a limit group if it doesn't exist, or updates its properties if it does.
            Input:  name: The limit group name.
                    limit: The limit.
                    listedSlaves: The list of Slaves.
                    isWhiteList: True if the list of Slaves is a whitelist.
                    progress: The release percentage.
                    excludedSlaves: The list of Slaves that will ignore this limit group.
            Returns: Success message.
        """
        body = '{"Command":"set", "Name":"'+name+'"'
            
        if limit != None:
                
            body = body + ',"Limit":'+str(limit)
                
        if WhitelistFlag != None:
                
            body = body + ',"White":'+str(WhitelistFlag).lower()
                
        if progress != None:
                
            body = body + ',"RelPer":'+str(progress)
        
        if slaveList != None:
            
            body = body + ',"Slaves":'+json.dumps(slaveList)
            
        if excludedSlaves != None:
            
            body = body + ',"SlavesEx":'+json.dumps(excludedSlaves)
            
        body = body +'}'

        return self.connectionProperties.__put__("/api/limitgroups", body)

    def SaveLimitGroup(self, info):
        """ Updates a limit group's properties in the database.
            Input:    info: the limit group object.
            Returns: Success message.
        """
        info = json.dumps(info)
        
        body = '{"Command":"save", "LimitGroup":'+info+'}'
        
        return self.connectionProperties.__put__("/api/limitgroups", body)

    def DeleteLimitGroup(self, name):
        """ Deletes a limit group.
            Input: name: The limit group name (may be a list).
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/limitgroups?Names="+ArrayToCommaSeparatedString(name).replace(' ','+'))

    def ResetLimitGroup(self, name):
        """ Resets the usage counts for a limit group.
            Input: name: The limit group name.
            Returns: Success message.
        """
        body = '{"Command":"reset", "Name":"'+name+'"}'
        
        return self.connectionProperties.__put__("/api/limitgroups", body)