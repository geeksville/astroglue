# Astroglue

A tool for automating/simplifying/managing/sharing repeatable astrophotography workflows and datasets.

(I'm currently just playing with ideas - so this README is super rough.  Any feedback appreciated - I'd like for this tool to be useful for others besides me...)

# Usage

This tool is invoked via one commandline command "astroglue <command> [options]", see below for details.  It is intended to work well with camera controllers such as asiair, seestar, N.I.N.A, EKOS" etc and data processing tools like Siril and Graxpert.

# Supported platforms

Windows/Linux/MacOS - with easy installers for all of the popular subflavors. 

# Features

## Version 0.1: September 2025?
* This will provide a service to scan your LAN and watch for telescopes appearing (using mDNS usually, see below for details). 
* When new images appear (either stacked/processed or raw subs, based on user preference) they will be moved to a large disk somewhere (your 'archive').  
* Filenames and FITS metadata will be used to organize files in that archive.

## Version 0.2: October 2025?
Adds the first really useful end-user feature.  

* Lets you search your archive (which is not necessarily on the machine you use for image processing) for things like 'M51 newer than 9/2024' (and optional things like 'taken with camera Y' etc...).  
* Based on these searches it will show you stats like # of matching subs, corresponding flats/darks/biases (either already specified or proposed based on time of aquisition), filter options etc...
* Once you are happy with the proposed working set you can say "astroglue work pull" and it will fetch the relevant files/metadata to construct a directory tree laid our for Siril etc...
* After you have had your fun with image processing, you can say "astroglue work push" and it will copy your new processed data (and associated metadata about which subs were selected/settings-used) back to your archive.  

See below for some early rough guesses on what the commands might look like.

## Version 0.3: TBD
Address user feedback from 0.2 (the first release likely to be useful for others) also add support for custom telescope sources (see below)

## Version 0.4: TBD
Big update.  Hopefully it will let users start saying stuff on forums like "Here's my latest version of M51 and the recipe I used to make it..." please give me feedback on said recipe.

* Use something like [IPFS](https://ipfs.tech/) behind the scenes to allow users to start sharing images/recipes/workflows with others (without file hosting hassles).  
* Probably with a nice repeatable mechanism for attribution etc... 
* Very vague for now, will tweak as experience with 0.2 occurs.

# Implementation plan

## Phase 0.1: Basic telescope scanning and snarfing into archive

* astroglue archive add --dir=/some/path/bigdisk

* astroglue scan background --enable=true/false: watch for devices (telescopes) appearing on the LAN, when found move images to local archive (this flag is persistent)
* astroglue scan once: just check once for any connected devices, and archive as needed

## Phase 0.2: Workspace pull/push for Processing tool usage

* astroglue archive list
* astroglue archive search --target=M51: print info about # of known images, sources of those images, recipes etc...

* astroglue work reset : starts a new local workspace (in the current directory)
* astroglue work add --target=M51 otheroptions=fixme : adds proposed lights/darks/flats/bias etc... and prints a summary of what it proposes
prints various messages about 'assuming flat frame X' etc... 

* astroglue work remove --older=7/2024 : by using add and remove you can tweak your working set
* astroglue work pull : pulls the actual files from the archive into the current directory formmated with subdirs sirl expects
Note: even after doing a pull you can keep using add/remove to tweak your working set as you wish

< do your favorite image processing workflow here >

* astroglue work push : store processed files back to the default archive
metadata about what was selected (and eventually siril operations etc...) will be pushed back to the archive.  This metadata can be used in the future if you wish to reedit or just see what settings you used to make a particular final image

## Phase 0.3: Allow custom telescopes

Not just mDNS scanning...

* astroglue scope add myscope 
* astroglue scope set myscope --ip 192.168.0.45 --archive-subs=true/false --archive-other=true/false (defaults true)
* astroglue scope list

## Phase 0.4: Optional sharing of images/subs with others

(This is very rough - will tweak later)

* astroglue set --author="myname kevinh@geeksville.com" --attribution="How I want my stuff attributed"
* astroglue archive add --hub=TBD

* astroglue group add public # by default anyone on the web can use/see my stuff
* astroglue group add clubname # by anyone in that group can see use my stuff
* astroglue group add myfriend
* astroglue group list

## Developing

We actively encourage others to develop on this project (and we're friendly).  In the future these instructions will get better, but if you have questions or want to change something please open a github issue and we can chat there!

### GitHub Codespaces
If you'd like to try developing on this project without needing to install **any** tools you can use a github codespace (on the web)

Follow these steps to open this sample in a Codespace:
1. Click the **Code** drop-down menu.
2. Click on the **Codespaces** tab.
3. Click **Create codespace on main** .

For more info, check out the [GitHub documentation](https://docs.github.com/en/free-pro-team@latest/github/developing-online-with-codespaces/creating-a-codespace#creating-a-codespace).

### VS Code
If you are using VSCode this project includes built in support for devcontainers.  So it should automatically install/use anything you need to build/run this while developing (compilers, auto-formatting etc...).  Should be able to just "git clone", run the app and then see your changes applied instantly.

1. If this is your first time using a development container, please ensure your system meets the pre-reqs (i.e. have Docker installed) in the [getting started steps](https://aka.ms/vscode-remote/containers/getting-started).

2. Start developing:

   - Clone this repository to your local filesystem.
   - Press <kbd>F1</kbd> and select the **Dev Containers: Open Folder in Container...** command.
   - Select the cloned copy of this folder, wait for the container to start, and try things out!
   
## Things to try

FIXME: following boilerplate needs to go.  Please ignore for now...

Once you have this sample opened, you'll be able to work with it like you would locally.

Some things to try:

1. **Edit:**
   - Open `server.go`
   - Try adding some code and check out the language features.
   - Make a spelling mistake and notice it is detected. The [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) extension was automatically installed because it is referenced in `.devcontainer/devcontainer.json`.
   - Also notice that utilities like `gopls` and the [Go](https://marketplace.visualstudio.com/items?itemName=golang.Go) extension are installed. Tools are installed in the `mcr.microsoft.com/devcontainers/go` image and Dev Container settings and metadata are automatically picked up from [image labels](https://containers.dev/implementors/reference/#labels).

2. **Terminal:** Press <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>\`</kbd> and type `uname` and other Linux commands from the terminal window.
3. **Build, Run, and Debug:**
   - Open `server.go`
   - Add a breakpoint (e.g. on line 22).
   - Press <kbd>F5</kbd> to launch the app in the container.
   - Once the breakpoint is hit, try hovering over variables, examining locals, and more.   
   - Continue (<kbd>F5</kbd>). You can connect to the server in the container by either: 
        - Clicking on `Open in Browser` in the notification telling you: `Your service running on port 9000 is available`.
        - Clicking the globe icon in the 'Ports' view. The 'Ports' view gives you an organized table of your forwarded ports, and you can get there by clicking on the "1" in the status bar, which means your app has 1 forwarded port.
   - Notice port 9000 in the 'Ports' view is labeled "Hello Remote World." In `devcontainer.json`, you can set `"portsAttributes"`, such as a label for your forwarded ports and the action to be taken when the port is autoforwarded.

   > **Note:** In Dev Containers, you can access your app at `http://localhost:9000` in a local browser. But in a browser-based Codespace, you must click the link from the notification or the `Ports` view so that the service handles port forwarding in the browser and generates the correct URL.
   
8. **Generate tests:**
    - Open `hello.go` and press <kbd>F1</kbd> and run the **Go: Generate Unit Tests For File** command.
    - Implement a test case: Open file `hello_test.go` and edit the line with the `TODO` comment: `{"hello without name", "Hello, "},` 
    - You can toggle between implementation file and test file with press <kbd>F1</kbd> and run the **Go: Toggle Test File**
    - Tests can also run as benchmarks: Open file `hello_test.go`, press <kbd>F1</kbd> and run the **Go: Benchmark File**
9. **Stub generation:** ( [details](https://github.com/josharian/impl))
   - define a struct `type mock struct {}`, enter a new line , press <kbd>F1</kbd> and run the **Go: Generate interface stubs** command.
   - edit command `m *mock http.ResponseWriter`
10. **Fill structs:** ([details](https://github.com/davidrjenni/reftools/tree/master/cmd/fillstruct))
   - Open `hello.go` and select `User{}` of variable asignment, press <kbd>F1</kbd> and run the **Go: Fill struct** command.
11. **Add json tags to structs:** ([details](https://github.com/fatih/gomodifytags))
   - Open `hello.go` and go with cursor in to a struct, press <kbd>F1</kbd> and run the **Go: Add Tags To Struct Fields** command.

## License

Some sort of open-source license TBD but probably will be GPL.  If you have opinions on this please let me know!

