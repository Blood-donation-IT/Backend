import os
import sys
import subprocess
import shutil
import argparse

parser = argparse.ArgumentParser(description="Generate protobuf and optionally mypy-protobuf files")
parser.add_argument("--mypy", action="store_true", help="Generate mypy-protobuf files")
args = parser.parse_args()

def run_command(cmd, **kwargs):
    print("[Running]:", " ".join(cmd))
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
        print(f"[WARNING] gRPC file not found for import fix: {grpc_file_path}")
        return
    with open(grpc_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace(
        "from notifications import notifications_pb2 as notifications_dot_notifications__pb2",
        "from . import notifications_pb2 as notifications_dot_notifications__pb2"
    )
    if new_content != content:
        with open(grpc_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Fixed import in {grpc_file_path}")
    else:
        print(f"[INFO] No import fix needed in {grpc_file_path}")

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
            print("[WARNING] mypy-protobuf timed out - skipping")

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
    notifications_dir = os.path.join(PROTO_OUT, "notifications")
    os.makedirs(notifications_dir, exist_ok=True)
    open(os.path.join(PROTO_OUT, "__init__.py"), "a").close()
    open(os.path.join(notifications_dir, "__init__.py"), "a").close()

    print("[Starting] protobuf generation...")
    print(f"[Root]: {ROOT_DIR}")
    print(f"[Python]: {sys.executable}")

    ver = sys.version_info
    cur_ver = f"{ver.major}.{ver.minor}"
    print(f"[Version]: {cur_ver}")

    proto_files = []
    notifications_proto_dir = os.path.join(PROTO_SRC, "notifications")
    if not os.path.isdir(notifications_proto_dir):
        print(f" Proto source directory not found: {notifications_proto_dir}")
        sys.exit(1)
    for filename in os.listdir(notifications_proto_dir):
        if filename.endswith(".proto"):
            proto_path = os.path.join("notifications", filename).replace("\\", "/")
            proto_files.append(proto_path)
    if not proto_files:
        print("No .proto files found!")
        sys.exit(1)

    try:
        print("[OK] Using current Python environment.")
        generate_protobuf(sys.executable, proto_files, PROTO_SRC, PROTO_OUT)
    except Exception as e:
        print(f"[WARNING] Failed with current Python: {e}")
        if ver >= (3, 13):
            print("[WARNING] Python too new (>3.12), trying to use Python 3.12...")
            py312 = find_python312()
            if not py312:
                print("[ERROR] Python 3.12 not found. Please install Python 3.12 or use compatible version.")
                print("[INFO] Trying to continue with current Python anyway...")
                try:
                    generate_protobuf(sys.executable, proto_files, PROTO_SRC, PROTO_OUT)
                except:
                    print("[ERROR] Generation failed. Please install Python 3.12 or fix the issue.")
                    sys.exit(1)
            else:
                print(f"[OK] Using Python 3.12 interpreter: {py312}")
                generate_protobuf(py312, proto_files, PROTO_SRC, PROTO_OUT)
        else:
            raise

    grpc_file = os.path.join(PROTO_OUT, "notifications", "notifications_pb2_grpc.py")
    fix_import_in_grpc_file(grpc_file)

if __name__ == "__main__":
    main()

