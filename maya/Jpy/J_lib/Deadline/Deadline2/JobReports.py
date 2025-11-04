from ConnectionProperty import ConnectionProperty

class JobReports:
    """
        Class used by DeadlineCon to send Job Report requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetAllJobReports(self, id):
        """ Gets all types of reports for a single Job.
            Input:  id: The Job ID.
            Returns: The Job reports.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id)

    def GetJobErrorReports(self, id):
        """ Gets all error reports for a single Job.
            Input:  id: The Job ID.
            Returns: The error reports.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=error")

    def GetJobLogReports(self, id):
        """ Gets all log reports for a single Job.
            Input:  id: The Job ID.
            Returns: The log reports.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=log")

    def GetJobRequeueReports(self, id):
        """ Gets all requeue reports for a single Job.
            Input:  id: The Job ID.
            Returns: The requeue reports.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=requeue")

    def GetJobHistoryEntries(self, id):
        """ Gets all history entries for a single Job.
            Input:  id: The Job ID.
            Returns: The history entries.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=history")
        
    def GetAllJobReportsContents(self, id):
        """ Gets contents of all types of reports for a single Job.
            Input:  id: The Job ID.
            Returns: The Job reports contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=allcontents")

    def GetAllJobErrorReportsContents(self, id):
        """ Gets all error reports contents for a single Job.
            Input:  id: The Job ID.
            Returns: The error reports contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=allerrorcontents")

    def GetAllJobLogReportsContents(self, id):
        """ Gets all log reports contents for a single Job.
            Input:  id: The Job ID.
            Returns: The log reports contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=alllogcontents")

    def GetAllJobRequeueReportsContents(self, id):
        """ Gets all requeue reports contents for a single Job.
            Input:  id: The Job ID.
            Returns: The requeue reports contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+id+"&Data=allrequeuecontents")

    def GetJobErrorReportContents(self, jobId, reportId):
        """ Gets the error report contents for a single Job.
            Input:  jobId: The Job ID.
                    reportId: The report ID.
            Returns: The error report contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+jobId+"&ReportID="+reportId+"&Data=errorcontents")

    def GetJobLogReportContents(self, jobId, reportId):
        """ Gets the log report contents for a single Job.
            Input:  jobId: The Job ID.
                    reportId: The report ID.
            Returns: The log report contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+jobId+"&ReportID="+reportId+"&Data=logcontents")

    def GetJobRequeueReportContents(self, jobId, reportId):
        """ Gets the requeue report contents for a single Job.
            Input:  jobId: The Job ID.
                    reportId: The report ID.
            Returns: The requeue report contents.
        """
        return self.connectionProperties.__get__("/api/jobreports?JobID="+jobId+"&ReportID="+reportId+"&Data=requeuecontents")