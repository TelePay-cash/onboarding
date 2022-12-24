import subprocess
import requests
import json
import socket

from pygments import highlight
from pygments.lexers import JsonLexer, PythonLexer
from pygments.formatters import TerminalFormatter

from time import sleep


def lolcat(client, asset, duration=2):
    o = subprocess.run(["lolcat", asset, "-S", "20", "-a", "-d", str(duration)], capture_output=True)
    client.send(o.stdout)


def typewrite(client, text, speed=0.1):
    for char in text:
        sleep(speed)
        client.send(bytes(char, "utf-8"))


def output(client, text, animate=False, speed=0.1):
    for line in text.split("\n"):
        line = "    " + line
        if animate:
            typewrite(client, line, speed)
            client.send(bytes("\n", "utf-8"))
        else:
            client.send(bytes(line, "utf-8"))


def clear(client):
    client.send(b'\033[2J')


def read(client):
    return client.recv(1024).decode()


def pause(client):
    output(
        client,
        "\nPress [ENTER] to continue...\n",
        animate=True,
        speed=0.01
    )
    read(client)


def format_json(data):        
    code = json.dumps(data, indent=4)
    return highlight(code, JsonLexer(), TerminalFormatter())


def format_python(code):
    return highlight(code, PythonLexer(), TerminalFormatter())


if __name__ == '__main__':

    HOST = "telepay.cash"
    PORT = 23

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable the TCP keepalive mechanism
    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    # Set the idle time before keepalives are sent
    server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)

    # Set the interval between keepalive probes
    server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)

    # Set the number of unacknowledged probes before the connection is considered dead
    server.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
    
    server.bind((HOST, PORT))
    server.listen()
    print("TCP server started on port", PORT)

    while True:

        # Accept incoming connections
        client, address = server.accept()
        print("Connected by", address)

        try:

            # slide 1
            clear(client)
            lolcat(client, "assets/telepay.logo.txt")
            output(
                client,
                "\n"
                "Welcome to TelePay!\n\n"
                "Ready to receive crypto payments?\n\n"
                "In this demo, you will learn how to receive crypto payments using TelePay.\n\n"
                "First, you will need to create a merchant.\n\n"
                "Go to https://telepay.cash/addMerchant, create a merchant, go to the Developers section inside your dashboard and copy the private API key.\n",
                animate=True
            )
            output(
                client,
                "Type your secret API key:\n",
                animate=True,
                speed=0.01
            )
            output(
                client,
                ">>> "
            )
            key = read(client)
            key = str(key).replace('\r', '').replace('\n', '')

            # TODO: handle empty

            output(
                client,
                "\n"
                "Got it! Now we will request info about your merchant to the API.\n\n"
                "Using your API key as 'Authorization' header, we call the /getMe endpoint.\n\n"
                "For that, we will use the 'requests' library and the Python language. 🐍\n",
                animate=True
            )

            output(
                client,
                format_python(
                    'import requests\n'
                    'base_url = "https://api.telepay.cash/rest"\n'
                    'headers = {"Authorization": "' + key + '"}\n'
                    'response = requests.get(base_url + "/getMe", headers=headers)\n'
                    'print(response.json())'
                ),
                animate=True,
                speed=0.01
            )

            output(
                client,
                "[API] Calling the endpoint...",
                animate=True,
                speed=0.01
            )

            # calling API
            base_url = "https://api.telepay.cash/rest"
            headers = {"Authorization": key}
            response = requests.get(base_url + "/getMe", headers=headers)
            data = response.json()

            output(
                client,
                f"[API] Received a JSON response with status {response.status_code}.\n",
                animate=True,
                speed=0.001
            )
            output(
                client,
                format_json(data),
                animate=True,
                speed=0.001
            )
            output(
                client,
                "And that's how you get info about your merchant! 😉\n\n"
                "Docs: https://telepay.readme.io/reference/getme\n\n"
                "Now let's create an invoice.\n\n"
                "We will use the API again, the invoice amount will be 10 TON, in the testnet network.",
                animate=True
            )
            pause(client)

            # calling API
            data = {
                "asset": "TON",
                "blockchain": "TON",
                "network": "testnet",
                "amount": 10,
                "description": "Invoice from the onboarding demo",
                "expires_at": 3
            }
            response = requests.post(base_url + "/createInvoice", data=data, headers=headers)
            data = response.json()

            output(
                client,
                format_python(
                    'import requests\n'
                    'base_url = "https://api.telepay.cash/rest"\n'
                    'headers = {"Authorization": "' + key + '"}\n'
                    'data = {"asset": "TON", "blockchain": "TON", "network": "testnet", "amount": 10, "description": "Invoice from the onboarding demo", "expires_at": 3}\n'
                    'response = requests.post(base_url + "/createInvoice", data=data, headers=headers)\n'
                    'print(response.json())'
                ),
                animate=True,
                speed=0.01
            )

            output(
                client,
                "[API] Calling the endpoint...",
                animate=True,
                speed=0.01
            )

            data = {
                "asset": "TON",
                "blockchain": "TON",
                "network": "testnet",
                "amount": 10,
                "description": "Invoice from the onboarding demo",
                "expires_at": 3
            }
            response = requests.post(base_url + "/createInvoice", data=data, headers=headers)
            data = response.json()

            output(
                client,
                f"[API] Received a JSON response with status {response.status_code}.\n",
                animate=True,
                speed=0.001
            )
            output(
                client,
                format_json(data),
                animate=True,
                speed=0.001
            )
            output(
                client,
                f"Your invoice number is {data['number']}. Go to {data['checkout_url']} to see the checkout page. 🤑\n\n"
                "Hurry up! It will expire in 3 minutes!",
                animate=True
            )
            pause(client)

            # slide 3
            clear(client)
            lolcat(client, "assets/telepay.logo.txt")
            output(
                client,
                "\n"
                "And that's how you create an invoice! 😉\n\n"
                "Docs: https://telepay.readme.io/reference/createinvoice\n\n"
                "There's a lot of things you can do, like cancel or delete invoices, receive webhooks, transfer funds off-chain and withdraw your funds to an on-chain wallet.\n\n"
                "But this was just a demo... 😜\n\n"
                "This demo is open source, you can see the code and collaborate, here:\n\n"
                "https://github.com/TelePay-cash/onboarding\n\n"
                "Feel free to improve it, create your pull requests and we will consider your improvements. Any feedback over there is also welcome.\n",
                animate=True
            )
            output(
                client,
                "More info about TelePay:\n"
                "* Website: https://telepay.cash\n"
                "* Community: https://telepay.cash/community (channels, social media, blog, etc)\n"
                "* API Docs: https://telepay.readme.io\n",
                animate=True,
                speed=0.001
            )
            lolcat(client, "assets/pikachu.txt")
            output(client, "\nGood bye! 👋\n", animate=True)

            # Close the connection
            client.close()
        
        except Exception as e:
            client.close()

    #######################################
    # ⭐️ star the repo if you saw this ⭐️ #
    #######################################
