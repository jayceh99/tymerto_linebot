from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
from datetime import datetime
from selenium.webdriver import FirefoxOptions #for Firefox 

class c_find_train:
    def __init__(self,start_,end_, start_or_arriv_time) -> None:
        self.start_ = start_
        self.end_ = end_
        self.start_or_arriv_time = start_or_arriv_time
                  
    def f_name_to_number(self):
        self.start_station_number = None
        self.end_station_number = None

        if 'a' in self.start_:
            self.start_ =  self.start_.replace('a','A')
        if 'a' in self.end_:
            self.end_ = self.end_.replace('a','A')
        name = {'A1台北車站':'1' , 'A2三重站':"2" , 'A3新北產業園區站':"3" , 'A4新莊副都心站':"4" , "A5泰山站":"5" , "A6泰山貴和站":"6" ,"A7體育大學站":"7" , 
            "A8長庚醫院站":"8" , "A9林口站":"9" , "A10山鼻站":"10" , "A11坑口站":'11' , "A12機場第一航廈站":'12' , "A13機場第二航廈站":"13" , "A14a機場旅館站":"15" ,
            "A15大園站":"16" , "A16橫山站":"17" , "A17領航站":"18" , "A18高鐵桃園站":"19" , "A19桃園體育園區站":"20" , "A20興南站":'21' , "A21環北站":'22' , "A22老街溪站":'23'}

        for i in name:
            if self.start_ in i:
                self.start_station_number = name[i]
                break
        for i in name:
            if self.end_ in i:
                self.end_station_number = name[i]
                break


    def f_check_input(self):
        if self.start_station_number == None or self.end_station_number == None:
            int('!')
        self.start_or_arrive = None
        if "!" in self.start_or_arriv_time or '！' in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('!' , '').replace('！' , '')
            self.start_or_arrive = 1
            self.shift_tmp_i = -5
            self.now_ = False
            print(1)
        elif "@" in self.start_or_arriv_time or '＠' in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('@' , '').replace("＠" , '')
            self.start_or_arrive = 2
            self.shift_tmp_i = -6
            self.now_ = False
            print(3)
        elif '%' in self.start_or_arriv_time:
            self.start_or_arriv_time = datetime.now()
            self.start_or_arriv_time = str(self.start_or_arriv_time.strftime("%H%M"))
            self.start_or_arrive = 1
            self.shift_tmp_i = -5
            self.now_ = True
            print(2)
        
        else:
            int('@')

        self.start_or_arriv_time = self.start_or_arriv_time[0]+self.start_or_arriv_time[1]+":"+self.start_or_arriv_time[2]+self.start_or_arriv_time[3]+":00"
        self.start_or_arriv_time = datetime.strptime(self.start_or_arriv_time , "%H:%M:%S")


    def f_find_train(self):
        
        #for Edge
        
        option = webdriver.EdgeOptions()
        option.add_argument("headless")
        driver = webdriver.Edge(options=option)
        
        #for Firefox
        '''
        option = FirefoxOptions()
        option.add_argument("-headless")
        driver = webdriver.Firefox(options=option)
        '''
        driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')
        start_ = Select(driver.find_element(by = By.NAME, value='start_station'))
        start_.select_by_value(self.start_station_number)
        end_ = Select(driver.find_element(by = By.NAME, value='end_station'))
        end_.select_by_value(self.end_station_number)
        submmit = driver.find_element(by = By.XPATH , value="//button[@class='btn btn-lg']")
        submmit.click()
        data = html.fromstring(driver.page_source)
        self.start_station_name = data.xpath("//li[@class='start']/text()")[0]
        self.end_station_name = data.xpath("//li[@class='end']/text()")[0]
        self.train_all_list = data.xpath("//td[@class='all_time']/text()")
        driver.close()


    def f_test(self):
        next_train = 86400
        tmp_len = len(self.train_all_list)
        for i in range(0,tmp_len):
            if i%3 == self.start_or_arrive :
                time2 = datetime.strptime(str(self.train_all_list[i])+":00", "%H:%M:%S")
                time_3 = time2 - self.start_or_arriv_time
                if int(time_3.seconds) < next_train:
                    next_train = int(time_3.seconds)
                    tmp_i = i
                if next_train < 1800:
                    break

        tmp_i = tmp_i + self.shift_tmp_i
        print(self.train_all_list[tmp_i+2])
        print(self.train_all_list)
        if self.now_ == False:
            if tmp_i+9 > tmp_len :
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+2]+' > '+self.train_all_list[tmp_i+3]+'\n'+\
                self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+'\n')
            else:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+2]+' > '+self.train_all_list[tmp_i+3]+'\n'+\
                    self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+'\n'+self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9])
        else :
            if tmp_i+12 > tmp_len :
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+'\n'+\
                    self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9])
            else:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+'\n'+\
                    self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+'\n'+self.train_all_list[tmp_i+11]+' > '+self.train_all_list[tmp_i+12])
        
        return txt

def main(text_input):
    #try:
        text_input = text_input.replace(' ','')
        if ',' in text_input:
            text_input = text_input.split(',')
        elif '，' in text_input:
            text_input = text_input.split('，')
        else:
            int('#')

        if len(text_input) == 2:
            text_input.append('%')

        c_find_train_q = c_find_train(start_=text_input[0] , end_= text_input[1] , start_or_arriv_time= text_input[2])
        c_find_train_q.f_name_to_number()
        c_find_train_q.f_check_input()
        c_find_train_q.f_find_train()
        txt = c_find_train_q.f_test()
        return txt
    
    #except Exception as e:
    #    print(e)
    #    return'站名或格式錯誤,輸入?查看說明'

if __name__ == "__main__":
    print(main('A22,A1,!2300'))