from ConnectionProperty import ConnectionProperty

class MaximumPriority:
    """
        Class used by DeadlineCon to send Maximum Priority requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetMaximumPriority(self):
        """ Gets the maximum Job priority.
            Returns: The maximum Job priority.
        """
        return self.connectionProperties.__get__("/api/maximumpriority")