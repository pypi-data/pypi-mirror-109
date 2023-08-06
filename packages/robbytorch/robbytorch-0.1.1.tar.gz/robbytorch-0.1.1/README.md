# SZKLANKA

W Tej chwili można korzystać z kernela videoresearch albo video - na szklance.

Na porcie 5001 jest też postawione MLFlow

## Env

Na szklance trzeba zaktualizować sterowniki, dlatego instalujemy starszą wersję pytorch oraz cudatoolkit:

```
conda create --name <nazwa środowiska> python=3.8 pip
conda activate <nazwa środowiska>
conda install pytorch torchvision torchaudio cudatoolkit=10.1 -c pytorch -c conda-forge
pip install jupyter numpy tensorboard matplotlib tqdm pandas seaborn scikit-image livelossplot robustness mypy mlflow
```

Ew. wersja [1.7.1 pytorcha](https://pytorch.org/get-started/previous-versions/):
```
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.1 -c pytorch
```

## Dodanie env jako kernela na szklance

Trzeba odpalić z poziomu usera `portal`, można to zrobić przez `!` w komórce notatnika:
```
<rezultat odpalenia 'which python' z wnętrza środowiska> -m ipykernel install --prefix=/home/portal/.local --name "<Nazwa kernela, jaka ma być widoczna z poziomu notebooka>"
```

## Inne

- [MLFlow](docs/mlflow.md)
- [git hooks](docs/git_hooks.md)