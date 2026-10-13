#!/usr/bin/env bash
# Launches the Scrapling MCP server (stdio). uvx installs scrapling[ai] on
# first run, so nothing needs to be pre-installed besides uv.
args=(mcp)
# Reuse a preinstalled Chromium (e.g. Claude Code cloud containers) when present,
# so the browser-based tools work without running `scrapling install`.
if [ -x /opt/pw-browsers/chromium ]; then
  args+=(--executable-path /opt/pw-browsers/chromium)
fi
exec uvx --from "scrapling[ai]" scrapling "${args[@]}"
