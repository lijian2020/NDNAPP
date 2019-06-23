
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

    @staticmethod
    def facemod(FaceMod_suffix_list):
        nodeid = OSCommand.getnodeid()
        if (FaceMod_suffix_list[1] == '0x0001'):  # destroy a face
            command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face destroy {1}". \
                                                     format(nodeid, FaceMod_suffix_list[0])], shell=True)
            return command_output

        elif (FaceMod_suffix_list[1] == '0x0000'):  # add a create
            command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face create {1}". \
                                                     format(nodeid, FaceMod_suffix_list[0])], shell=True)
            print("=========333333333===========")
            return command_output
