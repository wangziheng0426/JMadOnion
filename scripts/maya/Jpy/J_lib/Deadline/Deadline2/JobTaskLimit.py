from ConnectionProperty import ConnectionProperty

class JobTaskLimit:
    """
        Class used by DeadlineCon to send Job task limit requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetJobTaskLimit(self):
        """ Gets the Job task limit.
            Returns: The Job task limit.
        """
        return self.connectionProperties.__get__("/api/jobtasklimit")