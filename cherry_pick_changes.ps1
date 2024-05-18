# Define the source branch with the changes
$sourceBranch = "infinite"

# Get the list of all branches
$branches = git branch --list | ForEach-Object { $_.Trim() -replace '\* ', '' }

# Get the latest commit hash from the source branch
$latestCommit = git log -n 1 --pretty=format:"%H" $sourceBranch

Write-Host "Source branch: $sourceBranch"
Write-Host "Latest commit hash from source branch: $latestCommit"
Write-Host "Branches to cherry-pick into: $branches"

# Loop through each branch and cherry-pick the changes
foreach ($branch in $branches) {
    if ($branch -ne $sourceBranch) {
        Write-Host "Cherry-picking changes into $branch"
        git checkout $branch

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to checkout branch $branch" -ForegroundColor Red
            continue
        }

        git cherry-pick $latestCommit

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to cherry-pick commit into branch $branch" -ForegroundColor Red
            # Optionally, abort the cherry-pick if there's a conflict
            git cherry-pick --abort
            continue
        }
    }
}

# Checkout back to the source branch at the end
git checkout $sourceBranch

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to checkout back to source branch $sourceBranch" -ForegroundColor Red
}