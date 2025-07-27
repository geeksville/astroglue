# You probably don't want this

unformatted musings...

git add -A; git commit -m "Fix goreleaser permissions"

git tag -f -a v0.0.1 -m "testing goreleaser CI"
git push origin --tags -f

## Setup CLI options

go install github.com/spf13/cobra-cli@latest
go mod init github.com/geeksville/astroglue

See https://github.com/spf13/cobra/blob/main/site/content/user_guide.md 

cobra-cli init --author "Kevin Hester kevinh@geeksville.com" --license GPL-3.0
cobra-cli add serve
cobra-cli add config
cobra-cli add create -p 'configCmd'

scope add myasi 
scope set myasi --ip 192.168.0.45 --archive-subs=true/false --archive-other=true/false (defaults true)
scope list

archive add --dir=/bigdisk
archive add --astroglue
archive list

set --author="myname kevinh@geeksville.com" --attribution="How I want my stuff attributed"

group add public # by default anyone on the web can use/see my stuff
group add clubname # by anyone in that group can see use my stuff
group list

watch on: look for devices (telescopes) appearing on the LAN, when found move images to local archive
watch off: stop looking for devices
