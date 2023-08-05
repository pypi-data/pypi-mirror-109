# WL-align

[![pipeline status](https://gitlab.inria.fr/cobcom/wlalign/badges/master/pipeline.svg)](https://gitlab.inria.fr/cobcom/wlalign/-/commits/master)
[![coverage report](https://gitlab.inria.fr/cobcom/wlalign/badges/master/coverage.svg)](https://gitlab.inria.fr/cobcom/wlalign/-/commits/master)  
[![Documentation Status](https://readthedocs.org/projects/wl-align/badge/?version=latest)](https://wl-align.readthedocs.io/en/latest/?badge=latest)


`wlalign` is a pure Python package that implements the graph-alignment routine 
based on the generalization of the Weisfeiler-Lehman algorithm proposed in 
our [Network Neuroscience paper](https://doi.org/10.1162/netn_a_00199).

The software provides the ``wlalign`` Python module, which includes all the
**functions and tools that are necessary for computing network alignments and 
similarity**.
In particular, specific functions are devoted to:

* Computing the **graph Jaccard index** of **similarity** between two weighted 
graphs.
* Solving the **graph alignment problem** with **WL-align**.

The package is [available at Pypi](#)
and can be easily installed from the command line.

```bash
    pip install wlalign
```

Talon is a free software released under [MIT license](LICENSE).

Documentation
-------------
The documentation of WL-align is available on
[Read the Docs](https://wl-align.readthedocs.io).

Getting help
------------
The preferred way to get assistance in running code that uses ``wlalign`` is
through the issue system of the
[Gitlab repository](https://gitlab.inria.fr/cobcom/wlalign) where the 
source code is available.
Developers and maintainers frequently check newly opened issues and will be
happy to help you.


Contributing guidelines
-----------------------
The development happens in the ``devel`` branch of the
[Gitlab repository](https://gitlab.inria.fr/cobcom/wlalign) while the
``master`` is kept for the stable releases only.
We will consider only merge requests towards the ``devel`` branch.


How to cite
-----------
If you publish works using WL-align, please cite us as follows:

>Matteo Frigo, Emilio Cruciani, David Coudert, Rachid Deriche, Emanuele Natale,
Samuel Deslauriers-Gauthier; Network alignment and similarity reveal 
atlas-based topological differences in structural connectomes. Network 
Neuroscience 2021; doi: https://doi.org/10.1162/netn_a_00199


Funding
-------
The development of WL-align was funded by the European Research Council (ERC)
under the European Union’s Horizon 2020 research and innovation program (ERC
Advanced Grant agreement No 694665: [CoBCoM - Computational Brain Connectivity
Mapping](https://project.inria.fr/cobcom/) ).

<img src="doc/source/img/logo_erc_eu.jpg" alt="logo ERC" width="800"/>
