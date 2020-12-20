# -*- coding: utf-8 -*-
"""ArtLine(Try it on Colab).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/vijishmadhavan/Light-Up/blob/master/ArtLine(Try_it_on_Colab).ipynb

# **ArtLine**
**Create** **Amazing** **Line** **Art**.
"""

#!git clone https://github.com/vijishmadhavan/ArtLine.git ArtLine

#cd ArtLine

#!pip install -r colab_requirements.txt

"""# **Runtime**

* Hardware Accelerator = GPU 

"""

import fastai
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import open_image, load_learner, image, torch
import numpy as np
import urllib.request
import PIL.Image
from io import BytesIO
import torchvision.transforms as T
from PIL import Image
import requests
from io import BytesIO
import fastai
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import open_image, load_learner, image, torch
import numpy as np
import urllib.request
import PIL.Image
from io import BytesIO
import torchvision.transforms as T
from torchvision.utils import save_image

class FeatureLoss(nn.Module):
    def __init__(self, m_feat, layer_ids, layer_wgts):
        super().__init__()
        self.m_feat = m_feat
        self.loss_features = [self.m_feat[i] for i in layer_ids]
        self.hooks = hook_outputs(self.loss_features, detach=False)
        self.wgts = layer_wgts
        self.metric_names = ['pixel',] + [f'feat_{i}' for i in range(len(layer_ids))
              ] + [f'gram_{i}' for i in range(len(layer_ids))]

    def make_features(self, x, clone=False):
        self.m_feat(x)
        return [(o.clone() if clone else o) for o in self.hooks.stored]
    
    def forward(self, input, target):
        out_feat = self.make_features(target, clone=True)
        in_feat = self.make_features(input)
        self.feat_losses = [base_loss(input,target)]
        self.feat_losses += [base_loss(f_in, f_out)*w
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.feat_losses += [base_loss(gram_matrix(f_in), gram_matrix(f_out))*w**2 * 5e3
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.metrics = dict(zip(self.metric_names, self.feat_losses))
        return sum(self.feat_losses)
    
    def __del__(self): self.hooks.remove()

#MODEL_URL = "https://www.dropbox.com/s/p9lynpwygjmeed2/ArtLine_500.pkl?dl=1 "
#urllib.request.urlretrieve(MODEL_URL, "ArtLine_500.pkl")
path = Path("Model")
learn=load_learner(path, 'ArtLine_500.pkl')

"""# **URL**
Type in a url to a direct link of an **high quality image**. Usually that means they'll end in .png, .jpg, etc. 

**Note** : Works well with **portrait photos having good lighting and plain background**. But you're free to explore.

Link to high-quality portrait pics. Click on the image, let it expand and then copy image address.

https://www.freepik.com/search?dates=any&format=search&from_query=Portrait&page=1&query=Portrait&sort=popular&type=photo
"""

#url = 'https://image.freepik.com/free-photo/woman-field-running_23-2148574732.jpg' #@param {type:"string"}
url='../test/drawing_004.jpg'

#response = requests.get(url)
#img = PIL.Image.open(BytesIO(response.content)).convert("RGB")
img = PIL.Image.open(url).convert("RGB")
img_t = T.ToTensor()(img)
img_fast = Image(img_t)
show_image(img_fast, figsize=(7,7), interpolation='nearest');

"""# **Output**"""

p,img_hr,b = learn.predict(img_fast)
#Image(img_hr).show(figsize=(7,7))
save_image(img_hr, "output.png")

"""# **Recommended image sources**

https://www.freepik.com/search?dates=any&format=search&from_query=Portrait&page=1&query=Portrait&sort=popular&type=photo

https://www.pexels.com/search/portrait%20man/

https://www.flickr.com/search/?user_id=37277626%40N07&sort=date-taken-desc&safe_search=1&view_all=1&tags=portrait
"""
