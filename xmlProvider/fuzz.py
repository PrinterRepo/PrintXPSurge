#coding=UTF-8
import os
import time
import random
def generate_random_str(randomlength=16):
	random_str =''
	base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
	length =len(base_str) -1
	for i in range(randomlength):
		random_str +=base_str[random.randint(0, length)]
	return random_str
while True: 
    os.system("del C:\\Crashdump\\*.dmp")
    os.system("py -3 xsd2xml.py -s my.xsd  -e FixedPage -c ") #easy xml

    os.system("copy 1.fpage mb01\\Documents\\1\\Pages >1.txt") #xps 
    os.system("go.bat >1.txt")
    os.system("del mb01\\test.*") 

    os.system("xpsps-fuzz.exe test.xps")    #ps5
    os.system("xpspcl6-fuzz.exe test.xps")  #pcl6
    
    for f1 in os.listdir("C:\\Crashdump"):  #crashdump 
        s="C:\\CrashDump\\"+f1
        os.system("kd.exe -z "+ s +" -c \"!analyze -v;q\" >" +f1+".txt")
        result_sum = open(""+f1+".txt")
        dir="test"
        for line in result_sum:
            line=line.strip("\n")
            if str(line)[0:14]=="SYMBOL_NAME:  ":
                dir=(str(line)[14:]).replace(":","")
                dir=dir.replace("+","")
            if str(line)[0:20]=="FAILURE_BUCKET_ID:  ":
                dir1="whoami\\"+(str(line)[20:54])
                if(os.path.exists("C:\\Users\\fuzz\\Desktop\\xsd2xml\\"+dir1)==False):
                    os.system("mkdir "+dir1)
                dir=dir1+"\\"+dir
            #break
        result_sum.close()
        if(os.path.exists("C:\\Users\\fuzz\\Desktop\\xsd2xml\\"+dir)==False):
            os.system("mkdir "+dir)
        if(len(os.listdir(dir))<20):
            os.system("copy test.xps"+" C:\\Users\\fuzz\\Desktop\\xsd2xml\\"+dir+"\\"+f1+".xps")
        if(len(os.listdir(dir))<10):
            os.system("move "+s+" C:\\Users\\fuzz\\Desktop\\xsd2xml\\"+dir)
            os.system("move "+f1+".txt"+" C:\\Users\\fuzz\\Desktop\\xsd2xml\\"+dir)
        else:
            os.system("del "+f1+".txt")

