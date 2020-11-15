import socks, socket, requests
import argparse
import time

arg_description = "GoogleFormSpammer.py <post-url> <entry-id> <entry-value>"

def get_args():
  parser = argparse.ArgumentParser(description="Spam a Google Form.")
  
  parser.add_argument("postUrl", type=str, help="url where the values get posted to")
  parser.add_argument("entryId", type=str, help="id of the entry to send")
  parser.add_argument("entryValue", type=str, help="value of the entry to send")
  parser.add_argument("-t", "--tor", help="use the tor network", action="store_true")
  parser.add_argument("-d", "--delay", type=int, help="sending delay in seconds")
  parser.add_argument("-n", "--number", type=int, help="number of payloads")
  
  return parser.parse_args()

def prepare_entry_id(entry_id):
  if entry_id.startswith("entry."):
    return entry_id
  else:
    return "entry." + entry_id

def tor_is_available():
  port_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  if port_test.connect_ex(("127.0.0.1", 9150)) == 0:
    return True
  else:
    return False

if __name__ == '__main__':
  args = get_args()
  
  if args.tor:
    if tor_is_available():
      socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
      socket.socket = socks.socksocket
      print("You are using tor.")
    else:
      print("Tor connection is not available!!!")
      answer = input("Continue anyways?(Y/n): ")

      if answer != "Y":
        exit()
  else:
    print("You are not using tor.")
  
  print("Your IP: " + requests.get("http://icanhazip.com").content.decode("utf-8"))
  
  if args.number is None:
    print("Sending payloads...")
  else:
    print(f"Sending {args.number} payloads...")
  
  counter = 0
  try:
    while args.number is None or counter < args.number:
      counter += 1
      print(f"Sending payload {counter}: {args.entryValue}")
      requests.post(args.postUrl, {
        args.entryId: args.entryValue,
      })
      
      if args.delay is not None:
        time.sleep(args.delay)
  except KeyboardInterrupt:
    print("Stopping...")
    exit()
  
  print("Finished sending.")