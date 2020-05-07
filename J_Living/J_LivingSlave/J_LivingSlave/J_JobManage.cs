using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Threading;
using System.IO;

namespace J_LivingSlave
{
    class J_JobManage
    {//任务列表
        public List<J_JsonJobData> jobList = new List<J_JsonJobData>();
        List<J_JobCompute> jobComputeList = new List<J_JobCompute>();
        bool slaveState = false;
        public J_SlaveSetting slave = new J_SlaveSetting();
       public J_SoftWareSetting softWares = new J_SoftWareSetting();
        private static readonly J_JobManage instance = new J_JobManage();
        private J_JobManage()
        {
            //读取设置
            Console.WriteLine("Read setting file");
            if (File.Exists(Directory.GetCurrentDirectory() + @"/slaveSetting.txt"))
            {
                string readSetting = File.ReadAllText(Directory.GetCurrentDirectory() + @"/slaveSetting.txt");
                try
                { slave = JsonConvert.DeserializeObject<J_SlaveSetting>(readSetting); }
                catch { }
            }
            else
            {
                slave.saveData(Directory.GetCurrentDirectory() + @"/slaveSetting.txt");
            }
            if (File.Exists(Directory.GetCurrentDirectory() + @"/softWareSetting.txt"))
            {
                string readSetting = File.ReadAllText(Directory.GetCurrentDirectory() + @"/softWareSetting.txt");
                try
                { softWares = JsonConvert.DeserializeObject<J_SoftWareSetting>(readSetting); }
                catch
                {
                    Console.WriteLine("read soft setting");
                }
            }
            else
            {
                softWares.softList.Add(new J_softWareData("ffmpeg", "c:/ffmpeg.exe", "2018"));
                //softWares.soft.Add(new J_softWareData("max", "c:x", "201x"));
                softWares.saveData(Directory.GetCurrentDirectory() + @"/softWareSetting.txt");
            }
        }
        public void Job_start()
        {
            Thread slaveThread = new Thread(J_CreateJob);
            slaveThread.Start();
        }

        public static J_JobManage GetJ_JobManage()
        {
            return instance;
        }
        public List<string> J_GetJobList()
        {
            List<string> res = new List<string>();
            foreach (J_JsonJobData temp in jobList)
            {
                res.Add(temp.ToString());
            }
            return res;
        }
        public string J_JobOperation(string operation, J_JsonJobData json_JobData)
        {
            string res = operation;
            if (operation == "add_job")
            {
                bool notInList = true;
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id) { notInList = false; res = "job id:" + json_JobData.job_Id + " already in list"; break; }
                }
                if (notInList)
                {
                    jobList.Add(json_JobData);
                    res = json_JobData.job_Id + "->" + json_JobData.job_name + ":" + "job added to list";
                }
            }
            if (operation == "remove_job")
            {
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id && i.job_name == json_JobData.job_name)
                    {
                        jobList.Remove(i);
                        res = json_JobData.job_Id + "->" + json_JobData.job_name + ":" + "job_removed";
                        //c#foreach迭代器好像有问题，移除元素后会超出循环范围，以后再解决吧，先break
                        break;
                    }
                }
            }
            if (operation == "start_job")
            {
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id && i.job_name == json_JobData.job_name)
                    {
                        i.job_state = "waiting";
                        res = "set job state to " + operation;
                    }
                }
            }
            if (operation == "stop_job")
            {
                foreach (var i in jobList)
                {
                    if (i.job_Id == json_JobData.job_Id && i.job_name == json_JobData.job_name)
                    {
                        i.job_state = "stop";
                        res = "set job state to " + operation;
                    }
                }
            }
            if (operation == "start_slave")
            {
                slaveState = true;
                res = "slave started";
            }
            if (operation == "stop_slave")
            {
                slaveState = false;
                res = "slave stoped";
            }
            return res;
        }
        void J_CreateJob()
        {
            while (true)
            {
                if (slaveState)
                {
                    int taskCountSetting = int.Parse(slave.slaveTaskNum);
                    Thread.Sleep(5000);
                    if (jobList.Count == 0)
                    {
                        continue;
                    }
                    foreach (J_JsonJobData item in jobList)
                    {
                        if( jobComputeList.Count >= taskCountSetting) continue;
                        J_softWareData job_softData = null;                        
                        if (item.job_state != "waiting")
                        {
                            continue;
                        }
                        foreach (J_softWareData itemSoft in softWares.softList)
                        {
                            if (item.job_softWare == itemSoft.name && item.job_softWareVersion == itemSoft.version)
                            {
                                job_softData = itemSoft;
                            }
                        }
                        if (job_softData == null)
                        {
                            string running_Result = "job soft ware:" + item.job_softWare
                                + " or version:" + item.job_softWareVersion + " not exists";
                            item.job_state = "stop";
                            Console.WriteLine(running_Result);
                        }
                        else
                        {
                            jobComputeList.Add(new J_JobCompute(item, job_softData));
                        }
                    }
                    foreach (var item in jobComputeList)
                    {
                        if (item.jobDone)
                        {
                            Console.WriteLine("xxxx\n\n");
                            jobComputeList.Remove(item);
                            break;
                        }
                    }
                    
                }
            }
        }
    }
}
