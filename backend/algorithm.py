import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
"""수정한 부분입니다"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data/data.csv")

def delete_user_from_db(best_match_name):
    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8")
        df = df[df["인스타그램 아이디"] != best_match_name]
        df.to_csv(DATA_PATH, index=False, encoding="utf-8")

        print(f"{best_match_name} 삭제 완료!")
        return True

    except Exception as e:
        print(f"CSV 업데이트 중 오류 발생: {str(e)}")
        return False

def encode_single_response(question_idx, answer):
    """
    question_idx:
      0, 1, 2 => 단일값(0 or 1)
      3, 6 => 4차원 one-hot
      나머지 => 단일값(0 or 1)
    """
    if question_idx == 3 or question_idx == 6:
        vec = np.zeros(4, dtype=int)
        if 1 <= answer <= 4:
            vec[answer - 1] = 1
        return vec
    else:
        # answer==1 -> [0], else [1]
        return np.array([0]) if answer == 1 else np.array([1])

def encode_all_responses(responses):
    encoded_list = []
    for q_idx, ans in enumerate(responses):
        encoded_vec = encode_single_response(q_idx, ans)
        encoded_list.append(encoded_vec)
    return np.concatenate(encoded_list)

def scale_encoded_vectors_for_cosine_9(encoded_matrix, question_weights):
    encoded_matrix = encoded_matrix.astype(float)  # ★ 핵심: float 변환

    w_sqrt = np.sqrt(question_weights)
    encoded_matrix[:, 0]    *= w_sqrt[0]
    encoded_matrix[:, 1]    *= w_sqrt[1]
    encoded_matrix[:, 2]    *= w_sqrt[2]
    encoded_matrix[:, 3:7]  *= w_sqrt[3]
    encoded_matrix[:, 7]    *= w_sqrt[4]
    encoded_matrix[:, 8]    *= w_sqrt[5]
    encoded_matrix[:, 9:13] *= w_sqrt[6]
    encoded_matrix[:, 13]   *= w_sqrt[7]
    encoded_matrix[:, 14]   *= w_sqrt[8]
    return encoded_matrix

def load_candidate_data(user_insta, csv_file='data/data.csv'):
    candidates = []
    candidate_names = []
    
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        for row in reader:
            if len(row) < 11:
                continue
            if row[1] == user_insta:
                continue
            
            candidate_names.append(row[1])
            candidate_answers = row[2:11]
            candidates.append(candidate_answers)

    print(candidate_names)
    return candidates, candidate_names


def calculate_match_with_db(user_data):
    mapping = {
        'gender': {'남성': 1, '여성': 2},
        'weekend_comment': {'맛집': 1, '휴식': 2},
        'conflict_response': {'정리 후 말하기': 1, '즉각 대화': 2},
        'contact_frequency': {'30분': 1, '1시간': 2, '2시간': 3, '상관없음': 4},
        'friend_party': {'절대 안됨': 1, '아는 사람은 괜찮다': 2, '이성친구와 밥/술자리': 3},
        'possible_party': {'짝 맞춘 술자리': 1, '단둘이': 2, '6명 이상': 3, '대규모': 4},
        'date_course': {'엑티비티': 1, '맛집/카페': 2, '영화관': 3, '집': 4},
        'team_comment': {'멘트1': 1, '멘트2': 2},
        'music_taste': {'힙합': 1, '발라드/R&B': 2, '밴드': 3, 'K-pop': 4}
    }

    responses = [
        mapping['gender'].get(user_data.get('gender'), 1),
        mapping['weekend_comment'].get(user_data.get('weekend_comment'), 1),
        mapping['conflict_response'].get(user_data.get('conflict_response'), 1),
        mapping['contact_frequency'].get(user_data.get('contact_frequency'), 1),
        mapping['friend_party'].get(user_data.get('friend_party'), 1),
        mapping['possible_party'].get(user_data.get('possible_party'), 1),
        mapping['date_course'].get(user_data.get('date_course'), 1),
        mapping['team_comment'].get(user_data.get('team_comment'), 1),
        mapping['music_taste'].get(user_data.get('music_taste'), 1),
    ]
    user_vec = encode_all_responses(responses)

    user_gender_str = user_data.get('gender', '남성')
    opposite_gender_str = '여성' if user_gender_str == '남성' else '남성'

    candidate_list, candidate_names = load_candidate_data(user_data.get("1"))

    filtered_candidates = []
    filtered_names = []
    for c_ans, c_name in zip(candidate_list, candidate_names):
        cand_gender_str = c_ans[0]
        if cand_gender_str == opposite_gender_str:
            filtered_candidates.append(c_ans)
            filtered_names.append(c_name)

    if not filtered_candidates:
        print("❌ 매칭할 이성 후보가 없습니다.")
        return 0.0, -1, "No Match", np.array([])

    converted_candidates = []
    for cand in filtered_candidates:
        cand_int = [
            mapping['gender'].get(cand[0], 1),
            mapping['weekend_comment'].get(cand[1], 1),
            mapping['conflict_response'].get(cand[2], 1),
            mapping['contact_frequency'].get(cand[3], 1),
            mapping['friend_party'].get(cand[4], 1),
            mapping['possible_party'].get(cand[5], 1),
            mapping['date_course'].get(cand[6], 1),
            mapping['team_comment'].get(cand[7], 1),
            mapping['music_taste'].get(cand[8], 1),
        ]
        converted_candidates.append(cand_int)

    candidate_vecs = [encode_all_responses(c) for c in converted_candidates]
    all_vectors = np.vstack([user_vec] + candidate_vecs)
    
    question_weights = np.array([1.0, 1.3, 1.5, 1.8, 1.2, 1.1, 1.7, 1.0, 1.0])
    scaled_matrix = scale_encoded_vectors_for_cosine_9(all_vectors.copy(), question_weights)
    
    sim_matrix = cosine_similarity(scaled_matrix)
    user_similarities = sim_matrix[0, 1:]
    best_match_idx = np.argmax(user_similarities)
    best_score = user_similarities[best_match_idx]
    best_match_name = filtered_names[best_match_idx]
    
    return best_score, best_match_idx, best_match_name, user_similarities

if __name__ == "__main__":
    print()
    test_user_data = {
        'gender': '남성',
        'weekend_comment': '맛집',
        'conflict_response': '정리 후 말하기',
        'contact_frequency': '30분',
        'friend_party': '절대 안됨',
        'possible_party': '짝 맞춘 술자리',
        'date_course': '영화관',
        'team_comment': '멘트1',
        'music_taste': '힙합'
    }

    score, idx, nm, sims = calculate_match_with_db(test_user_data)
    print("매칭 점수:", score)
    print("매칭 인덱스:", idx)
    print("매칭된 후보 이름:", nm)
    print("전체 유사도:", sims)
