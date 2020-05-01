using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace J_LivingSlave
{

    class J_JobCompute
    {
        class JobInfo
        {
            public J_JsonJobData jobData;
            public System.Diagnostics.ProcessStartInfo startInfo;
        }

        bool jobDone = false;
        public J_JobCompute(J_JsonJobData _job, J_softWareData _soft)
        {
            _job.job_state = "running";
            System.Diagnostics.ProcessStartInfo jobInfo = new System.Diagnostics.ProcessStartInfo();
            jobInfo.Arguments = "";
            jobInfo.RedirectStandardOutput = true;
            jobInfo.UseShellExecute = false;
            jobInfo.CreateNoWindow = true;
            Thread slaveThread = new Thread(J_JobRuning);
            slaveThread.Start(jobInfo);

            _job.job_state = "finished";
        }
        

        public void J_JobRuning(object _jobInfo)
        {

            System.Diagnostics.Process p = new System.Diagnostics.Process();
            p.StartInfo = _jobInfo as System.Diagnostics.ProcessStartInfo;

            p.Start();
        }
    }
}
