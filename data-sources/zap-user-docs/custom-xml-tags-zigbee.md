# Custom XML Tags for Zigbee

The following document talks about each of the xml tags associated with Zigbee.

- Each xml file is listed between the `configurator` tags: 
```xml
  <configurator></configurator>
```

- Data types can be defined within the `configurator` tag. Zigbee currently supports the definition of bitmaps, enums, integers, strings or structs. Before defining more types make sure to check all the existing atomic types defined in types.xml and all the non-atomic types defined in the other xml files. You may define them as follows:
  - Bitmap:
    - name: name of bitmap type.
    - type: Bitmap with a size between 8-64 bits can be defined, all of which should be multiples of 8.
    - Each bitmap can have multiple fields with a name and a mask associated with it.
    - eg:
    ```xml
    <bitmap name="bitmapName" type="BITMAP8">
        <field name="field1" mask="0x0F"/>
        <field name="field2" mask="0xF0"/>
    </bitmap>```
  
  - Enum:
    - name: name of enum type.
    - type: Enum with a size between 8-64 bits can be defined, all of which should be multiples of 8.
    - Each enum can have multiple items with a name and a value associated with it.
    - eg:
    ```xml
    <enum name="enumName" type="ENUM8">
        <item name="enumItem1" value="0x00"/>
        <item name="enumItem2" value="0x10"/>
        <item name="enumItem3" value="0x20"/>
    </enum>```
  
  - Integer:
    - Integer types are already defined under atomic types which exist in types.xml. Their size can range from 8-64 bits and can be signed or unsigned.
    - eg:
    ```xml
    <type id="0x28" name="int8s" size="1" description="Signed 8-bit integer" signed="true"/>
    ```

  - String:
    - String types are already defined under atomic types which exist in types.xml. Current string types include octet string, char string, long octet string and long char string
    - eg:
    ```xml
    <type id="0x44" name="long_char_string" description="Long character string" discrete="true" string="true" char="true" long="true"/>
    ```

  - Struct:
    - name: name of struct type.
    - Each struct can have multiple items with a name and a type associated with it. The type can be any predefined types under data types.
    - eg:
    ```xml
    <struct name="structname">
        <item name="structItem1" type="INT8U"/>
        <item name="structItem2" type="[Any defined type name in the xml files]"/>
    </struct>
    ```

- Custom Clusters can be defined within the `configurator` tag.
  - name: name of the cluster
  - domain: domain of the cluster. The cluster will show up in the ZAP UI under this domain.
  - description: Descirption of the cluster
  - code: cluster code
  - define: cluster define which is used by code generator to define the cluster in a certain way
  - manufacturerCode: Used to define a manufacturing specific cluster. This has to be between 0xfc00 - 0xffff. The manufacturer code for the cluster needs to be defined as follows: 
  ```xml
  <cluster manufacturerCode="0x1002">
  ```
    - A manufacturing cluster automatically makes the attributes and commands under it of the same manufacturer code unless they explicitly  list the manufacturer code.
  - introducedIn: Used to determine the spec version in which the cluster was introduced. This is used by code generator to add additional logic.
  - removedIn: Used to determine the spec version in which the cluster was removed. This is used by code generator to add additional logic.
  - singleton(boolean): Is used to determine a cluster as a singleton such that there is only one instance of that cluster shared across the endpoints.
  - attribute:
    - defines an attribute for the cluster
    - name: Name of attribute is mentioned between the attribute tag.
    ```xml
    <attribute>attribute name</attribute>
    ```
    - side(client/server): The side of the cluster to which the attribute is associated too.
    - code: attribute code
    - manufacturer code: This can be used to define a manufacturer specific attribute outside the zigbee specification mentioned by the standard xml.
    - define: attribute define which is used by code generator to define an attribute in a certain way
    - type: the type of the attribute which can be any of the data types mentioned in the xml
    - default: default value for the attribute.
    - min: Minimum allowed value for an attribute
    - max: Maximum allowed value for an attribute
    - writable: Is attribute value writable or not. This can be used to prevent the attribute from being modified by write commands.
    - optional(boolean): Used to determine if an attribute is optional or not for the cluster.
    - min: Minimum allowed value for an attribute when it is an integer, enum or bitmap type.
    - max: Maximium allowed value for the attribute when it is an integer, enum or bitmap type
    - length: Used to specify the maximum length of the attribute when it is of type string.
    - minLength: Used to specify the minimum length of the attribute when it is of type string.
    - reportable(boolean): Tells if an attribute is reportable or not
    - isNullable(boolean): Allows null values for the attribute.
    - array(boolean): Used to declare an attribute of type array.
    - introducedIn: Used to determine the spec version in which the attribute was introduced. This is used by code generator to add additional logic.
    - removedIn: Used to determine the spec version in which the attribute was removed. This is used by code generator to add additional logic.
  - command:
    - define a command for a cluster
    - name: Name of command.
    ```xml
    <command name="commandName"></command>
    ```
    - code: command code
    - manufacturer code: This can be used to define a manufacturer specific command outside the zigbee specification mentioned by the standard xml.
    - description: description of the command
    - source(client/server): source of the command.
    - optional(boolean): Used to determine if a command is optional or not for the cluster.
    - introducedIn: Used to determine the spec version in which the command was introduced. This is used by code generator to add additional logic.
    - removedIn: Used to determine the spec version in which the command was removed. This is used by code generator to add additional logic.
    - command arguments:
      - Each command can have a set of command arguments
      - name: name of the command argument
      - type: type of the command argument which could be any of the types mentioned in the xml.
      - min: Minimum allowed value for an argument when it is an integer, enum or bitmap type.
      - max: Maximium allowed value for an argument when it is an integer, enum or bitmap type
      - length: Used to specify the maximum allowable length for a command argument when it is of type string.
      - minLength: Used to specify the minimum allowable length for a command argument when it is of type string.
      - array(boolean): To determine if the command argument is of type array.
      - presentIf(string): This can be a conditional string of logical operations based on other command arguments where you can expect the command argument if the conditional string evaluates to true.
      eg:
      ```xml
      <arg name="transitionTime" type="INT16U" presentIf="status==0"/>
      ```
      Note: Here `status` is another command argument name.
      - optional(boolean): Used to determine the command argument as optional.
      - countArg: Used when the command argument is of type array. This is used to mention the other command argument which denotes the size of array for this argument.
      ```xml
      <arg name="numberOfAg" type="INT8U"/>
      <arg name="zoneIds" type="INT8U" array="true" countArg="numberOfZones"/>
      ```
      - introducedIn: Used to determine the spec version in which the command argument was introduced. This is used by code generator to add additional logic.
      - removedIn: Used to determine the spec version in which the command argument was removed. This is used by code generator to add additional logic.
- Cluster Extension can be defined within the `configurator` tag.
  - Cluster extension is used to extend a standard cluster with manufacturing attributes and commands
  - eg
  ```xml
  <clusterExtension code="0x0006">
    <attribute side="server" code="0x0000" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME" type="INT16U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1002">Sample Mfg Specific Attribute: 0x0000 0x1002</attribute>
    <attribute side="server" code="0x0000" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_2" type="INT8U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1049">Sample Mfg Specific Attribute: 0x0000 0x1049</attribute>
    <attribute side="server" code="0x0001" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_3" type="INT8U" min="0x0000" max="0xFFFF" writable="true" default="0x00" optional="true" manufacturerCode="0x1002">Sample Mfg Specific Attribute: 0x0001 0x1002</attribute>
    <attribute side="server" code="0x0001" define="SAMPLE_MFG_SPECIFIC_TRANSITION_TIME_4" type="INT16U" min="0x0000" max="0xFFFF" writable="true" default="0x0000" optional="true" manufacturerCode="0x1049">Sample Mfg Specific Attribute: 0x0001 0x1040</attribute>
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
