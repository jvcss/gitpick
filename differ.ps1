param(
    [string]$RepoURL = "https://github.com/jvcss/gitpick.git",
    [string]$DiretorioDestino = "source"
)

$ignore = @(
    ".gitignore"
)
#🔥
function Get-ContentDiffReverse {
    param (
        [string]$File,
        [string]$Branch,
        [string]$BaseA = "main"
    )
    #displays the changes that have been made in the $BaseA that are not present in the $Branch
    $difference = git diff $Branch..$BaseA -- $File

    return $difference
}
#🔥
function Get-Branches {
    param(
        [string]$BaseA = "main"
    )
    $branchesRemote = git branch -r | ForEach-Object {
        $_ -replace 'origin/', ''
    } | Where-Object { $_ -notmatch 'HEAD' } | Where-Object { $_ -notmatch $BaseA } | ForEach-Object { $_.Trim() }

    return $branchesRemote
}
#🔥
function Get-FileDiffs {
    param(
        [string]$Branch
    )
    $diffs = git diff main..$Branch --name-only

    $filteredDiffs = New-Object System.Collections.ArrayList

    foreach ($item in $diffs) {
        $matched = $false
        foreach ($pattern in $ignore) {
            if ($item -match $pattern) {
                $matched = $true
                break
            }
        }
        if (-not $matched) {
            #$filteredDiffs.Add($item)
            $filteredDiffs += $item
        }
    }

    return $filteredDiffs
}
#🔥
function Get-ContentDiff {
    param (
        [string]$File,
        [string]$Branch,
        [string]$BaseA = "main"
    )
    #displays the changes that have been made in the $Branch that are not present in the $BaseA
    $difference = git diff "$($BaseA)..$($Branch)" -- $File

    return $difference
}
#🔥
function Save-Diffs {
    param(
        [array]$Content,
        [string]$File,
        [string]$Branch,
        [string]$BaseA = "main",
        [string]$OutputFolder = "C:\Users\vitim\Documents\sources\javascript\apps\gitpick"
    )
    #should save in the diffs.json the new object with its new content property
    $outputFile = "$($OutputFolder)\diffs.json"
    #the new content to include
    $arrayContent = New-Object System.Collections.ArrayList
    for ($i = 0; $i -lt $Content.Count; $i++) {
        $arrayContent += $Content[$i]
    }
    #get the name of the pair
    $pair = "$($BaseA)_$($Branch)"

    # Create a hash table for the branch if it doesn't exist
    if (-not (Test-Path $outputFile)) {
        $diffs = @{}
        # Create a new object
        $newObject = @{
            $pair = @{
                $File = $arrayContent
            }
        }
         # Add the new object
        $diffs = $newObject
        # save in the file
        $diffs | ConvertTo-Json -Depth 100 | Set-Content -Path $outputFile
    }
    # Read the existing JSON data from the file
    else {
        # Convert $diffs into a hash table
        $diffsHash = Get-Content -Raw $outputFile | ConvertFrom-Json
        $hashTable = @{}
        $diffsHash.psobject.properties | ForEach-Object { $hashTable[$_.Name] = $_.Value }
        # The Pair exist
        if( $hashTable.$pair ){
            # need transfor to hashtable too
            $htPair = @{}
            $hashTable.$pair.psobject.properties | ForEach-Object { $htPair[$_.Name] = $_.Value }

            $addNewDiff = @{
                $File = $arrayContent
            }
            $htPair += $addNewDiff
            $hashTable.$pair = $htPair
        }
        # Create a Pair
        else{
            $addObject = @{
                $pair = @{
                    $File = $arrayContent
                }
            }
            # Add the new object to the hash table
            $hashTable += $addObject
        }
        # convert to json and save the file
        $hashTable | ConvertTo-Json -Depth 100 | Set-Content -Path $outputFile
    }

    Write-Host "Saved the encrypted diff for $File in branch $Branch." -ForegroundColor Green
}
#🔥
function Set-Checkout {
    param (
        [array]$Branches
    )
    foreach ($branch in $Branches) {
        # Check if the branch exists locally
        $branchExists = git branch --list $branch
        if ($branchExists) {
            Write-Host "Branch already in local repository" -ForegroundColor Green
        }
        else {
            try {
                git checkout $branch
                Start-Sleep -Seconds 1
            }
            catch {
                Set-ForceCheckout -Branch $branch
            }
        }
    }
}
#🔥
function Set-ForceCheckout {
    param(
        [string]$Branch
    )
    git fetch origin
    Start-Sleep -Seconds 1
    git checkout -b $Branch origin/$Branch
    Start-Sleep -Seconds 1
    git branch --set-upstream-to=origin/$Branch $Branch
    Write-Host "Forced Checkout to [${$Branch}]" -ForegroundColor Yellow
}
#🔥
function Get-Repository {
    param (
        [string]$URL,
        [string]$OutputFolder = "source"
    )

    if (-not (Test-Path ".\${$OutputFolder}")) {
        git clone $URL $OutputFolder
    }
    else {
        Write-Host "Project folder Already Exist" -ForegroundColor Cyan
    }
}

Get-Repository -URL $RepoURL -OutputFolder $DiretorioDestino

Push-Location $DiretorioDestino

# $contentDiffers = Get-ContentDiff -File "smart/android/app/src/main/kotlin/comercial/terasmart/terabytesolucoes/com/br/smart/MainActivity.kt" -Branch "cead"
# Save-Diffs -Content $contentDiffers -File "smart/android/app/src/main/kotlin/comercial/terasmart/terabytesolucoes/com/br/smart/MainActivity.kt" -Branch "cead"
$branches = Get-Branches
Set-Checkout -Branches $branches
foreach ($branch in $branches) {
    $fileDiffers = Get-FileDiffs -branch $branch
    foreach ($file in $fileDiffers) {
        $contentDiffers = Get-ContentDiff -File $file -Branch $branch
                
        Save-Diffs -Content $contentDiffers -File $file -Branch $branch
    }
}

Pop-Location
