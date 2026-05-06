#!/usr/bin/env bash
# Run baseline frontier model benchmarks.
#
# Usage:
#   ./scripts/run_baselines.sh              # run all baselines
#   ./scripts/run_baselines.sh gpt-4o       # run a single model
#
# Required env vars (set whichever providers you want to run):
#   OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
#
# Results are written to predictions/<model>.jsonl and evaluated under
# logs/run_evaluation/<model>/.

set -euo pipefail

DATASET="${DATASET:-all}"
PREDICTIONS_DIR="${PREDICTIONS_DIR:-predictions}"
mkdir -p "$PREDICTIONS_DIR"

# Canonical baseline models: provider model_name
#
# We split the list in two groups:
#   - Native-API models, exercised against the vendor's own SDK
#     (requires OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY).
#   - Cross-vendor frontier models routed through OpenRouter
#     (requires OPENROUTER_API_KEY).  The model identifiers contain a
#     '/' so the provider auto-detector below picks 'openrouter'.
BASELINES=(
    # Anchor / regression baselines (native APIs)
    "anthropic claude-sonnet-4-20250514"
    "anthropic claude-opus-4-20250514"
    "google gemini-2.5-pro"
    "openai gpt-4o"
    "openai gpt-5"

    # Newer frontier models routed through OpenRouter
    "openrouter anthropic/claude-sonnet-4.6"
    "openrouter moonshotai/kimi-k2.6"
    "openrouter mistralai/mistral-medium-3-5m"
    "openrouter x-ai/grok-4.3"
    "openrouter openai/gpt-5.5"
)

run_model() {
    local provider="$1"
    local model="$2"
    local safe_name
    safe_name=$(echo "$model" | tr '/' '_')
    local output="$PREDICTIONS_DIR/${safe_name}.jsonl"

    echo "=== Running $model ($provider) ==="
    if ! python -m brokerbench.inference.run_api \
        --model_name "$model" \
        --dataset "$DATASET" \
        --output_file "$output" \
        --provider "$provider"; then
        echo "*** $model failed, skipping evaluation ***"
        return 0
    fi

    echo "--- Evaluating $model ---"
    python -m brokerbench.harness.run_evaluation \
        --predictions_path "$output" \
        --dataset_name "$DATASET" \
        --run_id "$safe_name" || true

    echo ""
}

run_naive_baselines() {
    local out_dir="$PREDICTIONS_DIR/_naive"
    mkdir -p "$out_dir"
    echo "=== Running naive baselines (always-A/B/C/D, uniform-random, most-common) ==="
    python -m brokerbench.inference.run_baseline \
        --strategy all \
        --dataset "$DATASET" \
        --output_file "$out_dir"
    for f in "$out_dir"/*.jsonl; do
        local strat
        strat=$(basename "$f" .jsonl)
        python -m brokerbench.harness.run_evaluation \
            --predictions_path "$f" \
            --dataset_name "$DATASET" \
            --run_id "_naive_${strat}" || true
    done
    echo ""
}

# If a model name is passed as $1, run only that model
if [[ $# -ge 1 ]]; then
    model="$1"
    if [[ "$model" == "naive" ]]; then
        run_naive_baselines
        exit 0
    fi
    # Detect provider
    if echo "$model" | grep -qE '/'; then
        provider="openrouter"
    elif echo "$model" | grep -qiE '^(claude|anthropic)'; then
        provider="anthropic"
    elif echo "$model" | grep -qiE '^gemini'; then
        provider="google"
    else
        provider="openai"
    fi
    run_model "$provider" "$model"
    exit 0
fi

# Always run naive baselines first so any real-model report can be
# compared against them.
run_naive_baselines

# Run all baselines
for entry in "${BASELINES[@]}"; do
    read -r provider model <<< "$entry"
    run_model "$provider" "$model"
done

echo "=== All baselines complete ==="
echo "Predictions: $PREDICTIONS_DIR/"
echo "Reports:     logs/run_evaluation/"
