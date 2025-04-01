# Matter Device Type Feature Page

ZAP supports visualizing and toggling Matter features in the device type feature page. Only device type features specified in [matter-devices.xml](https://github.com/project-chip/connectedhomeip/blob/master/src/app/zap-templates/zcl/data-model/chip/matter-devices.xml) in CHIP repository will be displayed.

![Device Type Feature Page](./resources/feature-page.png)

## Navigating to the Feature Page
- Launch ZAP in Matter with up-to-date Matter SDK.
- Create an endpoint with a Matter device type.
- Click the `Device Type Features` button on the top middle of the cluster view. Note that this button is available only in ZAP configurations for Matter and when conformance data exists in the Matter SDK.
- Clicking this button will open the above image. 

## Conformance

Conformance defines optionality and dependency for attributes, commands, events, and data types. It determines whether an element is mandatory, optional, or unsupported under certain ZAP configurations.

Device type's feature conformance takes precedence over cluster's feature conformance. For example, the Lighting feature has optional conformance in the On/Off cluster but is declared as mandatory in the On/Off Light device type that includes the On/Off cluster. Creating an endpoint with the On/Off Light device type will show the Lighting feature as mandatory in the feature page.

## Feature Toggling
On the feature page, after clicking the toggle button to enable or disable a feature, ZAP will:

- Update associated elements (attributes, commands, events) to correct conformance, and display a dialogue showing the changes.
- Update the feature bit in the featureMap attribute of the associated cluster

| ![Enable Dialog](./resources/enable-dialog.png) | ![Disable Dialog](./resources/disable-dialog.png) |
|:-----------------------------------------------:|:------------------------------------------------:|
| *Enable Feature Dialogue*                | *Disable Feature Dialogue*                |

Toggling is disabled for some features when their conformance has an unknown value or a currently unsupported format. In this case, ZAP will show warnings in the notification pane.

## Element Conformance Warnings
When toggling an element, ZAP may display both [device compliance warnings](./spec-check.md) and conformance warnings. If the element's state does not match the expected conformance, ZAP will display a warning icon and log the warning in the notification pane.

Example of both compliance and conformance warnings displayed for an element:

![Element Warnings](./resources/element-warning.png)