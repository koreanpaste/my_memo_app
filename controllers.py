from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.templating import Jinja2Templates
from models import User,Memo
from schemas import UserCreate,UserLogin,MemoCreate,MemoUpdate
from dependencies import get_db,get_password_hash,verify_password_hash
from sqlalchemy.orm import Session

router=APIRouter()
templates= Jinja2Templates(directory="templates")

@router.post("/signup")
async def signup(signup_data:UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.username==signup_data.username).first()
    if existing_user is not None:
        raise HTTPException(status_code=404,detail="이미 동일 사용자 있음")
    hashed_password=get_password_hash(signup_data.password)
    new_user=User(username=signup_data.username,email=signup_data.email,hashed_password=hashed_password)
    db.add(new_user)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="회원가입 실패")
    
    db.refresh(new_user)
    return {"message":"Account Created successfully","user_id":new_user.id}

@router.post("/login")
async def login(request:Request,signin_data:UserLogin,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==signin_data.username).first()
    if user and verify_password_hash(signin_data.password,user.hashed_password):
        request.session["username"]=user.username
        return {"message":"logged in successfully"}
    else:
        raise HTTPException(status_code=401,detail="로그인 실패..")

@router.post('/logout') 
async def logout(request:Request):
    request.session.pop("username",None)
    return {"message":"Logged out successfully"}
   
@router.get('/')
async def read_root(request:Request):
    return templates.TemplateResponse('home.html',{"request":request})

@router.get('/about')
async def about():
    return {"message":"이것은 마이 메모앱의 소개 페이지입니다"}

@router.post("/memos/")
async def create_user(request:Request,memo:MemoCreate,db:Session=Depends(get_db)):
    username=request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401,detail="Not authorized")
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    new_memo=Memo(title=memo.title,content=memo.content,user_id=user.id)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return {"id":new_memo.id,"title":new_memo.title,"content":new_memo.content }

@router.put("/memos/{memo_id}")
async def updata_user(request:Request,memo_id:int,memo:MemoUpdate,db:Session=Depends(get_db)):
    username=request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401,detail="Not authorized")
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    db_memo=db.query(Memo).filter(Memo.id==memo_id,Memo.user_id==user.id).first()
    if db_memo is None:
        return {"error":"User not found"}
    if db_memo.title  is not None:
        db_memo.title=memo.title
    if db_memo.content is not None:
        db_memo.content=memo.content

    db.commit()
    db.refresh(db_memo)
    return {"id":db_memo.id,"title":db_memo.title,"content":db_memo.content}

@router.get("/memos/")
async def list_memos(request:Request,db:Session=Depends(get_db)):
    username = request.session.get("username")

    if username is None:
        raise HTTPException(status_code=401,detail="Not authorized")
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    memos =db.query(Memo).filter(Memo.user_id==user.id).all()
    return templates.TemplateResponse("memos.html",{"request":request,"memos":memos})

@router.delete("/memos/{memo_id}")
async def delete_user(request:Request,memo_id:int,db: Session=Depends(get_db)):
    username=request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401,detail="Not authorized")
    user=db.query(User).filter(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    db_memo=db.query(Memo).filter(Memo.id==memo_id,Memo.user_id==user.id).first()
    
    if db_memo is None:
        return {"error":"Not found"}
    db.delete(db_memo)
    db.commit()
    return {"message":"Memo deleted"}
