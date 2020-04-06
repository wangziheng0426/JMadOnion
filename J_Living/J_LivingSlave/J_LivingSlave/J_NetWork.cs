using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Net.Sockets;
using System.Net;

namespace J_LivingSlave
{
    class J_NetWork
    {
        public Socket socketSlave;
        public IPAddress ip;
        public int port = 0;
        //读取ip和端口
        public J_NetWork(string _ip, string _port)
        {
            socketSlave = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            if (!IPAddress.TryParse(_ip, out ip))
            {
                Console.WriteLine("start slave failed,check ip setting!");
                return;
            }

            if (!int.TryParse(_port, out port))
            {
                Console.WriteLine("start slave failed,check port setting!");
                return;
            }
            socketSlave.Bind(new IPEndPoint(ip, port));
            socketSlave.Listen(10);
            Console.WriteLine("start listening.");
            //开始监听
            while (true)
            {
                Socket _clientSocket = socketSlave.Accept();
                Thread slaveThread = new Thread(ListenClient);
                slaveThread.Start(_clientSocket);
            }

        }
        //执行任务操作
        void ListenClient(object _clientSocket)
        {            

            Console.WriteLine(socketSlave.LocalEndPoint.ToString());
            //客户端通信
            J_Client client = new J_Client(_clientSocket as Socket);
            
        }
    }
    //客户端
    class J_Client
    {
        Socket listenClient;
        private static byte[] result = new byte[4096];
        public J_Client(Socket _socket)
        {
            listenClient = _socket;
            Console.WriteLine("client created");
            while (listenClient.Connected)
            {
                try
                {
                    int dataLength = listenClient.Receive(result);
                    Console.WriteLine("shuju:"+ dataLength);
                    if (dataLength > 0)
                    {
                        Console.WriteLine(Encoding.ASCII.GetString(result, 0, dataLength) + "\n");
                        listenClient.Send(Encoding.UTF8.GetBytes("测试"));
                    }
                    //listenClient.Connected;
                }
                catch
                {
                    //listenClient.Close(); 

                    break;
                }
            }
        }
    }
}
