
import os
import sys
import platform
import requests
import gzip
import tarfile
import zipfile

def main():
    print(sys.path[0])
    h=Hardware()

    downloadUrl=""
    if h.isMac():
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_darwin_x86_64.tar.gz"
    elif h.isLinux() and h.isIntelCpu() and h.is64BitCpu():
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_x86_64.tar.gz"
    elif h.isLinux() and h.isArmCpu() and h.is64BitCpu():
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_armv64.tar.gz"
    elif h.isLinux() and h.isArmCpu() and not h.is64BitCpu():
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_armv6.tar.gz"
    elif h.isWindows() and h.isIntelCpu and h.is64BitCpu:
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_windows_x86_64.zip"
    elif h.isWindows() and h.isIntelCpu and not h.is64BitCpu:
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_windows_i386.zip"
    elif h.isWindows() and h.isArmCpu:
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_windows_armv6.zip"
    else:
        print("error:unknow system")
        exit(1)

    fileName=downloadUrl[downloadUrl.rindex("/")+1:]
    print(downloadUrl)
    print(fileName)
    r = requests.get(downloadUrl)
    with open(fileName, "wb") as code:
        code.write(r.content)
    
    tar=Tar(fileName)
    target=fileName.replace(".zip","")
    target=fileName.replace(".tgz","")
    target=fileName.replace(".tar.gz","")
    tar.extract(sys.path[0]+"/../"+target)
    os.remove(sys.path[0]+"/hc")
    os.symlink(sys.path[0]+"/../"+target+"/hc", sys.path[0]+"/hc")

class Hardware:
    system = ""
    machine = ""
    architecture = ""

    def __init__(self):
        uname=platform.uname()
        if type(uname)==tuple:
            self.system = uname[0]
            self.machine = uname[4]
            self.architecture = platform.architecture()[0]
        else:
            self.system = uname.system
            self.machine = uname.machine
            self.architecture = platform.architecture()[0]

    def isMac(self):
        return self.system.lower() == "darwin"
    def isLinux(self):
        return self.system.lower() == "linux"
    def isWindows(self):
        return self.system.lower() == "windows"
    def isIntelCpu(self):
        mc=self.machine.lower()
        return mc == "amd64" or mc == "x86_64" or mc == "i386"
    def isArmCpu(self):
        return self.machine.lower().index("arm") > -1
    def is64BitCpu(self):
        return self.architecture.index("64") > -1
class Tar:
    file=""
    def __init__(self,file):
        self.file=file
    def extract(self,target):
        if self.file.endswith(".zip"):
            self.un_zip(target)
        elif self.file.endswith(".tar.gz") or self.file.endswith(".tgz"):
             self.un_tgz(target)
        else:
            print("Error:not support")
    def un_tgz(self,target):
        tar = tarfile.open(self.file)
        if os.path.isdir(target):
            pass
        else:
            os.mkdir(target)
        for name in tar.getnames():
            tar.extract(name, target)
        tar.close()
    def un_zip(self,target):
        zip_file = zipfile.ZipFile(self.file)
        if os.path.isdir(target):
            pass
        else:
            os.mkdir(target)
        for names in zip_file.namelist():
            zip_file.extract(names,target)
        zip_file.close()  
if __name__ == '__main__':
    main()
    

#uname_result(system='Linux', node='VM-0-9-ubuntu', release='5.4.0-72-generic', version='#80-Ubuntu SMP Mon Apr 12 17:35:00 UTC 2021', machine='x86_64', processor='x86_64')
#uname_result(system='Windows', node='DESKTOP-6BV4V7I', release='10', version='10.0.17763', machine='AMD64', processor='Intel64 Family 6 Model 60 Stepping 3, GenuineIntel')
#uname_result(system='Darwin', node='MrKdeMacBook-Pro.local', release='20.5.0', version='Darwin Kernel Version 20.5.0: Sat May  8 05:10:33 PDT 2021; root:xnu-7195.121.3~9/RELEASE_X86_64', machine='x86_64', processor='i386')
#uname_result(system='Linux', node='raspberrypi', release='5.10.11-v7+', version='#1399 SMP Thu Jan 28 12:06:05 GMT 2021', machine='armv7l', processor='')
#uname_result(system='Linux', node='raspberrypi', release='5.10.17-v7l+', version='#1403 SMP Mon Feb 22 11:33:35 GMT 2021', machine='armv7l', processor='')
