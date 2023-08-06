# Insert your code here.
#coding = utf8
from BlueTest.toolbox import *


from BlueTest.logInit import *
null="null"
import requests,random,time





class apiTest(object):
    def __init__(self,data,encode=""):
        self.data = data
        self.min = 5
        self.max = 10000
        self.headers = self.data[csv_parm.HEADERS]


        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        self.error_list = MainParam.ERROR_LIST
        # self.error_list = ["error","Error","False","false","失败","错误","异常","禁止"]
        self.encode=encode
    def writError(self,data):
        path = "./result/result_error.txt"
        with open(path,"a",encoding='utf8') as file:
            url = re.findall("urlparams:(.*?) response", data)[0]
            all_message = eval(re.findall("response:.*", data)[0].replace("response:", ""))
            data_message = all_message[1]
            message = data_message
            code = ""
            try:
                if "<br" in message:
                    raise "error"
                try:
                    dict_message = eval(data_message)
                    code = str(dict_message["code"])
                    message = str(dict_message["message"])
                except:
                    pass

            except:
                pass
            finally:
                file.write(url + "\t" + code + "\t" + message + "\n")

            pass
    def recordResults(self,data):
        mkdir("./result/")
        with open("./result/data.txt","a",encoding='utf8') as file:
            file.write("%s \n"%(data)+"\n")
        log.logger.info("%s \n"%(data))
        if not self.responseAssert(data):
            errorlog.logger.error("%s \n"%(data))
            self.writError(data)
        # errorlog


    def responseAssert(self,data,error_list=False):
        if "0x000000" in str(data):
            return True
        else:
            return False
        # if not error_list:
        #     error_list = self.error_list
        # for error in error_list:
        #     if error in str(data):
        #         print(error)
        #         return False
        # return True
    def soloRequest(self,body=False,urlparams=False):
        error_list = self.error_list
        time.sleep(1)

        querystring = False
        payload = False

        if self.data[csv_parm.URLPARAMS]:
            querystring = self.data[csv_parm.URLPARAMS]
        if urlparams:
            querystring = urlparams
        if self.data[csv_parm.DATA] != "null":
            payload = self.data[csv_parm.DATA]
        if body:
            payload = body
        if self.data[csv_parm.DATATYPE] == csv_parm.RAW: #处理raw格式数据
            payload = str(payload)
            payload = payload.replace(" '", "\"").replace("' ", "\"").replace("'", "\"")

        # with requests.request(method=self.method, url=self.url, params=body) as response:
        if self.encode:
            if type(querystring) == str:
                querystring = querystring.encode(self.encode)
            if type(payload) == str :
                payload = payload.encode(self.encode)
        with requests.request(method=self.method,url=self.url, params=querystring,data=payload,headers =self.headers) as response :
            state = False
            for error in error_list:
                if error in response.text:
                        return False,response.text
            return True,response.text
    def specifyLength(self,spec_num=False):
        if not spec_num:
            low = self.min
            height = self.max
            mid =  int((low + height) / 2)
            # str(random.randint(10 ** mid, 10 ** (mid + 1)))
            # return int((low + height) / 2)
            return str(random.randint(10 ** mid, 10 ** (mid + 1)))
        else:
            return str(random.randint(10 ** spec_num, 10 ** (spec_num + 1)))
    def deepTemp(self,temp,value,key):
        str_temp = "temp"
        for index, ddd in enumerate(key):  # 置空
            str_temp += "[key[%d]]" % index
        str_temp += "=%s"%(str(value))
        exec(str_temp)

    def limitCheck(self,body,key,urlparams=False):
        temp = copy.deepcopy(body)
        self.deepTemp(temp,self.specifyLength(spec_num=100000),key)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(body=temp)


        self.deepTemp(temp, self.specifyLength(spec_num=1), key)
        if urlparams:
            spec_response_2 = self.soloRequest(urlparams = temp)
        else:
            spec_response_2 = self.soloRequest(body=temp)

        if spec_response_2 == spec_response:
            if urlparams:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)))
                self.recordResults("%s \n"%str(spec_response_2[1]))
            else:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)))
                self.recordResults("%s \n"%str(spec_response_2[1]))
            return True
        self.min = 1
        self.max = 100000
        while abs(self.min - self.max) > 1:
            temp_len = int((self.min + self.max) / 2)
            self.deepTemp(temp, self.specifyLength(), key)
            if urlparams:
                response = self.soloRequest(urlparams = temp)
            else:
                response = self.soloRequest(body=temp)

            log.logger.debug("key:%s max:%s min:%s cur:%s response:%s"%(key,str(self.max),str(self.min),str(temp_len),response))
            if response == spec_response:
                self.max = temp_len
            else:
                self.min = temp_len
        for i in range(self.max + 1, self.min - 2, -1):
            self.deepTemp(temp, self.specifyLength(spec_num=i), key)
            if urlparams:
                response = self.soloRequest(urlparams=temp)
            else:
                response = self.soloRequest(body = temp)
            log.logger.debug("finish check:%s response:%s"%(str(i+1),response))
            if response != spec_response:
                if urlparams:
                    self.recordResults("%s urlparams %s:limit:%s \n" % (self.name, str(key), str(i+1)))
                    self.recordResults("%s \n" % str(spec_response[1]))
                else:
                    self.recordResults("%s  %s:limit:%s \n" % (self.name, str(key), str(i+1)))
                    self.recordResults("%s \n" % str(spec_response[1]))
                return i
        return False
    def exceptionCheck2(self, body, key, urlparams=False):

        if urlparams:
            spec_response = self.soloRequest(urlparams=body)
        else:
            spec_response = self.soloRequest(body)
        # log.logger.debug(body)

        self.recordResults("%s exceptionCheck: 普通请求 urlparams:%s response:%s" % (self.name, str(self.url), spec_response))


    def exceptionCheck(self, body, key, urlparams=False):

        if urlparams:
            spec_response = self.soloRequest(urlparams=body)
        else:
            spec_response = self.soloRequest(body)

        log.logger.debug(body)

        self.recordResults("%s exceptionCheck: 普通请求 urlparams:%s response:%s" % (self.name, str(self.url), spec_response))


        temp = copy.deepcopy(body)
        str_temp="temp"
        for index,value in enumerate(key): #置空
            str_temp+="[key[%d]]"%index
        str_temp += "=\"\""

        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s exceptionCheck: %s为空 urlparams:%s response:%s" % (self.name, key, str(urlparams),spec_response))
        if "type" in key[-1].lower():
            str_temp = "temp"
            for index, value in enumerate(key):  # 置空
                str_temp += "[key[%d]]" % index
            str_temp  += "=\"999999\""
            exec(str_temp)
            if urlparams:
                spec_response = self.soloRequest(urlparams=temp)
            else:
                spec_response = self.soloRequest(temp)
            log.logger.debug(temp)
            self.recordResults(
                "%s exceptionCheck: %sType校验 urlparams:%s response:%s" % (self.name, key, str(urlparams), spec_response))


        str_temp = "temp"
        for index in range(len(key)-1):
            str_temp += "[key[%d]]" % index
        str_temp += ".pop(key[-1])"
        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s exceptionCheck: %s不传 urlparams:%s response:%s" % (self.name, key,str(urlparams) ,spec_response))
    def extrasCheck(self,body,key,urlparams=False):

        temp = copy.deepcopy(body)
        str_temp="temp"
        for index in range(len(key)-1):
            str_temp += "[key[%d]]" % index
        str_temp +='["test"]="test"'
        # for index,value in enumerate(key): #置空
        #     str_temp+="[key[%d]]"%index
        # str_temp += "=\"\""
        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s extrasCheck: %s 额外参数校验 response:%s" % (self.name, key, spec_response))
        # str_temp = "temp"
    def heartBeatTest(self):
        self.headers = self.data[csv_parm.HEADERS]
        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        d = Base()
        if self.data[csv_parm.DATA] != "null" and self.data[csv_parm.METHOD] == "POST":
            body = self.data[csv_parm.DATA]
            try:
                body = eval(body)
            except:
                pass
            keys, values = d.dataGetKeyAndValue(body)
            if not keys:
                self.exceptionCheck2(body, "")
            for key in keys:
                self.exceptionCheck2(body, key)
                break
        if self.data[csv_parm.METHOD] == "GET":
            body = self.data[csv_parm.URLPARAMS]
            keys, values = d.dataGetKeyAndValue(self.data[csv_parm.URLPARAMS])
            if not keys:
                self.exceptionCheck2(body, "")
            for key in keys:
                self.exceptionCheck2(body, key)
                break

    def dataReduction(self,data,limitcheck=True,extras_check=True):
        self.headers = self.data[csv_parm.HEADERS]
        # print(self.headers)
        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        d = Base()
        temp_len = 0
        if self.data[csv_parm.DATA] != "null" and self.data[csv_parm.METHOD] == "POST":
            body = self.data[csv_parm.DATA]
            try:
                body = eval(body)
            except:
                pass

            keys,values = d.dataGetKeyAndValue(body)
            temp_len = 0
            if not keys:
                self.exceptionCheck(body, "")
            for key in keys:
                self.exceptionCheck(body, key)
                break;
                self.exceptionCheck(body, key)
                if limitcheck:
                    for solo in range(3):
                        limit = self.limitCheck(body, key)
                        if limit:
                            break
                if extras_check :
                    if temp_len != len(key):
                        temp_len = len(key)
                        self.extrasCheck(body,key)

            temp_len = 0
        if self.data[csv_parm.METHOD] == "GET":
            body = self.data[csv_parm.URLPARAMS]
            keys, values = d.dataGetKeyAndValue(self.data[csv_parm.URLPARAMS])
            if not keys:
                self.exceptionCheck(body, "")
            for key in keys:
                self.exceptionCheck(body, key)
                break;

                self.exceptionCheck(body, key,urlparams=True)
                if limitcheck:
                    for solo in range(3):
                        limit = self.limitCheck(body, key,urlparams=True)
                        if limit:
                            break
                if extras_check :
                    if temp_len != len(key):
                        temp_len = len(key)
                        self.extrasCheck(body,key)

def initPostMan(name,result_path = "",encode=""):
    path = ""
    result_name = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not result_path:
        if path:
            result_name = name.split("\\")[-1].split("//")[-1].split("/")[-1].split(".")[0]
        else:
            result_name = name.split(".")[0]
        result_path = "./srcdata/%s.csv"%result_name
    if not path:
        test = Postman2Csv("./srcdata/%s.json.postman_collection"%name,resultpath=result_path,encode=encode)
    else:
        test = Postman2Csv(path,resultpath=result_path,encode=encode)

        

    test.run()

def testByCsvData(name,normal_test=True,mkpy=False,limit_check = False,extras_check=True,encode="",case_type="",counter=True,need=0):
    """test API by csv data

        :param name: csv name or csv path.
        :param normal_test: Test open main switch.LV > mkpy,limit_check,extras_check
        :param mkpy: creat .py file(Support 3.X py) . like postman Generate Code .type Bool
        :param limit_check:  Check the length of parameters.Length range 1-100000. It's a waste of time. Close it if it's not necessary. type Bool
        :param extras_check: Adding non-agreed additional parameters for request validation. type Bool
        :param case_type: "HeartTest" ,Single request verification for YApi
        :param need: Requests need to start from the number of interfaces
        Usage::
          >>> import BlueTest
          >>> BlueTest.testByCsvData("test",limit_check=False,extras_check=True)
          >>> BlueTest.testByCsvData("test",case_type="HeartTest",need=5)
        """
    path = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not path:
        test = Csv2Dict("./srcdata/%s.csv" % name)
    else:
        test = Csv2Dict(path)
    d = test.run()
    if not d:
        log.logger.error("CSV serialize False.")
        return False
    start = 0
    if normal_test:
        for i in d:
            if counter:
                print(start, i["Url"], i["Method"])
                if start < need:
                    start += 1
                    continue
            start += 1
            test = apiTest(i, encode=encode)
            if case_type == "HeartTest":
                test.heartBeatTest()
            else:
                test.dataReduction(1, limitcheck=limit_check, extras_check=extras_check)

if __name__ == '__main__':
    pass


