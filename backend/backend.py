from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from algo_temp import calculate_match_with_db, delete_user_from_db

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],               # 개발 시 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 매칭 API
@app.post("/api/match")
async def match(request: Request):
    user_data = await request.json()
    print(user_data)
    match_score, match_name, _ = calculate_match_with_db(user_data)
    return JSONResponse(content={
        "best_match": match_name,
        "score": match_score
    })

# DB 업데이트 api
@app.post("/api/update")
async def update_user(request: Request):
    answer_data = await request.json()
    delete_user_from_db(answer_data)
    return JSONResponse(content={"message": "User deleted successfully!"})

# backend.py
# @app.post("/api/update")
# async def update_user(request: Request):
#     data = await request.json()
#     success = delete_user_from_db(data.get("best_match_name"))
#     return {"success": success}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
