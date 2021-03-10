from subprocess import check_output
from urllib.parse import unquote

def add_option(label, options, index, **kwargs):

  cmd = """-d OPTION{index}NAME={label} """.format(index=index, label=label)

  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}SELECT{ii}={value} """.format(index=index, ii=ii, value=option["value"])
  for ii,option in enumerate(options):
    cmd += """-d L_OPTION{index}PRICE{ii}={price} """.format(index=index, ii=ii, price=option["price"])

  return cmd

def create_button(options):

  command = """
curl https://api-3t.sandbox.paypal.com/nvp \
  -s \
  --insecure \
  -d USER=sb-65mzm5298450_api1.business.example.com \
  -d PWD=ZB699ZS7KUXMQTX9 \
  -d SIGNATURE=Adab29VfWTNUD.w2uMl4W1.o8Gx4AjkBeAC3JsTc9kV8A138WK8kn4C- \
  -d VERSION=51.0 \
  -d METHOD=BMCreateButton \
  -d BUTTONCODE=HOSTED \
  -d BUTTONTYPE=CART \
  -d BUTTONSUBTYPE=PRODUCTS \
  -d BUTTONCOUNTRY=US \
  -d L_BUTTONVAR1=item_name%3Dshoehorn \
  -d L_BUTTONVAR2=tax=%3D21 \
  -d L_BUTTONVAR3=item_number%3D123456 \
"""

  command += add_option("Options", options, 0)
  output = check_output(command,shell=True)
  output = output.decode('utf-8')  
  output = output.split('WEBSITECODE=')[1].split("&HOSTED")[0]
  html = unquote(output).strip()

  # make changes to the formating here 

  return html

if __name__ == "__main__":

  html = create_button(None)
  print(html)