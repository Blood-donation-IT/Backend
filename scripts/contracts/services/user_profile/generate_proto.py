import os
import sys
import subprocess
import shutil
import argparse

parser = argparse.ArgumentParser(description="Generate protobuf and optionally mypy-protobuf files")
parser.add_argument("--mypy", action="store_true", help="Generate mypy-protobuf files")
args = parser.parse_args()

def run_command(cmd, **kwargs):
    print("🧩 Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, **kwargs)

def find_python312():
    candidates = []
    if sys.platform.startswith("win"):
        for p in os.getenv("PATH", "").split(";"):
            candidate = os.path.join(p, "python3.12.exe")
            if os.path.isfile(candidate):
                candidates.append(candidate)
    else:
        for name in ["python3.12", "python3.12m"]:
            path = shutil.which(name)
            if path:
                candidates.append(path)
    return candidates[0] if candidates else None

def fix_import_in_grpc_file(grpc_file_path):
    if not os.path.isfile(grpc_file_path):
        print(f"⚠️ gRPC file not found for import fix: {grpc_file_path}")
        return
    with open(grpc_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace import line for user_profile_pb2
    # Original: import user_profile_pb2 as user_dot_user__profile__pb2
    # New: from . import user_profile_pb2 as user_dot_user__profile__pb2
    new_content = content.replace(
        "from user import user_profile_pb2 as user_dot_user__profile__pb2",
        "from . import user_profile_pb2 as user_dot_user__profile__pb2"
    )
    if new_content != content:
        with open(grpc_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Fixed import in {grpc_file_path}")
    else:
        print(f"ℹ️ No import fix needed in {grpc_file_path}")

def generate_protobuf(python_executable, proto_files, proto_src, proto_out):
    protoc_cmd = [
        python_executable, "-m", "grpc_tools.protoc",
        f"-I={proto_src}",
        f"--python_out={proto_out}",
        f"--grpc_python_out={proto_out}",
    ] + proto_files
    run_command(protoc_cmd)

    if args.mypy:
        mypy_cmd = [
            python_executable, "-m", "mypy_protobuf.main",
            f"--proto-path={proto_src}",
            f"--python_out={proto_out}",
            f"--mypy_out={proto_out}",
        ] + proto_files
        try:
            run_command(mypy_cmd, timeout=30)
        except subprocess.TimeoutExpired:
            print("⚠️ mypy-protobuf timed out — skipping")

def main():
    ROOT_DIR = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE, text=True
    ).stdout.strip() or os.getcwd()

    PROTO_SRC = os.path.join(ROOT_DIR, "api-specs")
    PROTO_OUT = os.path.join(ROOT_DIR, "contracts", "src", "contracts")
    TEMP_VENV = os.path.join(ROOT_DIR, ".temp_proto_env")
    CACHE_DIR = os.path.join(ROOT_DIR, ".proto_wheels")

    os.makedirs(CACHE_DIR, exist_ok=True)
    user_dir = os.path.join(PROTO_OUT, "user")
    os.makedirs(user_dir, exist_ok=True)
    open(os.path.join(PROTO_OUT, "__init__.py"), "a").close()
    open(os.path.join(user_dir, "__init__.py"), "a").close()

    print("🚀 Starting protobuf generation...")
    print(f"📂 Root: {ROOT_DIR}")
    print(f"🐍 Using Python: {sys.executable}")

    ver = sys.version_info
    cur_ver = f"{ver.major}.{ver.minor}"
    print(f"🔍 Detected Python version: {cur_ver}")

    proto_files = []
    user_proto_dir = os.path.join(PROTO_SRC, "user")
    if not os.path.isdir(user_proto_dir):
        print(f"❌ Proto source directory not found: {user_proto_dir}")
        sys.exit(1)
    for filename in os.listdir(user_proto_dir):
        if filename.endswith(".proto"):
            proto_files.append(os.path.join("user", filename))
    if not proto_files:
        print("❌ No .proto files found!")
        sys.exit(1)

    # If Python version > 3.12, use temporary Python 3.12 environment
    if ver >= (3, 13):
        print("⚠️  Python too new (>3.12), using temporary Python 3.12 environment...")

        py312 = find_python312()
        if not py312:
            print("⏬ Python 3.12 not found locally.")
            if shutil.which("pyenv"):
                run_command(["pyenv", "install", "-s", "3.12.6"])
                py312 = shutil.which("python3.12")
            elif sys.platform.startswith("darwin"):
                # brew install python@3.12 might not be installed quietly, so ignore errors
                subprocess.run(["brew", "install", "python@3.12"], check=False)
                py312 = shutil.which("python3.12")
            else:
                print("⚠️ Please install Python 3.12 manually from https://www.python.org/downloads/")
                sys.exit(1)

        if not py312:
            print("❌ Could not locate or install Python 3.12.")
            sys.exit(1)

        print(f"✅ Using Python 3.12 interpreter: {py312}")

        if os.path.exists(TEMP_VENV):
            shutil.rmtree(TEMP_VENV)
        run_command([py312, "-m", "venv", TEMP_VENV])

        bin_dir = "Scripts" if sys.platform.startswith("win") else "bin"
        pip = os.path.join(TEMP_VENV, bin_dir, "pip")
        python = os.path.join(TEMP_VENV, bin_dir, "python")

        run_command([pip, "install", "--upgrade", "pip"])
        run_command([pip, "install", "--no-cache-dir", "--find-links", CACHE_DIR, "-q", "grpcio-tools", "mypy-protobuf"])
        run_command([pip, "download", "-d", CACHE_DIR, "grpcio-tools", "mypy-protobuf"])

        generate_protobuf(python, proto_files, PROTO_SRC, PROTO_OUT)

        print("🧹 Cleaning up temporary environment...")
        shutil.rmtree(TEMP_VENV, ignore_errors=True)
        print("✅ Done with temporary environment.")

    else:
        print("✅ Python version is compatible. Using current environment.")
        generate_protobuf(sys.executable, proto_files, PROTO_SRC, PROTO_OUT)

    # Fix import in user_profile_pb2_grpc.py
    grpc_file = os.path.join(PROTO_OUT, "user", "user_profile_pb2_grpc.py")
    fix_import_in_grpc_file(grpc_file)

if __name__ == "__main__":
    main()