import socket
import threading
import os
import configparser
import curses
from curses import textpad

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".pyirssi_config")

class IRCClient:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.config = self.load_config()
        self.server = self.config['DEFAULT']['Server']
        self.port = int(self.config['DEFAULT']['Port'])
        self.nickname = self.config['DEFAULT']['Nickname']
        self.channels = []
        self.current_channel_idx = 0
        self.windows = {}
        self.irc_socket = None

    def load_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(CONFIG_FILE):
            config['DEFAULT'] = {
                'Server': 'irc.libera.chat',
                'Port': '6667',
                'Nickname': 'PyIrssiUser',
                'Channel': '#testchannel'
            }
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        else:
            config.read(CONFIG_FILE)
        return config

    def connect(self):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect((self.server, self.port))
        self.irc_socket.send(f"NICK {self.nickname}\r\n".encode("UTF-8"))
        self.irc_socket.send(f"USER {self.nickname} 0 * :{self.nickname}\r\n".encode("UTF-8"))

    def join_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)
            self.irc_socket.send(f"JOIN {channel}\r\n".encode("UTF-8"))
            self.create_channel_window(channel)
        self.switch_channel_by_name(channel)

    def create_channel_window(self, channel):
        height, width = self.stdscr.getmaxyx()
        chat_win = curses.newwin(height - 3, width, 0, 0)
        input_win = curses.newwin(3, width, height - 3, 0)
        textpad.rectangle(self.stdscr, height - 4, 0, height - 1, width - 1)
        self.stdscr.refresh()
        self.windows[channel] = {'chat': chat_win, 'input': input_win}

    def switch_channel_by_name(self, channel):
        if channel in self.channels:
            self.current_channel_idx = self.channels.index(channel)
            self.refresh_ui()

    def switch_channel_by_index(self, idx):
        if 0 <= idx < len(self.channels):
            self.current_channel_idx = idx
            self.refresh_ui()

    def switch_channel_next(self):
        self.current_channel_idx = (self.current_channel_idx + 1) % len(self.channels)
        self.refresh_ui()

    def switch_channel_prev(self):
        self.current_channel_idx = (self.current_channel_idx - 1) % len(self.channels)
        self.refresh_ui()

    def refresh_ui(self):
        current_channel = self.channels[self.current_channel_idx]
        chat_win = self.windows[current_channel]['chat']
        input_win = self.windows[current_channel]['input']
        chat_win.clear()
        input_win.clear()
        chat_win.addstr(0, 0, f"Channel {self.current_channel_idx + 1}: {current_channel}")
        chat_win.refresh()
        input_win.refresh()

    def irc_listen(self):
        while True:
            try:
                response = self.irc_socket.recv(4096).decode("UTF-8")
                if response:
                    if response.startswith("PING"):
                        self.irc_socket.send(f"PONG {response.split()[1]}\r\n".encode("UTF-8"))
                    else:
                        self.display_message(response)
            except Exception as e:
                self.display_message(f"Error: {e}")
                break

    def display_message(self, message):
        current_channel = self.channels[self.current_channel_idx]
        chat_win = self.windows[current_channel]['chat']
        chat_win.addstr(message + "\n")
        chat_win.refresh()

    def run(self):
        # Initialize curses
        curses.curs_set(0)
        self.stdscr.clear()

        # Connect to the IRC server
        self.connect()

        # Start listener thread
        listener_thread = threading.Thread(target=self.irc_listen)
        listener_thread.daemon = True
        listener_thread.start()

        # Join initial channel
        initial_channel = self.config['DEFAULT']['Channel']
        self.join_channel(initial_channel)

        # Send messages to the IRC server
        while True:
            try:
                input_win = self.windows[self.channels[self.current_channel_idx]]['input']
                input_win.clear()
                input_win.refresh()
                curses.echo()
                message = input_win.getstr(1, 1).decode("UTF-8")
                curses.noecho()

                if message.startswith("/quit"):
                    self.irc_socket.send(f"QUIT :Bye!\r\n".encode("UTF-8"))
                    break
                elif message.startswith("/join"):
                    channel = message.split(" ")[1]
                    self.join_channel(channel)
                elif message.startswith("/msg"):
                    target, msg = message.split(" ", 2)[1:]
                    self.irc_socket.send(f"PRIVMSG {target} :{msg}\r\n".encode("UTF-8"))
                elif message.startswith("/") and len(message) == 2 and message[1].isdigit():
                    idx = int(message[1]) - 1
                    self.switch_channel_by_index(idx)
                elif message == "/next":
                    self.switch_channel_next()
                elif message == "/prev":
                    self.switch_channel_prev()
                else:
                    current_channel = self.channels[self.current_channel_idx]
                    self.irc_socket.send(f"PRIVMSG {current_channel} :{message}\r\n".encode("UTF-8"))
            except KeyboardInterrupt:
                self.irc_socket.send(f"QUIT :Bye!\r\n".encode("UTF-8"))
                break
            except Exception as e:
                self.display_message(f"Error: {e}")
                break

        self.irc_socket.close()

if __name__ == "__main__":
    curses.wrapper(lambda stdscr: IRCClient(stdscr).run())
