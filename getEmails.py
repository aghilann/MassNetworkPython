class EmailGetter:
    @staticmethod
    def get_databricks_email(first_name, last_name):
        return f"{first_name}.{last_name}@databricks.com"

    @staticmethod
    def get_google_email(first_name, last_name):
        return f"{first_name[0]}{last_name}@google.com"

    @staticmethod
    def get_stripe_email(first_name, last_name):
        return f"{first_name}@stripe.com"

    @staticmethod
    def get_meta_email(first_name, last_name):
        return f"{first_name[0]}{last_name}@fb.com"

    @staticmethod
    def get_microsoft_email(first_name, last_name):
        return f"{first_name}.{last_name}@microsoft.com"

    @staticmethod
    def get_apple_email(first_name, last_name):
        return f"{first_name[0]}{last_name}@apple.com"

    @staticmethod
    def get_microsoft_email(first_name, last_name):
        return f"{first_name}.{last_name}@microsoft.com"

    @staticmethod
    def get_amazon_email(first_name, last_name):
        return f"{first_name}{last_name[0]}@amazon.com"

    @staticmethod
    def get_notion_email(first_name, last_name):
        return f"{first_name}@makenotion.com"
    
    @staticmethod
    def get_nvidia_email(first_name, last_name):
        return f"{first_name[0]}{last_name}@nvidia.com"

    @staticmethod
    def get_asana_email(first_name, last_name):
        return f"{first_name}{last_name}@asana.com"