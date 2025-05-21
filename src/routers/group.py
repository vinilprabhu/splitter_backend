from fastapi import APIRouter, Depends, HTTPException
from src.models.group import Group
from src.models.user import User
from bson import ObjectId
from pydantic import BaseModel
from typing import List

from src.auth import get_current_user
from src.models.user import User as UserModel

router = APIRouter(prefix="/groups", tags=["Groups"])

class GroupCreate(BaseModel):
    name: str

@router.post("/", response_model=dict)
async def create_group(data: GroupCreate, user: User = Depends(get_current_user)):
    
    group = Group(
                name=data.name, 
                created_by=ObjectId(user['id']), 
                members=[ObjectId(user['id'])]
            )
    
    await group.insert()
    return {"id": str(group.id)}

@router.post("/{group_id}/add_member")
async def add_member(group_id: str, member_id: str, user: User = Depends(get_current_user)):
    
    group = await Group.get(ObjectId(group_id))

    print('group',group)
    print('user',user)
    
    if group is None or group.created_by != ObjectId(user['id']):
        raise HTTPException(status_code=403, detail="Unauthorized or not found")
    
    member = await UserModel.get(ObjectId(member_id))
    if member is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if ObjectId(member_id) not in group.members:
        group.members.append(ObjectId(member_id))
        await group.save()
        return {"message": "Member added"}
    else:
        raise HTTPException(status_code=400, detail="User already a member")

    

@router.get("/", response_model=List[dict])
async def get_all_groups(user: User = Depends(get_current_user)):
    groups = await Group.find({"members": ObjectId(user['id'])}).to_list(None)
    return [{"id": str(group.id), "name": group.name} for group in groups]

@router.get("/{group_id}", response_model=dict)
async def get_group_details(group_id: str, user: User = Depends(get_current_user)):
    group = await Group.get(ObjectId(group_id))
    if group is None or ObjectId(user['id']) not in group.members:
        raise HTTPException(status_code=404, detail="Group not found or access denied")

    members = []
    for member_id in group.members:
        member = await UserModel.get(member_id)
        if member:
            members.append({
                "id": str(member.id),
                "name": member.name,
                "email": member.email
            })
    return {
        "id": str(group.id),
        "name": group.name,
        "created_at": str(group.created_at),
        "members": members
    }
