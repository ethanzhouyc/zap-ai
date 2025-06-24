# Custom XML


## Adding Custom XML from the ZAP UI
- Click on "Extensions" icon in the ZAP UI.
- Click on the "+" add button to select a custom xml file
- The custom clusters, attributes, commands, etc should show up in the ZAP UI once the custom xml has been added.


## Creating your own custom XML in Zigbee

The section shows how to create your own custom clusters and extend existing standard clusters with custom attributes and commands for Zigbee.

### Manufacturer-Specific Clusters in Zigbee:
You can add manufacturer-specific clusters to a standard profile. We provide an example of this below. In order to do this you must satisfy two obligations:
- The cluster ID MUST be in the manufacturer-specific range,
  0xfc00 - 0xffff.
- The cluster definition must include a manufacturer code which will be applied to ALL attributes and commands within that cluster and must be provided when sending and receiving commands and interacting with attributes.
- Example: 
```xml
<cluster manufacturerCode="0x1002">
    <name>Sample Mfg Specific Cluster</name>
    <domain>General</domain>
    <description>This cluster provides an example of how the Application 
      Framework can be extended to include manufacturer-specific clusters.
      </description>
    <code>0xFC00</code>
    <attribute side="server" code="0x0000" define="ATTRIBUTE_ONE" type="INT8U" min="0x00" max="0xFF" writable="true" default="0x00" optional="true">ember sample attribute</attribute>
    <attribute side="server" code="0x0001" define="ATTRIBUTE_TWO" type="INT8U" min="0x00" max="0xFF" writable="true" default="0x00" optional="true">ember sample attribute 2</attribute>
    <command source="client" code="0x00" name="CommandOne" optional="true">
      <description>
        A sample manufacturer-specific command within the sample manufacturer-specific
        cluster.
      </description>
      <arg name="argOne" type="INT8U"/>
    </command>
</cluster>
```

### Manufacturer-Specific Commands in Standard Zigbee Cluster:
You can add your own commands to any standard Zigbee cluster with the following requirements:
- Your manufacturer-specific commands may use any command id within the command id range, 0x00 - 0xff. 
- You must also provide a manufacturer code for the command so that it can be distinguished from other commands in the cluster and handled appropriately.
- Example of extending the On/Off cluster with manufacturing commands:
```xml
<clusterExtension code="0x0006">
    <command source="client" code="0x00" name="SampleMfgSpecificOffWithTransition" optional="true" manufacturerCode="0x1002">
      <description>Client command that turns the device off with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
    <command source="client" code="0x01" name="SampleMfgSpecificOnWithTransition" optional="true" manufacturerCode="0x1002">
      <description>Client command that turns the device on with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
    <command source="client" code="0x02" name="SampleMfgSpecificToggleWithTransition" optional="true" manufacturerCode="0x1002">
      <description>Client command that toggles the device with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
    <command source="client" code="0x01" name="SampleMfgSpecificOnWithTransition2" optional="true" manufacturerCode="0x1049">
      <description>Client command that turns the device on with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
    <command source="client" code="0x02" name="SampleMfgSpecificToggleWithTransition2" optional="true" manufacturerCode="0x1049">
      <description>Client command that toggles the device with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
  </clusterExtension>
```

### Manufacturer-Specific Attributes in Standard Zigbee Cluster:
You can add your own attributes to any standard Zigbee cluster with the following requirements:
- Your manufacturer-specific attributes may use any attribute id within the attribute id range, 0x0000 - 0xffff. 
- You must also provide a manufacturer code for the attribute so that it can be distinguished from other attributes in the cluster and handled appropriately.
- Example of extending the On/Off cluster with manufacturing attributes:
```xml
<clusterExtension code="0x0006">
    <attribute side="server" code="0x0000" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME" type="INT16U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1002">Sample Mfg Specific Attribute: 0x0000 0x1002</attribute>
    <attribute side="server" code="0x0000" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_2" type="INT8U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1049">Sample Mfg Specific Attribute: 0x0000 0x1049</attribute>
    <attribute side="server" code="0x0001" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_3" type="INT8U" min="0x0000" max="0xFFFF" writable="true" default="0x00" optional="true" manufacturerCode="0x1002">Sample Mfg Specific Attribute: 0x0001 0x1002</attribute>
    <attribute side="server" code="0x0001" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_4" type="INT16U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1049">Sample Mfg Specific Attribute: 0x0001 0x1040</attribute>
</clusterExtension>
```


## Creating your own custom XML in Matter

The section shows how to create your own custom clusters and extend existing standard clusters with custom attributes and commands for Matter. 

### Manufacturer-Specific Clusters in Matter:
You can add manufacturer-specific clusters to in Matter. We provide an example of this below.
- The `<code>` is a 32-bit combination of the manufacturer code and the id for the cluster. (**required**)
    * The most significant 16 bits are the manufacturer code. The range for test manufacturer codes is 0xFFF1 - 0xFFF4.
    * The least significant 16 bits are the cluster id. The range for manufacturer-specific clusters are: 0xFC00 - 0xFFFE.
- In the following example, the combination of the vendor ID (Test Manufacturer ID) of 0xFFF1 and the cluster ID of 0xFC20 results in a `<code>` value of 0xFFF1FC20.
- The commands and attributes within this cluster will adopt the same Manufacturer ID.
- Example:
```xml
  <cluster>
    <domain>General</domain>
    <name>Sample MEI</name>
    <code>0xFFF1FC20</code>
    <define>SAMPLE_MEI_CLUSTER</define>
    <description>The Sample MEI cluster showcases a cluster manufacturer extensions</description>
    <attribute side="server" code="0x0000" define="FLIP_FLOP" type="boolean" writable="true" default="false" optional="false">FlipFlop</attribute>
    <command source="server" code="0x01" name="AddArgumentsResponse" optional="false" disableDefaultResponse="true">
      <description>
        Response for AddArguments that returns the sum.
      </description>
      <arg name="returnValue" type="int8u"/>
    </command>
    <command source="client" code="0x02" name="AddArguments" response="AddArgumentsResponse" optional="false">
      <description>
        Command that takes two uint8 arguments and returns their sum.
      </description>
      <arg name="arg1" type="int8u"/>
      <arg name="arg2" type="int8u"/>
    </command>
    <command source="client" code="0x00" name="Ping" optional="false">
      <description>
        Simple command without any parameters and without a response.
      </description>
    </command>
  </cluster>
```

### Manufacturer-Specific Attributes in Standard Matter Clusters:
You can add manufacturer specific attributes to any standard Matter cluster with the following requirements:
- The cluster that the attributes are being added to must be specified - `<clusterExtension code="<code of cluster being extended>">`
- The `code` of the attribute is a 32-bit combination of the manufacturer code and the id for the attribute.
    * The most significant 16 bits are the manufacturer code. The range for test manufacturer codes is 0xFFF1 - 0xFFF4.
    * The least significant 16 bits are the attribute ID. The range for non-global attributes is 0x0000 - 0x4FFF.
- Example of extending On/Off Matter cluster with manufacture-specific attributes:
```xml
<clusterExtension code="0x0006">
    <attribute side="server" code="0xFFF10000" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_2" type="INT8U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true">Sample Mfg Specific Attribute 2</attribute>
    <attribute side="server" code="0xFFF10001" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_4" type="INT16U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true">Sample Mfg Specific Attribute 4</attribute>
</clusterExtension>
```
### Manufacturer-Specific Commands in Standard Matter Clusters:
You can add manufacturer specific commands to any standard Matter cluster with the following requirements:
- The cluster that the commands are being added to must be specified - `<clusterExtension code="<code of cluster being extended>">`
- The `code` of the command is a 32-bit combination of the manufacturer code and the id for the command.
    * The most significant 16 bits are the manufacturer code. The range for test manufacturer codes is 0xFFF1 - 0xFFF4.
    * The least significant 16 bits are the command ID. The range for non-global commands is 0x0000 - 0x00FF.
- Example of extending On/Off Matter cluster with manufacture-specific clusters:
```xml
<clusterExtension code="0x0006">
    <command source="client" code="0xFFF10000" name="SampleMfgSpecificOnWithTransition2" optional="true">
        <description>Client command that turns the device on with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
    <command source="client" code="0xFFF10001" name="SampleMfgSpecificToggleWithTransition2" optional="true">
        <description>Client command that toggles the device with a transition given
        by the transition time in the Ember Sample transition time attribute.</description>
    </command>
</clusterExtension>
```

