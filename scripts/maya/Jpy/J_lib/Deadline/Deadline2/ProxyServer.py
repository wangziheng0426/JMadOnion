from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString

import json

class ProxyServer:
    """ Class used by DeadlineCon to send ProxyServer requests.
        Stores the address of the Web Service for use in sending requests.
    """
    URL = "/api/proxyserver"
    
    def __init__( self, connectionProperties ):
        self.connectionProperties = connectionProperties
        
    def GetProxyServerNames( self ):
        """ Gets all Proxy Server names.
            Returns: List of Proxy Server names.
        """
        return self.connectionProperties.__get__( self.URL + "?NamesOnly=true" )
        
    def GetProxyServerInfo( self, name ):
        """ Gets ProxyServerInfo object for a Proxy Server.
            Inputs:
                Name: The Proxy Server's name.
            Returns: ProxyServerInfo object for specified Proxy Server.
        """
        formatted_name = name.replace( ' ', '+' )
        return self.connectionProperties.__get__( self.URL + "?Name=" + formatted_name + "&Info=true" )
        
    def GetProxyServerInfos( self, names=None ):
        """ Gets ProxyServerInfo objects for specified Proxy Servers.
            Inputs:
                Names: Proxy Server names to retrieve Infos for. Gets all Infos if `None`.
            Returns: List of ProxyServerInfo objects for all specified Proxy Servers.
        """
        url = self.URL + '?Info=True'
        if( names != None ):
            url += '&Names=' + ArrayToCommaSeparatedString( names ).replace( ' ', '+' )
        return self.connectionProperties.__get__( url )
        
    def GetProxyServerSettings( self, name ):
        """ Gets ProxyServerSettings object for a Proxy Server.
            Inputs:
                Name: The Proxy Server's name.
            Returns: ProxyServerSettings object for specified Proxy Server.
        """
        formatted_name = name.replace( ' ', '+' )
        return self.connectionProperties.__get__( self.URL + "?Name=" + formatted_name + "&Settings=true" )
        
    def GetProxyServerSettingsList( self, names=None ):
        """ Gets ProxyServerSettings objects for specified Proxy Servers.
            Inputs:
                Names: Proxy Server names to retrieve Settings for. Gets all Settings if `None`.
            Returns: List of ProxyServerSettings objects for all specified Proxy Servers.
        """
        url = self.URL + '?Settings=True'
        if( names != None ):
            url += '&Names=' + ArrayToCommaSeparatedString( names ).replace( ' ', '+' )
        return self.connectionProperties.__get__( url )

    def GetProxyServerInfoSettings( self, name ):
        """ Gets ProxyServerInfoSettings object for a Proxy Server.
            Inputs:
                Name: The Proxy Server's name.
            Returns: ProxyServerInfoSettings object for specified Proxy Server.
        """
        formatted_name = name.replace( ' ', '+' )
        return self.connectionProperties.__get__( self.URL + "?Name=" + formatted_name )
    
    def GetProxyServerInfoSettingsList( self, names=None ):
        """ Gets ProxyServerInfoSettings objects for specified Proxy Servers.
            Inputs:
                Names: Proxy Server names to retrieve InfoSettings for. Gets all InfoSettings if `None`.
            Returns: List of ProxyServerInfoSettings objects for all specified Proxy Servers.
        """
        url = self.URL
        if( names != None ):
            url += '?Names=' + ArrayToCommaSeparatedString( names ).replace( ' ', '+' )
        return self.connectionProperties.__get__( url )
        
    def SaveProxyServerInfo( self, info ):
        """ Saves Proxy Server Info object to the Database.
            Input:
                Info: JSON-serialized ProxyServerInfo object.
            Returns: Success.
        """
        info = json.dumps( info )
        body = '{ "Command": "saveinfo", "ProxyServerInfo": ' + info + ' }'
        return self.connectionProperties.__put__( self.URL, body )
        
    def SaveProxyServerSettings( self, settings ):
        """ Saves Proxy Server Settings object to the Database.
            Input:
                Info: JSON-serialized ProxyServerSettings object.
            Returns: Success.
        """
        settings = json.dumps( settings )
        body = '{ "Command": "savesettings", "ProxyServerSettings": ' + settings + ' }'
        return self.connectionProperties.__put__( self.URL, body )
        
    def DeleteProxyServer( self, name ):
        """ Deletes specified Proxy Server.
            Input:
                Name: The name of the Proxy Server to delete.
            Returns: Success.
        """
        return self.connectionProperties.__delete__( self.URL + '?Name=' + name )