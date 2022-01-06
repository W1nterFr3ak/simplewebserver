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
  
  When you navigate to https://127.0.0.1:8080 you will see the following. You can edit the index.html file as much as you want or remove it to allow listing of files on the server.
  
  ## index.html available and served
![image](https://user-images.githubusercontent.com/55146805/148378002-ae78a05f-bcf9-4cf6-ad22-ecb50da0b2e4.png)
  
  ## renamed index.html to index-old.html listing showed
![image](https://user-images.githubusercontent.com/55146805/148378694-0b3656b0-4061-4cb6-82b1-8b818d46c76a.png)

