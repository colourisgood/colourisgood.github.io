---
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
row0:
- alt: placehold text
  excerpt: $99.99
  image_path: /assets/images/neck1.png
  image_url: product/1
  title: Hidden Jaguar
- alt: placehold text
  excerpt: $79.99
  image_path: /assets/images/neck2.png
  image_url: product/2
  title: Sullen Dragon
- alt: placehold text
  excerpt: $399.99
  image_path: /assets/images/neck3.jpg
  image_url: product/3
  title: Delicious Breakfast Sandwhich
row1:
- alt: placehold text
  excerpt: $40.99
  image_path: /assets/images/neck4.png
  image_url: product/4
  title: Radical Rubies
- alt: placehold text
  excerpt: $219.99
  image_path: /assets/images/neck1.png
  image_url: product/5
  title: Luxurious Floating Panda

---

{% include feature_row id="intro" type="center" %}

{% include cgallery id="row0" %}
{% include cgallery id="row1" %}
