using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;

namespace J_LivingSlave
{
    class J_NetWork
    {
        Socket socketSlave;
        public J_NetWork(Socket _socketSlave)
        {
            socketSlave = _socketSlave;
        }
    }
}
