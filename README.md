# Analyse Rust Stack Allocations

Small utility to analyse stack size for rust libraries.

## Installation

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
