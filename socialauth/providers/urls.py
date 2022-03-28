def _create_provider_urls():
    """
    :return: Django urls
    :rtype: list
    """
    from django.urls import path, include
    from . import registry

    urls = []

    for provider in registry.get_providers_list():
        provider_id = provider.id
        provider_module_name = provider.get_module_name()
        provider_url_module = f"{provider_module_name}.urls"
        urls.append(path(f"{provider_id}/", include(provider_url_module)))

    return urls


urlpatterns = _create_provider_urls()
