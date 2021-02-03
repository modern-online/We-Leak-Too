# We-Leak-Too
in collaboration with Leon Eckert

We Leak Too is an overly honest open-source voice assistant with an integrated packet sniffer. Every time a packet goes through its local network, the device will announce it being logged. If a plain-text packet gets intercepted, its contents are read aloud. The device otherwise acts as a regular voice assistant, serving commands, telling the wether, making lame jokes. 

Project's real-time [website](https://weleaktoo.com/)
More about the [project](https://vjnks.com/works/we-leak-too-43).

## parser.py 

The script parses text from intercepted html packets on a local network and sends it to the voice assistant to be spoken aloud. Other types of intercepted packets are directly uploaded to the server via the requests library. 

This repository only deals with physical-object-level tasks. The website infrastructure was made by [Leon Eckert](https://leoneckert.com/) and he should be contacted with questions related to that.

The project was built on Linux (Ubuntu 20.04) and uses the following external dependencies:
1) [Mycroft](https://github.com/mycroftai) open-source voice-assistant framework,
2) [TCPFlow](https://github.com/simsong/tcpflow) to perform real-time packet interception and reconstrcution,
3) [Ettercap](https://github.com/Ettercap/ettercap) for ARP interception 

All the above are standalone installations. 

### IMPORTANT!
The script has to be launched within activated Mycroft's virtual environment (refer to Mycroft documentation on mycroft-message-bus) in order to properly communicate with the framework. 

Other required external Python modules: 
[html2text](https://pypi.org/project/html2text/) (html parser), [watchdog](https://pypi.org/project/watchdog/) (system monitor) 

## pixel_ring

Scripts within the pixel_ring folder are mainly used to opperate an LED Pixel Ring by Adafruit as part of the voice assistant's physical design. 
