$repoWin = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($repoWin)) { throw "No se pudo resolver la ruta Windows del repositorio." }
$repoWinForWsl = $repoWin -replace '\\','/'
$repoWsl = (wsl.exe -d Ubuntu -- wslpath -a $repoWinForWsl).Trim()
if ([string]::IsNullOrWhiteSpace($repoWsl)) { throw "wslpath devolvió una ruta WSL vacía para: $repoWin" }
$id = '48823'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'xhigh'
$promptWsl = "$repoWsl/temp_prompt_48823.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '44551'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'xhigh'
$promptWsl = "$repoWsl/temp_prompt_44551.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '46227'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'xhigh'
$promptWsl = "$repoWsl/temp_prompt_46227.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '43442'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'xhigh'
$promptWsl = "$repoWsl/temp_prompt_43442.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
