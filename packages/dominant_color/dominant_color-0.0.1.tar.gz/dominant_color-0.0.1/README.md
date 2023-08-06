# Just a demo of different dominant color extraction algorithms

Currently implemented:

 - kmeans
 - median cut quantization

## Usage

```
usage: image_palette.py [-h] image {kmeans,mediancut} ...

Test different color extraction algorithms.

positional arguments:
  image
  {kmeans,mediancut}  Algorithms
    kmeans            Using K-Means clustering
    mediancut         Using a median cut quantization

optional arguments:
  -h, --help          show this help message and exit
```