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
                jobList.Add(json_JobData);
                res = json_JobData.job_name + "add_job to list";
            }
            return res;
        }
    }

}
