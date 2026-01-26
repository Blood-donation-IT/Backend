import grpc
# from src.protos.user import user_profile_pb2_grpc, user_profile_pb2
from contracts.user import user_profile_pb2_grpc, user_profile_pb2
from src.application.use_cases.create_user import CreateUserUseCase
from src.application.use_cases.get_user_by_id import GetUserByIdUseCase
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

class UserProfileService(user_profile_pb2_grpc.UserProfileServiceServicer):
    def __init__(self,
                 create_user_profile_use_case: CreateUserUseCase,
                 get_user_by_id_use_case: GetUserByIdUseCase
                 )->None:
        self.create_user_profile_use_case: CreateUserUseCase = create_user_profile_use_case
        self.get_user_by_id_use_case: GetUserByIdUseCase = get_user_by_id_use_case
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
            
            ts =Timestamp()
            return user_profile_pb2.UserProfile(
                user_id=user.id,
                full_name=user.full_name,
                email=user.email,
                blood_type=user.blood_type,
                is_verified=user.is_verified,
                total_donations=user.total_donations,
                last_donation_at=ts.FromDatetime(user.last_donation_at) if user.last_donation_at else None,
                roles=map_roles_to_enum(user.roles),
                is_banned=user.is_banned,
                updated_at=ts.FromDatetime(user.updated_at) if user.updated_at else None,
                is_active=user.is_active,
                created_at=ts.FromDatetime(user.created_at) if user.created_at else None
            )
        except ValueError as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                if request.user_id > 0:
                    try:
                        existing_user = await self.get_user_by_id_use_case.execute(request.user_id)
                        ts = Timestamp()
                        return user_profile_pb2.UserProfile(
                            user_id=existing_user.id,
                            full_name=existing_user.full_name,
                            email=existing_user.email,
                            blood_type=existing_user.blood_type,
                            is_verified=existing_user.is_verified,
                            total_donations=existing_user.total_donations,
                            last_donation_at=ts.FromDatetime(existing_user.last_donation_at) if existing_user.last_donation_at else None,
                            roles=map_roles_to_enum(existing_user.roles),
                            is_banned=existing_user.is_banned,
                            updated_at=ts.FromDatetime(existing_user.updated_at) if existing_user.updated_at else None,
                            is_active=existing_user.is_active,
                            created_at=ts.FromDatetime(existing_user.created_at) if existing_user.created_at else None
                        )
                    except Exception:
                        pass
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return user_profile_pb2.UserProfile()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_profile_pb2.UserProfile()
    
    async def GetProfileById(self,
                            request: user_profile_pb2.GetProfileRequestById,
                            context: grpc.aio.ServicerContext
                            ) -> user_profile_pb2.UserProfile:
        try:
            user: User = await self.get_user_by_id_use_case.execute(request.user_id)
            ts = Timestamp()
            return user_profile_pb2.UserProfile(
                user_id=user.id,
                full_name=user.full_name,
                email=user.email,
                blood_type=user.blood_type,
                is_verified=user.is_verified,
                total_donations=user.total_donations,
                last_donation_at=ts.FromDatetime(user.last_donation_at) if user.last_donation_at else None,
                roles=map_roles_to_enum(user.roles),
                is_banned=user.is_banned,
                updated_at=ts.FromDatetime(user.updated_at) if user.updated_at else None,
                is_active=user.is_active,
                created_at=ts.FromDatetime(user.created_at) if user.created_at else None
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_profile_pb2.UserProfile()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_profile_pb2.UserProfile()