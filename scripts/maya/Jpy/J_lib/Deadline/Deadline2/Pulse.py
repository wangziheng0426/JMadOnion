from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Pulse:
    """
        Class used by DeadlineCon to send Pulse requests. 
        Stores the address of the Web Service for use in sending requests.
    """    
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetPulseNames(self):
        """ Gets all the Pulse names.
            Returns: The list of Pulse names.
        """
        return self.connectionProperties.__get__("/api/pulse?NamesOnly=true")

    def GetPulseInfo(self, name):
        """ Gets a Pulse info.
            Input: name: The Pulse name.
            Returns: The Pulse info.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Info=true")

    def GetPulseInfos(self, names = None):
        """ Gets a list of Pulse infos.
            Input: name: The Pulse names to be retrieved. If None then gets all Pulse infos.
            Returns: The Pulse infos.
        """
        script = "/api/pulse?Info=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SavePulseInfo(self, info):
        """ Saves a Pulse info to the database.
            Input: info: Json object of the Pulse info.
            Returns: Success message.
        """
        info = json.dumps(info)
        
        body = '{"Command":"saveinfo", "PulseInfo":'+info+'}'
        
        return self.connectionProperties.__put__("/api/pulse", body)
        
    def GetPulseSettings(self, name):
        """ Gets a Pulse settings.
            Input: name: The Pulse name.
            Returns: The Pulse settings.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Settings=true")

    def GetPulseSettingsList(self, names = None):
        """ Gets a list of Pulse settings.
            Input: name: The Pulse names to be retrieved. If None then gets all Pulse settings.
            Returns: The Pulse settings.
        """
        script = "/api/pulse?Settings=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)

    def SavePulseSettings(self, settings):
        """ Saves a Pulse settings to the database.
            Input: settings: Json object of the Pulse settings.
            Returns: Success message.
        """
        settings = json.dumps(settings)
        
        body = '{"Command":"savesettings", "PulseSettings":'+settings+'}'
        
        return self.connectionProperties.__put__("/api/pulse", body)
        
    def GetPulseInfoSettings(self, name):
        """ Gets a Pulse info settings.
            Input: name: The Pulse name.
            Returns: The Pulse info settings.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Settings=true&Info=true")

    def GetPulseInfoSettingsList(self, names = None):
        """ Gets a list of Pulse info settings.
            Input: name: The Pulse names to be retrieved. If None then gets all Pulse info settings.
            Returns: The Pulse info settings.
        """
        script = "/api/pulse"
        if names != None:
            script = script+"?Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script) 
        
    def DeletePulse(self, name):
        """ Deletes the Pulse instance associated with the name provided.
            Input: name: The Pulse name to delete.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/pulse?Name="+name)