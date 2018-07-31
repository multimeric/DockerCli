# Docker CLI

`docker-cli` is a command-line tool for running executable docker images, which automatically mounts any necessary
files into the container.

For example, let's say you want to run the command-line tool [`bwa`](http://bio-bwa.sourceforge.net/). If you have
`bwa` installed locally, you could use a command like this. Easy!
```bash
bwa index hg19.fasta
```

However, if you wanted to do this inside a docker container, you would first have to mount the file into the container,
making the command much more complicated and slow to write:
```bash
docker run -v hg19.fasta:/tmp lh3lh3/bwa index /tmp/hg19.fasta
```
`docker-cli` automatically generates these mount flags, allowing you to instead run:

```bash
docker-cli lh3lh3/bwa hg19.fasta
```

## Installation
To install the command, first ensure you have Python 3.6 or above installed. Then, run:

```bash
python3- m pip install git+https://github.com/TMiguelT/DockerCli
```

## Usage
Once you install this package, you will have the `docker-cli` command available. Use this command exactly as you would
the normal `docker run` command; `docker run --rm mycontainer` becomes `docker-cli mycontainer`.

The full command line interface, including additional flags, is listed here:

```
usage: docker-cli [-h] [-n] [-p] [-e] ...

Runs a Docker image, automatically converting filepaths to a bindmount inside
the container

positional arguments:
  arguments           Arguments to pass to the docker container

optional arguments:
  -h, --help          show this help message and exit
  -n, --no-rm         Don't delete the container after it runs (the default)
  -p, --mount-parent  Mount the containing folder for each file, rather than
                      mounting each file individually. This can be helpful when
                      using index files etc.
  -e, --echo-command  Print the generated docker command instead of running
```
