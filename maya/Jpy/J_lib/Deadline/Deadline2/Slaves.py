from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Slaves:
    """
        Class used by DeadlineCon to send Slave requests, as well as a few Pool and Group requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSlaveNames(self):
        """ Gets all the Slave names.
            Returns: The list of Slave names.
        """
        return self.connectionProperties.__get__("/api/slaves?NamesOnly=true")

    def GetSlavesInfoSettings(self, names = None):
        """ Gets multiple Slave info settings.
            Inputs: names: The names of the Slaves to get. If None get all Slaves.
            Returns: The list of Slaves' infos and settings.
        """
        script = "/api/slaves?Data=infosettings"
        if names != None:
            script = script +"&Name="+ ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def GetSlaveInfoSettings(self, name):
        """ Gets a Slave info settings.
            Input: name: The Slave name.
            Returns: The Slave info settings.
        """
        result = self.connectionProperties.__get__("/api/slaves?Data=infosettings&Name="+name.replace(' ','+'))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def GetSlaveInfo(self, name):
        """ Gets a Slave info object.
            Input: name: The Slave name.
            Returns: The Slave info.
        """
        result = self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=info")
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result
        
    def GetSlaveInfos(self, names = None):
        """ Gets multiple Slave info objects.
            Input: name: The Slave names. If None return all info for all Slaves.
            Returns: List of the Slave infos.
            """
        script = "/api/slaves?Data=info"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SaveSlaveInfo(self, info):
        """ Saves Slave info to the database.
            Input:  info: Json object of the Slave info.
            Returns: Success message.
        """
        info = json.dumps(info)
        body = '{"Command":"saveinfo", "SlaveInfo":'+info+'}'
        return self.connectionProperties.__put__("/api/slaves", body)

    def GetSlaveSettings(self, name):
        """ Gets a Slave settings object.
            Input: name: The Slave name.
            Returns: The Slave settings.
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=settings")
    
    def GetSlavesSettings(self, names = None):
        """ Gets multiple Slave settings objects.
            Input: name: The Slave names. If None return all info for all Slaves.
            Returns: List of the Slave settings's info.
        """
        script = "/api/slaves?Data=settings"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeparatedString(names).replace(' ','+')
            
        return self.connectionProperties.__get__(script)

    def SaveSlaveSettings(self, info):
        """ Saves Slave Settings to the database.
            Input:  info: Json object of the Slave settings.
            Returns: Success message.
        """
        info = json.dumps(info)
        body = '{"Command":"savesettings", "SlaveSettings":'+info+'}'
        
        return self.connectionProperties.__put__("/api/slaves", body)

    def DeleteSlave(self, name):
        """ Removes a Slave from the repository.
            Input:  name: The name of the Slave to be removed.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/slaves?Name="+name)

    def AddGroupToSlave(self, slave, group):
        """ Adds a Group to a Slave.
            Input:  slave: The name of the Slave or Slaves (may be a list).
                    group: The name of the Group or Groups (may be a list).
            Returns: Success message.
        """
        body = '{"Slave":'+json.dumps(slave)+', "Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def AddPoolToSlave(self, slave, pool):
        """ Adds a Pool to a Slave.
            Input:  slave: The name of the Slave or Slaves (may be a list).
                    pool: The name of the Pool or Pools (may be a list).
            Returns: Success message.
        """
        body = '{"Slave":'+json.dumps(slave)+', "Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def RemovePoolFromSlave(self, slave,pool):
        """ Adds a Pool from a Slave.
            Input:  slave: The name of the Slave or Slaves (may be a list).
                    pool: The name of the Pool or Pools (may be a list).
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/pools?Slaves="+ArrayToCommaSeparatedString(slave)+"&Pool="+ArrayToCommaSeparatedString(pool))

    def RemoveGroupFromSlave(self, slave,group):
        """ Adds a Group from a Slave.
            Input:  slave: The name of the Slave or Slaves (may be a list).
                    group: The name of the Group or Group (may be a list).
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/groups?Slaves="+ArrayToCommaSeparatedString(slave)+"&Group="+ArrayToCommaSeparatedString(group))

    def GetSlaveNamesInPool(self, pool):
        """ Gets the names of all Slaves in a specific Pool.
            Input:  pool: The name of the Pool to search in (may be a list).
            Returns: A list of all Slaves that are in the Pool.
        """
        return self.connectionProperties.__get__("/api/pools?Pool="+ArrayToCommaSeparatedString(pool).replace(' ','+'))

    def GetSlaveNamesInGroup(self, group):
        """ Gets the names of all Slaves in a specific Group.
            Input:  group: The name of the Group to search in (may be a list).
            Returns: A list of all Slaves that are in the Groups.
        """
        return self.connectionProperties.__get__("/api/groups?Group="+ArrayToCommaSeparatedString(group).replace(' ','+'))

    def SetPoolsForSlave(self, slave,pool = []):
        """ Sets all of the Pools for one or more Slaves overriding their old lists.
            Input:  slave: Slaves to be modified (may be a list).
                    pool: List of Pools to be used.
            Returns: Success message.
        """
        body = '{"OverWrite":true, "Slave":'+json.dumps(slave)+',"Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def SetGroupsForSlave(self, slave,group = []):
        """ Sets all of the Groups for one or more Slaves overriding their old lists.
            Input:  slave: Slaves to be modified (may be a list).
                    pool: List of Groups to be used.
            Returns: Success message.
        """
        body = '{"OverWrite":true, "Slave":'+json.dumps(slave)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def GetSlaveReports(self, name):
        """ Gets the reports for a Slave.
            Input:  name: The name of the Slave.
            Returns: All reports for the Slave.
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=reports")
        
    def GetSlaveReportsContents(self, name):
        """ Gets the reports contents for a Slave.
            Input:  name: The name of the Slave.
            Returns: All reports contents for the Slave.
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=reportcontents")

    def GetSlaveHistoryEntries(self, name):
        """ Gets the history entries for a Slave.
            Input:  name: The name of the Slave.
            Returns: All history entries for the Slave.
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=history")