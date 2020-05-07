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
        public bool jobDone = false;
        J_JsonJobData jobData;
        public J_JobCompute(J_JsonJobData _job, J_softWareData _soft)
        {
            jobData = _job;
            _job.job_state = "running";
            Console.WriteLine(_job.job_name+"start-----------------");
            System.Diagnostics.ProcessStartInfo jobInfo = new System.Diagnostics.ProcessStartInfo();
            jobInfo.FileName = _soft.path;
            jobInfo.Arguments =string.Join(" ",_job.job_args) ;
            jobInfo.RedirectStandardOutput = true;
            jobInfo.UseShellExecute = false;
            jobInfo.CreateNoWindow = false;
            Thread slaveThread = new Thread(J_JobRuning);
            slaveThread.Start(jobInfo);     

        }
        

        public void J_JobRuning(object _jobInfo)
        {

            System.Diagnostics.Process p = new System.Diagnostics.Process();
            p.StartInfo = _jobInfo as System.Diagnostics.ProcessStartInfo;

            p.Start();
            p.WaitForExit();
            if (p.HasExited)
            {
                jobData.job_state = "finished";
                jobDone = true;
            }            
        }
    }
}
