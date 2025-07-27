# You probably don't want this

unformatted musings...

git add -A; git commit -m "Fix goreleaser permissions"

git tag -f -a v0.0.1 -m "testing goreleaser CI"
git push origin --tags -f

## Setup CLI options

go install github.com/spf13/cobra-cli@latest
go mod init github.com/geeksville/astroglue

Setup per https://github.com/spf13/cobra/blob/main/site/content/user_guide.md 

cobra-cli init --author "Kevin Hester kevinh@geeksville.com" --license GPL-3.0
cobra-cli add serve
cobra-cli add config
cobra-cli add create -p 'configCmd'

FIXME check to make sure multiple scans can't be running at once


