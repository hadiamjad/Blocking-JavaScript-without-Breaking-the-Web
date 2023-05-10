FROM joyzoursky/python-chromedriver
USER root
RUN ls
RUN pip3 install numpy==1.24.3
RUN pip3 install pandas==2.0.1
RUN pip3 install adblockparser==0.7
RUN pip3 install openpyxl==3.1.2
RUN pip3 install pyvirtualdisplay==3.0
RUN pip3 install selenium==4.9.1
RUN pip3 install seaborn==0.12.2
RUN pip3 install tldextract==3.4.1
RUN pip3 install webdriver-manager==3.8.6
RUN pip3 install matplotlib==3.7.1
RUN pip3 install xlrd==2.0.1
RUN pip3 install beautifulsoup4==4.12.2

RUN apt-get update
RUN apt install -y nodejs
RUN apt-get install -y tmux
RUN apt install -y xvfb

WORKDIR /Crawler
COPY . /Crawler
CMD ["/bin/bash"]