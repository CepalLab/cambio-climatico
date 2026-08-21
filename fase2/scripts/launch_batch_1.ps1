$repoWin = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($repoWin)) { throw "No se pudo resolver la ruta Windows del repositorio." }
$repoWinForWsl = $repoWin -replace '\\','/'
$repoWsl = (wsl.exe -d Ubuntu -- wslpath -a $repoWinForWsl).Trim()
if ([string]::IsNullOrWhiteSpace($repoWsl)) { throw "wslpath devolvió una ruta WSL vacía para: $repoWin" }
$id = '90001'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'medium'
$promptWsl = "$repoWsl/temp_prompt_90001.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '48304'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'medium'
$promptWsl = "$repoWsl/temp_prompt_48304.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '89934'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'medium'
$promptWsl = "$repoWsl/temp_prompt_89934.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
$id = '86527'
$model = 'gpt-5.6-luna'
$reasoningEffort = 'xhigh'
$promptWsl = "$repoWsl/temp_prompt_86527.md"
$wslCommand = "export PATH=/home/abustamante/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin; cd '$repoWsl' && cat '$promptWsl' | /home/abustamante/.nvm/versions/node/v24.14.0/bin/codex exec --model $model -c model_reasoning_effort=$reasoningEffort --dangerously-bypass-approvals-and-sandbox -C '$repoWsl' -"
$childCommand = "wsl.exe -d Ubuntu -- bash -lc `"$wslCommand`""
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childCommand))
Start-Process powershell.exe -ArgumentList '-NoExit','-NoProfile','-EncodedCommand',$encoded
Start-Sleep -Seconds 1
