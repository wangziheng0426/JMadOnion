from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Pools:
    """
        Class used by DeadlineCon to send Pool requests. Additional
        Pool requests related to Slaves can be found in the Slaves.py file. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties

    def GetPoolNames(self):
        """ Gets the Pool names.
            Returns: The list of Pool names.
        """
        return self.connectionProperties.__get__("/api/pools")

    def AddPool(self, name):
        """ Adds a Pool to the repository.
            Params: name: The Pool name.
            Returns: Success message.
        """
        body = '{"Pool":"'+name+'"}'
        
        return self.connectionProperties.__post__("/api/pools", body)
        
    def AddPools(self, names):
        """ Adds some Pools to the repository.
            Params: names: List of Pool names to add.
            Returns: Success message.
        """
        body = '{"Pool":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/pools", body)
        
    def PurgePools(self, replacementPool="none", pools=[], overwrite=False):
        """ Purges obsolete Pools from repository using the provided replacementPool. 
        If Overwrite is set, the Pools provided will overwrite the old Pools and the 
        replacementPool must be a Pool in the provided Pools list. If Overwrite is 
        not set, the Pools provided will be added to the repository and obsolete Pools
        will be purged using the replacement Pool. If Overwrite is not set, then no Pools
        are required.
        
            Params: replacementPool: The Pool to replace obsolete Pools on purge.
                    pools: The list of Pools to set or add.
                    overwrite: Boolean flag that determines whether we are setting or adding Pools.
            Returns: Success message.
        """
        body = '{"ReplacementPool":"'+replacementPool+'", "Pool":'+json.dumps(pools)+', "OverWrite":'+json.dumps(overwrite)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def DeletePool(self, name):
        """ Removes a Pool from the repository.
            Params: name: The Pool name.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/pools?Pool="+name.replace(' ','+'))
        
    def DeletePools(self, names):
        """ Removes some Pools from the repository.
            Params: names: List of Pool names to remove.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/pools?Pool="+ArrayToCommaSeparatedString(names).replace(' ','+'))