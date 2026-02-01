import grpc
# from src.protos.user import user_profile_pb2_grpc, user_profile_pb2
from contracts.user import user_profile_pb2_grpc, user_profile_pb2
from src.application.use_cases.create_user import CreateUserUseCase
from src.application.use_cases.get_user_by_id import GetUserByIdUseCase
from src.application.use_cases.update_user import UpdateUserUseCase
from src.domain.entities.user import User
from google.protobuf.timestamp_pb2 import Timestamp

ROLE_MAP = {
    "DONOR": user_profile_pb2.UserRole.DONOR,
    "DOCTOR": user_profile_pb2.UserRole.DOCTOR,
    "ADMIN": user_profile_pb2.UserRole.ADMIN,
    "UNKNOWN": user_profile_pb2.UserRole.UNKNOWN,
}

def map_roles_to_enum(roles):
    return [ROLE_MAP.get(role.upper(), user_profile_pb2.UserRole.UNKNOWN) for role in roles]


def _user_to_proto(user: User, ts: Timestamp) -> "user_profile_pb2.UserProfile":
    lives = getattr(user, "lives_saved_count", None)
    if lives is None:
        lives = (user.total_donations or 0) * 3
    return user_profile_pb2.UserProfile(
        user_id=user.id,
        name=user.full_name,
        email=user.email,
        phone=user.phone or "",
        blood_type=user.blood_type or "",
        is_verified=user.is_verified,
        total_donations=user.total_donations,
        last_donation_at=ts.FromDatetime(user.last_donation_at) if user.last_donation_at else None,
        roles=map_roles_to_enum(user.roles),
        is_banned=user.is_banned,
        updated_at=ts.FromDatetime(user.updated_at) if user.updated_at else None,
        is_active=user.is_active,
        created_at=ts.FromDatetime(user.created_at) if user.created_at else None,
        avatar_url=getattr(user, "avatar_url", None) or "",
        lives_saved_count=lives,
        donor_status=getattr(user, "donor_status", None) or "",
        has_donor_book=getattr(user, "has_donor_book", False),
        test_is_done=getattr(user, "test_is_done", False),
    )

class UserProfileService(user_profile_pb2_grpc.UserProfileServiceServicer):
    def __init__(self,
                 create_user_profile_use_case: CreateUserUseCase,
                 get_user_by_id_use_case: GetUserByIdUseCase,
                 update_user_use_case: UpdateUserUseCase,
                 )->None:
        self.create_user_profile_use_case: CreateUserUseCase = create_user_profile_use_case
        self.get_user_by_id_use_case: GetUserByIdUseCase = get_user_by_id_use_case
        self.update_user_use_case: UpdateUserUseCase = update_user_use_case
    async def CreateProfile(self,
                            request:user_profile_pb2.CreateProfileRequest,
                            context:grpc.aio.ServicerContext
                            ) -> user_profile_pb2.UserProfile:
        try:
            user_id = request.user_id if request.user_id > 0 else None
            
            user:User = await self.create_user_profile_use_case.execute(
                full_name=request.full_name,
                email=request.email,
                phone=request.phone or None,
                password_hash=request.password_hash if request.password_hash else "",
                user_id=user_id
            )
            
            ts = Timestamp()
            return _user_to_proto(user, ts)
        except ValueError as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                if request.user_id > 0:
                    try:
                        existing_user = await self.get_user_by_id_use_case.execute(request.user_id)
                        ts = Timestamp()
                        return _user_to_proto(existing_user, ts)
                    except Exception:
                        pass
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return user_profile_pb2.UserProfile()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_profile_pb2.UserProfile()

    async def UpdateProfile(self,
                            request: user_profile_pb2.UpdateProfileRequest,
                            context: grpc.aio.ServicerContext
                            ) -> user_profile_pb2.UpdateProfileResponse:
        try:
            if request.user_id <= 0:
                context.set_details("user_id is required")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return user_profile_pb2.UpdateProfileResponse(success=False, message="user_id is required")
            full_name = request.full_name if request.full_name else None
            blood_type = request.blood_type if request.blood_type else None
            avatar_url = request.avatar_url if request.avatar_url else None
            await self.update_user_use_case.execute(
                user_id=request.user_id,
                full_name=full_name,
                blood_type=blood_type,
                avatar_url=avatar_url,
            )
            return user_profile_pb2.UpdateProfileResponse(success=True, message="Profile updated")
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_profile_pb2.UpdateProfileResponse(success=False, message=str(e))
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_profile_pb2.UpdateProfileResponse(success=False, message=str(e))
    
    async def GetProfileById(self,
                            request: user_profile_pb2.GetProfileRequestById,
                            context: grpc.aio.ServicerContext
                            ) -> user_profile_pb2.UserProfile:
        try:
            user: User = await self.get_user_by_id_use_case.execute(request.user_id)
            ts = Timestamp()
            return _user_to_proto(user, ts)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_profile_pb2.UserProfile()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_profile_pb2.UserProfile()