# Analyse Rust Stack Allocations

Small utility to analyse stack size for rust libraries.

## Installation

### Dependencies

```
poetry install
```

Also requires that `cargo` and `llvm-readobj` are on your PATH.

On Mac, `llvm-readobj` can be installed using Homebrew:

```
brew install llvm
```

For convenience, `analyse-stack.py` will automatically add Homebrew's default
LLVM bin directory to `PATH` while attempting to execute `llvm-readobj`.

### Rust

Until `rustc`'s `-Z emit-stack-size` feature stabilizes (https://github.com/rust-lang/rust/issues/54192),
you must have the nightly toolchain installed.

```
rustup toolchain install nightly
```

## Usage

### Build for analysis

From the root of your project:

```
analyse-stack.py build
```

Pass any additional flags through to cargo (e.g.):

```
analyse-stack.py build -- --no-default-features --target thumbv7em-none-eabi
```

### Analyse

Now request analysis (e.g.):

```
analyse-stack.py analyse target/thumbv7em-none-eabi/release/libgateway_nrf52840_rust.a
```

```
func_a: 10064 bytes
func_b: 4256 bytes
func_c: 792 bytes
```
