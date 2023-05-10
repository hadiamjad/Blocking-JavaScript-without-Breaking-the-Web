# Blocking JavaScript without Breaking the Web
`Blocking JavaScript without Breaking the Web
Abdul Haddi Amjad, Zubair Shafiq, Muhammad Ali Gulzar
Proceedings on Privacy Enhancing Technologies Symposium (PETS), 2023`

The ArXiv version of the manuscript is avaibable at : [Blocking JS without Breaking the Web](https://arxiv.org/pdf/2302.01182.pdf)

This repository provides the complete instrumentation to evaluate different JS blocking strategies proposed in the paper. 

## Methodology
In this paper we propose a three step process:
1. **JavaScript Corpus Collection:**  In this process we crawl landing pages of websites using chrome extension to capture network requests and its associated call stacks. Then, each request is labeled using Filter Lists.

2. **Localizing Tracking and Functional JS Code:** We use previously labelled dataset to generate spectra of entites (script and methods) using spectra-based fault localization.
![webcheck](ScreenShots/webcheck.png)

3. **JS Blocking Impact Analysis:** Eventually we use the annotated spectra of entities to try different JS blocking strategies. 
![configs](ScreenShots/Table.png)

4. We report (1) network request count and (2) missing functional tag URLs as a breakage metric.
![breakage](ScreenShots/breakage.png)

## Installation

#### 0. Minimum Requirements
These artifacts are rigrously tested on Macbook with following configuration:
1. Intel core i7 processor
2. 4-core CPU
3. 16 GB Ram
4. 500 GB SSD
   
> Note that the base image in the dockerfile supports `amd64` i.e, x86-64 machines.

##### Python dependency
- numpy==1.24.3
- pandas==2.0.1
- adblockparser==0.7
- openpyxl==3.1.2
- pyvirtualdisplay==3.0
- selenium==4.9.1
- seaborn==0.12.2
- tldextract==3.4.1
- webdriver-manager==3.8.6
- matplotlib==3.7.1
- xlrd==2.0.1
- beautifulsoup4==4.12.2

#### 1. Clone the the github repository
`git clone https://github.com/hadiamjad/Blocking-JavaScript-without-Breaking-the-Web.git` and move in the directory using `cd` command

#### 2. Build the docker using Dockerfile

Make sure Docker has these minimum requirements:
![docker-build](ScreenShots/docker-requirements.png)

Expected time for the build: approximately 50 seconds

Expected image size: 2.05 GB

- This command `docker build -t blockingjs .` will build docker image using Dockerfile.
![docker-build](ScreenShots/1.png)

- Run the docker image using `docker run -it blockingjs`
![docker-run](ScreenShots/2.png)

- Try running `ls` command in the docker terminal and it will list all the files inside this repository.

#### 3. OPTIONAL: Tmux session (You can skip this step if you are already familiar with tmux)
In this tutorial we will be using tmux sessions to create server and client sessions for testing.
Some important commands:
- To create new session `tmux new -s {session-name}`
- To leave existing session `Cntrl + b` followed by `d`
- To join existing session`tmux a -t {session-name}`

### 4. Running above methodology

##### Step 1: Run servers for all configurations
> Make sure your docker build was successful.

- Create new tmux session for running all server `tmux new -s server`. This will automatically join the session as well.

- Run the following command `bash server.sh` this will start all servers for different configurations.
![server](ScreenShots/3.png)

- Leave the `server` session using `Cntrl + b` followed by `d`.

##### Step 2: Running JavaScript Corpus Collection & Localizing Tracking and Functional JS Code

- Create new tmux session for running **JavaScript Corpus Collection & Localizing Tracking and Functional JS Code** using this `tmux new -s client` command. This will automatically join the session as well.

- Now run `cd Control/webpage-crawler-extension` and then once you are inside the directory, simply run `bash client.sh` or `chmod +x ./client.sh` followed by `./client.sh` to start crawler.  


It involves crawlling the landing pages of 10 sample websites listed in 'Control\webpage-crawler-extension\csv\test.csv', then label it using filter lists, print the number of tracking and functional requests count in control setting, eventually run SBFL.py to generate tracking score for other configurations.

Expected time:

Once all steps are complete the output will look like this:
![Control](ScreenShots/4.png)

> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

##### Step 3: Running JS Blocking Impact Analysis
- Using the same tmux session i.e `client`, you can test other configurations. 

Expected time:

###### Testing `ALL` configuration
- Staying inside `client` session.
- Go inside `cd ../../ALL/webpage-crawler-extension` and run `bash client.sh`  or `chmod +x ./client.sh` followed by `./client.sh` .

 This will crawl the landing pages of websites(from previous step) in ALL setting(all tracking, functional and mixed scripts are blocked). This step will crawl the websites, then label it using filter lists, print the number of tracking and functional requests count in ALL setting.  

> Note last two lines report the raw numbers (1) network request count and (2) missing functional tag URLs as a breakage metric. These numbers may vary from screenshot due to dynamic nature of website

The output will look like this(number may vary due to dynamic nature of websites):
![All](ScreenShots/5.png)
> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

###### Testing `TS` configuration
- Staying inside `client` session.

- Go inside `cd ../../TS/webpage-crawler-extension` and run `bash client.sh`  or `chmod +x ./client.sh` followed by `./client.sh` .

 This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TS setting where all tracking scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TS setting. 

> Note last two lines report the raw numbers of (1) network request count and (2) missing functional tag URLs as a breakage metric. These numbers may vary from screenshot due to dynamic nature of website

The output will look like this(number may vary due to dynamic nature of websites):
![ts](ScreenShots/6.png)
> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

###### Testing `MS` configuration
- Staying inside `client` session.
- Go inside `cd ../../MS/webpage-crawler-extension` and run `bash client.sh`  or `chmod +x ./client.sh` followed by `./client.sh` .

 This will crawl the landing pages of websites(from Control setting) using chrome extension configured with MS setting where all mixed scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in MS setting. 

> Note last two lines report the raw numbers of (1) network request count and (2) missing functional tag URLs as a breakage metric. These numbers may vary from screenshot due to dynamic nature of website.

The output will look like this(number may vary due to dynamic nature of websites):
![ts](ScreenShots/7.png)
> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

###### Testing `TMS` configuration
- Staying inside `client` session.
- Go inside `cd ../../TMS/webpage-crawler-extension` and run `bash client.sh`  or `chmod +x ./client.sh` followed by `./client.sh` .

 This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TMS setting where all tracking scripts and mixed scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TMS setting. 

> Note last two lines report the raw numbers of (1) network request count and (2) missing functional tag URLs as a breakage metric. These numbers may vary from screenshot due to dynamic nature of website

The output will look like this(number may vary due to dynamic nature of websites):
![tms](ScreenShots/8.png)
> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

###### Testing `TM` configuration
- Staying inside `client` session.
- Go inside `cd ../../TM/webpage-crawler-extension` and run `bash client.sh`  or `chmod +x ./client.sh` followed by `./client.sh` .

 This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TM setting where all tracking methods are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TM setting. 

> Note last two lines report the raw numbers of (1) network request count and (2) missing functional tag URLs as a breakage metric. These numbers may vary from screenshot due to dynamic nature of website

The output will look like this(number may vary due to dynamic nature of websites):
![tm](ScreenShots/9.png)
> Make sure you have stable internet otherwise it might end up with this error
![server](ScreenShots/internet.png)

###### How to clear state if script crashes
Before reeunning the `client.sh` script, clear the folders inside `server/output` for specific configuration.

### 5. Generating figures
Go back in main directory `cd ../../`
#### Generating `Number of Request` figures for all RQ's
- You can simply run the following command: `python -W ignore requestCountBarPlots.py {Configuration 1} {Configuration 2}` --- here `{Configuration 1}`and `{Configuration 2}` are placeholders. For example:
- RQ4: `python -W ignore requestCountBarPlots.py TMS TM`
- RQ3: `python -W ignore requestCountBarPlots.py TS MS`
- RQ1: `python -W ignore requestCountBarPlots.py ALL`


> This will generate plot pdf in `Figures/BarPlot.pd` 


#### Generating `% Reduction` figures for all RQ's
- You can simply run the following command: `python -W ignore reductionBarPlots.py {Configuration 1} {Configuration 2}` --- here `{Configuration 1}` and `{Configuration 2}` are placeholders. For example: 
- RQ4: `python -W ignore reductionBarPlots.py TMS TM`
- RQ4: `python -W ignore reductionBarPlots.py TS MS`
- RQ4: `python -W ignore reductionBarPlots.py ALL`
> This will generate plot pdf in `Figures/ReductionPlot.pd` 

#### Generating `Distribution Plots` figures for all RQ's
- You can simply run the following command: `python -W ignore requestDistribution.py {Configuration 1}` --- here `{Configuration 1}` is placeholders. For example, if you want to create for RQ2 you can run following command:
 `python -W ignore rrequestDistribution.py TMS`
- This will generate plot pdf in `Figures/DistributionPlot.pd` 

#### Retrieving Figures folder on local to view it
You can run the following command in LOCAL REPOSITORY SHELL to copy the Figures folder to local machine:

`docker cp {container_id}:/Crawler/Figures .` 

The container id is located on the docker shell
![tm](ScreenShots/container.png)

`docker cp  7c486e87b63a:/Crawler/Figures .`

### 6. Artifact Support
- The artifact as of hash `4260a02`
- contact: hadiamjad@vt.edu