import os
from subprocess import check_output
from urllib.parse import unquote, quote

def add_option(label, options, index, **kwargs):

  cmd = """-d OPTION{index}NAME={label} """.format(index=index, label=label)

  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}SELECT{ii}={value} """.format(index=index, ii=ii, value=option["value"])
  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}PRICE{ii}={price} """.format(index=index, ii=ii, price=option["price"])

  return cmd

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
  -d NO_SHIPPING=2 \
  -d L_BUTTONVAR1=item_name={name} \
  -d L_BUTTONVAR2=item_number=123456 \
""".format(
  url=api_url,
  user=paypal_user,
  password=paypal_password,
  signature=paypal_signature,
  name=quote(name))
  #shipping=shipping)

  command += add_option("Options", options, 0)
  output = check_output(command,shell=True)
  output = output.decode('utf-8')  
  print(command)
  print(unquote(output))
  output = output.split('WEBSITECODE=')[1].split("&HOSTED")[0]
  html = unquote(output).strip()
  return html

if __name__ == "__main__":

  html = create_button(None)
  print(html)