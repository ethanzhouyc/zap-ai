# Update ZAP



## Update ZAP in Simplicity Studio

This mechanism can be used when working with Matter extension or Zigbee from the Silicon Labs SDK releases. ZAP can be updated within Simplicity Studio without a Simplicity Studio release by downloading the latest [ZAP executable (recommended)](https://github.com/project-chip/zap/releases) or pulling the latest from [ZAP source](https://github.com/project-chip/zap) as shown in [ZAP Installation Guide](../zap-getting-started/zap-installation.md). After you have the latest ZAP based on your currently used OS, you can update ZAP within Studio as an adapter pack. Follow the instructions below after downloading the latest ZAP:

- Go to Simplicity Studio and select `Preferences > Simplicity Studio > Adapter Packs.`
- Click `Add...` and browse to the expanded ZAP folder you downloaded and click `Select Folder`.
- Click `Apply and Close` and then the newly-added ZAP will be used whenever a .zap file is opened.

Note: Sometimes there might be older instances of ZAP already running even after updating to the latest ZAP. Make sure to end all existing ZAP instances such that the newly fetched ZAP is used instead of an old instance, which is still working in the background.

## Update ZAP for Matter Development in Github

When working with the [Matter](https://github.com/project-chip/zap) or [Matter-Silicon Labs](https://github.com/SiliconLabs/matter) repos on Github, set the environment variables with respect to ZAP to create/generate new ZAP configurations or re-generate existing sample ZAP configurations after applying changes to them. Set the `ZAP_DEVELOPMENT_PATH` to [ZAP from source](https://github.com/project-chip/zap) by pulling the latest or set `ZAP_INSTALLATION_PATH` to [ZAP executable](https://github.com/project-chip/zap/releases) you downloaded last in your local directory. Note that when both `ZAP_DEVELOPMENT_PATH` and `ZAP_INSTALLATION_PATH` are set, `ZAP_DEVELOPMENT_PATH` is used.

The following are examples that show the above environment variables in use:
- [Launching ZAP using Matter specification](https://github.com/project-chip/connectedhomeip/blob/master/scripts/tools/zap/run_zaptool.sh)
- [Regenerating all the sample ZAP configurations for Matter applications](https://github.com/project-chip/connectedhomeip/blob/master/scripts/tools/zap_regen_all.py)


Note: When using ZAP executables, ensure you are using an official release over a nightly release for more stability. See `Downloading the ZAP Executable` in [ZAP Installation Guide](../zap-getting-started/zap-installation.md)