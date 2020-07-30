using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace J_LivingWorker
{
    class J_JobLogger
    {
        private static readonly J_JobLogger instance = new J_JobLogger();
        public  static J_JobLogger Get_JobLogger()
        {
            return instance;
        }
    }
}
