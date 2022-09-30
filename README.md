
# ev3tg-python
Telegram Client port for EV3Dev written in Python.
## Requirements
 - Configured USB Connection to PC if running for the first time
 - Configured Internet connection
## Installing
To install ev3tg-python, there are 2 variants:
### Visual Studio Code
1. Download the zip or clone the repository
2. Open VS Code in downloaded directory
3. Install [ev3dev-browser](https://github.com/ev3dev/vscode-ev3dev-browser) for VS Code
4. Connect to your EV3 using the extension
5. Connect to EV3DEV ssh
	1. Update all apt libraries using `sudo apt update && sudo apt upgrade`(password: maker)
	2. Install pip using `sudo apt install python3-pip` and then run `pip install telethon pillow`
### Manual installation
1. [Connect to ev3dev's ssh using terminal](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/)
2. Update all apt libraries using `sudo apt update && sudo apt upgrade`(password: maker)
3. Install git using `sudo apt install git`(password: maker)
4. Clone the repository using `git clone https://github.com/f1refa11/ev3tg-python.git`
5. Install pip using `sudo apt install python3-pip` and then install needed libraries using `pip install -r requirements.txt`
## Configuring ev3tg-python
1. Go to https://my.telegram.org/, enter your phone number and then type verification code that will be sent in Telegram.
2. Go to "API development tools"
3. Fill **only** App Title, Short name (description and device type are allowed). 
4. Open config.json from file browser(VS Code) or using nano(ssh) and set api_id and api_hash to values given on telegram site.
5. When running script first time, you will need to type your mobile number in terminal. Then type new verification code from Telegram Desktop Client and your secret code if you have one. After that, a session file will be created.
## Running ev3tg-python
### Visual Studio Code
2. Open `main.py`, press F5, choose EV3DEV, select your device from the list, and then choose "Download and run current file in interactive terminal".
### Manually(ssh)
1. Go to ev3tg-python directory
2. Execute`chmod +x main.py`
3. Run the script using `python3 main.py`
# Issues
**WARNING:** All issues about EV3DEV and NOT ev3tg-python **MUST** be discussed in ev3dev's repository! Issues that are not about ev3tg-python will be deleted.