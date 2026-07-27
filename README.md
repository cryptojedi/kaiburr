# Kaiburr

**Evaluating ML-KEM at (much) higher security levels.**

See each directory for its own `README.md` with details.

## Cloning

This repo uses git submodules for the paper bibliography (`cryptobib`) and the
three implementations under `src/`. Clone recursively:

```bash
git clone --recurse-submodules https://github.com/cryptojedi/kaiburr.git
# if already cloned without --recurse-submodules:
git submodule update --init --recursive
```

## Building the paper

```bash
cd paper && make
```

## Building the poster / proposal

```bash
cd poster/proposal && make