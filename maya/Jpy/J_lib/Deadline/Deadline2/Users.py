from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Users:
    """
        Class used by DeadlineCon to send User and UserGroup requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetUserNames(self):
        """ Gets all the User names.
            Returns: The list of User names.
        """
        return (self.connectionProperties.__get__("/api/users?NamesOnly=true"))

    def GetUser(self, name):
        """ Gets a User's info.
            Input:  name: The User's name.
            Returns: The User info.
        """
        result = (self.connectionProperties.__get__("/api/users?Name="+name.replace(' ','+')))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result
    
    def GetUsers(self, names = None):
        """ Gets all the User infos.
            Input: names: The names of the Users you want info for. If None get all Users infos.
            Returns: The list of User infos.
        """
        script = "/api/users"
        if names != None:
            script =script +"?Name=" + ArrayToCommaSeparatedString(names).replace(' ','+')
            
        return (self.connectionProperties.__get__(script))

    def SaveUser(self, info):
        """ Saves a Users info to the database.
            Input:  info: The Json object holding the Users info.
            Returns: Success message, or User name and ID if the User info is for a new User.
        """
        info = json.dumps(info)
            
        return self.connectionProperties.__put__("/api/users", info)

    def DeleteUser(self, name):
        """ Deletes a User.
            Input: name: The Users name (may be a list).
            Returns: Success message.
        """ 
        return self.connectionProperties.__delete__("/api/users?Name=" + ArrayToCommaSeparatedString(name).replace(' ','+'))
        
    def AddUserToUserGroup(self, user,group):
        """ Adds all of the Users given to one or more User Groups.
            Input:  user: The Users to be for the User Group (may be a list).
            group: The User Group (may be a list).
            Returns: Success message.
        """ 
        body = '{"Command":"add","User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
            
        return self.connectionProperties.__put__("/api/usergroups", body)

    def RemoveUserFromUserGroup(self, user,group):
        """ Removes all of the Users given for one or more User Groups.
            Input:  user: The Users to be for the User Group (may be a list).
            group: The User Group (may be a list).
            Returns: Success message.
        """
        body = '{"Command":"remove", "User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/usergroups", body)

    def SetUsersForUserGroups(self, user,group):
        """ Sets all of the Users for one or more User Groups overriding their old lists.
            Input:  user: The Users to be for the User Group (may be a list).
            group: The User Group (may be a list).
            Returns: Success message.
        """ 
        body = '{"Command":"set", "User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/usergroups", body)
        
    def GetUserGroupNames(self):
        """ Gets all the User Group names.
            Returns: The User Group names.
        """
        return (self.connectionProperties.__get__("/api/usergroups"))
        
    def GetUserGroupsForUser(self, user):
        """ Gets all the User Group names for a User.
            Input: The User name.
            Returns: A list of all the names of the User Groups for the User.
        """
        result = (self.connectionProperties.__get__("/api/usergroups?User="+user.replace(' ','+')))
            
        return result
    
    def GetUserGroup(self, name):
        """ Gets the Users for the User Group with the given name.
            Input: The User Group name.
            Returns: The Users for the User Group.
        """
        result = (self.connectionProperties.__get__("/api/usergroups?Name="+name.replace(' ','+')))
            
        return result
        
    def NewUserGroups(self, names):
        """ Creates and saves new User Groups with the given names. If no valid names are given an error will be returned.
            Input: The names for the new User Group names. Any names that match existing user. Group names will be ignored.
            Returns: Success message.
        """
        body = '{"Group":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/usergroups", body)
        
    def DeleteUserGroup(self, name):
        """ Deletes the User Group with the given name.
            Input: The name of the User Group to delete.
            Returns: Success message.
        """
        result = (self.connectionProperties.__delete__("/api/usergroups?Name="+name.replace(' ','+')))
        
        return result