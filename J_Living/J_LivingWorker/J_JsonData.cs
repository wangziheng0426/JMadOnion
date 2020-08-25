using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Net;
using Newtonsoft.Json;

namespace J_LivingWorker
{

    //运算节点设置
    class J_WorkerSetting
    {        
        public string workerName = "";
        public string workerIp = "";
        public string workerPort = "";
        public string workerTaskNum = "";

        public string userName = "";
        public string password = "";


        public string serverIp = "";
        public string serverPort = "";
        public string serverName = "";


        public J_WorkerSetting()
        {
            serverIp = "192.168.1.250";
            serverPort = "6666";
            serverName = "J_server";
            workerName = Dns.GetHostName();            
            workerIp = Dns.GetHostByName(workerName).AddressList[0].ToString();
            workerPort = "6666";
            workerTaskNum = "1";
            userName = "admin";
            password = "admin";
            
        }
        public void readServerSetting(string _settings)
        {
            Type t = this.GetType();
            FieldInfo[] f = t.GetFields();
            
            if (_settings.StartsWith("{"))
            {
                J_WorkerSetting temp = JsonConvert.DeserializeObject<J_WorkerSetting>(_settings);
                foreach (var i in f)
                {
                    i.SetValue(this, i.GetValue(temp));
                }
            }
            else
            {
                string[] temp = { "\n"};
                string[] settingList = _settings.Split(temp, StringSplitOptions.RemoveEmptyEntries);
                foreach (var i in f)
                {
                    foreach (var j in settingList)
                    {
                        if(i.Name==j.Split(':')[0])
                        i.SetValue(this, j.Split(':')[1]);
                    }
                }
            }
            
        }
        public void saveServerSetting(string _path,string _model="json")
        {
            string lines = "";
            if (_model == "json")
            {
                lines = JsonConvert.SerializeObject(this);
                File.WriteAllLines(_path, new string[] { lines, "" });
            }
            else
            {
                Type t=this.GetType();
                FieldInfo[] f = t.GetFields();
                foreach (var i in f)
                {
                     lines += i.Name+":" + i.GetValue(this)+"\n";
                }
                File.WriteAllText(_path,lines);
            }
        }
    }
    //软件设置相关
    class J_SoftWareSetting
    {
        public List<J_softWareData> softList = new List<J_softWareData>();
        public void openSettings(string settings)
        {
            J_SoftWareSetting temp = JsonConvert.DeserializeObject<J_SoftWareSetting>(settings);
        }
        public void saveSettings(string path)
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
        public string job_projectPath;
        public string job_workFile;
        public string job_scriptFile;
        //"waiting" 等待执行  "error" 执行崩溃或者出错 "stop" 未执行，或停止 "running" 运行中,"finished" 已完成
        public string job_state;
        public List<string> job_args;
        public string job_logPath;
        public J_JsonJobData()
        {
            job_Id = 0; job_name = ""; job_softWare = "";
            job_projectPath = ""; job_workFile = ""; job_scriptFile = ""; job_state = "";
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
