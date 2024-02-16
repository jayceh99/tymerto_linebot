from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxOptions #for Firefox 
class c_find_train:
    def __init__(self,start_,end_, start_or_arriv_time) -> None:
        self.start_ = start_
        self.end_ = end_
        self.start_or_arriv_time = start_or_arriv_time
        self.start_or_arrive = None
        self.now_ = None
        self.start_station_number = None
        self.end_station_number = None
        self.start_station_express_check = False
        self.end_station_express_check = False
        self.car_type = None
        self.car_type_time = None
        self.start_station_name = None
        self.end_station_name = None
        self.train_all_list = None
        self.last_train = False
        
    def f_check_input(self):
        if '#' in self.start_[0] or '＃' in self.start_[0]:
            self.car_type = '2'
            self.car_type_time = '04:00'
            self.start_ = self.start_.replace('#','').replace('＃','')
            self.f_name_to_number()
            self.f_check_express_train()
            if self.start_station_express_check == False or self.end_station_express_check == False:
                return '輸入的起點或終點站沒有直達車喔！'
        else:
            self.car_type = ''
            self.car_type_time = '04:00'
            self.f_name_to_number()

        if self.start_station_number == None or self.end_station_number == None :
            return '輸入的站名有誤喔！'
        
        if self.start_station_number == self.end_station_number :
            return '輸入的起點跟終點相同喔！'

        if "!" in self.start_or_arriv_time or '！' in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('!' , '').replace('！' , '')
            self.start_or_arrive = 1
            self.shift_tmp_i = -5
            self.now_ = False

        elif "@" in self.start_or_arriv_time or '＠' in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('@' , '').replace("＠" , '')
            self.start_or_arrive = 2
            self.shift_tmp_i = -6
            self.now_ = False

        elif '%' in self.start_or_arriv_time:
            self.start_or_arriv_time = datetime.now()
            self.start_or_arriv_time = str(self.start_or_arriv_time.strftime("%H%M"))
            self.start_or_arrive = 1
            self.shift_tmp_i = -5
            self.now_ = True

        else:
            return '輸入的時間格式有錯喔！輸入?查看說明'

        self.start_or_arriv_time = self.start_or_arriv_time[0]+self.start_or_arriv_time[1]+":"+self.start_or_arriv_time[2]+self.start_or_arriv_time[3]+":00"
        self.start_or_arriv_time = datetime.strptime(self.start_or_arriv_time , "%H:%M:%S")


    def f_name_to_number(self):
        
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


    def f_check_express_train(self):
        
        name = {'A1台北車站':'1' , 'A3新北產業園區站':"3" , "A8長庚醫院站":"8" , "A12機場第一航廈站":'12' , "A13機場第二航廈站":"13" , "A18高鐵桃園站":"19" , "A21環北站":'22' }
        for i in name:
            if self.start_station_number == name[i]:
                self.start_station_express_check = True
                break
        for i in name:
            if self.end_station_number == name[i]:
                self.end_station_express_check = True
                break


    def f_find_train(self):
        
        #for Edge
        
        #option = webdriver.EdgeOptions()
        #option.add_argument("headless")
        #driver = webdriver.Edge()
        
        #for Firefox
        
        option = FirefoxOptions()
        option.add_argument("-headless")
        driver = webdriver.Firefox(options=option)
        
        try :
            driver.set_page_load_timeout(10)
            driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')
            car_type_select = Select(driver.find_element(by = By.NAME, value='car_type'))
            car_type_select.select_by_value(self.car_type)
            car_type_time_select = Select(driver.find_element(by = By.NAME, value='gotime'))
            car_type_time_select.select_by_value(self.car_type_time)
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
        except TimeoutException :
            driver.close()
            return '機器人好像出了點問題，請再試一次'
        except Exception as e:
            driver.close()
            return '機器人好像出了點問題'

    def f_search(self):
        next_train = 86400
        tmp_len = len(self.train_all_list)
        #print(self.train_all_list)
        for i in range(0,tmp_len):
            if i%3 == self.start_or_arrive :
                time2 = datetime.strptime(str(self.train_all_list[i])+":00", "%H:%M:%S")
                time_3 = time2 - self.start_or_arriv_time
                if int(time_3.seconds) < next_train:
                    next_train = int(time_3.seconds)
                    tmp_i = i
                    #print(tmp_i)
                if next_train < 1800:
                    break
        if next_train > 10800:
            self.last_train = True
                    
        tmp_i = tmp_i + self.shift_tmp_i
        if self.last_train == True:
            txt = self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+2]+' > '+self.train_all_list[tmp_i+3]+' '+self.train_all_list[tmp_i+1]
            return  txt+'\n這班車是末班車！'
        
        if self.now_ == False:

            if tmp_i+9 > tmp_len :
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+2]+' > '+self.train_all_list[tmp_i+3]+' '+self.train_all_list[tmp_i+1]+'\n'+\
                self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4]+'\n')

            elif tmp_i+2 < 0:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+\
                self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4]+'\n'+self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+' '+self.train_all_list[tmp_i+7])

            else:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+2]+' > '+self.train_all_list[tmp_i+3]+' '+self.train_all_list[tmp_i+1]+'\n'+\
                    self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4]+'\n'+self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+' '+self.train_all_list[tmp_i+7])
        else :
            if tmp_i+12 > tmp_len :

                if tmp_i+8 > tmp_len:
                    txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4])
                else:
                    txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4]+'\n'+\
                    self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+' '+self.train_all_list[tmp_i+7])
                
            elif tmp_i+5 < 0:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+\
                self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+' '+self.train_all_list[tmp_i+7]+'\n'+self.train_all_list[tmp_i+11]+' > '+self.train_all_list[tmp_i+12]+' '+self.train_all_list[tmp_i+10])
            
            else:
                txt = (self.start_station_name+' > '+self.end_station_name+'\n'+self.train_all_list[tmp_i+5]+' > '+self.train_all_list[tmp_i+6]+' '+self.train_all_list[tmp_i+4]+'\n'+\
                    self.train_all_list[tmp_i+8]+' > '+self.train_all_list[tmp_i+9]+' '+self.train_all_list[tmp_i+7]+'\n'+self.train_all_list[tmp_i+11]+' > '+self.train_all_list[tmp_i+12]+' '+self.train_all_list[tmp_i+10])
        
        return txt

def main(text_input):
    check_text = None
    try:
        text_input = text_input.replace(' ','').replace("　",'')
        if ',' in text_input:
            text_input = text_input.split(',')
        elif '，' in text_input:
            text_input = text_input.split('，')
        else:
            int('#')

        if len(text_input) == 2:
            text_input.append('%')

        c_find_train_q = c_find_train(start_=text_input[0] , end_= text_input[1] , start_or_arriv_time= text_input[2])
        check_text = c_find_train_q.f_check_input()
        if check_text != None:
            return check_text
        check_text = c_find_train_q.f_find_train()
        if check_text != None:
            return check_text
        txt = c_find_train_q.f_search()
        return txt
        
    except  :
        return'站名或格式錯誤,輸入?查看說明'

#if __name__ == "__main__":
#    print(main('A2,A17,!1830'))