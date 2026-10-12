#!/bin/bash
set -e
echo "=== installing Rust (rustup, minimal) ==="
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
source "$HOME/.cargo/env"
rustc --version; cargo --version
echo "=== cargo build LARQL (release) ==="
cd $LLMDB_ROOT/external_prior_art/larql
cargo build --release 2>&1 | tail -50
echo "=== built binaries ==="
ls -la target/release/ 2>/dev/null | grep -vE '\.d$|deps|build|incremental|fingerprint' | head -20
echo "BUILD_DONE"
