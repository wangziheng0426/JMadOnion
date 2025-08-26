from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Groups:
    """
        Class used by DeadlineCon to send Group requests. Additional
        Group requests related to Slaves can be found in the Slaves.py file.
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetGroupNames(self):
        """ Gets the Group names.
            Returns: The list of Group names.
        """
        return self.connectionProperties.__get__("/api/groups")

    def AddGroup(self, name):
        """ Adds a Group to the repository.
            Params: name: The Group name.
            Returns: Success message.
        """
        body = '{"Group":"'+name+'"}'
        
        return self.connectionProperties.__post__("/api/groups", body)

    def AddGroups(self, names):
        """ Adds some Groups to the repository.
            Params: names: List of Group names to add.
            Returns: Success message.
        """
        body = '{"Group":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/groups", body)
        
    def PurgeGroups(self, replacementGroup="none", groups=[], overwrite=False):
        """ Purges obsolete Groups from repository using the provided replacementGroup. 
        If Overwrite is set, the Groups provided will overwrite the old Groups and the 
        replacementGroup must be a Group in the provided Groups list. If Overwrite is 
        not set, the Groups provided will be added to the repository and obsolete Groups
        will be purged using the replacement Group. If Overwrite is not set, then no Groups
        are required.
        
            Params: replacementGroup: The Group to replace obsolete Groups on purge.
                    groups: The list of Groups to set or add.
                    overwrite: Boolean flag that determines whether we are setting or adding Groups.
            Returns: Success message.
        """
        body = '{"ReplacementGroup":"'+replacementGroup+'", "Group":'+json.dumps(groups)+', "OverWrite":'+json.dumps(overwrite)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def DeleteGroup(self, name):
        """ Removes a Group to the repository.
            Params: name: The Group name.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/groups?Group="+name.replace(' ', '+'))
    
    def DeleteGroups(self, names):
        """ Removes some Groups from the repository.
            Params: names: List of Group names to remove.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/groups?Group="+ArrayToCommaSeparatedString(names).replace(' ','+'))