#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "用法: $0 <base_url> <output_dir>"
    echo "示例: $0 http://192.168.1.10:8000 /tmp/env_install_site"
    exit 1
fi

BASE_URL="$1"
OUTPUT_DIR="$2"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

case "$BASE_URL" in
    */) ;;
    *) BASE_URL="${BASE_URL}/" ;;
esac

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

cp -r "$REPO_ROOT/tools" "$OUTPUT_DIR/"
cp -r "$REPO_ROOT/docs" "$OUTPUT_DIR/"
cp "$REPO_ROOT/install.py" "$OUTPUT_DIR/"

sed "s|http://mirror.fishros.com/install/|${BASE_URL}|g" \
    "$REPO_ROOT/install" >"$OUTPUT_DIR/install"
sed "s|http://mirror.fishros.com/install/|${BASE_URL}|g" \
    "$REPO_ROOT/robot_env_install" >"$OUTPUT_DIR/robot_env_install"

chmod +x "$OUTPUT_DIR/install" "$OUTPUT_DIR/robot_env_install"

echo "静态站点已生成: $OUTPUT_DIR"
echo "通用入口: ${BASE_URL}install"
echo "机器人环境入口: ${BASE_URL}robot_env_install"
