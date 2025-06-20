# Frequently Asked Questions


**Q: How to start up UI in a development mode?**

**A:**

You can start the UI in a development mode, which will result in a
following setup:

- Separate quasar development HTTP server, which does live refresh on port 8080
- ZAP back end running on port 9070
- Chrome or other browser, running independently

To get to that setup, follow the instructions below.

1. First, run the ZAP development server, which starts on port 9070.

```bash
npm run zap-devserver
```

2. Next, run the quasar development server, which starts on port 8080.

```bash
quasar dev
```

3. Point your browser or run one against the proper URL with the `restPort` argument:

```bash
google-chrome http://localhost:8080/?restPort=9070
```

---

**Q: How to make this work on Mac/Linux OS?**

**A:**

`npm install` is used to download all required dependency packages.

If you see errors related to `node-gyp` and missing local libraries, like `pixman`, and so on, you are missing native dependencies to satisfy to compile non-prebuilt node binaries for some combination of platforms and versions. Npm on the cloud is constantly updating the list of provided binaries, so it's possible that you will pick them up just fine, but if you don't, these are instructions for different platforms:

**Fedora Core** with `dnf`:

```bash
dnf install pixman-devel cairo-devel pango-devel libjpeg-devel giflib-devel
```

or run script:

```bash
src-script/install-packages-fedora
```

**Ubuntu** with `apt-get`:

```bash
apt-get update
apt-get install --fix-missing libpixman-1-dev libcairo-dev libsdl-pango-dev libjpeg-dev libgif-dev
```

or run script:

```bash
src-script/install-packages-ubuntu
```

**OSX on a Mac** with Homebrew `brew`:

```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

or run script:

```bash
src-script/install-packages-osx
```

---

**Q: How to make this work on Windows OS?**

**A:**

Make sure it's always up to date and there are no changes that haven't been committed. Tip: git pull, git status & git stash are your friends.

You must use Chocolately to make Zap work on Windows OS. Make sure to download the pkgconfiglite package.

```bash
choco install pkgconfiglite
```

If you have issues with cairo, for example if you get an error about cairo.h': No such file or directory, do the following:

1. Check if your computer is 32 or 64 bit.
2. Depending on that, download the appropriate package from this site https://github.com/benjamind/delarre.docpad/blob/master/src/documents/posts/installing-node-canvas-for-windows.html.md.
3. Create a folder on your C drive called GTK if it doesn't already exist.
4. Unzip the downloaded content into C:/GTK.
5. Copy all the dll files from C:/GTK/bin to your node_modules/canvas/build/Release folder in your zap folder.
6. Add C:/GTK to the path Environment Variable by going to System in the Control Panel and doing the following:

- Click on Advanced System Settings.
- In the advanced tab click on Environment Variables.
- In the section System Variables, find the PATH environment variable and select it.
- Click Edit and add C:/GTK to it.
- If the PATH environment variable does not exist, click New.

If jpeglib.h is not found, try the following:

1. On the terminal, run:
   choco install libjpeg-turbo
2. Make sure it's clean by using:
   git clean -dxff and run npm install again
3. if no errors occur and only warnings appear, try to use
   npm audit fix
4. if you can't run ZAP, go to file src-script/zap-start.js
5. Change
6. `const { spawn } = require('cross-spawn')`
   to
   `const { spawn } = require('child_process')`
7. Run npm and run zap.

References:

- https://github.com/fabricjs/fabric.js/issues/3611
- https://github.com/benjamind/delarre.docpad/blob/master/src/documents/posts/installing-node-canvas-for-windows.html.md
- https://chocolatey.org/packages/libjpeg-turbo#dependencies

---

**Q: I get an error "sqlite3_node" not found or similar.**

**A:** Rebuild your native sqlite3 bindings.

To fix this in most cases, run:

- `npm install`
- `./node_modules/.bin/electron-rebuild -w sqlite3 -p`

If it still doesn't get fixed, do:

- `rm -rf node_modules`
  and then try the above commands again.

Occasionally upgrading your `npm` also makes a difference:

- `npm install -g npm`

---

**Q: I get an error "The N-API version of this Node instance is 1. This module supports N-API version(s) 3. This Node instance cannot run this module."**

**A:** Upgrade your node version.

The solution for this is discussed in this Stack Overflow thread: https://stackoverflow.com/questions/60620327/the-n-api-version-of-this-node-instance-is-1-this-module-supports-n-api-version

---

**Q: My development PC doesn't work with ZAP for whatever reason. Can I use a docker container?**

**A:** Yes you can. TBD.

---

**Q: How do I run ZAP inside VSCode?**

**A:** If you VSCode in your path enter the `zap` repo and type `code .` This will open ZAP in VSCode. To run ZAP in debug mode, select the ZAP workspace and click on the `Run` icon on the left hand toolbar. You will have a couple of options to choose from to run ZAP, choose `Node.js Debug Terminal`. This will open a terminal window from which you can enter `npm run zap`, which will attach the debugger and run ZAP as you would normally from the command line. Congratulations, you should now see ZAP running in the debugger. You can set breakpoints in VSCode as you would in any other IDE.

---

**Q: UI unit test fails with some errors around canvas not build for the right version of node. What do I do?**

**A:** If you see the following error:

```bash
 FAIL  test/ui.test.js
  ● Test suite failed to run
    The module 'canvas.node'
    was compiled against a different Node.js version using
    NODE_MODULE_VERSION 80. This version of Node.js requires
    NODE_MODULE_VERSION 72. Please try re-compiling or re-installing
    the module (for instance, using `npm rebuild` or `npm install`).
      at Object.<anonymous> (node_modules/canvas/lib/bindings.js:3:18)
```

then run: `npm rebuild canvas --update-binary`