from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import ecies
import socket
import binascii
import sys
import threading
import time

reader = SimpleMFRC522()

# --- Socket Setup ---
HEADER = 64
PORT = 50512
FORMAT = "utf-8"
DCMSG = "DISCONNECT"
publicKey = b""
SERVER = "10.76.95.177"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
connected = True

server_messages = []

# Function for recieving and decoding messages
def receiveMsgs(client):
    global connected, publicKey
    while True:
        msgLength = client.recv(HEADER).decode(FORMAT)
        if msgLength != "":
            msgLength = int(msgLength)
            msg = client.recv(msgLength).decode(FORMAT)
            
            #print(SERVER, msg)
            if msg == "DISCONNECTED":
                print(SERVER, msg)
                connected = False
                sys.exit("Disconnected from server.")
            msgArgs = msg.split(":")
            if msgArgs[0] == "PUBLICKEY":
                publicKey = binascii.unhexlify(msgArgs[1])
            else:
                print(SERVER, msg)

        else:
            break

#Function for sending and encoding data
def send(client, msg):
    if publicKey == b"":
        print("[ERROR] Key is empty (Key has not been received).")
    else:
        encodedMsg = ecies.encrypt(publicKey, msg.encode("utf-8"))

        msgLength = f"{len(encodedMsg):<{HEADER}}".encode(FORMAT)
        client.send(msgLength)
        client.send(encodedMsg)

receiver = threading.Thread(target=receiveMsgs, args=[client])
receiver.start()


def wait_for_server_response(tag):
    # Wait until a response for a specific card ID comes back
    timeout = time.time() + 5  # 5 seconds timeout
    while time.time() < timeout:
        for msg in server_messages:
            if tag in msg:
                server_messages.remove(msg)
                return msg
        time.sleep(0.1)
    return "[ERROR] No server response."

# --- Main loop ---
try:
    while connected:
        print("\n[INFO] Please tap your card to make a payment...")
        card_id = reader.read_id()

        print(f"[INFO] Detected card ID: {card_id}")
        pin = input("Enter your PIN (typed): ").strip()

        # --- Step 1: Check current balance ---
        send(client, f"GETCARDINFO:{card_id}")
        balance_info = wait_for_server_response(str(card_id))
        print(f"[INFO] Card Info: {balance_info}")

        # try:
        #     balance = float(balance_info.split(":")[-1])
        # except ValueError:
        #     print("[ERROR] Failed to parse balance.")
        #     continue

        # --- Step 2: Ask for payment amount ---
        amount = input("Enter payment amount: ").strip()
        try:
            amount = float(amount)
        except ValueError:
            print("[ERROR] Invalid amount.")
            continue

        

        # if amount > balance:
        #     print("[ERROR] Insufficient funds.")
        #     continue

        # --- Step 3: Send TRYCHARGE request ---
        send(client, f"TRYCHARGE:{card_id}:{pin}:{amount}")
        print(f"[INFO] Sent TRYCHARGE request for {amount} units.")

except KeyboardInterrupt:
    print("\n[INFO] Exiting program.")
finally:
    GPIO.cleanup()
    send(client, DCMSG)
    client.close()
