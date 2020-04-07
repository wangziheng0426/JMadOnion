using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Net.Sockets;


namespace J_LivingSlave
{
    class Program
    {
        static void Main(string[] args)
        {

            //设置信息
            J_JobManage j_JobManage = J_JobManage.GetJ_JobManage();
            J_SlaveSetting slave = new J_SlaveSetting();
            J_SoftWareSetting softWares = new J_SoftWareSetting();

            Console.WriteLine("Read setting file");
            
            if (File.Exists(Directory.GetCurrentDirectory() + @"/slaveSetting.txt"))
            {
                string readSetting = File.ReadAllText(Directory.GetCurrentDirectory() + @"/slaveSetting.txt");
                try
                { slave = JsonConvert.DeserializeObject<J_SlaveSetting>(readSetting); }
                catch
                {
                }
                
            }
            slave.saveData(Directory.GetCurrentDirectory() + @"/slaveSetting.txt");
            if (File.Exists(Directory.GetCurrentDirectory() + @"/softWareSetting.txt"))
            {
                string readSetting = File.ReadAllText(Directory.GetCurrentDirectory() + @"/softWareSetting.txt");
                try
                { softWares = JsonConvert.DeserializeObject<J_SoftWareSetting>(readSetting); }
                catch
                {
                    Console.WriteLine("read soft fff");
                }

            }
            softWares.soft.Add(new J_softWareData("maya", "c:", "2018"));
            softWares.soft.Add(new J_softWareData("max", "c:x", "201x"));
            softWares.saveData(Directory.GetCurrentDirectory() + @"/softWareSetting.txt");
            
            //test

            //test

            Console.WriteLine("ip:"+slave.slaveIp);
            Console.WriteLine("port:" + slave.slavePort);
            Console.WriteLine("slave:" + slave.slaveName);
            Console.WriteLine("Start slave");
            J_NetWork SlaveServer = new J_NetWork(slave.slaveIp, slave.slavePort);
            //Console.ReadKey();
        }
    }
    
}
