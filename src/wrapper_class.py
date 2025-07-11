class VariantFunction:
    def __init__(
        self,
        variant_headers,
        variant_globals,
        variant_functions,
        orig_target_func_name,
        orig_target_func_param_count,
        replacer_variant_func_name,
        variant_function_names,
    ):
        self.variant_headers = variant_headers
        self.variant_globals = variant_globals
        self.variant_functions = variant_functions
        self.orig_target_func_name = orig_target_func_name
        self.orig_target_func_param_count = orig_target_func_param_count
        self.replacer_variant_func_name = replacer_variant_func_name
        self.variant_function_names = variant_function_names

    def __repr__(self):
        return f"<VariantFunction orig_target_func_name='{self.orig_target_func_name}', replacer_variant_func_name='{self.replacer_variant_func_name}'>"
