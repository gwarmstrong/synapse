# synapse
generating a hierarchical model of the synapse

### Environment

To install a compatible conda environment, do

```bash
conda env create -n synapse --file resources/environment.yml
```

Then activate the environment with `conda activate synapse`

Next, install `ddot` with the following:

```bash
pip install resources/ddot
```


You will also need to make the CliXO executables, do this with the following commands:

```bash
cd resources/CliXO
rm *.o
make
```

