import os
import yaml

template = """---
layout: archive
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
title: "Splash Page"
layout: splash
permalink: index
date: 2016-03-23T11:48:41-04:00
header:
  overlay_color: "#000"
  overlay_filter: "0.5"
  overlay_image: /assets/images/foo-bar-identity.jpg
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
intro:
  - excerpt: 'Nullam suscipit et nam, tellus velit pellentesque at malesuada, enim eaque. Quis nulla, netus tempor in diam gravida tincidunt, *proin faucibus* voluptate felis id sollicitudin. Centered with `type="center"`'
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
    "excerpt" : "$" + v["price"]
  }
  items.append(item)

itemsets = [items[i:i+3] for i in range(0,len(items),3)]
content = {"row" + str(i) : itemset for i,itemset in enumerate(itemsets)}
rows = "\n".join(['{{% include cgallery id="row{}" %}}'.format(i) for i in range(len(content))])

with open("index.markdown", "w") as f:
  f.write( template.format(content=yaml.dump(content), rows=rows) )
