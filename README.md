# What's In My Fridge

Tracks what's in the fridge and when it expires so you use it before it goes bad.
Runs on a Raspberry Pi. Open it from your phone via Tailscale.

- Add item + expiry date
- Items expiring within 3 days (or already expired) pinned at the top
- Search by name
- Slider for % remaining
- Delete when used up

Stack: Python + Flask + SQLite, single HTML file. No build step.

## Setup on the Pi

```sh
git clone https://github.com/mihirk460/whatsinmyfridge.git ~/whatsinmyfridge
cd ~/whatsinmyfridge
pip3 install flask   # if this refuses (externally-managed-environment): sudo apt install python3-flask
sudo cp fridge.service /etc/systemd/system/
sudo systemctl enable --now fridge
```

Check it on home Wi-Fi: `http://192.168.1.229:8000`

## Phone access from anywhere (Tailscale)

```sh
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip -4
```

Install the Tailscale app on your phone, log in with the same account, then open
`http://<tailscale-ip>:8000`. Add it to your home screen.

## Update

```sh
cd ~/whatsinmyfridge && git pull && sudo systemctl restart fridge
```

Data lives in `fridge.db` next to `server.py`. Back it up by copying that file.
