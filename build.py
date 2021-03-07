import os
import yaml
from PIL import Image

template = """---
layout: product
title: {name}
permalink: /product/{product_id}
product_id: {product_id}
---"""

with open("_data/products.yml") as file:
  products = yaml.load(file, Loader=yaml.FullLoader)

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


items = []
for k,v in products.items():
  item = {
    "image_path" : v["image"],
    "image_url" : "product/{}".format(k),
    "alt" : "placehold text",
    "title" : v["name"],
    "excerpt" : "$" + v["price"],
    "background" : v.get("background", "red")
  }
  items.append(item)

  # convert images
  convert_image(v["image"])
  for image in v.get("images",[]):
    print(image)
    if not image["path"] == "video":
      convert_image(image["path"])


itemsets = [items[i:i+3] for i in range(0,len(items),3)]
content = {"row" + str(i) : itemset for i,itemset in enumerate(itemsets)}
rows = "\n".join(['{{% include cgallery id="row{}" %}}'.format(i) for i in range(len(content))])

with open("index.markdown", "w") as f:
  f.write( template.format(content=yaml.dump(content), rows=rows) )
