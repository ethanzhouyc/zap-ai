# Multiple Device Types Per Endpoint

This is a Matter-only feature where a user can select more than one device type per endpoint. The addition of multiple device types will add the cluster configurations within the device types to the endpoint configuration.

![Multiple Device Types Per Endpoint](./resources/multiple-device-types-per-endpoint.png)

The above image shows that endpoint 1 has more than one device types selected. The "Primary Device" denotes primary device type that the endpoint will be associated with. The primary device type is always present at index 0 of the list of device types selected so selecting a different primary device type will change the ordering of the device types selected. The device type selections also have constraints based on the Data Model Specification. ZAP protects the users from choosing invalid combinations of device types on an endpoint using these constraints.