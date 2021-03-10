import os
import yaml
import json
import copy
from itertools import product
from PIL import Image
from button import create_button

template = """---
layout: product
title: {name}
permalink: /product/{product_id}
product_id: {product_id}
---"""

with open("_data/products.yml") as file:
  products = yaml.load(file, Loader=yaml.FullLoader)

with open("_data/clasps.yml") as file:
  clasps = yaml.load(file, Loader=yaml.FullLoader)["clasps"]

# build the product pages
os.makedirs("product_pages", exist_ok=True)
for k,v in products.items():
  with open("product_pages/{}.markdown".format(k), "w") as f:
    f.write( template.format(product_id=k,name=v["name"]) )

template = """---
layout: splash
permalink: index
date: 2016-03-23T11:48:41-04:00
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
    "excerpt" : "$" + v["price"],
    "background" : v.get("background", "red")
  }
  items.append(item)

  # convert images
  #for image in v.get("images",[]):
  #  if image.get("video",None) is None:
  #    convert_image(image["path"])
  
  # make the button
  BLANK_OPTION = [{"value":"-", "price":"0.00"}]
  sizes = copy.deepcopy(v.get("sizes",BLANK_OPTION))
  styles = copy.deepcopy(v.get("styles",BLANK_OPTION))

  merged_options = []
  merged_options_yml = {}
  for ii,opts in enumerate(product(sizes,styles,clasps)):
    value = "&".join([str(opt["value"]) for opt in opts])
    price = float(v["price"]) + sum([float(opt["price"]) for opt in opts])
    price = "{:.2f}".format(price)
    merged_options.append({"value":ii,"price":price})
    merged_options_yml[value] = {"value":ii,"price":price}

  buttons[product_num+1] = create_button(merged_options)
  all_options[product_num+1] = json.dumps(merged_options_yml)


# write buttons to a yaml
with open("_data/paypal_buttons.yml", "w") as f:
  yaml.dump(buttons, f)

with open('_data/merged_options.yml', 'w') as f:
  yaml.dump(all_options, f)

itemsets = [items[i:i+3] for i in range(0,len(items),3)]
content = {"row" + str(i) : itemset for i,itemset in enumerate(itemsets)}
rows = "\n".join(['{{% include cgallery id="row{}" %}}'.format(i) for i in range(len(content))])

with open("index.markdown", "w") as f:
  f.write( template.format(content=yaml.dump(content), rows=rows) )
