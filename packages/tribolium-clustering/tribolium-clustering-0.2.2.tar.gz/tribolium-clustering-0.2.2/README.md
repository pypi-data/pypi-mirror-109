# Tribolium Clustering
This is a library that is specifically used for image analysis and data analysis of developing tribolium embryos. It is optimised for stained nuclei of the embryos and 3D imaging. Most functions are wrappers for other libraries, mostly [pyclesperanto](https://clij.github.io/clij2-docs/api_intro), [scikit-image](https://scikit-image.org/), [scikit-learn](https://scikit-learn.org/stable/), [UMAP](https://umap-learn.readthedocs.io/en/latest/index.html) and [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/). 
Image analysis is based almost entirely around functions from pyclesperanto which requires a powerful GPU with high memory capacities to work with high resolution files. If memory is insufficient you will probably encounter errors when using functions of this library and you need to make sure that you specify your powerful gpu in pyclesperanto with the command:

```python
import pyclesperanto_prototype as cle

# "GTX" has to be replaced with the identifyer for your main GPU
cle.select_device("GTX")
```

The data analysis is based on scikit learn functions as well as other external data science algorithms that follow a similar convention. The basics of which can be found [here](https://scikit-learn.org/stable/).
Since the functions were developed with a group of datasets modification of the functions could be required for the image analysis workflows but possibly also the data analysis workflows.
