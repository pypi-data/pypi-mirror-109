from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.webapp.constants import FieldMode


class AzureFunctionApp(AzureResource):
    """
        Attributes:
            name: Function app resource name.
            auth_settings: Function app authentication settings.
            http2_enabled: Indication if http2 protocol should be enabled or not.
            minimum_tls_version: The minimum supported TLS version for the function app.
    """
    def __init__(self, name: str, auth_settings: AuthSettings, http2_enabled: bool,
                 minimum_tls_version: str, client_cert_mode: FieldMode = None) -> None:
        super().__init__(AzureResourceType.AZURERM_FUNCTION_APP)
        self.name = name
        self.auth_settings: AuthSettings = auth_settings
        self.client_cert_mode: FieldMode = client_cert_mode
        self.http2_enabled: bool = http2_enabled
        self.minimum_tls_version: str = minimum_tls_version
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.name, self.location]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Function App'
        else:
            return 'Function Apps'

    @property
    def is_tagable(self) -> bool:
        return True
