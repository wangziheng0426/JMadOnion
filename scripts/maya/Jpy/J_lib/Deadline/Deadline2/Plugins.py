from ConnectionProperty import ConnectionProperty

class Plugins:
    """
        Class used by DeadlineCon to send Plugin requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetPluginNames(self):
        """ Gets the Plugin names.
            Returns: The list of Plugin names.
        """
        return self.connectionProperties.__get__("/api/plugins")

    def GetEventPluginNames(self):
        """ Gets the event Plugin names.
            Returns: The list of event Plugin names.
        """
        return self.connectionProperties.__get__("/api/plugins?EventNames=true")