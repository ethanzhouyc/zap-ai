# ZAP Installation

The following sections describe ZAP installation and how to update ZAP in Simplicity Studio IDE.


## Downloading the ZAP Executable (Recommended)

This is the recommended way of getting started with ZAP. You can get the latest ZAP binaries from https://github.com/project-chip/zap/releases. Prebuilt binaries come in two different versions.

- Official release: Verified builds with dedicated Matter and Zigbee test suites. The release name format is vYYYY.DD.MM.
- Pre-release: Builds with the latest features and bug fixes but these builds are NOT verified with dedicated Matter and Zigbee test suites. The release name format is vYYYY.DD.MM-nightly.


## Installing ZAP from Source

### Basic instructions to Install ZAP

Because this is a node.js application, you need the node environment installed. The best way to do this is download the latest install of [node](https://nodejs.org/en/download/), which includes node and npm. If you have an older version of node installed on your workstation, it may cause issues, particularly if it's very old. Make sure you have the latest node v16.x version with the npm that's included. Run `node --version` to check which version is picked up. v18.x is recommended.

After you have a desired version of node, you can run the following:

#### Install the Dependencies

Use the following commands to install dependencies:

```bash
npm install
```
Note: For Windows-specific ZAP installation, see [ZAP Installation for Windows OS](zap-installation-windows.md)

It is not uncommon to run into native library compilation problems at this point.
There are various `src-script/install-*` scripts for different platforms. See [FAQ](faq.md) information about which script to run on different platforms and then rerun `npm install`.

#### Start the Application

Use the following commands to start up the application:

```bash
npm run zap
```

#### Start the Front-End in Development Mode

Supports hot-code reloading, error reporting, and so on.
Use the following commands to start the front-end in development mode:

```bash
quasar dev -m electron
```

or

```bash
npm run electron-dev
```