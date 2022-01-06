# Problem 1: Web server (with optional secure communication).
# simplewebserver
Basic HTTP web-server application which can listen on a configurable TCP port and serve both static HTML and dynamically generated HTML
It Checks for an index.html file in the current working directory and serves it else it lists the files in the directory
The servers port is configurable through the terminal

### Run Server
# python3 webserver.py <port>
```
$ git clone https://github.com/W1nterFr3ak/simplewebserver
$ cd simplewebserver
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
$ python3 simplewebserver 8080
```
  ![image](https://user-images.githubusercontent.com/55146805/148377428-3c226593-f182-49f4-83ba-bb57602bc7f5.png)

