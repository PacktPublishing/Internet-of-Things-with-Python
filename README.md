#Internet of Things with Python

This is the code repository for [Internet of Things with Python](https://www.packtpub.com/hardware-and-creative/internet-things-python), published by Packt. It contains all the supporting project files necessary to work through the book from start to finish.

##Instructions and Navigation

The code included with this book is meant for use as an aid in performing the exercises and should not be used as a replacement for the book itself.
Used out of context, the code may result in an unusable configuration and no warranty is given.

The commands and instructions will look like the following:
```
==== Interface configurations ====

# ifcfg-enp0s3

TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=no
IPV4_FAILURE_FATAL=no
IPV6INIT=no
NAME=enp0s3
DEVICE=enp0s3
ONBOOT=yes
IPADDR=10.254.254.100
PREFIX=24

# ifcfg-enp0s9

TYPE=Ethernet
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=no
NAME=enp0s9
DEVICE=enp0s9
ONBOOT=yes 

# Enabling interfaces

sudo ifdown enp0s3; sudo ifdown enp0s9; 
sudo ifup enp0s3; sudo ifup enp0s9;
```


##Related OpenStack Products:
* [Smarter Decisions - The Intersection of Internet of Things and Decision Science](https://www.packtpub.com/big-data-and-business-intelligence/smarter-decisions-intersection-internet-things-and-decision-scien)
* [Internet of Things with the Arduino Yún](https://www.packtpub.com/hardware-and-creative/internet-things-arduino-y%C3%BAn)

