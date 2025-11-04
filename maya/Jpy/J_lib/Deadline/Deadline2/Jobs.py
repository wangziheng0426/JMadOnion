import json
import ast
from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString

class Jobs:
    """
        Class used by DeadlineCon to send Job requests. 
        Stores the address of the Web Service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
    
    def GetJobIds(self):
        """    Gets all the Job IDs.
            Returns: The list of IDs.
        """
        return self.connectionProperties.__get__("/api/jobs?IdOnly=true")

    def GetJobs(self, ids = None):
        """    Gets all specified Jobs, or all Jobs if none specified.
            Input: List of Job Ids.
            Returns: The list of Jobs.
        """
        script = "/api/jobs"
        if ids != None:
            script = script +"?JobID=" + ArrayToCommaSeparatedString(ids)
        return self.connectionProperties.__get__(script)

    def CalculateJobStatistics(self, jobID):
        "Gets job statistics for the specified job"
        return self.connectionProperties.__get__("/api/jobs?JobID=" + jobID + "&Statistics=true")

    def GetJobsInState(self, state):
        """    Gets all jobs in the specified state.
            Input: The state. Valid states are Active, Suspended, Completed, Failed, and Pending. Note that Active covers both Queued and Rendering jobs.
            Returns: The list of Jobs in the specified state.
        """
        return self.connectionProperties.__get__("/api/jobs?States=" + state)
        
    def GetJobsInStates(self, states):
        """    Gets all jobs in the specified states.
            Input: The list of states. Valid states are Active, Suspended, Completed, Failed, and Pending. Note that Active covers both Queued and Rendering jobs.
            Returns: The list of Jobs in the specified states.
        """
        return self.connectionProperties.__get__("/api/jobs?States=" + ",".join(states))

    def GetJob(self, id):
        """Gets a Job.
            Input: id: The Job ID (may be a list).
            Returns: The Job/s (list).
        """
        jobId = ArrayToCommaSeparatedString(id)
        
        result = self.connectionProperties.__get__("/api/jobs?JobID="+jobId)
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def SaveJob(self, jobData):
        """    Updates a Job's properties in the database.
            Input: jobData: The Jobs information in json format.
            Returns: Success message.
        """
        jobData = json.dumps(jobData)
        body = '{"Command":"save", "Job":'+jobData+'}'

        return self.connectionProperties.__put__("/api/jobs", body)

    def SuspendJob(self, id):
        """    Suspend a queued, rendering, or pending job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"suspend", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def SuspendJobNonRenderingTasks(self, id):
        """ Suspends the Tasks for a Job that are not in the rendering state.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"suspendnonrendering", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ResumeJob(self, id):
        """    Resumes a job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"resume", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ResumeFailedJob(self, id):
        """    Resumes a failed Job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"resumefailed", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def DeleteJob(self, id):
        """    Deletes a Job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        return self.connectionProperties.__delete__("/api/jobs?JobID="+id)

    def RequeueJob(self, id):
        """    Requeues a Job. All rendering and completed Tasks for the Job will be requeued.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"requeue", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ArchiveJob(self, id):
        """    Archive a non-queued, non-rendering Job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"archive", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ImportJob(self,file):
        """    Imports an archived Job and returns it.
            Input: file: file location for archived Job.
            Returns: Success message.
        """
        body = '{"Command":"import", "File":"'+file+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def PendJob(self, id):
        """    Place a Job with dependencies in the pending state.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"pend", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ReleasePendingJob(self, id):
        """    Releases a pending Job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"releasepending", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def CompleteJob(self, id):
        """    Completes a Job. All incomplete Tasks for the Job will be marked as complete.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"complete", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def FailJob(self, id):
        """    Fails a Job. All incomplete Tasks for the Job will be marked as failed.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"fail", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def UpdateJobSubmissionDate(self, id):
        """    Sets the Job's submission date to the current time.
            Input: id: The Jobs ID.
            Returns: Success message.
        """
        body = '{"Command":"updatesubmissiondate", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def SubmitJobFiles(self, info, plugin, aux = [], idOnly = False):
        """    Submit a new Job using Job info file and plugin info file.
            Input:  info: The location of the Job Info File.
                    plugin: The location of the Plugin Info File.
                    aux: Array of any additional auxiliary submission files, defaults to empty.
                    idOnly: If True, only the Job's ID is returned, defaults to False.
            Returns: The new Job.
        """
        if not isinstance(aux, list):
            aux = [aux]
        
        return self.connectionProperties.__post__("/api/jobs", buildJobSubmission(info, plugin, aux, idOnly))
        
    def SubmitJob(self, info, plugin, aux = [], idOnly = False):
        """    Submit a new Job.
            Input:  info: Dictionary of Job information.
                    plugin: Dictionary of Plugin information for the Job.
                    aux: Array of any additional auxiliary submission files, defaults to empty.
                    idOnly: If True, only the Job's ID is returned, defaults to False.
            Returns: The new Job.
        """
        if not isinstance(aux, list):
            aux = [aux]
        
        body = '{"JobInfo":'+json.dumps(info)+',"PluginInfo":'+json.dumps(plugin)+',"AuxFiles":'+json.dumps(aux)
        if idOnly:
            body += ',"IdOnly":true'
        body += '}'
        return self.connectionProperties.__post__("/api/jobs", body)

    def SubmitJobs(self, jobs=[], dependent=False):
        """    Submits multiple Jobs.
            Input:  jobs: List of Jobs as dictionaries. Job dictionaries should contain the following properties:
                        JobInfo - Dictionary of Job information. Required property.
                        PluginInfo - Dictionary of Plugin information for the Job. Required property.
                        AuxFiles - List of any additional auxiliary submission files (defaults to empty). Required property.
                        DependsOnPrevious - True to make the Job dependent on the previously submitted Job. Defaults to false.
                    dependent: True to make each Job submitted dependent on the previous (except for the first one). Defaults to false.
            Returns: Success message.
        """
        if not isinstance(jobs, list):
            jobs = [jobs]

        body = '{"Jobs":' + json.dumps(jobs) + ',"Dependent":"' + str(dependent).lower() + '"}'
        return self.connectionProperties.__post__( "/api/jobs", body )

    #Machine Limits
    def SetJobMachineLimit(self, id, limit, slaveList, whiteListFlag):
        """    Sets a Job's machine limit.
            Input:  id: The Job ID.
                    limit: The maximum number of Slaves that can work on this Job at any one time.
                    slaveList: A list of Slaves which are either not allowed to work on or are the only allowed Slave for a Job.
                    whiteListFlag: If true the Slaves in the slavelist are the only Slaves allowed to work on the Job else, the Slaves are now allowed to work on the Job.
            Returns: Success message.
        """
        body = json.dumps({"Command":"setjobmachinelimit","JobID":id, "Limit":limit, "SlaveList":slaveList,"WhiteListFlag":whiteListFlag})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def AddSlavesToJobMachineLimitList(self, id, slaveList):
        """    Add additional Slaves to the Jobs limit list.
            Input:  id: The Job ID.
            slaveList: The Slaves to be added to the Jobs machine limit list.
            Returns: Success message.
        """
        body = json.dumps({"Command":"addslavestojobmachinelimitlist","JobID":id, "SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def RemoveSlavesFromJobMachineLimitList(self, id, slaveList):
        """    Remove chosen Slaves from the Jobs limit list.
            Input: id: The Job ID.
            slaveList: The Slaves to be removed from the Jobs machine limit list.
            Returns: Success message.
        """
        body = json.dumps({"Command":"removeslavesfromjobmachinelimitlist","JobID":id,"SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def SetJobMachineLimitListedSlaves(self, id, slaveList):
        """    Sets a Job's machine limit Slave list.
            Input:  id: The Job ID.
            slaveList: A list of Slaves which are either not allowed to work on or are the only allowed Slave for a Job.
            Returns: Success message.
        """
        body = json.dumps({"Command":"setjobmachinelimitlistedslaves","JobID":id, "SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobMachineLimitWhiteListFlag(self, id, whiteListFlag):
        """    Sets a Job's machine limit white list flag.
            Input:  id: The Job ID.
            whiteListFlag: If true the Slaves in the slavelist are the only Slaves allowed to work on the Job else, the Slaves are now allowed to work on the Job.
            Returns: Success message.
        """
        body = json.dumps({"Command":"setjobmachinelimitwhitelistflag","JobID":id, "WhiteListFlag":whiteListFlag})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobMachineLimitMaximum(self, id, limit):
        """    Sets a Job's machine limit maximum number of Slaves.
            Input:  id: The Job ID.
            limit: The maximum number of Slaves that can work on this Job at any one time.
            Returns: Success message.
        """
        body = json.dumps({"Command":"setjobmachinelimitmaximum","JobID":id, "Limit":limit})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def AppendJobFrameRange(self, id, frameList):
        """    Appends to a Job's frame range without affecting the existing Tasks. The only exception is if the Job's chunk size is greater than one, and the last Task is having frames appended to it.
            Input: id: The Job ID.
            frameList: The additional frames to append.
            Returns: Success message.
        """
        body = json.dumps({"Command":"appendjobframerange","JobID":id, "FrameList":frameList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobFrameRange(self, id, frameList, chunkSize):
        """    Modifies a Job's frame range. If the Job is currently being rendered, any rendering Tasks will be requeued to perform this operation.
            Input: id: The Job ID.
            frameList: The frame list.
            chunkSize: The chunk size.
            Returns: Success message.
        """
        body = json.dumps({"Command":"setjobframerange","JobID":id, "FrameList":frameList, "ChunkSize":chunkSize})
    
        return self.connectionProperties.__put__("/api/jobs", body)
        
    #Job Details
    def GetJobDetails(self, ids):
        """ Gets the Job details for the provided Job IDs.
            Input: The Job IDs (may be a list).
            Returns: The Job Details for the valid Job IDs provided.
        """
        script = "/api/jobs"

        script = script +"?JobID=" + ArrayToCommaSeparatedString(ids)+"&Details=true"
        return self.connectionProperties.__get__(script)
        
    #Undelete/Purge Deleted
    def GetDeletedJobs(self, ids = None):
        """ Gets the undeleted Jobs that correspond to the provided Job IDs. If no IDs are provided, gets all the deleted Jobs.
            Input: The Job IDs (optional, may be a list).
            Returns: The Job/s (list).
        """
        script = "/api/jobs?Deleted=true"
        
        if ids != None:
            script = script +"&JobID=" + ArrayToCommaSeparatedString(ids)
        return self.connectionProperties.__get__(script)
            
    def GetDeletedJobIDs(self):
        """    Gets all the deleted Job IDs.
            Returns: The list of deleted Job IDs.
        """
        return self.connectionProperties.__get__("/api/jobs?IdOnly=true&Deleted=true")
        
    def PurgeDeletedJobs(self, ids):
        """ Purges the deleted Jobs that correspond to the provided IDs from the deleted Job collection.
            Input: The deleted Job IDs (may be a list).
            Returns: Success message.
        """
        script = "/api/jobs?Purge=true"
        
        script = script +"&JobID=" + ArrayToCommaSeparatedString(ids)
        return self.connectionProperties.__delete__(script)
        
    def UndeleteJob(self, id):
        """    Undeletes deleted Job.
            Input: id: The Job ID.
            Returns: Success message.
        """
        body = '{"Command":"undelete", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def UndeleteJobs(self, ids):
        """    Undeletes deleted Jobs.
            Input: id: The Job IDs.
            Returns: Success message.
        """
        body = json.dumps({"Command":"undelete","JobIDs":ids})
        
        return self.connectionProperties.__put__("/api/jobs", body)
        
def buildJobSubmission(info, plugins, aux, idOnly):
    
    infoText = fileRead(info)
    
    pluginsText = fileRead(plugins)
    
    body = '{"JobInfo":'+infoText+',"PluginInfo":'+pluginsText+',"AuxFiles":'+json.dumps(aux)
    if idOnly:
        body += ',"IdOnly":true'
    body += '}'
    
    return body
    
def fileRead(filelocation):
    
    file = open(filelocation, 'r')
    
    obj = '{'
    
    for line in file:
        
        line = line.replace('\n', '')
        line = line.replace('\t', '')
        
        tokens = line.split("=",1)
        if len(tokens) == 2:
            obj = obj + '"'+tokens[0].strip()+'":"'+tokens[1].strip()+'",'
        
    obj = obj[:-1]
    
    obj = obj + '}'
    
    return obj