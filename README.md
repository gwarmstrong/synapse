# synapse
generating a hierarchical model of the synapse

### Install

When first downloading this repo, run the following command to get the `ddot` and `CliXO` source dependencies.

```bash
git submodule update --init --recursive
```

Then, to install a compatible conda environment, do

```bash
conda env create -n synapse --file resources/environment.yml
```

Then activate the environment with `conda activate synapse`

Next, install `ddot` with the following:

```bash
cd resources/ddot
make
pip install .
cd ../..
```


You will also need to make the CliXO executables, do this with the following commands:

```bash
cd resources/CliXO
rm *.o
make
```

