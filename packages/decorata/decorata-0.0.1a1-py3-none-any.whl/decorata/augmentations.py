import random
import numpy as np
from albumentations import BasicTransform


class CutMix(BasicTransform):
    def __init__(self, dataset, always_apply=False, p=1):
        super(CutMix, self).__init__(always_apply, p)
        self.dataset = dataset
        self.sub_sample = None
        self.r = 0.

    def image_apply(self, image, **kwargs):
        index = random.randrange(self.dataset.__len__())
        self.sub_sample = self.dataset[index]
        bx, by, bw, bh, self.r = rand_bbox(image.shape)
        image[by:by+bh, bx:bx+bw, :] = self.sub_sample["image"][by:by+bh, bx:bx+bw, :]
        return image

    def label_apply(self, label, **kwargs):
        label = label * (1 - self.r) + self.sub_sample["label"] * self.r
        return label

    @property
    def targets(self):
        return {"image": self.image_apply, "label": self.label_apply}


class MixUp(BasicTransform):
    def __init__(self, dataset, always_apply=False, p=1):
        super(MixUp, self).__init__(always_apply, p)
        self.dataset = dataset
        self.sub_sample = None
        self.r = 0.

    def image_apply(self, image, **kwargs):
        index = random.randrange(self.dataset.__len__())
        self.sub_sample = self.dataset[index]
        self.r = random.uniform(0.4, 0.6)
        image = image * (1 - self.r) + 0.5 + self.sub_sample["image"] * self.r
        image = np.int16(image)
        return image

    def label_apply(self, label, **kwargs):
        label = label * (1 - self.r) + self.sub_sample["label"] * self.r
        return label

    @property
    def targets(self):
        return {"image": self.image_apply, "label": self.label_apply}

def rand_bbox(image_shape):
    # shape: (h, w, c)
    W = image_shape[1]
    H = image_shape[0]
    rw = random.uniform(0.2, 0.8)
    rh = random.uniform(0.2, 0.8)
    bw = int(W * rw + 0.5)
    bh = int(H * rh + 0.5)
    bx = random.randrange(W - bw)
    by = random.randrange(H - bh)
    r = rw * rh
    return bx, by, bw, bh, r



