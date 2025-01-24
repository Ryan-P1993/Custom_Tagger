# Custom_Tagger
Apply Custom Tags for Entities in AppDynamics

Made with Python 3.12

This script uses the APIs listed on this documentation page: https://docs.appdynamics.com/appd/24.x/25.1/en/extend-cisco-appdynamics/cisco-appdynamics-apis/custom-tag-apis#id-.CustomTagAPIsv24.10-DeleteCustomTagsforEntitiesinaGroup

Additional information on tagging; https://docs.appdynamics.com/appd/23.x/latest/en/application-monitoring/overview-of-application-monitoring#tags

# Usage
python3 custom_tag.py [-t|-d] [List of Entities] (Optional) [TagList] (Optional)

**-t** : Tags the *List of Entities* with the *TagList*.

**-d** : Deletes Tags from the selected *List of Entities*.

**List of Entities** : A List of Entities to tag. i.e. "['Ryan_Test_Application_1','Ryan_Test_Application_2']"

**TagList** : A List of Tags to apply. i.e. '[{"key" : "cheese", "value" : "Swiss" }]'

# Configuration
**controllerurl**  : URL of the AppDynamics Controller

**accountname**    : Account Name of the License

**apiclientname**  : Name of the Api Client

**apisecret**      : Secret to get the Authorization Token

