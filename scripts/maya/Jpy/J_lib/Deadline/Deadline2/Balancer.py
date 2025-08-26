from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Balancer:
    """
        Class used by DeadlineCon to send Balancer requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetBalancerNames(self):
        """ Gets all the Balancer names.
            Returns: The list of Balancer names.
        """
        return self.connectionProperties.__get__("/api/balancer?NamesOnly=true")

    def GetBalancerInfo(self, name):
        """ Gets a Balancer info.
            Input: name: The Balancer name.
            Returns: The Balancer info.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Info=true")

    def GetBalancerInfos(self, names = None):
        """ Gets a list of Balancer infos.
            Input: name: The Balancer names to be retrieved. If None then gets all Balancer infos.
            Returns: The Balancer infos.
        """
        script = "/api/balancer?Info=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SaveBalancerInfo(self, info):
        """ Saves a Balancer info to the database.
            Input: info: Json object of the Balancer info.
            Returns: Success message.
        """
        info = json.dumps(info)
        
        body = '{"Command":"saveinfo", "BalancerInfo":'+info+'}'
        
        return self.connectionProperties.__put__("/api/balancer", body)
        
    def GetBalancerSettings(self, name):
        """ Gets a Balancer settings.
            Input: name: The Balancer name.
            Returns: The Balancer settings.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Settings=true")

    def GetBalancerSettingsList(self, names = None):
        """ Gets a list of Balancer settings.
            Input: name: The Balancer names to be retrieved. If None then gets all Balancer settings.
            Returns: The Balancer settings.
        """
        script = "/api/balancer?Settings=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)

    def SaveBalancerSettings(self, settings):
        """ Saves a Balancer settings to the database.
            Input: settings: Json object of the Balancer settings.
            Returns: Success message.
        """
        settings = json.dumps(settings)
        
        body = '{"Command":"savesettings", "BalancerSettings":'+settings+'}'
        
        return self.connectionProperties.__put__("/api/balancer", body)
        
    def GetBalancerInfoSettings(self, name):
        """ Gets a Balancer info settings.
            Input: name: The Balancer name.
            Returns: The Balancer info settings.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Settings=true&Info=true")

    def GetBalancerInfoSettingsList(self, names = None):
        """ Gets a list of Balancer info settings.
            Input: name: The Balancer names to be retrieved. If None then gets all Balancer info settings.
            Returns: The Balancer info settings.
        """
        script = "/api/balancer"
        if names != None:
            script = script+"?Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)
        
    def DeleteBalancer(self, name):
        """ Deletes the Balancer instance associated with the name provided.
            Input: name: The Balancer name to delete.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/balancer?Name="+name)