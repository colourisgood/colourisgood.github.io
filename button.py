from subprocess import check_output
from urllib.parse import unquote

def create_button():

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
    -d L_BUTTONVAR2=amount%3D1464.46 \
    -d L_BUTTONVAR3=tax=%3D21 \
    -d L_BUTTONVAR4=item_number%3D123456
  """

  output = check_output(command,shell=True)
  output = output.decode('utf-8')
  output = output.split('WEBSITECODE=')[1].split("&EMAILLINK")[0]
  html = unquote(output).strip()
  return html


html = create_button()