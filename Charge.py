import time
import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


salary = 0
expend = 0
diff = 0
card1 = 0
card2 = 0
transfer = 0
detail = []
detail2 = []

#disternation mail address
mail_address = "xxx@gmail.com"

# send from (your email address)
mail_address2 = "xxx@gmail.com"

def count(context):
    global salary
    global expend
    global card1
    global card2
    global detail
    global transfer
    global mail_address
    
    if str(context[3]) is str('+'):
        #收入
        salary += int(context[2])
    elif str(context[3]) is str('-'):
        #支出
        expend += int(context[2])
        detail.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+" "+context[2]+"元\n")
    elif str(context[3]) is str('*'):
        #花旗消費
        card1 += int(context[2])
        detail.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+context[2]+"元\n")
        detail2.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+context[2]+"元\n")
    elif str(context[3]) is str('/'):
        #新光消費
        card2 += int(context[2])
        detail.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+context[2]+"元\n")
        
    if str(context[3]) is str('%'):
        #公費-應匯帳款
        transfer += int(context[2])
        detail.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+context[2]+"元\n")
        detail2.append(context[0]+" 於 "+context[4]+" 消費"+context[1]+context[2]+"元(應付費用)\n")
        
def summary(salary,expend,card1,card2,transfer,start_date,end_date):
    month = time.strftime("%b")
    file_name = str(time.strftime("%b")) + "_Charge_Summary.txt"
    f = open(file_name,'w')
    f.writelines("產生時間: "+str(time.strftime("%b %d %Y %H:%M:%S"))+"\n")
    text = "報表產生時間: "+str(time.strftime("%b %d %Y %H:%M:%S"))+"\n"
    f.writelines("計算週期: "+str(start_date)+"-"+str(end_date)+"\n")
    text += "計算週期: "+str(start_date)+"-"+str(end_date)+"\n"
    f.writelines("\n--------------------------------\n")
    text += "--------------------------------\n" 
    f.writelines("總收入金額: "+str(salary)+" 元\n")
    f.writelines("總支出金額: "+str(expend)+" 元\n")
    f.writelines("花旗信用卡消費: "+str(card1)+" 元\n")
    f.writelines("新光信用卡消費: "+str(card2)+" 元\n")
    f.writelines("本次應匯公費帳款為: "+str(transfer)+" 元\n")
    text += "本次應匯帳款為: "+str(transfer)+" 元\n"
    f.writelines("\n\n花旗信用卡消費明細如下:\n")
    text += "\n\n消費明細如下:\n"
    for i in range(0,len(detail)):
        f.writelines(detail[i])
    
    f.close()
    for i in range(0,len(detail2)):
        text +=detail2[i]
    notify(text,mail_address)
    notify(text,mail_address2)

def notify(text,mail_address):
    # --- Email 的收件人與寄件人address ---
    emailfrom = "xx@gmail.com"
    emailto = mail_address
    # # --- Email 附件檔案 Attachment -----------  
    username = "xxx@gmail.com" # --- 寄信的SMTP的帳號----
    password = "xxx" # --- 寄信的SMTP的密碼----

    msg = MIMEMultipart() 
    msg["From"] = emailfrom 
    msg["To"] = emailto 
    # --- Email 的主旨 Subject ---
    msg["Subject"] = "本月花旗信用卡消費明細"
    msg["preamble"] = 'You will not see this in a MIME-aware mail reader.\n' 

    #----- Email 的信件內容 Message ----- 
    part = MIMEText(text, _charset="UTF-8") 

    msg.attach(part)
    # --- 寄件的 SMTP mail server --- 
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    # --- 如果是 Gmail 可使用這行 ---
    # server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    # --- 如果SMTP server 不需要登入則可把 server.login 用 # mark 掉
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
        
    
def main():
    global expend
    global salary
    global card1
    global card2
    global detail
    global transfer
    
    ftpr = open("Charge.txt",'r')
    line = ftpr.readline()
    context2 = line.split(" ")
    start_date = context2[0]

    while line:        
        context = line.split(" ")
        for i in range(0,len(context)):
            try:
                context[i]=context[i].replace("(","")
                context[i]=context[i].replace(")","")
                context[i]=context[i].replace("\n","")
            except:
                pass
        count(context)
        end_date = context[0]
        line = ftpr.readline()

    summary(salary,expend,card1,card2,transfer,start_date,end_date)

if __name__ == "__main__":
    main()


