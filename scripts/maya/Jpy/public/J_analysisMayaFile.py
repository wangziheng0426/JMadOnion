# -*- coding:utf-8 -*-
# 解析maya文件,获取参考节点
import maya.standalone
import maya.cmds as cmds
import sys
import subprocess
import os,re,json
class J_analysisMayaFile(object):
    def __init__(self,mayaFile):
        self.mayaFile=mayaFile
        
    def analysisFile(self):
        maya.standalone.initialize(name=u'python')
        try:
            # 打开 Maya 文件
            refs=[]
            cmds.file(self.mayaFile, open=True,prompt=False, force=True)
            # 获取所有引用文件
            for item in cmds.file(query=True, reference=True):
                refNone=cmds.referenceQuery(item,rfn=1)
                refs.append({refNone:item})
            return refs
        except Exception as e:
            print(u"Error parsing references:"+e)
            return []
        finally:
            # 关闭 Maya 的 Python 环境
            maya.standalone.uninitialize()
    def getRefsFiles(self):
        # 如果是ma直接打开,查找所有参考文件路径
        res=[]
        if self.mayaFile.endswith(u'.ma'):
            with open(self.mayaFile,'r') as f:
                line=f.readline()
                while line:
                    node_match = re.search(r'-rfn "([^"]+)"', line)
                    file_match = re.search(r'"([^"]+\.(?:ma|mb))"', line)  
                    
                    if node_match and file_match:
                        res.append({node_match.group(1):file_match.group(1)})
                    line=f.readline()
                    if line.find('requires')!=-1:
                        break
        elif self.mayaFile.endswith('.mb'):
            mayapy_path=cmds.__file__.split('Python')[0].replace('\\','/')+'bin/mayapy.exe'
            #mayapy_path='C:/Program Files/Autodesk/Maya2022/bin/mayapy.exe'
            script_path=os.path.abspath(__file__).replace('\\','/')
            #script_path='D:/evenPro/MadOnion/maya/Jpy/public/J_analysisMayaFile.py'
            # 构建命令
            cmd = [mayapy_path, script_path, self.mayaFile]
            # 调用 mayapy.exe 解析 Maya 文件
            process = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode != 0:
                #print(f"Error parsing references: {err}")
                return []
            # 解析输出
            # 打开保存的文件
            s=out.decode('utf-8')
            print(s)
            rr=re.findall(r'@xx@.+@xx@',s)
            if rr:
                res=json.loads(res[0].replace('@xx@',''))
        return res

    # def start_analysis_thread(self):
    #     analysis_thread = threading.Thread(target=self.getRefs,)
    #     analysis_thread.start()
# 调用示例
# temp=Jpy.public.J_analysisMayaFile(r'Y:\yingjiao\v.mb')
# ff=temp.getRefs()
    # 调用mayapy.exe解析maya文件
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: mayapy parse_references.py <path_to_maya_file>")
        sys.exit(1)

    maya_file = sys.argv[1]
    temp = J_analysisMayaFile(maya_file)
    references = temp.analysisFile()
    # 写入文件
    print('@xx@'+json.dumps(references)+"@xx@")
