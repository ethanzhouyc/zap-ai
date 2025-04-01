# Data Model and ZCL Specification Compliance

This feature in ZAP helps users see compliance failures for Data Model or ZCL with their existing ZAP configurations. The warning messages for compliance failures will appear on the `Notifications` pane in the ZAP UI and will also be logged onto the console when running ZAP through the CLI. The compliance feature currently provides warnings for device type compliance and cluster compliance on an endpoint.

## Compliance Warnings in the ZAP UI
When a user opens a .zap file using the ZAP UI they will see warnings in the notifications pane of the ZAP UI for all the compliance failures. For example, the image below shows the session notifications page after a .zap file was opened with compliance issues.

![Display Compliance Notifications](./resources/spec-compliance-warnings.png)

The compliance messages will go away once the issues are resolved using the ZAP UI such that you can keep track of only the remaining compliance issues. New warnings will also show up for compliance if user disables mandatory elements(cluster/commands/attributes) of the configuration. Specification compliance notifications will always keep track of any failures that are introduced into the ZAP configuration but note that the warnings which show up during the opening of a .zap file are more elaborate on why it failed compliance when compared to the warnings which show up while interacting with the UI. This is by design and a full compliance check is performed during the opening of a .zap file.


## Compliance Warnings on the Console
When a user opens a .zap file using the ZAP standalone UI or the ZAP CLI they will see warnings logged into the console/terminal for all the compliance failures. For example, the image below shows the session notification warnings on the console/terminal after a .zap file was opened with compliance issues.

![Display Compliance Notifications on Console](./resources/spec-compliance-warnings-console.png)