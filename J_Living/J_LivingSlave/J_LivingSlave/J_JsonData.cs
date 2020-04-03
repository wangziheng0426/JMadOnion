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
    class J_JsonData
    {
    }
    class J_SlaveSetting
    {
        public string serverIp ="";
        public string serverPort = "";
        public string serverName = "";

        public string slaveName = "";
        public string slaveIp = "";
        public string slavePort = "";               

        public string userName = "";
        public string password = "";
        public J_SlaveSetting()
        {
            serverIp = "192.168.1.250";
            serverPort = "6666";
            serverName = "J_server";
            slaveName = Dns.GetHostName();            
            //slaveIp = Dns.GetHostAddresses(slaveName)[4].MapToIPv4().ToString();
            slaveIp = Dns.GetHostByName(slaveName).AddressList[0].ToString();
            //IPAddress[] ff= Dns.GetHostByName(slaveName).AddressList;
            //IPAddress[] aa = Dns.GetHostAddresses(slaveName);
            //foreach (IPAddress i in aa)
            //{
            //    Console.WriteLine(i.ToString());
                
            //}
            slavePort = "6666";
            userName = "admin";
            password = "admin";
            
        }
        public void saveData(string path)
        {
            string lines= JsonConvert.SerializeObject(this);
            File.WriteAllLines(path, new string[]{ lines,""});
        }
    }
    class J_SoftWareSetting
    {
        public List<J_softWareData> soft = new List<J_softWareData>();
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
}
