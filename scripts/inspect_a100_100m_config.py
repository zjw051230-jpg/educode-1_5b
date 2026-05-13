from __future__ import annotations

import sys
from pathlib import Path

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.tiny_model import model_config_from_dict

CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "educode_100m_a100_draft.json"


def count_current_model_parameters(config: dict[str, object]) -> dict[str, int]:
    model_config = model_config_from_dict(config)

    token_embedding = model_config.vocab_size * model_config.d_model
    position_embedding = model_config.context_length * model_config.d_model
    per_layer_attention = 4 * model_config.d_model * model_config.d_model
    per_layer_mlp = 3 * model_config.d_model * model_config.d_ff
    per_layer_norm = 2 * model_config.d_model
    transformer_blocks = model_config.num_layers * (per_layer_attention + per_layer_mlp + per_layer_norm)
    final_norm = model_config.d_model
    lm_head = model_config.vocab_size * model_config.d_model
    total = token_embedding + position_embedding + transformer_blocks + final_norm + lm_head

    return {
        "token_embedding": token_embedding,
        "position_embedding": position_embedding,
        "per_layer_attention": per_layer_attention,
        "per_layer_mlp": per_layer_mlp,
        "per_layer_norm": per_layer_norm,
        "transformer_blocks": transformer_blocks,
        "final_norm": final_norm,
        "lm_head": lm_head,
        "total": total,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    config = load_json_config(CONFIG_PATH)
    tokenizer_path = PROJECT_ROOT / config["tokenizer"]["path"]
    loaded_tokenizer = Tokenizer.from_file(str(tokenizer_path))
    loaded_vocab_size = loaded_tokenizer.get_vocab_size()
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    parameter_counts = count_current_model_parameters(config)

    print(f"config path: {CONFIG_PATH}")
    print(f"run_name: {config['run']['run_name']}")
    print(f"status: {config.get('status', 'missing')}")
    print(f"hardware.target: {config['hardware']['target']}")
    print(f"hardware.gpu: {config['hardware'].get('gpu', 'missing')}")
    print(f"tokenizer.path: {tokenizer_path}")
    print(f"tokenizer.vocab_size: {config['tokenizer']['vocab_size']}")
    print(f"loaded tokenizer vocab size: {loaded_vocab_size}")
    print(f"model.context_length: {config['model']['context_length']}")
    print(f"model.num_layers: {config['model']['num_layers']}")
    print(f"model.d_model: {config['model']['d_model']}")
    print(f"model.num_heads: {config['model']['num_heads']}")
    print(f"model.head_dim: {config['model']['head_dim']}")
    print(f"model.d_ff: {config['model']['d_ff']}")
    print(f"estimated total parameters: {parameter_counts['total']} (~{parameter_counts['total'] / 1_000_000:.2f}M)")
    print(
        "parameter estimate basis: current TinyDecoderOnlyTransformer parameterization "
        "with learned position embeddings and an untied lm_head"
    )
    print(f"training.max_steps: {config['training']['max_steps']}")
    print(f"training.batch_size: {config['training']['batch_size']}")
    print(
        "training.gradient_accumulation_steps: "
        f"{config['training']['gradient_accumulation_steps']}"
    )
    print(f"profiling.attention_backend: {config['profiling']['attention_backend']}")

    if errors:
        print("validation failed")
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
