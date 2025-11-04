from ConnectionProperty import ConnectionProperty

class Repository:
    """
        Class used by DeadlineCon to send Repository requests. 
        Stores the address of the Web Service for use in sending requests.
    """    
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def AddJobHistoryEntry(self, jobId, entry):
        """ Adds the provided entry for the Job ID provided.
            Input:  Job ID (string).
                    entry (string).
            Returns: Success if successful.
        """
        body = '{"Command":"jobhistoryentry","JobID":"'+jobId+'","Entry":"'+entry+'"}'
        
        return self.connectionProperties.__post__('/api/repository', body)
        
    def AddSlaveHistoryEntry(self, slaveName, entry):
        """ Adds the provided entry for the Slave name provided.
            Input:  Slave name (string).
                    entry (string).
            Returns: Success if successful.
        """
        body = '{"Command":"slavehistoryentry","SlaveName":"'+slaveName+'","Entry":"'+entry+'"}'
        
        return self.connectionProperties.__post__('/api/repository', body)
        
    def AddRepositoryHistoryEntry(self, entry):
        """ Adds the provided entry to the repository history.
            Input:  entry (string).
            Returns: Success if successful.
        """
        body = '{"Command":"repositoryhistoryentry","Entry":"'+entry+'"}'
        
        return self.connectionProperties.__post__('/api/repository', body)
    
    def GetRootDirectory(self):
        """ Gets the repository root directory.
            Returns: The root directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=root")))

    def GetBinDirectory(self):
        """ Gets the repository bin directory.
            Returns: The bin directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=bin")))

    def GetSettingsDirectory(self):
        """ Gets the repository settings directory.
            Returns: The settings directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=settings")))

    def GetEventsDirectory(self):
        """ Gets the repository events directory.
            Returns: The events directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=events")))

    def GetCustomEventsDirectory(self):
        """ Gets the repository custom events directory.
            Returns: The custom events directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=customevents")))

    def GetPluginsDirectory(self):
        """ Gets the repository plugins directory.
            Returns: The plugins directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=plugins")))

    def GetCustomPluginsDirectory(self):
        """ Gets the repository custom plugins directory.
            Returns: The custom plugins directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=customplugins")))

    def GetScriptsDirectory(self):
        """ Gets the repository scripts directory.
            Returns: The scripts directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=scripts")))

    def GetCustomScriptsDirectory(self):
        """ Gets the repository cusotm scripts directory.
            Returns: The custom scripts directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?Directory=customscripts")))

    def GetJobAuxiliaryPath(self,id):
        """ Gets the auxiliary file directory for the given Job.
            Input:    id: The ID of the Job.
            Returns: The auxiliary directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?AuxiliaryPath=job&JobID="+id)))

    def GetAlternateAuxiliaryPath(self):
        """ Gets the alternate auxiliary file directory based on the current operating system.
            Returns: The auxiliary directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?AuxiliaryPath=alternate")))

    def GetWindowsAlternateAuxiliaryPath(self):
        """ Gets the alternate auxiliary file directory for Windows.
            Returns: The auxiliary directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?AuxiliaryPath=windowsalternate")))

    def GetLinuxAlternateAuxiliaryPath(self):
        """ Gets the alternate auxiliary file directory for Linux.
            Returns: The auxiliary directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?AuxiliaryPath=linuxalternate")))

    def GetMacAlternateAuxiliaryPath(self):
        """ Gets the alternate auxiliary file directory for Mac OS X.
            Returns: The auxiliary directory.
        """
        return str((self.connectionProperties.__get__("/api/repository?AuxiliaryPath=macalternate")))
    
    def GetDatabaseConnectionString(self):
        """ Gets the database connection string in the form of (server:port,server:port...).
        If there is only one server configured, it will be in the form of (server:port).
        """
        return str((self.connectionProperties.__get__("/api/repository?DatabaseConnection=")))
        
    def GetDeadlineVersion(self):
        """ Gets the version of Deadline that the Web Service is running.
        """
        return str( self.connectionProperties.__get__("/api/repository?Version="))
        
    def GetDeadlineMajorVersion(self):
        """ Gets the Deadline major version number that the Web Service is running.
        """
        return str( self.connectionProperties.__get__("/api/repository?MajorVersion="))