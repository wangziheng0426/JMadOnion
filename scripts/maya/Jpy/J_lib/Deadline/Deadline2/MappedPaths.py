from ConnectionProperty import ConnectionProperty
import json

class MappedPaths:
    """
        Class used by DeadlineCon to send Mapped Path requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def MapPath(self, path, operatingSystem, region="none"):
        """ Performs path mapping on the given path.
            Params:  path: The path to map.
            operatingSystem: The operating system (Windows, Linux, or Mac), which is used to determine the path that will replace the given path.
            region: The name of the region, which is used to determine which path mapping settings to use.
            Returns: The mapped path.
        """
        return self.MapPaths( [path,], operatingSystem, region )[0]
        
    def MapPaths(self, paths, operatingSystem, region="none"):
        """ Performs path mapping on the given list of paths.
            Params:  paths: The list of paths to map.
            operatingSystem: The operating system (Windows, Linux, or Mac), which is used to determine the path that will replace the given path.
            region: The name of the region, which is used to determine which path mapping settings to use.
            Returns: The list of mapped paths.
        """
        if region:
            body = '{"OS":"' + operatingSystem + '", "Region":"' + region + '", "Paths":'+json.dumps(paths)+'}'
        else:
            body = '{"OS":"' + operatingSystem + '", "Paths":'+json.dumps(paths)+'}'
        
        return self.connectionProperties.__post__("/api/mappedpaths", body)