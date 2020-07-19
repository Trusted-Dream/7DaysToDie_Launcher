#!/bin/env python
import os
import re
import sys
import requests
import subprocess as prc
import time
import glob as g
from telnetlib import Telnet

class SDTD(object):

    def __init__(self):
        # Discord API
        self.discord = "Discord API"
        # Check home uer. Default environ['USER']
        self.screendir = "/var/run/screen/S-" + os.environ['USER']
        # Please check the game directory.
        self.gamedir = os.environ['HOME'] + "/steamcmd/sdtd"

    def port_check(self):
        p1 = prc.Popen(["lsof"], stdout=prc.PIPE)
        p2 = prc.Popen(["grep", "7Days"], stdin=p1.stdout, stdout=prc.PIPE)
        p3 = prc.Popen(["grep","-E","TCP..:"], stdin=p2.stdout, stdout=prc.PIPE)
        p4 = prc.Popen(["awk", "-F:", "NR==1 {print $2}"], stdin=p3.stdout, stdout=prc.PIPE)
        p5 = prc.Popen(["awk", "{print $1}"], stdin=p4.stdout, stdout=prc.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()
        p4.stdout.close()
        output = p5.communicate()[0].decode('utf-8')
        return output[:-1]

    def proc_check(self):
        p1 = prc.Popen(['ps', 'x'], stdout=prc.PIPE)
        p2 = prc.Popen(["grep", "-v","grep"], stdin=p1.stdout, stdout=prc.PIPE)
        p3 = prc.Popen(["grep", "7DaysToDieServer.x86_64"], stdin=p2.stdout, stdout=prc.PIPE)
        p4 = prc.Popen(["awk","{print $1}"], stdin=p3.stdout,stdout=prc.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()
        output = p4.communicate()[0].decode('utf-8')
        return output[:-1]

    def screen_check(self):
        p1 = prc.Popen(['ps', 'x'], stdout=prc.PIPE)
        p2 = prc.Popen(["grep", "-v","grep"], stdin=p1.stdout, stdout=prc.PIPE)
        p3 = prc.Popen(["grep", "SCREEN"], stdin=p2.stdout, stdout=prc.PIPE)
        p4 = prc.Popen(["awk","{print $1}"], stdin=p3.stdout, stdout=prc.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()
        output = p4.communicate()[0].decode('utf-8')
        return output[:-1]

    def command_help(self):
        lists = (
        "```/help                        この内容を表示します。\n"
        "/server-stop                 7Days to Die サーバを停止します。\n"
        "/server-start                7Days to Die サーバを起動します。\n"
        "/server-restart              7Days to Die サーバを再起動します。\n"
        "/server-status               7Days to Die サーバの状態を表示します。\n"
        "/member                      現在接続しているユーザーを確認します。\n```"
        )
        return lists

    def server_status(self):
        init = 0
        port = self.port_check()
        if port != "":
            port_status_msg = "ポート [" + port + "] で解放されています。"
            init += 1
        else:
            port_status_msg = "ポートは解放されていません。"
            init -= 1

        process = self.proc_check()
        if process != "":
            proc_status_msg = "GAME PID [" + process[:-1] + "] で稼働しています。"
            init += 1
        else:
            proc_status_msg = "プロセスは稼働していません。"
            init -= 1

        screen = self.screen_check()
        if screen != "":
            screen_status_msg = "SCREEN PID [" + screen[:-1] + "] で稼働しています。"
            init += 1
        else:
            screen_status_msg = "スクリーンは稼働していません。"
            init -= 1

        message = port_status_msg + "\n" + proc_status_msg + "\n" + screen_status_msg + "\n"

        return message,init

    def status(self):
        message = self.server_status()[0]
        return message

    def player_joined_check(self):
        status = self.server_status()[1]
        sts_msg = self.server_status()[0]
        if status <= 0:
            msg = "サーバが正常に起動していません。\n" + sts_msg
            return msg
        login_status = []
        member = ""
        with Telnet('localhost',8081) as tn:
            tn.write(b'lp\n')
            time.sleep(1)
            tn.write(b'exit\n')
            login_mem = tn.read_all().decode().split("\n")[16:-1]

            for i in range(len(login_mem)):
                login_status += [login_mem[i].replace('\r','\n')]
                member += login_status[i]

        return member[:-1]

    def start_check(self):
        for i in range(420):
            status = self.server_status()[1]
            if status == 3:
                timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
                payload = {
                    "content" : timemsg + "--- サーバの起動が完了しました。"
                }
                requests.post(self.discord, data=payload)
                sys.exit()

            time.sleep(1)

        else:
            status = self.server_status()[0]
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            payload = {
                "content" : timemsg + "--- サーバの起動に失敗しました。状況を確認してください。\n" + status
            }
            requests.post(self.discord, data=payload)
            sys.exit()

    def stop_check(self):
        for i in range(30):
            status = self.server_status()[1]
            if status == -3:
                timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
                payload = {
                    "content" : timemsg + "--- サーバの停止が完了しました。"
                }
                requests.post(self.discord, data=payload)
                sys.exit()

            time.sleep(1)

        else:
            status = self.server_status()[0]
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            payload = {
                "content" : timemsg + "--- サーバの停止に失敗しました。状況を確認してください。\n" + status
            }
            requests.post(self.discord, data=payload)
            sys.exit()

    def start(self):
        status = self.server_status()[1]
        if status == 3:
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            payload = {
                "content" : timemsg + "--- サーバは既に起動しています。"
            }
            requests.post(self.discord, data=payload)
            sys.exit()

        os.chdir(self.gamedir)
        com1 = prc.run(["screen", "-dmS", "sdtd"], stdout=prc.PIPE)
        time.sleep(2)
        com2 = prc.run(['screen','-S','sdtd','-p','0','-X','exec','/bin/bash','startserver.sh'], stdout=prc.PIPE)
        sys.stdout.buffer.write(com1.stdout)
        time.sleep(2)
        sys.stdout.buffer.write(com2.stdout)

        self.start_check()

    def stop(self):
        prc_chk = self.proc_check()
        scn_chk = self.screen_check()
        status = self.server_status()[1]
        if status == 3:
            message = "say 10秒後サーバを停止します。\n\n".encode('utf-8')
            with Telnet('localhost',8081) as tn:
                tn.write(message)
                time.sleep(10)
                tn.write(b'shutdown\n')
                try:
                    tn.interact()
                except: pass

        if status == -3:
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            payload = {
                "content" : timemsg + "--- サーバは既に停止しています。"
            }
            requests.post(self.discord, data=payload)
            sys.exit()

        if prc_chk != "":
            prc.Popen(['kill', '-9',prc_chk], stdout=prc.PIPE)

        if scn_chk != "":
            prc.Popen(['kill', '-9',scn_chk], stdout=prc.PIPE)
            os.chdir(self.screendir)
            for remove in g.glob("*"):
                os.remove(remove)

        self.stop_check()

#if __name__ == "__main__":
#    sdtd = SDTD()
#    print (sdtd.port_check())
