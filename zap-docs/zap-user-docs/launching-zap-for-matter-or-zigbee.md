# Launching ZAP for Matter or Zigbee Applications

The following sections describe launching ZAP in standalone mode with the Matter or Zigbee-specific metadata. The idea is to launch ZAP with the correct arguments related to XML metadata (the clusters and device types definitions as per the CSA specifications) and the generation templates, which are used to generate the appropriate code.


## Launching ZAP with Matter

The following script picks up the correct metadata from the Matter [SDK](https://github.com/project-chip/connectedhomeip) when launching ZAP.

https://github.com/project-chip/connectedhomeip/blob/master/scripts/tools/zap/run_zaptool.sh

Note: You can also take to the following Zigbee approach to launch ZAP in Matter.


## Launching ZAP with Zigbee

The following command launches ZAP with the ZCL specifications and generation templates from the [SDK](https://github.com/SiliconLabs/gecko_sdk).

```[zap-path] -z [sdk-path]/gsdk/app/zcl/zcl-zap.json -g [sdk-path]/gsdk/protocol/zigbee/app/framework/gen-template/gen-templates.json```

- zap-path: This is the path to the ZAP source or executable
- sdk-path: This is the path to the SDK


## Launching ZAP without Metadata

Remember that when launching ZAP directly through an executable or from source using `npm run zap` you are launching ZAP with test metadata for Matter/Zigbee built in within ZAP and not the actual metadata coming from the Matter and Zigbee SDKs mentioned above. Therefore, remember to create your ZAP configurations by using the SDK metadata and not by opening ZAP directly with the built in test metadata.