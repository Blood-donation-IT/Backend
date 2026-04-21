import grpc

from contracts.oauth import oauth_pb2, oauth_pb2_grpc


class OAuthGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def google_sign_in(
        self, id_token: str, email: str = "", name: str = "", avatar_url: str = ""
    ) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = oauth_pb2_grpc.OAuthServiceStub(channel)
            request = oauth_pb2.GoogleSignInRequest(
                id_token=id_token,
                email=email,
                name=name,
                avatar_url=avatar_url,
            )
            response = await stub.GoogleSignIn(request)
            return {
                "success": response.success,
                "message": response.message,
                "user_id": response.user_id,
                "email": response.email,
                "name": response.name,
                "avatar_url": response.avatar_url,
                "access_token": response.access_token,
                "refresh_token": response.refresh_token,
                "is_new_user": response.is_new_user,
            }
