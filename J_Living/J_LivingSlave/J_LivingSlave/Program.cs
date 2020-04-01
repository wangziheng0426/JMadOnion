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
            J_SlaveSetting slave = new J_SlaveSetting();
            J_SoftWareSetting softWares = new J_SoftWareSetting();

            Console.WriteLine("Read setting file");
            
            if (File.Exists(System.IO.Directory.GetCurrentDirectory() + @"/serverSetting.txt"))
            {
                string readSetting = File.ReadAllText(System.IO.Directory.GetCurrentDirectory() + @"/serverSetting.txt");
                try
                { slave = JsonConvert.DeserializeObject<J_SlaveSetting>(readSetting); }
                catch
                {
                }
                
            }
            if (File.Exists(System.IO.Directory.GetCurrentDirectory() + @"/softWareSetting.txt"))
            {
                string readSetting = File.ReadAllText(System.IO.Directory.GetCurrentDirectory() + @"/softWareSetting.txt");
                try
                { softWares = JsonConvert.DeserializeObject<J_SoftWareSetting>(readSetting); }
                catch
                {
                }

            }
            softWares.soft.Add(new J_softWareData("maya", "c:", "2018"));
            softWares.soft.Add(new J_softWareData("max", "c:x", "201x"));
            softWares.saveData();
            slave.saveData();
            //test

            //test

            Console.WriteLine("ip:"+slave.slaveIp);
            Console.WriteLine("port:" + slave.slavePort);
            Console.WriteLine("Start slave");

            Console.ReadKey();
        }
    }
    
}
