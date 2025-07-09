from box_sdk_gen import BoxClient, BoxJWTAuth, JWTConfig

jwt_config = JWTConfig.from_config_file(config_file_path="../auth.json")
auth = BoxJWTAuth(config=jwt_config)
client = BoxClient(auth=auth)

service_account = client.users.get_user_me()
print(f"Service Account user ID is {service_account.id}")