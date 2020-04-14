#coding=utf8
import subprocess
from threading import Thread
import time
MAX_LOG_SZ=2048

def STIME():
    return bytes(time.strftime("%m-%d %H:%M:%S "),encoding="utf8")
class Daemon:
    started=False
    mexec=[]
    mcwd=""
    Logbuffer=b""
    Dthread=None
    child=None
    lastTime=int(time.time()*10)
    ENCODE="utf8"
    logcnt=0
    def __init__(self,exec,cwd):
        self.mexec,self.mcwd=exec,cwd
        self._startLoop()
        pass
    def pLog(self,l:bytes):
        self.logcnt=self.logcnt+1
        if self.logcnt>MAX_LOG_SZ:
            self.Logbuffer=self.Logbuffer[self.Logbuffer.find('\n')+1:]+l
            self.logcnt=MAX_LOG_SZ
        else:
            self.Logbuffer=self.Logbuffer+l
        self.lastTime=int(time.time()*10)
    def proc(self):
        while True:
            if self.started:
                s=self.child.poll()
                if s!=None:
                    #died
                    if s==0:
                        self.pLog(STIME()+b"--- exited ---\n")
                        self.started=False
                    else:
                        #schedule restart
                        if self.started:
                            self.pLog(STIME()+b"--- died %d ---\n"%s)
                            self.started=False
                            time.sleep(3)
                            self.start()
                    continue
                print("before")
                x=self.child.stdout.readline()
                print("end")
                self.pLog(x)
            else:
                time.sleep(1)
        pass
    def _startLoop(self):
        self.Dthread=Thread(target=self.proc)
        self.Dthread.setDaemon(True)
        self.Dthread.start()
        pass
    def stop(self):
        if self.started==False:
            return False
        self.pLog(STIME()+b"--- stopped ---\n")
        self.started=False
        self.child.kill()
        pass
    def start(self):
        if self.started:
            return False
        self.started=True
        self.pLog(STIME()+b"--- started ---\n")
        try:
            self.child=subprocess.Popen(self.mexec,cwd=self.mcwd,bufsize=-1,shell=False,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        except Exception as e:
            self.pLog(STIME()+b"--- error ---"+bytes(repr(e),encoding=self.ENCODE)+b"\n")
    def getLog(self):
        return self.Logbuffer
    def input(self,i):
        if self.started==False:
            return False
        self.child.stdin.write(i)
        self.child.stdin.write(b'\n')
        self.child.stdin.flush()