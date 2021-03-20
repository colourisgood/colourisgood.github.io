import os
import yaml
import json
import copy
from itertools import product
from PIL import Image
from button import create_button
from urllib.parse import quote

product_page_template = """---
layout: product
title: {name}
permalink: /product/{product_id}
product_id: {product_id}
---"""

main_page_template = """---
layout: splash
permalink: index
date: 2016-03-23T11:48:41-04:00
header:
  image: /assets/images/welcome_web.png
intro:
  - excerpt: 'encounter colour'
{content}
---

{{% include feature_row id="intro" type="center" %}}

{rows}
"""

def convert_image(path):
  # convert image if necessary
  folder = os.path.dirname(os.path.realpath(__file__))
  raw_folder = os.path.join(os.path.dirname(path),"raw")
  raw_path = os.path.join(raw_folder,os.path.basename(path))
  im = Image.open(folder + raw_path)
  im.thumbnail((1000,1000))
  im.save(folder + path)

if __name__ == "__main__":

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--paypal", action="store_true")
  parser.add_argument("--convert", action="store_true")
  parser.add_argument("--production", action="store_true")
  args = parser.parse_args()

  with open("_data/products.yml") as file:
    products = yaml.load(file, Loader=yaml.FullLoader)

  with open("_data/clasps.yml") as file:
    raw_clasps = yaml.load(file, Loader=yaml.FullLoader)["clasps"]

  # build the product pages
  os.makedirs("product_pages", exist_ok=True)
  for k,v in products.items():
    with open("product_pages/{}.markdown".format(k), "w") as f:
      f.write( product_page_template.format(product_id=k,name=v["name"]) )

  all_options = {}
  buttons = {}
  items = []
  for product_num,(k,v) in enumerate(products.items()):
    print("BUILDING ", product_num)
    item = {
      "image_path" : v["images"][0]["path"],
      "image_url" : "product/{}".format(k),
      "alt" : "placehold text",
      "title" : v["name"],
      "excerpt" : "${price}".format(price=v["price"]),
      "background" : v.get("background", "red")
    }
    if v.get("sold",False):
      item["excerpt"] = "<span style=\"color:red\"><del>${price}</del>&nbsp;<b>SOLD</b></span>".format(price=v["price"])
    items.append(item)

    # convert images
    if args.convert:
      for image in v.get("images",[]):
        if image.get("video",None) is None:
          convert_image(image["path"])
    
    # make the button
    if args.paypal:
      BLANK_OPTION = [{"value":"-", "price":"0.00"}]
      sizes = copy.deepcopy(v.get("sizes",BLANK_OPTION))
      styles = copy.deepcopy(v.get("styles",BLANK_OPTION))
      clasps = raw_clasps if v.get("necklace",False) else BLANK_OPTION

      merged_options = []
      merged_options_yml = {}
      for ii,opts in enumerate(product(sizes,styles,clasps)):
        backend_value = "&".join([str(opt["value"]) for opt in opts])
        value = "size:{} style:{} {}".format(*[str(opt["value"]) for opt in opts])
        price = float(v["price"]) + sum([float(opt["price"]) for opt in opts])
        price = "{:.2f}".format(price)
        merged_options.append({"value":quote(value),"price":price})
        merged_options_yml[backend_value] = {"value":value,"price":price}

      # hidding the actual mechanics
      button_html = create_button(merged_options, v["name"], sandbox=args.production==False)
      button_html = button_html.replace("<table>","<table style=\"display:none;\">")
      button_html = button_html.replace("method=\"post\">", "method=\"post\" style=\"padding:0px\">")
      buttons[product_num+1] = button_html
      all_options[product_num+1] = json.dumps(merged_options_yml)

      #break


  if args.paypal:
    with open("_data/paypal_buttons.yml", "w") as f:
      yaml.dump(buttons, f)

    with open('_data/merged_options.yml', 'w') as f:
      yaml.dump(all_options, f)
  

  # build the main page
  itemsets = [items[i:i+3] for i in range(0,len(items),3)]
  content = {"row" + str(i) : itemset for i,itemset in enumerate(itemsets)}
  rows = "\n".join(['{{% include cgallery.html id="row{}" %}}'.format(i) for i in range(len(content))])

  with open("index.markdown", "w") as f:
    f.write( main_page_template.format(content=yaml.dump(content), rows=rows) )
