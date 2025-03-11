import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# JSON 파일 경로 설정
file_path = "c:/Users/xorkd/ibas_loveAlarm/ibas_loveAlarm/day3.json"

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # 헤더 항목(첫 번째 항목) 제거
    if data and isinstance(data[0], dict) and "instagram_id" in data[0]:
        first_item = data[0]
        # 첫 번째 항목의 값이 모두 문자열인지 확인
        if all(isinstance(val, str) for val in first_item.values()):
            # 첫 번째 항목이 헤더인 경우 제거
            data = data[1:]
            print("헤더 항목이 제거되었습니다.")
            
    return data

def save_json_data(data):
    # 원본 데이터 읽기 (헤더 보존을 위해)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(file)
            
        # 첫 번째 항목이 헤더인지 확인
        if original_data and isinstance(original_data[0], dict) and "instagram_id" in original_data[0]:
            first_item = original_data[0]
            if all(isinstance(val, str) for val in first_item.values()):
                # 헤더 항목 보존
                data = [first_item] + data
                print("헤더 항목이 보존되었습니다.")
    except Exception as e:
        print(f"원본 데이터 읽기 중 오류: {e}")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())

def insert_user_to_db(user_data):
    """
    새 사용자 데이터를 JSON 파일에 추가하는 함수
    """
    try:
        # 현재 데이터 읽기
        data = read_json(file_path)
        print(f"삽입 전 사용자 수: {len(data)}")
        
        # 같은 인스타그램 ID가 이미 존재하는지 확인
        instagram_id = user_data.get("instagram_id")
        if any(user.get("instagram_id") == instagram_id for user in data):
            print(f"⚠️ 이미 존재하는 인스타그램 ID입니다: {instagram_id}")
            return False
            
        # 데이터 추가
        data.append(user_data)
        print(f"삽입 후 사용자 수: {len(data)}")
        
        # 변경 사항 저장
        save_json_data(data)
        print(f"✅ {instagram_id} 추가 완료!")
        return True
        
    except Exception as e:
        print(f"JSON 업데이트 중 오류 발생: {str(e)}")
        return False

def delete_user_from_db(best_match_name):
    try:
        data = read_json(file_path)
        print(f"삭제 전 사용자 수: {len(data)}")
        data = [user for user in data if user["instagram_id"] != best_match_name]
        print(f"삭제 후 사용자 수: {len(data)}")
        save_json_data(data)
        print(f"{best_match_name} 삭제 완료!")
        return True
    except Exception as e:
        print(f"JSON 업데이트 중 오류 발생: {str(e)}")
        return False

def is_numeric(value):
    """
    값이 숫자로 변환 가능한지 확인
    """
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False

def safe_int(value, default=0):
    """
    안전하게 정수로 변환하는 함수
    """
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return default
    return default

def encode_single_response(question_idx, answer):
    answer = safe_int(answer, 0)
        
    if question_idx in [3, 6]:
        vec = np.zeros(4, dtype=int)
        if 1 <= answer <= 4:
            vec[answer - 1] = 1
        return vec
    else:
        return np.array([0]) if answer == 1 else np.array([1])

def encode_all_responses(responses):
    try:
        # 응답 목록이 비어있는 경우
        if not responses or len(responses) == 0:
            print("경고: 응답 목록이 비어있습니다. 기본 벡터 반환.")
            return np.zeros(15)
            
        # 숫자로 변환 가능한 값만 처리
        numeric_responses = []
        for resp in responses:
            if is_numeric(resp):
                numeric_responses.append(safe_int(resp))
            else:
                numeric_responses.append(0)
                
        # 필요한 수만큼 응답 추가
        while len(numeric_responses) < 9:
            numeric_responses.append(0)
            
        # 응답 인코딩
        encoded_list = []
        for i, resp in enumerate(numeric_responses[:9]):  # 첫 9개만 처리
            encoded_list.append(encode_single_response(i, resp))
            
        # 결과 연결
        if encoded_list:
            return np.concatenate(encoded_list)
        else:
            return np.zeros(15)
    except Exception as e:
        print(f"인코딩 중 오류: {e}")
        return np.zeros(15)

def scale_encoded_vectors_for_cosine(encoded_matrix, question_weights):
    try:
        encoded_matrix = encoded_matrix.astype(float)
        w_sqrt = np.sqrt(question_weights)
        
        # 행렬 크기 확인
        if encoded_matrix.shape[1] < 15:
            padding = np.zeros((encoded_matrix.shape[0], 15 - encoded_matrix.shape[1]))
            encoded_matrix = np.hstack((encoded_matrix, padding))
            
        encoded_matrix[:, :3] *= w_sqrt[:3]
        encoded_matrix[:, 3:7] *= w_sqrt[3]
        encoded_matrix[:, 7] *= w_sqrt[4]
        encoded_matrix[:, 8] *= w_sqrt[5]
        encoded_matrix[:, 9:13] *= w_sqrt[6]
        encoded_matrix[:, 13] *= w_sqrt[7]
        encoded_matrix[:, 14] *= w_sqrt[8]
        return encoded_matrix
    except Exception as e:
        print(f"스케일링 중 오류: {e}")
        return encoded_matrix

def calculate_match_with_db(user_data):
    candidates = read_json(file_path)
    user_gender = safe_int(user_data.get("gender"))
    
    print(f"사용자 성별: {user_gender}")
    
    valid_candidates = []
    
    for c in candidates:
        candidate_gender = safe_int(c.get('gender'))
        if candidate_gender != user_gender:
            valid_candidates.append(c)
            print(f"후보: {c.get('instagram_id')}, 성별: {candidate_gender}")
    
    if len(valid_candidates) == 0:
        print("❌ 매칭할 반대 성별 후보가 없습니다.")
        return 0.0, "No Match", []
    
    # user_data에서 값들만 추출
    user_values = []
    for key in ["gender", "weekend_plan", "fight_reaction", "preferred_contact_frequency", 
               "allow_opposite_gender_friends", "opposite_gender_meal_drink", 
               "date_course", "team_project_stress", "music_taste"]:
        if key in user_data:
            user_values.append(user_data[key])
        else:
            user_values.append(0)
    
    user_vec = encode_all_responses(user_values)
    
    # 유효한 후보들의 벡터 계산
    candidate_vecs_list = []
    filtered_candidates = []
    
    for c in valid_candidates:
        try:
            c_values = []
            for key in ["gender", "weekend_plan", "fight_reaction", "preferred_contact_frequency", 
                       "allow_opposite_gender_friends", "opposite_gender_meal_drink", 
                       "date_course", "team_project_stress", "music_taste"]:
                if key in c:
                    c_values.append(c[key])
                else:
                    c_values.append(0)
                    
            c_vec = encode_all_responses(c_values)
            candidate_vecs_list.append(c_vec)
            filtered_candidates.append(c)
        except Exception as e:
            print(f"후보 {c.get('instagram_id')} 처리 중 오류: {e}")
    
    if not candidate_vecs_list:
        print("처리할 수 있는 후보가 없습니다.")
        return 0.0, "No Match", []
    
    candidate_vecs = np.array(candidate_vecs_list)
    
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
    best_match_name = filtered_candidates[top_candidate_idx]["instagram_id"]
    
    return best_match_score, best_match_name, user_similarities

if __name__ == "__main__":
    # 파일 경로 확인
    print(f"사용 중인 파일 경로: {file_path}")
    if os.path.exists(file_path):
        print(f"파일이 존재합니다: {file_path}")
    else:
        print(f"파일이 존재하지 않습니다: {file_path}")
        
    # 새 사용자 데이터 추가 테스트
    new_user = {
        "instagram_id": "new_test_user3",  # 중복 방지를 위해 이름 변경
        "gender": 1,  # gender 값: 0 또는 1
        "weekend_plan": 2,
        "fight_reaction": 2,
        "preferred_contact_frequency": 2,
        "allow_opposite_gender_friends": 2,
        "opposite_gender_meal_drink": 2,
        "date_course": 2,
        "team_project_stress": 2,
        "music_taste": 2
    }
    
    print("\n=== 사용자 추가 테스트 ===")
    insert_result = insert_user_to_db(new_user)
    print(f"사용자 추가 결과: {'성공' if insert_result else '실패'}")
    
    # 매칭 테스트
    print("\n=== 매칭 테스트 ===")
    test_user = {
        "instagram_id": "test_user",
        "gender": 0,  # gender 값: 0 또는 1
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
    
    # 매칭된 사용자 삭제 테스트
    print("\n=== 사용자 삭제 테스트 ===")
    if match_name not in ["No Match", "Error"]:
        delete_result = delete_user_from_db(match_name)
        print(f"삭제 결과: {'성공' if delete_result else '실패'}")
        
        # 삭제 후 다시 매칭 시도
        print("\n삭제 후 다시 매칭 시도...")
        new_score, new_match, _ = calculate_match_with_db(test_user)
        print(f"새 매칭 결과: {new_match} (점수: {new_score})")