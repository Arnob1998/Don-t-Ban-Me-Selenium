import sys
from matplotlib import projections
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os, time
import subprocess
from fake_useragent import UserAgent
# MUST - the browser from cmd run must match the browser in webdriver, match - incognito, useragent, port
# cmd_custom_session = '"{}" --remote-debugging-port={} --user-data-dir="{}" --user-agent="{}"'.format(dir_exe_chrome,port,dir_file_chrome_profile,self.userAgent)
class BrowserControl:
    dir_root = os.getcwd()
    port = 9222
    ua = UserAgent()
    userAgent = ua.random

    def __init__(self,  useragentspoofing = True, incognito = True, browserprofilemodee = True):
        self.browserprofilemodee = browserprofilemodee
        self.useragentspoofing = useragentspoofing
        self.incognito = incognito
        pass

    def halt(self,seconds):
        print("---------------------------------------------------")
        print("Enterning sleep mode for {} seconds".format(seconds))
        for i in range(seconds):
            time.sleep(1)
            print("Time elapsed : {} | Time remaining {}".format(i,seconds-i))
        print("---------------------------------------------------")

    def create_custom_session(self,dir_exe_chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        dir_exe_chrome = dir_exe_chrome
        dir_file_chrome_profile = self.dir_root + r"\chrome data"
        port = self.port

        cmd_dir_profile = '--user-data-dir="{}"'.format(dir_file_chrome_profile)
        cmd_useragent = '--user-agent="{}"'.format(self.userAgent)
        cmd_mode = "--incognito"
        # must maintain serial
        status_mode = [self.browserprofilemodee, self.useragentspoofing, self.incognito]
        status = [cmd_dir_profile, cmd_useragent, cmd_mode]

        cmd_custom_session = '"{}" --remote-debugging-port={}'.format(dir_exe_chrome,port)

        for i in range(len(status_mode)):
            if status_mode[i]:
                cmd_custom_session += " " + status[i]

        print("\tStarting custom browser")
        print("Running command: {}".format(cmd_custom_session))
        process = subprocess.Popen(cmd_custom_session, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

    def connect_to_session(self):
        dir_gecko_exe = self.dir_root + "/chromedriver_102.exe"
        port = self.port
        
        if not (os.path.exists(dir_gecko_exe)):
            print("Invalid gecko path")
            sys.exit(1)
    
        service = Service(dir_gecko_exe)

        print("\n\tSetting up browser")

        chrome_options = webdriver.ChromeOptions()
        print("Setting port - {}".format(port))
        chrome_options.add_experimental_option("debuggerAddress","localhost:{}".format(port))

        if self.useragentspoofing:
            print("Setting user agent - {}".format(self.userAgent))
            chrome_options.add_argument('--user-agent="{}"'.format(self.userAgent))

        if self.incognito:
            print("Creating session in incognito mode")
            chrome_options.add_argument("--incognito")

        print("\n\tBrowser Capabiliteies:")
        capabilities = chrome_options.to_capabilities()

        for item in capabilities:
            print("{} : {}".format(item,capabilities[item]))
            if type(capabilities[item]) == dict:
                for item1 in capabilities[item]:
                    print("{} : {}".format(item1,capabilities[item][item1]))

        print("\n\tConnect to remote browser:")
        driver = webdriver.Chrome(service=service, options= chrome_options)
        print("Driver connected to remote browser")
        print("Session ID : {}".format(driver.session_id))
        print("User Agent : {}".format(driver.execute_script("return navigator.userAgent")))

        return driver

    def get_driver(self):
        self.create_custom_session()

        print("Waiting for browser to start the extension")
        self.halt(5)

        return self.connect_to_session()