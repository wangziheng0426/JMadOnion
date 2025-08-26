from ConnectionProperty import ConnectionProperty

class SlavesRenderingJob:
    """
        Class used by DeadlineCon to send Slaves Rendering Job requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSlavesRenderingJob(self, id, getIpAddress=False):
        """ Gets the list of Slaves that are currently rendering a Job.
            Input:  id: The Job ID.
            getIpAddress: If True, the IP address of the Slaves will be returned instead.
            Returns: The list of Slave names, or the list of Slave IP addresses if getIpAddress is True.
        """
        return self.connectionProperties.__get__("/api/slavesrenderingjob?JobID="+id+"&GetIpAddress="+str(getIpAddress))