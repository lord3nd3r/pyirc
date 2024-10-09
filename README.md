PyIRC - IRC Client in Python

PyIRC is a simple IRC client written in Python that provides basic IRC functionalities similar to irssi. This client allows you to connect to an IRC server, join multiple channels, and interact with other users in a terminal-based environment. The interface is built using the curses library for a dynamic and interactive text-based UI.

Features

Multiple Channel Management: You can join multiple channels and switch between them seamlessly.

Terminal-based User Interface: Uses curses to provide an interactive UI similar to irssi.

Configuration File: Keeps configuration settings in the user's home directory for easy customization.

Basic Command Support: Supports commands for joining channels, sending messages, and switching between channels.

Installation

Prerequisites

Python 3.x

curses library (included in standard Python library for Unix-based systems)

Clone the Repository

$ git clone https://github.com/yourusername/pyirc.git
$ cd pyirc

Configuration

The configuration file is automatically created in your home directory as .pyirc_config when you first run the script. The default configuration looks like this:

[DEFAULT]
Server = irc.libera.chat
Port = 6667
Nickname = PyIrssiUser
Channel = #testchannel

You can manually edit this file to set your preferred server, port, nickname, and default channel.

Usage

To start the IRC client, simply run the script:

$ python pyirc.py

Keyboard Shortcuts and Commands

/join <channel>: Joins a specified channel.

Example: /join #examplechannel

/msg <target> <message>: Sends a private message to a specific user or channel.

Example: /msg user123 Hello!

/quit: Disconnects from the IRC server and closes the client.

/1, /2, ...: Switches to the specified channel by its index.

Example: /1 switches to the first channel in the list.

/next: Switches to the next channel in the list.

/prev: Switches to the previous channel in the list.

Channel Identification

Each channel window displays its number and name at the top, making it easier to identify which channel you are currently in. For example:

Channel 1: #examplechannel

How It Works

Configuration Loading: The script reads the configuration from the .pyirc_config file in the user's home directory. If the file doesn't exist, it creates a default configuration.

Socket Connection: The client uses a socket to connect to the specified IRC server and port.

Multi-Channel Support: The client allows you to join multiple channels and switch between them using commands.

Curses-based UI: The UI is divided into two parts: the chat window and the input window. The chat window displays messages, while the input window allows you to type commands and messages.

Code Overview

IRCClient Class: The main class that handles the connection to the server, joining channels, sending and receiving messages, and managing the user interface.

load_config(): Loads the configuration from the .pyirc_config file.

connect(): Establishes the connection to the IRC server.

join_channel(channel): Joins a specified channel and creates a new window for it.

switch_channel_by_index(idx): Switches to the channel at the specified index.

irc_listen(): Listens for incoming messages from the IRC server and displays them in the appropriate channel window.

Known Limitations

No Scripting Support: Unlike irssi, PyIRC does not support scripting or plugins.

Limited Theming: The UI is text-based and does not support extensive theming options like irssi.

No Logging: Currently, there is no built-in logging functionality to save chat history.

Future Improvements

Add Logging: Implement chat logging to save conversations to a file.

Improve Theming: Add color options and customizable themes.

Multi-Server Support: Allow connecting to multiple servers simultaneously.
