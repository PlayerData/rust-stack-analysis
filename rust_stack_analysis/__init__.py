import argparse
import json
import os
import subprocess

from rust_demangler import demangle


def cargo_build(*buildflags):
    env = os.environ.copy()
    env["RUSTFLAGS"] = "-Z emit-stack-sizes"

    subprocess.run(["cargo", "+nightly", "build", *buildflags], env=env)


def llvm_read_stack_sizes(path):
    env = os.environ.copy()
    env["PATH"] = os.environ["PATH"] + ":" + "/opt/homebrew/opt/llvm/bin/"

    llvm_readobj = subprocess.run(
        [
            "llvm-readobj",
            "--stack-sizes",
            path,
            "--elf-output-style=JSON",
        ],
        capture_output=True,
        env=env,
    )

    try:
        return json.loads(llvm_readobj.stdout)
    except json.JSONDecodeError as e:
        print("\n")
        print("Failed to decode JSON response from LLVM:")
        print("")
        print(llvm_readobj.stderr.decode("utf-8"))
        print(llvm_readobj.stdout.decode("utf-8"))
        print("\n")
        raise e


def get_function_name(mangled):
    try:
        return demangle(mangled)
    except Exception:
        return mangled


def analyse(path, min_size):
    stacks = [
        item["Entry"] for f in llvm_read_stack_sizes(path) for item in f["StackSizes"]
    ]
    # {'Functions': ['_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h996a137daa97c5ceE'], 'Size': 32}

    stacks = [
        {"function": get_function_name(i["Functions"][0]), "size": i["Size"]}
        for i in stacks
    ]
    # {'function': '<&T as core::fmt::Debug>::fmt::h996a137daa97c5ce', 'size': 32}

    stacks = [i for i in stacks if i["size"] >= min_size]
    stacks = sorted(stacks, key=lambda i: i["size"], reverse=True)

    for i in stacks:
        print(f"{i['function']}: {i['size']} bytes")


def entrypoint():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="mode")

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("flags", nargs=argparse.REMAINDER)

    analyse_parser = subparsers.add_parser("analyse")
    analyse_parser.add_argument("path")
    analyse_parser.add_argument(
        "--min-size",
        type=int,
        default=512,
        help="Minimum stack size to print in output",
    )

    args = parser.parse_args()

    if args.mode == "build":
        if "--" in args.flags:
            args.flags.remove("--")
        cargo_build(*args.flags)
    elif args.mode == "analyse":
        analyse(args.path, args.min_size)


if __name__ == "__main__":
    entrypoint()
