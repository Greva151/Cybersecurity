import queue
import threading
from colorama import Fore, Style
from scapy.contrib.automotive.uds import UDS, UDS_NR

from services_handler import *

handlers = {0x27: security_access}
q = queue.Queue(config.QUEUE_SIZE)


def send_msg(pkt):
    print(f"The server sent: {bytes(pkt).hex()}\n{pkt.show2(dump=True)}\n", flush=True)
    return


def worker():
    while True:
        pkt = q.get()
        try:
            handlers[pkt[UDS].service](pkt)
        except Exception as e:
            print(e)
            send_msg(UDS() / UDS_NR(requestServiceId=pkt[UDS].service, negativeResponseCode=0x11))
        q.task_done()


def inactivity():
    while True:
        if gl.CURRENT_SESSION != 1 and not gl.BUSY:
            time.sleep(1)
            gl.TIME_ELAPSED += 1
            if gl.TIME_ELAPSED > config.SESSION_RESET_TIMEOUT:
                gl.CURRENT_SESSION = 1
                gl.AUTH = False
                gl.TIME_ELAPSED = 0
        else:
            time.sleep(0.1)


def handle_packet(pkt):
    gl.TIME_ELAPSED = 0
    if pkt[UDS].service in config.SUPPORTED_SERVICES:
        try:
            q.put(pkt, block=False)
        except queue.Full:
            return
    else:
        p = UDS() / UDS_NR(requestServiceId=pkt[UDS].service, negativeResponseCode=0x11)
        send_msg(p)


threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=inactivity, daemon=True).start()


def main():
    while True:
        print(f"\n{Fore.GREEN}--- UDS Packet Menu ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Insert a packet")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} View the packet details")
        print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Send the packet")
        print(f"{Fore.RED}[0]{Style.RESET_ALL} Quit")

        choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}").strip()

        if choice == "0":
            print(f"{Fore.RED}Exiting... Goodbye!{Style.RESET_ALL}")
            break
        elif choice == "1":
            data = input(f"{Fore.CYAN}Write your UDS packet (hex format): {Style.RESET_ALL}")
            try:
                global pkt  # Declare `pkt` as global to reuse in other options
                data = bytes.fromhex(data)
                pkt = UDS(data)
                print(f"{Fore.GREEN}Packet created successfully!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid hex data! Please try again.{Style.RESET_ALL}")
        elif choice == "2":
            try:
                if 'pkt' in globals():
                    print(f"\n{Fore.GREEN}Packet Details:{Style.RESET_ALL}")
                    print(f"{bytes(pkt).hex()}\n{pkt.show2(dump=True)}", flush=True)
                else:
                    print(f"{Fore.RED}No packet available. Please create one first!{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error viewing packet: {e}{Style.RESET_ALL}")
        elif choice == "3":
            try:
                if 'pkt' in globals():
                    handle_packet(pkt)
                    while not q.empty():
                        time.sleep(0.1)
                    print(f"{Fore.GREEN}Packet sent successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No packet available. Please create one first!{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error sending packet: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
