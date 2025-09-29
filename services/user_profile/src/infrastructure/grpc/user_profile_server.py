import grpc
# from src.protos.user import user_profile_pb2_grpc, user_profile_pb2
from contracts.user import user_profile_pb2_grpc, user_profile_pb2
from src.application.use_cases.create_user import CreateUserUseCase
from src.domain.entities.user import User
from google.protobuf.timestamp_pb2 import Timestamp

class UserProfileService(user_profile_pb2_grpc.UserProfileServiceServicer):
    def __init__(self,
                 create_user_profile_use_case:CreateUserUseCase,
                #  get_user_profile_use_case
                 )->None:
        self.create_user_profile_use_case:CreateUserUseCase = create_user_profile_use_case
        # self.get_user_profile_use_case = get_user_profile_use_case
    async def CreateProfile(self,
                            request:user_profile_pb2.CreateProfileRequest,
                            context:grpc.aio.ServicerContext
                            ) -> user_profile_pb2.UserProfile:
        user:User = await self.create_user_profile_use_case.execute(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
        )
        ts =Timestamp()
        return user_profile_pb2.UserProfile(
            user_id=user.id,
            full_name=user.full_name,
            email=user.email,
            blood_type=user.blood_type,
            is_verified=user.is_verified,
            total_donations=user.total_donations,
            last_donation_at=ts.FromDatetime(user.last_donation_at),
            roles=user.roles,
            is_banned=user.is_banned,
            updated_at=ts.FromDatetime(user.updated_at),
            is_active=user.is_active,
            created_at=ts.FromDatetime(user.created_at)
            
        )