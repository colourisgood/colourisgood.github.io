import os
from subprocess import check_output
from urllib.parse import unquote, quote

# https://developer.paypal.com/docs/paypal-payments-standard/integration-guide/Appx-websitestandard-htmlvariables/

def add_option(label, options, index, **kwargs):

  cmd = """-d OPTION{index}NAME={label} """.format(index=index, label=label)

  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}SELECT{ii}={value} """.format(index=index, ii=ii, value=option["value"])
  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}PRICE{ii}={price} """.format(index=index, ii=ii, price=option["price"])

  return cmd

def get_header(sandbox=True):
  api_url = "https://api-3t.paypal.com/nvp"
  paypal_user = os.getenv("PAYPAL_USER")
  paypal_password = os.getenv("PAYPAL_PWD")
  paypal_signature = os.getenv("PAYPAL_SIG")

  if sandbox:
    api_url = "https://api-3t.sandbox.paypal.com/nvp"
    paypal_user = os.getenv("PAYPAL_SANDBOX_USER")
    paypal_password = os.getenv("PAYPAL_SANDBOX_PWD")
    paypal_signature = os.getenv("PAYPAL_SANDBOX_SIG")

  if paypal_user is None or paypal_password is None or paypal_signature is None:
    print("YOU NEED TO DEFINE ENVIRONMENT VARIABLES ...")
    assert False
  
  header = """
curl {url} \
  -s \
  --insecure \
  -d USER={user} \
  -d PWD={password} \
  -d SIGNATURE={signature} \
  -d VERSION=51.0 \
""".format(url=api_url,
  user=paypal_user,
  password=paypal_password,
  signature=paypal_signature)
  return header

def get_button_ids(sandbox=True):

  header = get_header(sandbox=sandbox)
  command = header + """-d METHOD=BMButtonSearch \
-d STARTDATE=2012-08-24T05:38:48Z \
-d ENDDATE=2022-08-24T05:38:48Z \
"""
  output = check_output(command,shell=True)
  output = output.decode('utf-8')  
  ids = unquote(output).split("&L_HOSTEDBUTTONID")
  ids = [x.split("=")[1] for x in ids[:-1]]
  return ids  

def delete_button(button_id, sandbox=True):
  header = get_header(sandbox=sandbox)
  command = header + """-d METHOD=BMManageButtonStatus \
-d HOSTEDBUTTONID={button_id} \
-d BUTTONSTATUS=DELETE \
""".format(button_id=button_id)
  output = check_output(command,shell=True)
  print(output.decode("utf-8"))

def delete_all_buttons(sandbox=True):
  button_ids = get_button_ids(sandbox=sandbox)
  for button_id in button_ids:
    delete_button(button_id, sandbox=sandbox)

def create_button(options, name, sandbox=True, shipping=3):

  api_url = "https://api-3t.paypal.com/nvp"
  paypal_user = os.getenv("PAYPAL_USER")
  paypal_password = os.getenv("PAYPAL_PWD")
  paypal_signature = os.getenv("PAYPAL_SIG")

  if sandbox:
    api_url = "https://api-3t.sandbox.paypal.com/nvp"
    paypal_user = os.getenv("PAYPAL_SANDBOX_USER")
    paypal_password = os.getenv("PAYPAL_SANDBOX_PWD")
    paypal_signature = os.getenv("PAYPAL_SANDBOX_SIG")

  if paypal_user is None or paypal_password is None or paypal_signature is None:
    print("YOU NEED TO DEFINE ENVIRONMENT VARIABLES ...")
    assert False

  command = """
curl {url} \
  -s \
  --insecure \
  -d USER={user} \
  -d PWD={password} \
  -d SIGNATURE={signature} \
  -d VERSION=51.0 \
  -d METHOD=BMCreateButton \
  -d BUTTONCODE=HOSTED \
  -d BUTTONTYPE=CART \
  -d BUTTONSUBTYPE=PRODUCTS \
  -d BUTTONCOUNTRY=US \
  -d L_BUTTONVAR1=item_name={name} \
  -d L_BUTTONVAR2=item_number=123456 \
  -d L_BUTTONVAR3=currency_code=CAD \
  -d L_BUTTONVAR4=lc=CAD \
  -d L_BUTTONVAR5=bn=CAD \
  -d L_BUTTONVAR6=no_shipping=2 \
""".format(
  url=api_url,
  user=paypal_user,
  password=paypal_password,
  signature=paypal_signature,
  name=quote(name))
  #shipping=shipping)

  # -d L_BUTTONVAR3=currency_code=CAD \

  command += add_option("Options", options, 0)
  output = check_output(command,shell=True)
  output = output.decode('utf-8')  
  print(command)
  print(unquote(output))
  output = output.split('WEBSITECODE=')[1].split("&HOSTED")[0]
  html = unquote(output).strip()
  return html

if __name__ == "__main__":

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--sandbox", action="store_true")
  args = parser.parse_args()

  delete_all_buttons(sandbox=args.sandbox)