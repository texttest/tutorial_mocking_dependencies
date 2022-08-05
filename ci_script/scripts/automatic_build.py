#!/usr/bin/env python

import os, sys, time, subprocess
from smtplib import SMTP

class Builder:
    def __init__(self):
        logName = ".build" + time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.logDir = os.path.join("logs", logName)
        if not os.path.isdir(self.logDir):
            os.makedirs(self.logDir)
        self.childProcesses = []
        
    def run(self):
        if not os.path.isdir("source"):
            return sys.stderr.write("No source directory found, not building\n")

        print("Updating source ...")
        updateLog = os.path.join(self.logDir, "src_update")
        cmdArgs = [ "git", "pull", "-u", "../repo" ]
        subprocess.call(cmdArgs, stdout=open(updateLog, "w"), stderr=subprocess.STDOUT, cwd="source")

        if self.shouldBuild(updateLog):
            print("Updated files found, starting build ...")
            self.buildAll()
        else:
            print("No files updated, not building")
        print("(Refer to logs under", self.logDir, "for more information.)")

    def shouldBuild(self, updateLog):
        for line in open(updateLog):
            if "updated" in line:
                return True
        return False

    def buildAll(self):
        self.buildOn("localhost")
        self.buildOn("my_other_machine")
        print("Waiting for remote builds...")
        sys.stdout.flush()
        while len(self.childProcesses) > 0:
            runningProcesses = []
            for proc, logFile in self.childProcesses:
                retcode = proc.poll()
                if retcode is not None:
                    self.checkBuild(logFile, retcode)
                else:
                    runningProcesses.append((proc, logFile))
            time.sleep(0.5)
            self.childProcesses = runningProcesses
        
    def buildOn(self, machine):
        logFile = os.path.join(self.logDir, "log." + machine)
        codePath = os.path.abspath("source")
        sourceFile = os.path.join(codePath, "main.c")
        targetPath = os.path.join(codePath, "program." + machine)
        cmdArgs = [ "gcc", "-o", targetPath, sourceFile ]
        if machine != "localhost":
            cmdArgs = [ "ssh", machine ] + cmdArgs
        print("Starting build on " + machine)
        sys.stdout.flush()
        try:
            proc = subprocess.Popen(cmdArgs, stdout=open(logFile, "w"), stderr=subprocess.STDOUT)
            self.childProcesses.append((proc, logFile))
        except OSError as e:
            open(logFile, "w").write("Compiler could not be run\n" + str(e) + "\n")
            self.checkBuild(logFile, 1)
    
    def checkBuild(self, logFile, retcode):
        if retcode > 0:
            resultString = " FAILED!"   
            errMsg = open(logFile).read()
            subject = "The build is broken - please check!"
            body = "Short information about the errors in log file \n'" + logFile + "' : \n\n => " + errMsg
            self.sendMail(subject, body)
        else:
            resultString = " SUCCEEDED!"
 
        print("Build on " + logFile.split(".")[-1] + ":" + resultString)
        sys.stdout.flush()
   
    def sendMail(self, subject, body):
        smtp = SMTP()
        smtp.connect("localhost")
        fromAddr = os.getenv("USER") + "@localhost"
        toAddr = os.getenv("USER")
        mailContents = "From: " + fromAddr + "\nTo: " + toAddr + "\n" + \
                       "Subject: " + subject + "\n\n" + body
        smtp.sendmail(fromAddr, toAddr, mailContents)
        smtp.quit()


if __name__ == "__main__":
    program = Builder()
    program.run()
    
