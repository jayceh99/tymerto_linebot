from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxOptions #for Firefox 
#預先查詢功能 須放入crontab 定期更新快取資料
def find_train_backup():

        start_number = ['1' , "2" , "3" , "4" ,"5" , "6" ,"7" , "8" , "9" , "10" , '11' , '12' , "13" , "15" ,"16" , "17" , "18" , "19" , "20" , '21' , '22' ,'23']
        end_number = ['1' , "2" , "3" , "4" ,"5" , "6" ,"7" , "8" , "9" , "10" , '11' , '12' , "13" , "15" ,"16" , "17" , "18" , "19" , "20" , '21' , '22' ,'23']
 
        ex_start_number = ['1' , "3" , "8" , '12' , "13" , "19" , '22']
        ex_end_number = ['1' , "3" , "8" , '12' , "13" , "19" , '22']
        #for Edge
        car_type_time = '04:00'
        #option = webdriver.EdgeOptions()
        #option.add_argument("headless")
        #driver = webdriver.Edge()
        
        #for Firefox
        
        option = FirefoxOptions()
        option.add_argument("-headless")
        driver = webdriver.Firefox(options=option)
        
        
        for i in start_number:
            for j in end_number:
                    if i == j :
                        continue
                  
                    driver.set_page_load_timeout(10)
                    driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')

                    car_type_select = Select(driver.find_element(by = By.NAME, value='car_type'))
                    car_type_select.select_by_value('')
                    car_type_time_select = Select(driver.find_element(by = By.NAME, value='gotime'))
                    car_type_time_select.select_by_value(car_type_time)
                    start_ = Select(driver.find_element(by = By.NAME, value='start_station'))
                    start_.select_by_value(i)
                    end_ = Select(driver.find_element(by = By.NAME, value='end_station'))
                    end_.select_by_value(j)
                    submmit = driver.find_element(by = By.XPATH , value="//button[@class='btn btn-lg']")
                    submmit.click()
                    data = html.fromstring(driver.page_source)

                    train_all_list = data.xpath("//td[@class='all_time']/text()")
                    path =  '/home/jayce/tymrtro/tymetro_linebot/data/A'+i+'-A'+j+'.txt'
                    f = open(path,'w')
                    f.write(str(train_all_list))
                    f.close()

        #driver.close()
        
        for i in ex_start_number:
            for j in ex_end_number:
                    if i == j :
                        continue
                  
                    driver.set_page_load_timeout(10)
                    driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')

                    car_type_select = Select(driver.find_element(by = By.NAME, value='car_type'))
                    car_type_select.select_by_value('2')
                    car_type_time_select = Select(driver.find_element(by = By.NAME, value='gotime'))
                    car_type_time_select.select_by_value(car_type_time)
                    start_ = Select(driver.find_element(by = By.NAME, value='start_station'))
                    start_.select_by_value(i)
                    end_ = Select(driver.find_element(by = By.NAME, value='end_station'))
                    end_.select_by_value(j)
                    submmit = driver.find_element(by = By.XPATH , value="//button[@class='btn btn-lg']")
                    submmit.click()
                    data = html.fromstring(driver.page_source)

                    train_all_list = data.xpath("//td[@class='all_time']/text()")
                    path =  '/home/jayce/tymrtro/tymetro_linebot/data/A'+i+'-A'+j+'ex.txt'
                    f = open(path,'w')
                    f.write(str(train_all_list))
                    f.close()

        driver.close()
        
if __name__ == '__main__':
    find_train_backup()
