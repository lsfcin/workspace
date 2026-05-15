#!/usr/bin/env pwsh
# PowerShell session-start launcher for Windows
param()

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$workspaceRoot = Resolve-Path (Join-Path $scriptDir "..")
Write-Output "== WORKSPACE.md =="
Get-Content -Path (Join-Path $workspaceRoot 'WORKSPACE.md') -TotalCount 120
