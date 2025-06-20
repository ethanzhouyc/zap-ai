# Generating Code for Matter, Zigbee or a Custom SDK

The following sections describe how to generate code using ZAP.


## Generate Code Using ZAP UI

Launch the ZAP UI as per the instructions in Launching ZAP for Matter or Zigbee and click on the Generate button in the top menu bar.


## Generate Code without the UI

The following instructions provide different ways of generating code through CLI without launching the ZAP UI.

### Generating Code from ZAP Source

Run the following command to generate code using ZAP from [source](https://github.com/project-chip/zap):

```node src-script/zap-generate.js --genResultFile --stateDirectory ~/.zap/gen -z ./zcl-builtin/silabs/zcl.json -g ./test/gen-template/zigbee/gen-templates.json -i ./test/resource/three-endpoint-device.zap -o ./tmp```

### Generating Code from ZAP Executable

Run the following command to generate code using ZAP [executable](https://github.com/project-chip/zap/releases):

```[zap-path] generate --genResultFile --stateDirectory ~/.zap/gen -z ./zcl-builtin/silabs/zcl.json -g ./test/gen-template/zigbee/gen-templates.json -i ./test/resource/three-endpoint-device.zap -o ./tmp```


### Generating Code from ZAP CLI Executable

Run the following command to generate code using ZAP [CLI Executable](https://github.com/project-chip/zap/releases):

```[zap-cli-path] generate --genResultFile --stateDirectory ~/.zap/gen -z ./zcl-builtin/silabs/zcl.json -g ./test/gen-template/zigbee/gen-templates.json -i ./test/resource/three-endpoint-device.zap -o ./tmp```