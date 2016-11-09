import os
import sys
import json
import time
import socket
import threading
from logging import getLogger
from reportlog.log_config import read_config_ini
from utils.log_logger import FWLOG_DEBUG

SERVER = {'smtp_address':'smtp.163.com',
          'smtp_port':'25',
          'send_address':'lo5twind',
          'password':'163456455',
          'gateway_mail':'on'}



class MailConfigFile:

    def __init__(self,path1,path2):
        #self.msmtprc = r'/home/mail/msmtprc/etc/msmtprc'
        #self.muttrc = r'/home/mail/mutt/etc/Muttrc'
        self.__msmtprc = path1
        self.__muttrc = path2

    def update_msmtprc(self,args):
        try:
            content = []
            content.append('account default\n')
            content.append('host %s' % args['smtp_address'] + '\n')
            content.append('port %s' % args['smtp_port'] + '\n')
            content.append('from %s' % args['send_address'] + '\n')
            content.append('auth login\n')
            content.append('tls off\n')
            content.append('user %s' % args['send_address'] + '\n')
            content.append('password %s' % args['password'] + '\n')
            content.append('logfile /usr/local/mail/msmtp/var/log/mmog')
        except e as Exception:
            FWLOG_DEBUG(e)

        with open(self.__msmtprc,'w+') as f:
            for item in content:
                f.write(item)

    def update_muttrc(self,args):
        try:
            content = []
            content.append('set editor="vi"\n')
            content.append('set from=%s' % args['send_address'] + '\n')
            content.append('set realname="BLUEDON-FW"\n')
            content.append('set sendmail="/usr/local/mail/msmtp/bin/msmtp"\n')
            content.append('set use_from=yes')

        except e as Exception:
            FWLOG_DEBUG(e)

        with open(self.__muttrc,'w+') as f:
            for item in content:
                f.write(item)

"""
    Description:
        Using Mysql database to synchronize Send/Post process,
        Where Send process may exists everywhere possible, produce message
        when necessary. Post process is a singleton process receiving the
        message from Send process, then post them to mail server.
"""
UDP_ADDR = '127.0.0.1'
UDP_PORT = 15680

def send_email_msg(source,subject,content):
    """
        Description:
            Insert information of mail to database
        Input:
            source:The source of mail producer
            subject:Subject of mail
            content:Content of mail
    """
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    msg = dict()
    msg['source'] = source
    msg['subject'] = subject
    msg['content'] = content

    try:
        sk.sendto(str(msg), (UDP_ADDR, UDP_PORT))
        FWLOG_DEBUG('sendmail: %s' % msg)
    except Exception as e:
        FWLOG_DEBUG(e)
        FWLOG_DEBUG('msg send:Error %s' % str(msg))
    finally:
        del msg
        sk.close()

def get_mail_socket(addr=UDP_ADDR, port=UDP_PORT):
    """
        Description:
            return a UDP socket for mail message sending and receiving
    """
    try:
        sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sk.settimeout(1)
        sk.bind((addr, port))
        return sk
    except:
        FWLOG_DEBUG('mail socket initial error')
        return None

def post_email_msg(mail):
    """
        Description:
            use mutt to send mail
    """
    # check if mail option is enable, and get receive_address
    config = read_config_ini('Server Config')
    if config['gateway_mail'] == 'on':
        r_addr = config['receive_address']
    else:
        return

    cmd = 'echo -e "%s" | /usr/local/mail/mutt/bin/mutt -s "%s" %s'
    mail_cmd = cmd % (mail['content'],mail['subject'],r_addr)
    getLogger('log_daemon').debug(mail_cmd)
    os.system(mail_cmd)
    pass

"""
    Description:
        LogMail create a thread to process mails in database, the thread fetch a
        record from db everytime, send it, and then delete the record
"""
class LogMail(threading.Thread):
    event = threading.Event()
    def __init__(self):
        super(LogMail,self).__init__()
        self.sk = get_mail_socket()
        self.mail_time = 0

    def run(self):
        if self.sk is None:
            FWLOG_DEBUG('LogMail socket open error...')
            return
        while 1:
            if self.event.isSet():
                FWLOG_DEBUG('EVENT SET:[LOGMAIL:run]')
                getLogger('log_daemon').debug('EVENT SET:[LOGMAIL:run]')
                break
            try:
                # receive from socket every second, but only send mail X(ten)
                # second after last mail had sent
                recv = self.sk.recvfrom(4096)[0]
            except:
                continue

            # send mail to server very X second
            if int(time.time()) - self.mail_time > 10:
                self.mail_time = int(time.time())
                # convert recv str to dict
                import ast
                mail = ast.literal_eval(recv)
                post_email_msg(mail)
                del mail

            del recv

        FWLOG_DEBUG('QUIT:[LOGMAIL:run]')
        getLogger('log_daemon').debug('QUIT:[LOGMAIL:run]')

    def start(self):
        super(LogMail,self).start()
        pass

    def stop(self):
        FWLOG_DEBUG('LOGMAIL stop')
        getLogger('log_daemon').debug('LOGMAIL stop')
        if not self.sk is None:
            self.sk.close()
        self.event.set()
        pass

    # def send_mail(self):
    #     """ get mails from queue and send alternately  """
    #     send_time = time.time()
    #     while 1:
    #         yield = _mail
    #         if _mail is not None:
    #             if time.time() - send_time > SEND_INTERVAL:
    #                 send_time = time.time()





if __name__ == '__main__':
    lm = LogMail()
    lm.run()
    #msmtprc_path = r'/usr/local/mail/msmtp/etc/msmtprc'
    #muttrc_path = r'/usr/local/mail/mutt/etc/Muttrc'
    #MailConfigFile(msmtprc_path,muttrc_path).update_msmtprc(SERVER)
    #MailConfigFile(msmtprc_path,muttrc_path).update_muttrc(SERVER)
