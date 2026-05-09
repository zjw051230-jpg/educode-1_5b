import platform
import subprocess
import sys
import traceback


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def safe_print(label: str, fn) -> None:
    try:
        value = fn()
        print(f"{label}: {value}")
    except Exception as exc:
        print(f"{label}: ERROR -> {exc}")


def run_command(cmd, timeout_seconds: int = 15):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout_seconds,
        )
        return True, (result.stdout or result.stderr).strip()
    except subprocess.TimeoutExpired as exc:
        return False, f"command timed out: {' '.join(cmd)} (timeout seconds: {timeout_seconds})"
    except Exception as exc:
        return False, str(exc)


def main() -> None:
    section("Python Runtime")
    safe_print("Python executable", lambda: sys.executable)
    safe_print("Python version", lambda: sys.version.replace("\n", " "))
    safe_print("Platform", platform.platform)

    try:
        import torch
        import torch.nn.functional as F
    except Exception as exc:
        section("Torch Import")
        print(f"Failed to import torch: {exc}")
        print(traceback.format_exc())
        torch = None
        F = None

    if torch is not None:
        section("Torch / CUDA Basics")
        safe_print("torch version", lambda: torch.__version__)
        safe_print("torch.cuda.is_available()", lambda: torch.cuda.is_available())
        safe_print("torch.version.cuda", lambda: torch.version.cuda)
        safe_print("torch.backends.cudnn.version()", lambda: torch.backends.cudnn.version())
        safe_print("CUDA device count", lambda: torch.cuda.device_count())

        cuda_available = False
        try:
            cuda_available = bool(torch.cuda.is_available())
        except Exception:
            cuda_available = False

        if cuda_available:
            section("CUDA Device Info")
            safe_print("current device index", lambda: torch.cuda.current_device())
            safe_print("device name", lambda: torch.cuda.get_device_name(torch.cuda.current_device()))
            safe_print(
                "total memory (GiB)",
                lambda: round(torch.cuda.get_device_properties(torch.cuda.current_device()).total_memory / (1024 ** 3), 2),
            )
            safe_print(
                "compute capability",
                lambda: f"{torch.cuda.get_device_capability(torch.cuda.current_device())[0]}.{torch.cuda.get_device_capability(torch.cuda.current_device())[1]}",
            )
            if hasattr(torch.cuda, "is_bf16_supported"):
                safe_print("torch.cuda.is_bf16_supported()", lambda: torch.cuda.is_bf16_supported())
            else:
                print("torch.cuda.is_bf16_supported(): NOT AVAILABLE IN THIS TORCH VERSION")

            section("TF32 Flags")
            safe_print("torch.backends.cuda.matmul.allow_tf32", lambda: torch.backends.cuda.matmul.allow_tf32)
            safe_print("torch.backends.cudnn.allow_tf32", lambda: torch.backends.cudnn.allow_tf32)

            section("CUDA Tensor Sanity Check")
            try:
                a = torch.randn((2, 3), device="cuda")
                b = torch.randn((3, 4), device="cuda")
                c = a @ b
                print(f"CUDA matmul success: result shape = {tuple(c.shape)}")
            except Exception as exc:
                print(f"CUDA matmul failed: {exc}")
                print(traceback.format_exc())

            section("bf16 Sanity Check")
            try:
                bf16_supported = bool(torch.cuda.is_bf16_supported()) if hasattr(torch.cuda, "is_bf16_supported") else False
                if bf16_supported:
                    a = torch.randn((2, 3), device="cuda", dtype=torch.bfloat16)
                    b = torch.randn((3, 4), device="cuda", dtype=torch.bfloat16)
                    c = a @ b
                    print(f"bf16 matmul success: result shape = {tuple(c.shape)}, dtype = {c.dtype}")
                else:
                    print("bf16 not supported or not reported by this torch build")
            except Exception as exc:
                print(f"bf16 matmul failed: {exc}")
                print(traceback.format_exc())

            section("PyTorch SDPA Sanity Check")
            try:
                q = torch.randn((1, 2, 8, 16), device="cuda", dtype=torch.float16)
                k = torch.randn((1, 2, 8, 16), device="cuda", dtype=torch.float16)
                v = torch.randn((1, 2, 8, 16), device="cuda", dtype=torch.float16)
                out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
                print(f"SDPA success: output shape = {tuple(out.shape)}, dtype = {out.dtype}")
            except Exception as exc:
                print(f"SDPA failed: {exc}")
                print(traceback.format_exc())
        else:
            section("CUDA Device Info")
            print("CUDA is not available; skipping CUDA, bf16, and SDPA runtime checks")

    section("Subprocess Timeout Protection")
    print("All subprocess.run calls use timeout=15 seconds to avoid hanging on external commands")

    section("nvidia-smi")
    ok, output = run_command(["nvidia-smi"], timeout_seconds=15)
    if ok:
        lines = output.splitlines()
        preview = "\n".join(lines[:12])
        print(preview)
    else:
        print(f"nvidia-smi failed: {output}")

    section("nvcc --version")
    ok, output = run_command(["nvcc", "--version"], timeout_seconds=15)
    if ok:
        print(output)
    else:
        print(f"nvcc --version failed: {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Fatal error in script main(): {exc}")
        print(traceback.format_exc())
