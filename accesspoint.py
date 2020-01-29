#! /usr/bin/python3
#
# @(!--#) @(#) accesspoint.py, version 007, 29-january-2020
#
# use Selenium to automate Firefox to login to
# a TP-Link WA801ND access point and change the
# SNMP community read and write strings
#

################################################################################################

#
# imports
#

import sys
import os
import argparse
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException

################################################################################################

#
# constants
#

DEFAULT_IMPLICIT_WAIT   = 5
DEFAULT_LOGFILE         = 'log.txt'
DEFAULT_USERNAME        = 'admin'
DEFAULT_PASSWORD        = 'admin'
DEFAULT_READ_COMMUNITY  = 'public'
DEFAULT_WRITE_COMMUNITY = 'private'

################################################################################################

def logger(msg):
    global progname
    global logfile
    
    now = datetime.datetime.now()

    for handle in [ logfile, sys.stdout ]:    
        print('{}: {} - {}'.format(progname, now, msg.strip()), file=handle)
    
    logfile.flush()
    
    return

################################################################################################

def cleanup(driver):
    global logfile
    
    logger('cleaning up')
    
    driver.quit()
    
    logfile.flush()
    
    sys.exit(0)

################################################################################################

def fixedsleep(delay):
    print('Waiting for {} seconds ...'.format(delay), end='', flush=True)
    
    time.sleep(delay)
    
    print(' done')

    return

################################################################################################

def gettitle(driver, timeout):
    title = driver.title
    
    while title == '':
        if timeout <= 0:
            break
          
        timeout -= 1
      
        time.sleep(0.1)

        title = driver.title

    return title

################################################################################################

def filltextfield(driver, field, value):
    global progname
    
    logger('filling in text field "{}"'.format(field))
    
    fielddict = {
                'username': 'userName',
                'password': 'pcPassword',
                'readcomm': 'rCommunity',
                'setcomm':  'sCommunity',
                }
    
    if field not in fielddict:
        print('{}: unknown field name "{}"'.format(progname, field), file=sys.stderr)
        cleanup(driver)

    try:
        fieldelement = driver.find_element_by_id(fielddict[field])
    except NoSuchElementException:
        print('{}: unable to find field "{}" ({})'.format(progname, field, fielddict[field]), file=sys.stderr)
        cleanup(driver)

    fieldelement.clear()
    fieldelement.send_keys(value)

    return

################################################################################################

def clickbutton(driver, button):
    global progname
    
    logger('clicking button "{}"'.format(button))

    buttondict = {
                 'login':      'loginBtn',
                 'tools':      'menu_tools',
                 'snmp':       'menu_snmp',
                 'enablesnmp': 'snmp_enable',
                 'save':       'saveBtn',
                 'logout':     'menu_logout',
                 }
    
    if button not in buttondict:
        print('{}: unknown button name "{}" ({})'.format(progname, button, buttondict[button]), file=sys.stderr)
        cleanup(driver)
        
    try:
        buttonelement = driver.find_element_by_id(buttondict[button])
    except NoSuchElementException:
        print('{}: unable to button "{}" ({})'.format(progname, button, buttondict[button]), file=sys.stderr)
        cleanup(driver)
    
    buttonelement.click()
    
    return

################################################################################################

def frameswitch(driver, frame):
    global progname

    logger('switching to frame "{}"'.format(frame))
        
    framedict = {
                'menu': 'bottomLeftFrame',
                'main': 'mainFrame',
                }
                
    if frame not in framedict:
        print('{}: unknown frame name "{}"'.format(progname, frame), file=sys.stderr)
        cleanup(driver)

    driver.switch_to.default_content()

    try:        
        driver.switch_to.frame(framedict[frame])
    except NoSuchFrameException:
        print('{}: error switching to frame "{}" ({})'.format(progname, frame, framedict[frame]), file=sys.stderr)
        cleanup(driver)
    
    return        

################################################################################################

def main():
    global progname
    global logfile

    parser = argparse.ArgumentParser()
        
    parser.add_argument('--truncate', help='truncate log file',                                                  action='store_true')
    parser.add_argument('--log',      help='log file name (default "{}")'.format(DEFAULT_USERNAME),              default=DEFAULT_LOGFILE)
    parser.add_argument('--read',     help='read community string (default "{}")'.format(DEFAULT_USERNAME),      default=DEFAULT_READ_COMMUNITY)
    parser.add_argument('--write',    help='write community string (default "{}")'.format(DEFAULT_USERNAME),     default=DEFAULT_WRITE_COMMUNITY)
    parser.add_argument('--user',     help='username to login as (default "{}")'.format(DEFAULT_USERNAME),       default=DEFAULT_USERNAME)
    parser.add_argument('--pword',    help='password to login as (default "{}")'.format(DEFAULT_PASSWORD),       default=DEFAULT_PASSWORD)
    parser.add_argument('--host',     help='host name or IPv4 address of the access point',                      required=True)

    args = parser.parse_args()

    if args.truncate:
        openmode = 'w'
    else:
        openmode = 'a'
        
    logfilename = args.log
    readcomm    = args.read
    writecomm   = args.write
    username    = args.user
    password    = args.pword
    hostname    = args.host
    
    if hostname == '':
        print('{}: value of --host argument is the null string'.format(progname), file=sys.stderr)
        sys.exit(1)
    
    try:
        logfile = open(logfilename, openmode, encoding='utf-8')
    except IOError:
        print('{}: unable to open log file "{}" for writing with mode "{}"'.format(progname, logfilename, openmode), file=sys.stderr)
        sys.exit(1)
                
    logger('starting Firefox web driver')
    driver = webdriver.Firefox()
    
    logger('setting implicit wait')
    driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
    
    logger('maximising window')
    driver.maximize_window()
    
    logger('getting login page')
    driver.get('http://' + hostname + '/')
    
    logger('getting title')
    btitle = gettitle(driver, 50)
    
    if btitle != 'TL-WA801ND':
        logger('this does not look like a TP=Link WA801ND access point')
        logger('browser title is "{}"'.format(btitle))
        cleanup(driver)

    filltextfield(driver, 'username', username)    

    filltextfield(driver, 'password', password)
    
    clickbutton(driver, 'login')
    
    if 'password is incorrect' in driver.page_source:
        logger('unable to login - bad username and password combination')
        cleanup(driver)

    frameswitch(driver, 'menu')

    clickbutton(driver, 'tools')
    clickbutton(driver, 'snmp')
    
    frameswitch(driver, 'main')
        
    clickbutton(driver, 'enablesnmp')
    
    filltextfield(driver, 'readcomm', readcomm)    
    filltextfield(driver, 'setcomm', writecomm)    

    clickbutton(driver, 'save')

    frameswitch(driver, 'menu')
    clickbutton(driver, 'logout')

    logger('switching to alert')    
    alert = driver.switch_to.alert
    
    if alert.text != 'Are you sure to logout?':
        logger('alert box does not contain correct text')
        cleanup(driver)
        
    logger('accepting alert')
    alert.accept()
                
    logger('quitting browser')    
    driver.quit()
    
    logger('done')
    
    logfile.flush()
    logfile.close()
    
    return 0

################################################################################################

progname = os.path.basename(sys.argv[0])

logfile = None

sys.exit(main())

# end of file
