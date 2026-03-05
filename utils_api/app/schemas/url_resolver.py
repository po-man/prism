from app.services.model_generator import create_dynamic_model


UrlResolverRequest = create_dynamic_model("v1/search.schema.json")
UrlResolverResponse = create_dynamic_model("v1/search.schema.json")

UrlResolverItem = UrlResolverRequest.model_fields["search_results"].annotation.__args__[0]