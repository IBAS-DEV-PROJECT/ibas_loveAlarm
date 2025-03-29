from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from algo_temp import calculate_match_with_db, delete_user_from_db, insert_user_to_db

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],               # 개발 시 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/match")
async def match(request: Request):
    user_data = await request.json()
    print("입력된 사용자 데이터:", user_data)
    
    # 사용자 데이터 DB에 추가 (이미 존재하는 경우에는 False가 반환됨)
    inserted = insert_user_to_db(user_data)
    if inserted:
        print("사용자 추가 성공!")
    else:
        print("사용자 추가 실패(이미 존재하거나 오류 발생)")
    
    # 매칭 수행
    match_score, match_name, _ = calculate_match_with_db(user_data)
    return JSONResponse(content={
        "best_match": match_name,
        "score": match_score
    })


# DB 업데이트 api
@app.post("/api/update")
async def update_user(request: Request):
    data = await request.json()
    best_match_name = data.get("best_match_name")
    if best_match_name:
        success = delete_user_from_db(best_match_name)
        return JSONResponse(content={"message": "User deleted successfully!" if success else "Deletion failed"})
    else:
        return JSONResponse(content={"message": "Invalid request data."}, status_code=400)


# backend.py
# @app.post("/api/update")
# async def update_user(request: Request):
#     data = await request.json()
#     success = delete_user_from_db(data.get("best_match_name"))
#     return {"success": success}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)