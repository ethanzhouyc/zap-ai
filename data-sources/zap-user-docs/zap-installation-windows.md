# ZAP Installation for Windows OS


## 1. Windows Powershell

In the desktop search bar, input `Windows Powershell` and run as administrator. Run all the following commands inside Powershell.


## 2. Chocolatey

Install from https://chocolatey.org/install.

Check if installed properly with the following commands:
```bash
choco -v
```
Install pkgconfiglite package with the following commands:
```bash
choco install pkgconfiglite
```


## 3. Install Node

Run the following commands to install:
```bash
choco install nodejs-lts
```
*The version has to be 18 to pass version check test, after install, check with `node -v`

*If you have installed Node already, and fail some tests similar to `cannot find Node`, reinstall Node with chocolatey again.


## 4. Follow the Basic Instructions to Install ZAP

Follow the ZAP installation instructions from source in [ZAP Installation](zap-installation.md). While following the basic instructions for installing ZAP watch out for the following errors and how to resolve them:

### sqlite3

When running ZAP (e.g., `npm run zap`), if you see an error about `sqlite3.node` in a pop up window, run:
```bash
npm rebuild sqlite3
```

### electron-builder

When doing npm install, in post-install, if an error occurs on the following command related to `electron-builder install-app-deps`, `npx electron-rebuild canvas failed` or `node-pre-gyp`, the current `canvas` version is not compatible with Windows and the installation error will not cause a failure in running ZAP. node-canvas is working on the solution now and the issue will be solved in the near future.
```bash
"postinstall": "electron-builder install-app-deps && husky install && npm rebuild canvas --update-binary && npm run version-stamp"
```

### Canvas

If `npm run test` fails because of the error `Test suite failed to run. Cannot find module '../build/Release/canvas.node'` or `\zap\node_modules\canvas\build\Release\canvas.node is not a valid Win32 application.`, rebuild canvas as follows:
```bash
npm rebuild canvas --update-binary
```

### get index.html or Other Server Issues

If `npm run test` fails because of the error `get index.html request failed with status code 404` in unit tests or having server connection issues in e2e-ci tests, run the following commands:
```bash
npm run build
```

### Other

Check if the node version is v18 and try to install it with Chocolatey.