import os
import yaml

template = """---
layout: product
title: temp
permalink: /product/{product_id}
product_id: {product_id}
---"""

with open("_data/products.yml") as file:
  products = yaml.load(file, Loader=yaml.FullLoader)

# build the product pages
os.makedirs("product_pages", exist_ok=True)
for k,v in products.items():
  with open("product_pages/{}.markdown".format(k), "w") as f:
    f.write( template.format(product_id=k) )

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

itemsets = [items[i:i+3] for i in range(0,len(items),3)]
content = {"row" + str(i) : itemset for i,itemset in enumerate(itemsets)}
rows = "\n".join(['{{% include cgallery id="row{}" %}}'.format(i) for i in range(len(content))])

with open("index.markdown", "w") as f:
  f.write( template.format(content=yaml.dump(content), rows=rows) )
