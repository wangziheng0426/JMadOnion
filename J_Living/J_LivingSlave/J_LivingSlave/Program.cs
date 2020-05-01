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
            

            Console.WriteLine("ip:"+ j_JobManage.slave.slaveIp);
            Console.WriteLine("port:" + j_JobManage.slave.slavePort);
            Console.WriteLine("slave:" + j_JobManage.slave.slaveName);
            Console.WriteLine("Start slave");
            J_NetWork SlaveServer = new J_NetWork(j_JobManage.slave.slaveIp, j_JobManage.slave.slavePort);
            //Console.ReadKey();这里不会运行
        }
    }
    
}
