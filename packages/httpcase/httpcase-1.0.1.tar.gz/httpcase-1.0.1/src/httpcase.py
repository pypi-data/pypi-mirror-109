
import os
import sys
import platform
import requests

def main():
    system = platform.uname().system
    machine = platform.uname().machine

    downloadUrl=""
    if system == "Darwin":
        downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_darwin_x86_64.tar.gz"
    elif system == "Linux":
        if machine == "x86_64":
            downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_x86_64.tar.gz"
        elif  "arm" in machine and "64" in machine:
            downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_armv64.tar.gz"
        elif "arm" in machine:
            downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_linux_armv6.tar.gz"
    elif system == "Windows":
        if machine == "AMD64" or machine == "x86_64":
            downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_windows_x86_64.zip"
        if machine == "i386":
            downloadUrl="https://github.com/roseboy/httpcase/releases/download/v1.0.10-beta/httpcase_1.0.10-beta_windows_x86_64.zip"
        elif "arm" in machine:
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




if __name__ == '__main__':
	main()

#uname_result(system='Linux', node='VM-0-9-ubuntu', release='5.4.0-72-generic', version='#80-Ubuntu SMP Mon Apr 12 17:35:00 UTC 2021', machine='x86_64', processor='x86_64')
#uname_result(system='Windows', node='DESKTOP-6BV4V7I', release='10', version='10.0.17763', machine='AMD64', processor='Intel64 Family 6 Model 60 Stepping 3, GenuineIntel')
#uname_result(system='Darwin', node='MrKdeMacBook-Pro.local', release='20.5.0', version='Darwin Kernel Version 20.5.0: Sat May  8 05:10:33 PDT 2021; root:xnu-7195.121.3~9/RELEASE_X86_64', machine='x86_64', processor='i386')
#uname_result(system='Linux', node='raspberrypi', release='5.10.11-v7+', version='#1399 SMP Thu Jan 28 12:06:05 GMT 2021', machine='armv7l', processor='')
#uname_result(system='Linux', node='raspberrypi', release='5.10.17-v7l+', version='#1403 SMP Mon Feb 22 11:33:35 GMT 2021', machine='armv7l', processor='')
