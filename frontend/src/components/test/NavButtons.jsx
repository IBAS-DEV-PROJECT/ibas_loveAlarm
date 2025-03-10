import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { useAnswers } from '../../context/AnswersContext';

// styles
import { FlexBox } from '../../styles/common/FlexStyle';

const NavButtonContainer = styled(FlexBox)`
  width: 40.5rem;
`;

const Button = styled.button`
  width: 19.5rem;
  height: 3.5rem;
  font-size: ${({ theme }) => theme.fontSize.text.l};
  cursor: pointer;
  border: 1px solid ${({ theme }) => theme.colors.gray.dark};
  border-radius: 10px;
  background: ${({ disabled, isPrev, theme }) =>
    disabled ? theme.colors.white : isPrev ? '#D3D3D3' : theme.colors.pink.next};
  color: ${({ disabled, isPrev, theme }) =>
    disabled ? theme.colors.black : isPrev ? theme.colors.black : theme.colors.white};
  transition: background 0.3s, color 0.3s;

  &:hover {
    background: ${({ disabled, isPrev, theme }) =>
      disabled ? theme.colors.white : isPrev ? '#D3D3D3' : theme.colors.pink.next};
  }

  &:disabled {
    cursor: not-allowed;
  }
`;

const NavButtons = ({ currentIndex, setCurrentIndex, questions, answers }) => {
  const navigate = useNavigate();
  const { setResult, setLoading } = useAnswers();

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = async () => {
    console.log('최종', answers);
    setLoading(true);

    const startTime = Date.now();

    try {
      const submitResponse = await fetch('http://0.0.0.0:8000/api/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(answers),
      });

      if (!submitResponse.ok) {
        throw new Error('Failed to submit answers');
      }

      const submitData = await submitResponse.json();
      console.log('✅ /api/submit 응답:', submitData);

      // 👉 insta_id와 score 받아오기
      const { best_match, score } = submitData;
      console.log('인스타:', best_match, '점수:', score);

      // result 상태로 저장
      setResult({ best_match, score });

      const elapsedTime = Date.now() - startTime;
      const minLoadingTime = 3000;
      if (elapsedTime < minLoadingTime) {
        await new Promise((resolve) => setTimeout(resolve, minLoadingTime - elapsedTime));
      }

      navigate('/result');
    } catch (error) {
      console.error('제출 중 오류 발생:', error);
      alert('제출 중 오류가 발생했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  const isAnswerSelected =
    answers[questions[currentIndex].key] !== undefined &&
    answers[questions[currentIndex].key] !== '';

  return (
    <NavButtonContainer row="between">
      <Button onClick={handlePrev} disabled={currentIndex === 0} isPrev={true}>
        이전
      </Button>
      <Button
        onClick={currentIndex < questions.length - 1 ? handleNext : handleSubmit}
        disabled={!isAnswerSelected}
      >
        {currentIndex < questions.length - 1 ? '다음' : '완료'}
      </Button>
    </NavButtonContainer>
  );
};

export default NavButtons;
