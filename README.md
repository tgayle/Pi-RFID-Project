# Pi-RFID-Project (COP 2006 Innovation Project)

A series of programs that make use of a Raspberry Pi equipped with a PN532 RFID/NFC reader connected via SPI. 

# Requirements:
---------------
- Python 2.7 
- PN532 RFID/NFC Reader (Tested with [ITEAD PN532](https://www.itead.cc/itead-pn532-nfc-module.html))
- libnfc >= 1.7.1
- [libnfc Python bindings](https://github.com/xantares/nfc-bindings)

# Setup:
--------
1. Connect a PN532 via SPI to the GPIO ports on a Raspberry Pi

2. Install [nfc-bindings](https://github.com/xantares/nfc-bindings) first

        git clone https://github.com/xantares/nfc-bindings.git
        cd nfc-bindings
        cmake -DCMAKE_INSTALL_PREFIX=~/.local .
        make install

3. Run these commands in a terminal

        cd ~
        git clone https://github.com/tgayle/Pi-RFID-Project.git
        cd Pi-RFID-Project
        python main.py
    
---
# Current features:

- Read a card's ID
- Add automations
	- Print a message
	- Add python scripts
	- Set HTTP requests (GET, POST)
- Execute automations
- Assign a name to a card
- List all cards
- Web UI for interaction

# Examples:
---
<img src="https://i.imgur.com/KW6CDyt.png" height="252" width=189>


