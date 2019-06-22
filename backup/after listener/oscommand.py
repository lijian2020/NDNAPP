
import subprocess


class OSCommand(object):

    @staticmethod
    def getnodeid():
        command_output = subprocess.check_output(["ifconfig | grep eth0"], shell=True)
        nodeid = str(command_output.split(b'-')[0],'utf-8')
        return nodeid




    @staticmethod
    def getface():
        nodeid=OSCommand.getnodeid()
        command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face ". \
                                format(nodeid)], shell=True)
        return command_output


    @staticmethod
    def getFIB():
        nodeid=OSCommand.getnodeid()
        command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc fib | grep / ". \
                                format(nodeid)], shell=True)
        return command_output


