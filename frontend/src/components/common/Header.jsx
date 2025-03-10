import React from 'react';
import styled from 'styled-components';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAnswers } from '../../context/AnswersContext';

// assets
import LogoImg from '../../assets/images/logo.png';

// styles
import { Img } from '../../styles/common/ImgStyle';
import FlexBox from '../../styles/common/FlexStyle';

const LogoWrapper = styled(FlexBox)`
  width: 48rem;
  height: fit-content;
  overflow: hidden;
  cursor: pointer;
  background-color: ${({ theme }) => theme.colors.pink.light};
`;

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { answers, result } = useAnswers();

  const handleClickLogoButton = async () => {
    console.log(result);
    if (location.pathname === '/result') {
      try {
        const response = await fetch('http://0.0.0.0:8000/api/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            best_match_name: result.best_match,
          }),
        });

        console.log('🔍 response.ok:', response.ok);
        console.log('🔍 response.status:', response.status);

        if (!response.ok) {
          throw new Error('DB 업데이트 실패 (HTTP 상태 오류)');
        }

        const data = await response.json();
        console.log('실제 데이터', data);

        if (data.message === 'User deleted successfully!') {
          console.log('✅ DB 업데이트 성공');
          navigate('/');
          window.location.reload();
        } else {
          throw new Error('DB 업데이트 실패 (응답 메시지 이상)');
        }
      } catch (error) {
        console.error('🚨 서버 오류:', error);
        alert('서버 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } else {
      window.open('https://www.inhabas.com/', '_blank');
    }
  };

  return (
    <LogoWrapper row="center">
      <Img src={LogoImg} width="17.375rem" height="5.75rem" onClick={handleClickLogoButton} />
    </LogoWrapper>
  );
};

export default Header;
