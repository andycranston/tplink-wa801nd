# tplink-wa801nd

Use Selenium and Firefox to change the SNMP community strings on a TP-Link TL-WA801ND wireless access point.

## YouTube video

A nice introduction (two minutes and twenty seconds worth):

[Using Selenium and Firefox to set SNMP community strings on a TP-Link TP-WA801ND access point](https://youtu.be/dkGR9WqeOlk)

## What you will need

+ Windows 10
+ A recent Python 3 installation
+ The Selenium package installed in your Python environment
+ The `accesspoint.py` Python program
+ One of more TP-Link TL-WA801ND wireless access points on your network

## Quick start

Copy the `accesspoint.py` Python program to a directory on your Windows 10 system.

Open a Windows command prompt, change to that directory and type:

```
python accesspoint.py --host hostname --read newpublicstring --write newwritestring
```

where:

+ `hostname` is the hostname or IP address of a TP-Link TL-WA801ND wireless access point
+ `newpublicstring` is the new community string you want to set for read access
+ `newwritestring` is the new community string you want to set for write access

By default the `accesspoint.py` program will try and log in as user `admin` with a
password of `admin` as these are the factory defaults.  If the password has been changed (and
it is recommended security practice to change it) then run as:

```
python accesspoint.py --host hostname --pword password --read newpublicstring --write newwritestring
```

and change `password` to the current password.

You can also specify a different user name to login as:

```
python accesspoint.py --host hostname --user username -pword password --read newpublicstring --write newwritestring
```

change `password` as appropriate.

## The code and useful web links

The Python code should be easy enough to understand even for a basic or intermediate Python programmer.

I do recommend looking at the following links:

[SeleniumHQ Browser Automation](https://selenium.dev/)

[Selenium Documentation](https://selenium.dev/selenium/docs/api/py/api.html)

[Selenium with Python](https://selenium-python.readthedocs.io/)

--------------------------------------------------------
End of README.md
