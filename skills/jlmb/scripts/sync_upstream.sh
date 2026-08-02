#!/usr/bin/env bash
set -euo pipefail

readonly REPOSITORY_URL="https://github.com/shi3z/japanese-llm-benchmark.git"

usage() {
  echo "Usage: $0 <checkout-directory>" >&2
}

if [[ $# -ne 1 || -z "${1:-}" ]]; then
  usage
  exit 2
fi

checkout_dir=$1
if [[ "$checkout_dir" == "/" ]]; then
  echo "Refusing to use the filesystem root as a checkout directory." >&2
  exit 2
fi

if [[ ! -e "$checkout_dir" ]]; then
  git clone --branch main --single-branch "$REPOSITORY_URL" "$checkout_dir"
  git -C "$checkout_dir" rev-parse HEAD
  exit 0
fi

if ! git -C "$checkout_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Target exists but is not a Git checkout: $checkout_dir" >&2
  exit 1
fi

remote_url=$(git -C "$checkout_dir" remote get-url origin)
case "$remote_url" in
  "$REPOSITORY_URL"|"https://github.com/shi3z/japanese-llm-benchmark"|"git@github.com:shi3z/japanese-llm-benchmark.git") ;;
  *)
    echo "Refusing to update an unexpected origin: $remote_url" >&2
    exit 1
    ;;
esac

if [[ -n "$(git -C "$checkout_dir" status --porcelain)" ]]; then
  echo "Refusing to update a checkout with uncommitted changes: $checkout_dir" >&2
  exit 1
fi

branch=$(git -C "$checkout_dir" branch --show-current)
if [[ "$branch" != "main" ]]; then
  echo "Refusing to change branches; current branch is '$branch', expected 'main'." >&2
  exit 1
fi

git -C "$checkout_dir" pull --ff-only origin main
git -C "$checkout_dir" rev-parse HEAD
