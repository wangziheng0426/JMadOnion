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
        List<J_JsonJobData> jobList = new List<J_JsonJobData>();
        bool slaveState = false;
        int runningJob =0;
        public J_SlaveSetting slave = new J_SlaveSetting();
        J_SoftWareSetting softWares = new J_SoftWareSetting();
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
            J_CreateJob();

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
            if(operation == "start_slave")
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
            Thread slaveThread = new Thread(J_JobRuning);
            if (slaveState)
            {
                slaveThread.Start();
            }
            else
            {
                slaveThread.Abort();
            }
        }

        public void J_JobRuning()
        {
            foreach (J_JsonJobData item in jobList)
            {
                if (item.job_state == "waiting")
                {
                    foreach (J_softWareData itemSoft in softWares.softList)
                    {

                    }
                    System.Diagnostics.Process p = new System.Diagnostics.Process();
                    p.StartInfo = new System.Diagnostics.ProcessStartInfo(@"c:\ffmpeg.exe");
                    p.StartInfo.Arguments = "/c dir";
                    p.StartInfo.RedirectStandardOutput = true;
                    p.StartInfo.UseShellExecute = false;
                    p.Start();
                    //p.WaitForExit();
                    string line = string.Empty;
                    while (true)
                    {
                        System.Threading.Thread.Sleep(1000);
                        line = p.StandardOutput.ReadLine();
                        if (line != null && line.Length > 0)
                        {
                            Console.WriteLine(line);
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }
     
        }
    }

}
