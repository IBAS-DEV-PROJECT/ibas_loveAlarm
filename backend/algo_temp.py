import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# JSON 파일 경로 설정
file_path = "/Users/haewon/Desktop/new_ibas/backend/cleaned_output_3_converted.json"

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json_data(data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def delete_user_from_db(best_match_name):
    try:
        data = read_json(file_path)
        data = [user for user in data if user["instagram_id"] != best_match_name]
        save_json_data(data)
        print(f"{best_match_name} 삭제 완료!")
        return True
    except Exception as e:
        print(f"JSON 업데이트 중 오류 발생: {str(e)}")
        return False

def encode_single_response(question_idx, answer):
    answer = int(answer)  # 문자열 데이터를 정수로 변환
    if question_idx in [3, 6]:
        vec = np.zeros(4, dtype=int)
        if 1 <= answer <= 4:
            vec[answer - 1] = 1
        return vec
    else:
        return np.array([0]) if answer == 1 else np.array([1])

def encode_all_responses(responses):
    responses = [int(ans) for ans in responses if isinstance(ans, (int, float))]
    encoded_list = [encode_single_response(q_idx, ans) for q_idx, ans in enumerate(responses)]
    return np.concatenate(encoded_list)

def scale_encoded_vectors_for_cosine(encoded_matrix, question_weights):
    encoded_matrix = encoded_matrix.astype(float)
    w_sqrt = np.sqrt(question_weights)
    encoded_matrix[:, :3] *= w_sqrt[:3]
    encoded_matrix[:, 3:7] *= w_sqrt[3]
    encoded_matrix[:, 7] *= w_sqrt[4]
    encoded_matrix[:, 8] *= w_sqrt[5]
    encoded_matrix[:, 9:13] *= w_sqrt[6]
    encoded_matrix[:, 13] *= w_sqrt[7]
    encoded_matrix[:, 14] *= w_sqrt[8]
    return encoded_matrix

def calculate_match_with_db(user_data):
    candidates = read_json(file_path)
    user_gender = user_data.get("gender")
    
    valid_candidates = []

    for c in candidates:
        if c['gender'] != user_gender:
            valid_candidates.append(c)
            print(c['gender'])


    if len(valid_candidates) == 0:
        print("❌ 매칭할 반대 성별 후보가 없습니다.")
        return 0.0, "No Match", []
    
    # 사용자 응답: 인스타그램 아이디를 제외한 값들을 순서대로 인코딩
    user_vec = encode_all_responses(list(user_data.values())[1:])
    
    candidate_vecs = np.array([
        encode_all_responses(list(c.values())[1:]) for c in valid_candidates
    ])
    
    # 사용자와 후보자 벡터 결합
    all_vectors = np.vstack([user_vec, candidate_vecs])
    
    question_weights = np.array([1.0, 1.3, 5, 1.8, 1.4, 1.1, 1.7, 1.0, 1.0])
    scaled_matrix = scale_encoded_vectors_for_cosine(all_vectors.copy(), question_weights)
    
    sim_matrix = cosine_similarity(scaled_matrix)
    user_similarities = sim_matrix[0, 1:]
    
    # 동일한 최대 점수를 가진 후보가 여러 개일 경우 랜덤 선택
    max_score = np.max(user_similarities)
    top_candidate_indices = np.where(user_similarities == max_score)[0]
    top_candidate_idx = np.random.choice(top_candidate_indices)
    
    best_match_score = user_similarities[top_candidate_idx]
    best_match_name = valid_candidates[top_candidate_idx]["instagram_id"]
    
    return best_match_score, best_match_name, user_similarities

if __name__ == "__main__":
    test_user = {
        "instagram_id": "test_user",
        "gender": 1,  # 예를 들어, 남성은 1, 여성은 2
        "weekend_plan": 1,
        "fight_reaction": 1,
        "preferred_contact_frequency": 1,
        "allow_opposite_gender_friends": 1,
        "opposite_gender_meal_drink": 3,
        "date_course": 1,
        "team_project_stress": 1,
        "music_taste": 2
    }

    match_score, match_name, _ = calculate_match_with_db(test_user)
    print(f"매칭된 사용자: {match_name} (점수: {match_score})")