在ubuntu的環境下使用seleium(Firefox)噴錯 selenium.common.exceptions.WebDriverException: Message: Process unexpectedly closed with status 1
好像是因為權限關係(?) Firefox不允許使用root權限執行(也可能是系統認為目前是在terminal下執行且試圖啟動firefox)
需要把seleium.options套件換成如get_all_train.py內的寫法
