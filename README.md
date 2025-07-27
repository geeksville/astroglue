# NOT READY YET

I'm currently just playing with ideas and started from this Go devcontainer...

## Developing

### GitHub Codespaces
If you'd like to try developing on this project without needing to install **any** tools you can use a github codespace (on the web)

Follow these steps to open this sample in a Codespace:
1. Click the **Code** drop-down menu.
2. Click on the **Codespaces** tab.
3. Click **Create codespace on main** .

For more info, check out the [GitHub documentation](https://docs.github.com/en/free-pro-team@latest/github/developing-online-with-codespaces/creating-a-codespace#creating-a-codespace).

### VS Code
If you are using VSCode this project includes built in support for devcontainers.  So it should automatically install/use anything you need to build/run this while developing.

1. If this is your first time using a development container, please ensure your system meets the pre-reqs (i.e. have Docker installed) in the [getting started steps](https://aka.ms/vscode-remote/containers/getting-started).

2. Start developing:

   - Clone this repository to your local filesystem.
   - Press <kbd>F1</kbd> and select the **Dev Containers: Open Folder in Container...** command.
   - Select the cloned copy of this folder, wait for the container to start, and try things out!
   
## Things to try

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
   
4. **Rebuild or update your container:** 

   You may want to make changes to your container, such as installing a different version of a software or forwarding a new port. You'll rebuild your container for your changes to take effect. 

   **Open browser automatically:** As an example change, let's update the `portsAttributes` in the `.devcontainer/devcontainer.json` file to open a browser when our port is automatically forwarded.
   
   - Open the `.devcontainer/devcontainer.json` file.
   - Modify the `"onAutoForward"` attribute in your `portsAttributes` from `"notify"` to `"openBrowser"`.
   - Press <kbd>F1</kbd> and select the **Dev Containers: Rebuild Container** or **Codespaces: Rebuild Container** command so the modifications are picked up.

6. **Refactoring - rename:**
    - Open `hello.go`, select method name `Hello` press <kbd>F1</kbd> and run the **Rename Symbol** command.
7. **Refactoring - extract:**
   - Open `hello.go` and select string, press <kbd>F1</kbd> and run the **Go: Extract to variable** command.
   - Open `hello.go` and select line with return statement, press <kbd>F1</kbd> and run the **Go: Extract to function** command.
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

