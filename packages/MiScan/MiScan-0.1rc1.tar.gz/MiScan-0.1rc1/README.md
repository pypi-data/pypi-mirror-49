# MiScan_core

Maxout-inferred SNV-based cancer prediction model | Apache Software License

# Tutorial

### installation

- install through `pip`

```bash
pip install MiScan -i https://pypi.python.org/pypi
```

- install through docker

```bash
docker pull jefferyustc/miscan_command_line:v0.2.1
```



### usage-commandline



```bash
MiScan --vcf /Users/jeffery/Downloads/SRR5447191.combined.filtered.vcf -o outputs --weight /Users/jeffery/workspace/projects/outputs/_MiScan_weights.hdf5
```

or with below command:

```bash
python -m MiScan --vcf /Users/jeffery/Downloads/SRR5447191.combined.filtered.vcf -o outputs --weight /Users/jeffery/workspace/projects/outputs/_MiScan_weights.hdf5
```

if with docker:

```bash
docker run --name miscan_cli_test -it -v /path/to/data:/path/in/docker 9fd
MiScan -o test_outputs --vcf ../model/SRR5447191.combined.filtered.vcf --weight ../model/_MiScan_weights.hdf5
```



### usage-script



```python
from MiScan import miscan_main

miscan_main(
    outDir='./outputs',
    inVcf='/Users/jeffery/Downloads/SRR5447191.combined.filtered.vcf',
    model_weight='/Users/jeffery/workspace/projects/outputs/_MiScan_weights.hdf5'
)
```

