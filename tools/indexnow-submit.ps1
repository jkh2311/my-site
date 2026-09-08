param(
  [Parameter(Mandatory=$true, Position=0)]
  [string[]]$Url
)

$ErrorActionPreference = 'Stop'
$HostName = 'haninelife.com'
$KeyFile = Get-ChildItem -Path (Join-Path $PSScriptRoot '..') -Filter '*.txt' -File |
  Where-Object { $_.BaseName -match '^[a-fA-F0-9-]{8,128}$' } |
  Select-Object -First 1
if (-not $KeyFile) { throw 'IndexNow key file not found in site root.' }
$Key = $KeyFile.BaseName
$KeyLocation = "https://$HostName/$Key.txt"

$urls = @()
foreach ($u in $Url) {
  if ([string]::IsNullOrWhiteSpace($u)) { continue }
  $candidate = $u.Trim()
  if ($candidate -notmatch '^https://') {
    $candidate = 'https://' + $HostName + '/' + $candidate.TrimStart('/')
  }
  $uri = [Uri]$candidate
  if ($uri.Scheme -ne 'https' -or $uri.Host -ne $HostName) {
    throw "Only https://$HostName URLs are allowed: $candidate"
  }
  $urls += $uri.AbsoluteUri
}
$urls = @($urls | Select-Object -Unique)
if ($urls.Count -eq 0) { throw 'No URL to submit.' }
if ($urls.Count -gt 10000) { throw 'IndexNow allows up to 10,000 URLs per POST.' }

# The key file must already be publicly reachable after deployment.
try {
  $onlineKey = (Invoke-WebRequest -Uri $KeyLocation -UseBasicParsing -TimeoutSec 15).Content.Trim()
} catch {
  throw "Key file is not reachable yet. Upload the site first, then run again: $KeyLocation"
}
if ($onlineKey -ne $Key) { throw 'Online IndexNow key content does not match the local key.' }

$payload = @{
  host = $HostName
  key = $Key
  keyLocation = $KeyLocation
  urlList = $urls
} | ConvertTo-Json -Depth 4

$response = Invoke-WebRequest -Method Post -Uri 'https://searchadvisor.naver.com/indexnow' `
  -ContentType 'application/json; charset=utf-8' -Body $payload -UseBasicParsing
Write-Host "IndexNow HTTP $($response.StatusCode)"
Write-Host "Submitted $($urls.Count) URL(s):"
$urls | ForEach-Object { Write-Host " - $_" }
