from nimbo import CONFIG
from nimbo.core.cloud_provider.provider_impl.aws.aws_provider import AwsProvider
from nimbo.core.cloud_provider.provider_impl.gcp.gcp_provider import GcpProvider
from nimbo.core.config.common_config import CloudProvider

if CONFIG.cloud_provider == CloudProvider.AWS:
    Cloud = AwsProvider()
else:
    Cloud = GcpProvider()
