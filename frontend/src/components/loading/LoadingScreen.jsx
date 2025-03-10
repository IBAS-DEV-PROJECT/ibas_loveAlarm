import React from 'react';
import styled, { keyframes } from 'styled-components';

// assets
import LockImg from '../../assets/images/lock.png';

// styles
import FlexBox from '../../styles/common/FlexStyle';
import { Img } from '../../styles/common/ImgStyle';

// 원형 애니메이션
const pulse = keyframes`
  0% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.6;
  }
  100% {
    transform: scale(1);
    opacity: 0.9;
  }
`;

// 배경 원 컨테이너
const Background = styled(FlexBox)`
  width: 100vw;
  height: 100vh;
  background: #000000;
  position: relative;
  overflow: hidden;
`;

// 원 스타일
const Circle = styled.div`
  position: absolute;
  width: ${({ size }) => size}px;
  height: ${({ size }) => size}px;
  border-radius: 50%;
  background: ${({ color }) => color};
  animation: ${pulse} 2s infinite ease-in-out;
`;

// 설명 텍스트
const Text = styled.p`
  color: white;
  font-size: 64px;
  text-align: center;
  margin-bottom: 30px;
  font-weight: 700;
  line-height: 1.4;
`;

const PinkCircle = styled.div`
  width: 120px;
  height: 120px;
  background: #e91e63;
  border-radius: 50%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  &::before {
    content: '';
    width: 100%;
    height: 100%;
    position: absolute;
    border-radius: 50%;
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.6);
    opacity: 0.6;
  }

  img {
    width: 60%;
    height: 60%;
    object-fit: contain;
  }
`;

const LoadingScreen = () => {
  return (
    <Background dir="col" row="center" col="center">
      <Text>매칭 중...</Text>

      {/* 배경 원 */}
      <Circle size={600} color="rgba(255, 255, 255, 0.2)" />
      <Circle size={500} color="rgba(255, 255, 255, 0.4)" />
      <Circle size={400} color="rgba(255, 255, 255, 0.6)" />

      {/* 하트 버튼 */}
      <PinkCircle>
        <Img src={LockImg} />
      </PinkCircle>
    </Background>
  );
};

export default LoadingScreen;
