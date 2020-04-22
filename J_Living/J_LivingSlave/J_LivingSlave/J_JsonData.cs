using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using Newtonsoft.Json;

namespace J_LivingSlave
{

    //运算节点设置
    class J_SlaveSetting
    {
        public string serverIp ="";
        public string serverPort = "";
        public string serverName = "";

        public string slaveName = "";
        public string slaveIp = "";
        public string slavePort = "";
        public string slaveTaskNum = "";

        public string userName = "";
        public string password = "";
        public J_SlaveSetting()
        {
            serverIp = "192.168.1.250";
            serverPort = "6666";
            serverName = "J_server";
            slaveName = Dns.GetHostName();            
            slaveIp = Dns.GetHostByName(slaveName).AddressList[0].ToString();
            slavePort = "6666";
            slaveTaskNum = "1";
            userName = "admin";
            password = "admin";
            
        }
        public void saveData(string path)
        {
            string lines= JsonConvert.SerializeObject(this);
            File.WriteAllLines(path, new string[]{ lines,""});
        }
    }
    //软件设置相关
    class J_SoftWareSetting
    {
        public List<J_softWareData> softList = new List<J_softWareData>();
        public void saveData(string path)
        {
            string lines = JsonConvert.SerializeObject(this);
            File.WriteAllLines(path, new string[] { lines, "" });
        }
    }
    class J_softWareData
    {
        public string name;
        public string path;
        public string version;
        public J_softWareData(string _name, string _path, string _version)
        {
            name = _name; path = _path; version = _version;
        }
    }
    //任务设置
    class J_JsonJobData
    {
        public int job_Id;
        public string job_name;
        public string job_softWare;
        public string job_softWareVersion;
        public string job_workFilePath;
        public string job_workFile;
        public string job_scriptFile;
        public string job_state;
        public List<string> job_args;
        public string job_logPath;
        public J_JsonJobData()
        {
            job_Id = 0; job_name = ""; job_softWare = "";
            job_workFilePath = ""; job_workFile = ""; job_scriptFile = ""; job_state = "";
            job_args = new List<string>(); job_logPath ="";
        }
        public override string ToString()
        {
           return JsonConvert.SerializeObject(this);
        }
        //public J_JsonJobData(int _job_Id,string _job_name,string _job_workFilePath, string _job_workFile, string _job_scriptFile, List<string> _job_args)
        //{
        //    job_Id = _job_Id; job_name = _job_name; job_workFilePath = _job_workFilePath; job_workFile = _job_workFile;
        //    job_scriptFile = _job_scriptFile; job_args = _job_args;
        //}
    }
}
