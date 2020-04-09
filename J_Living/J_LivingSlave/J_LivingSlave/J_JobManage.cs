using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace J_LivingSlave
{
    class J_JobManage
    {//任务列表
        public List<J_JsonJobData> jobList = new List<J_JsonJobData>();

        private static J_JobManage instance = null;
        private  J_JobManage()
        {
        }
        public static J_JobManage GetJ_JobManage()
        {
            if (instance==null)
            {
                instance = new J_JobManage();
            }
            return instance;
        }
        public string J_JobOperation(string operation, J_JsonJobData json_JobData)
        {
            string res = operation;
            if (operation == "add_job")
            {
                bool notInList = true;
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id) { notInList = false; res = "job id:"+ json_JobData.job_Id + " already in list";break; }
                }
                if (notInList)
                {
                    jobList.Add(json_JobData);
                    res = json_JobData.job_Id + "->" + json_JobData.job_name + ":" + "job added to list";                    
                }
            }
            if(operation=="remove_job")
            {
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id && i.job_name== json_JobData.job_name)
                    {
                        jobList.Remove(i);
                        res = json_JobData.job_Id+"->"+ json_JobData.job_name +":"+ "job_removed";
                    }
                }
            }
            return res;
        }
    }

}
