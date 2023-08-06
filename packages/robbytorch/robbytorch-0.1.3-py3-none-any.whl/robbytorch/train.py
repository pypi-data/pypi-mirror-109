import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from typing import Optional, List, Dict, Iterable, Callable, Union
from dataclasses import dataclass, field
from pathlib import Path
import shutil, os

from . import utils


# TODO 
# - podczas treningu co jakiś czas robić show_image_row przykładów z dużym eps
# - zrobić configi i ustandaryzować logowanie do mlflow (przerobić parametr writer etc.)


@dataclass
class Trainer(object):

    def __init__(self, 
        train_loader: DataLoader,
        val_loader: DataLoader,
        forward_train: DataLoader,
        forward_eval: Optional[Callable] = None,
        forward_train_eval: Optional[Callable] = None,
        expand_data: Optional[Callable] = None,
        expand_data_eval: Optional[Callable] = None
    ):
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.forward_train = forward_train
        self.forward_eval = forward_eval or self.forward_train
        self.forward_train_eval = forward_train_eval or self.forward_eval
        
        self.expand_data = expand_data
        self.expand_data_eval = expand_data_eval or self.expand_data


    def _loop(self, model, optimizer=None, train=False, epoch="-"):
        meters = utils.DefaultDict(lambda _: utils.AverageMeter())
        loader = self.train_loader if train else self.val_loader
        iterator = tqdm(iter(loader), total=len(loader))

        expand_data = self.expand_data if train else self.expand_data_eval
        forward_eval = self.forward_train_eval if train else self.forward_eval

        for data in iterator:
            msg = f"Epoch: {epoch}, {'Train' if train else 'VAL'}"
            model.train() if train else model.eval()
            data_len = len(data["data"])
            
            if expand_data:
                # add more keys to data (i.e. adversarial examples)
                data = expand_data(model, data)

            if train:
                train_result = self.forward_train(model, data)
                loss = train_result["loss"] # train_loss

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                for k, v in train_result.items():
                    meters[f"train_{k}"].update(v.item(), data_len)
                msg += f" train_loss={meters['train_loss'].avg:.4f}"

            with torch.no_grad():
                model.eval()
                
                eval_result = forward_eval(model, data)

                for k, v in eval_result.items():
                    meters[k].update(v.item(), data_len)
                msg += f" loss={meters['loss'].avg:.4f}"

                iterator.set_description(msg)
                iterator.refresh()

        return meters


    def train_model(self, model, optimizer=None, scheduler=None,
                epochs=10,
                log_iterations=10,
                save_per=10,
                lr=0.0003, # if optimizer is None
                writers=[],
                eval_before_training=False,
                save_path="ipython/trained_models/temp"): # TODO save_path should be a part of witer config
        _mkdir_and_preserve_group(save_path)

        if optimizer is None:
            optimizer = optim.Adam(model.parameters(), lr=lr)

        if eval_before_training:
            self._loop(model)

        for epoch in range(1, epochs+1):
            meters = self._loop(
                model,
                optimizer=optimizer,
                train=True,
                epoch=epoch
            )

            if epoch % log_iterations == 0 or epoch == epochs:
                val_meters = self._loop(
                    model, 
                    optimizer=None, 
                    train=False, 
                    epoch=epoch
                )
                val_meters = {f"val_{k}": v for k, v in val_meters.items()}
                meters = {**meters, **val_meters}

            if epoch % save_per == 0 or epoch == epochs:
                torch.save(model.state_dict(), f"{save_path}/model_epoch_{epoch}.pt")

            if scheduler:
                scheduler.step()

            meters = {k: v.avg for k, v in meters.items()}
            for writer in writers:
                writer.log_metrics(meters, epoch)

        return



def _mkdir_and_preserve_group(path: Union[str, os.PathLike]) -> str:
    path = Path(path)
    ancestor = path
    while not ancestor.exists():
        ancestor = ancestor.parent
    group = ancestor.group()
    path.mkdir(parents=True, exist_ok=True)
    ancestor = path
    while not ancestor.group() == group:
        shutil.chown(ancestor, group="approx")
    return group