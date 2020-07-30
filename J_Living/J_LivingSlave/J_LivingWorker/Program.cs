using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Net.Sockets;


namespace J_LivingWorker
{
    class Program
    {
        static void Main(string[] args)
        {

            //设置信息
            J_JobManage j_JobManage = J_JobManage.GetJ_JobManage();
            j_JobManage.Job_start();

            Console.WriteLine("ip:"+ j_JobManage.worker.workerIp);
            Console.WriteLine("port:" + j_JobManage.worker.workerPort);
            Console.WriteLine("worker:" + j_JobManage.worker.workerName);
            Console.WriteLine("Start worker");
            J_NetWork WorkerServer = new J_NetWork(j_JobManage.worker.workerIp, j_JobManage.worker.workerPort);
            //Console.ReadKey();这里不会运行
        }
    }
    
}
