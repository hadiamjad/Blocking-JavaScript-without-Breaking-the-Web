# Blocking JavaScript without Breaking the Web
`Blocking JavaScript without Breaking the Web
Abdul Haddi Amjad, Zubair Shafiq, Muhammad Ali Gulzar
Proceedings on Privacy Enhancing Technologies Symposium (PETS), 2023`

The ArXiv version of the manuscript is avaibable at : [Blocking JS without Breaking the Web](https://arxiv.org/pdf/2302.01182.pdf)

This repository provides the complete instrumentation to evaluate different JS blocking strategies proposed in the paper. 

## Methodology
In this paper we propose three step process:
1. JavaScript Corpus Collection:  In process we crawl landing pages of websites using chrome extension to capture network requests and its associated call stacks. Then, each request is labeled using Filter Lists. 

2. Localizing Tracking and Functional JS Code: We use previously labelled dataset to generate spectra of entites (script and methods) using spectra-based fault localization.

3. JS Blocking Impact Analysis: Eeventually we use the annotated spectra of entities to try different JS blocking strategies. We report network request count and missing functional tag URLs as a breakage metric.

## Installation

#### 1. Clone the the github repository
``
#### 2. Build the docker using Dockerfile
- This command `docker build -t BlockingJS .` will build docker image using Dockerfile.
- Run the docker image using `docker run -it BlockingJS`.
- Try running `ls` command in the docker terminal and it will list all the files inside this repository.

#### 3. Tmux session (You can skip this step if you are already familiar with tmux)
In this tutorial we will be using tmux sessions to create server and client sessions for testing.
Some important commands:
- To create new session `tmux new -s {session-name}`
- To leave existing session `Cntrl + b` followed by `d`
- To join existing session`tmux a -t {session-name}`

### 4. Running above methodology
##### Step 1: Run servers for all configurations
- Make sure your docker build was successful and you are inside docker container after running `step 2` and `ls` command shows the content of this repository.
- Create new tmux session for running all server `tmux new -s server`. This will automatically join the session as well.
- Run the following command `./server.sh` this will start all servers for different configurations.
> hadi add image
- Leave the `server` session using `Cntrl + b` followed by `d`.
> hadi add image
##### Step 2: Running JavaScript Corpus Collection & Localizing Tracking and Functional JS Code
- Create new tmux session for running `JavaScript Corpus Collection & Localizing Tracking and Functional JS Code` using this `tmux new -s client` command. This will automatically join the session as well.
> add image
- Now run `cd Control/webpage-crawler-extension` and then once you are inside the directory, simply run `./client.sh` to start crawler. This will crawl the landing pages of 10 sample websites [link here]. This step will first crawl the all websites, then label it using filter lists, print the number of tracking and functional requests count in control setting, eventually run SBFL.py to create spectra of entites with tracking score for other configurations. Once all steps are complete the output will look like this:
> hadi add image
##### Step 3: Running JS Blocking Impact Analysis
- Using the same tmux session i.e `client`, you can test other configurations. 
###### Testing `ALL` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd ALL/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from previous step) in ALL setting(all tracking, functional and mixed scripts are blocked). This step will crawl the websites, then label it using filter lists, print the number of tracking and functional requests count in ALL setting. 
the output will look like this(number may vary due to dynamic nature of websites):
> hadi add image
###### Testing `ALL` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd ALL/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from Control setting) using chrome extension configured with ALL setting where all tracking, functional and mixed scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in ALL setting. 
The output will look like this(number may vary due to dynamic nature of websites):
> hadi add image

###### Testing `TS` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd TS/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TS setting where all tracking scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TS setting. 
The output will look like this(number may vary due to dynamic nature of websites):
> hadi add image

###### Testing `MS` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd MS/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from Control setting) using chrome extension configured with MS setting where all mixed scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in MS setting. 
The output will look like this(number may vary due to dynamic nature of websites):
> hadi add image

###### Testing `TMS` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd TMS/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TMS setting where all tracking scripts and mixed scripts are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TMS setting. 
The output will look like this(number may vary due to dynamic nature of websites):
> hadi add image

###### Testing `TM` configuration
- Staying inside `client` session, run `cd ../../` to go back in the main directory.
- Go inside `cd TM/webpage-crawler-extension` and run `./client.sh` This will crawl the landing pages of websites(from Control setting) using chrome extension configured with TM setting where all tracking methods are blocked. Then label it using filter lists, and print the number of tracking and functional requests count in TM setting. 
The output will look like this(number may vary due to dynamic nature of websites):
> hadi add image

### 5. Generating figures
