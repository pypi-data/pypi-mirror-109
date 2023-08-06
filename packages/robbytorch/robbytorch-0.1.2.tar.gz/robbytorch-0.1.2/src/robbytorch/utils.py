import os
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from tqdm import tqdm, trange

from .input_transforms import PGD
from .transforms import TRAIN_TRANSFORMS_DEFAULT, TEST_TRANSFORMS_DEFAULT, TRAIN_TRANSFORMS_TRANSFER, TEST_TRANSFORMS_TRANSFER

import matplotlib.pyplot as plt

from typing import Union
PathLike = Union[str, os.PathLike]


def explain_regression(model, loader, multiplier=2, target_col='CR',
        constraint='2', num_img=10, eps=15, step_size=1, Nsteps=20):
    
    assert multiplier >= 1
    
    data = next(iter(loader))
    im = data['data']
    im = im[:num_img].cuda()
    targ = data[target_col][:num_img].unsqueeze(1).cuda()
    
    higher_targ = multiplier*targ
    lower_targ = (1/multiplier)*targ
#     ones = torch.ones_like(targ).float()*0.1

    def custom_loss(mod, inp, target, normalization=None):
        return torch.nn.MSELoss()(mod(inp), target)

    advs = []
    for target in [higher_targ, lower_targ]:
        im_adv = PGD(model, im, target, normalization=None, custom_loss=custom_loss,
                step_size=step_size, Nsteps=Nsteps, constraint=constraint, eps=eps, targeted=True, use_tqdm=True)
        advs.append(im_adv.cpu())
       
    show_image_row([im.cpu()]+advs, ["original", "higher", "lower"], fontsize=10)
#     show_image_row([im.cpu()]+advs, ["original", "lower", "higher"], fontsize=10)
    return advs


def explain_target(model, loader, label_map, 
        constraint='2', num_img=10, eps=15, step_size=1, Nsteps=20, normalization=None, targets=[0, 1]):
    """
        explain 2 selected targets
    """
    
    im, true_target = next(iter(loader))

    im = im[:num_img]
    true_target = true_target[:num_img]

    im = im.cuda()
    true_target = true_target.cuda()

    advs = []
    modes = [label_map[targets[1]], label_map[targets[0]], f"non_{label_map[targets[1]]}", f"non_{label_map[targets[0]]}",]
    for mode in modes:
        targeted = "non_" not in mode
        target = torch.ones_like(true_target)*targets[1] if label_map[targets[1]] in mode else torch.ones_like(true_target)*targets[0]
        im_adv = PGD(model, im, target, normalization, 
                    step_size=step_size, Nsteps=Nsteps, constraint=constraint, eps=eps, targeted=targeted, use_tqdm=True)
        
        advs.append(im_adv.cpu())
       
    show_image_row([im.cpu()]+advs, ["source"]+modes, tlist=[
        [label_map[int(i)] for i in true_target],
        [f"{label_map[int(i)]} -> {modes[0]}" for i in true_target],
        [f"{label_map[int(i)]} -> {modes[1]}" for i in true_target],
        [f"{label_map[int(i)]} -> {modes[2]}" for i in true_target],
        [f"{label_map[int(i)]} -> {modes[3]}" for i in true_target]
    ], fontsize=10)
    return advs


def transfer_model(model, num_classes=2):
    model.fc = nn.Linear(model.fc.in_features, num_classes)


def freeze_model(model):
    for param in model.parameters():
        param.requires_grad = False


def get_gradient(mod, im, targ, normalization, custom_loss=None):
    '''
    Compute model gradients w.r.t. inputs.
    Args:
        mod: model
        im (tensor): batch of images
        normalization (function): normalization function to be applied on inputs
        custom_loss (function): custom loss function to employ (optional)
        
    Returns:
        grad: model gradients w.r.t. inputs
        loss: model loss evaluated at inputs
    '''    
    def compute_loss(inp, target, normalization):
        if custom_loss is None:
            output = forward_pass(mod, inp, normalization)
            return torch.nn.CrossEntropyLoss()(output, target.cuda())
        else:
            return custom_loss(mod, inp, target.cuda(), normalization)
        
    x = im.clone().detach().requires_grad_(True)
    loss = compute_loss(x, targ, normalization)
    grad, = torch.autograd.grad(loss, [x])
    return grad.clone(), loss.detach().item()


def visualize_gradient(t):
    '''
    Visualize gradients of model. To transform gradient to image range [0, 1], we 
    subtract the mean, divide by 3 standard deviations, and then clip.
    
    Args:
        t (tensor): input tensor (usually gradients)
    '''  
    mt = torch.mean(t, dim=[2, 3], keepdim=True).expand_as(t)
    st = torch.std(t, dim=[2, 3], keepdim=True).expand_as(t)
    return torch.clamp((t - mt) / (3 * st) + 0.5, 0, 1)


# DEPRECATED
def get_predictions(mod, im, normalization=None):
    '''
    Determine predictions of linear classifier.
    Args:
        im (tensor): batch of images
        mod: model

    Returns:
        pred (tensor): batch of predicted labels
    ''' 
    with torch.no_grad():
        logits = forward_pass(mod, im, normalization)
        pred = logits.argmax(dim=1)
    return pred


# DEPRECATED
def accuracy(net, im, targ, normalization=None):
    '''
    Evaluate the accuracy of a given linear classifier.
    Args:
        net: model
        im (tensor): batch of images
        targ (tensor): batch of labels
        
    Returns:
        x: batch of adversarial examples for input images
    '''  
    pred = get_predictions(net, im, normalization)
    acc = (pred == targ.cuda()).sum().item() / len(im) * 100
    return acc


def get_accuracy(logits, target):
    pred = logits.argmax(dim=1)
    accuracy = (pred == target.cuda()).sum().item() / len(target) * 100
    return accuracy


def get_axis(axarr, H, W, i, j):
    H, W = H - 1, W - 1
    if not (H or W):
        ax = axarr
    elif not (H and W):
        ax = axarr[max(i, j)]
    else:
        ax = axarr[i][j]
    return ax


def show_image_row(xlist, ylist=None, fontsize=12, size=(2.5, 2.5), tlist=None, filename=None):
    H, W = len(xlist), len(xlist[0])
    fig, axarr = plt.subplots(H, W, figsize=(size[0] * W, size[1] * H))
    for w in range(W):
        for h in range(H):
            ax = get_axis(axarr, H, W, h, w)                
            ax.imshow(xlist[h][w].permute(1, 2, 0))
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])
            if ylist and w == 0: 
                ax.set_ylabel(ylist[h], fontsize=fontsize)
            if tlist:
                ax.set_title(tlist[h][w], fontsize=fontsize)
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    plt.show()


class DefaultDict(dict):
    """
        collections.defaultdict does not let arguments to be passed to factory
    """

    def __init__(self, factory):
        super().__init__
        self.factory = factory

    def __missing__(self, key):
       res = self[key] = self.factory(key)
       return res


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count