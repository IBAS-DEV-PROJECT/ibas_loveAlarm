import React from 'react';
import styled, { keyframes } from 'styled-components';

// assets
import HeartImg from '../../assets/images/heart.png';

// styles
import { Img } from '../../styles/common/ImgStyle';
import FlexBox from '../../styles/common/FlexStyle';

const typing = keyframes`
  0% { width: 0;}
  100% { width: 110%;}
`;

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

const ResultTitle = styled.p`
  width: 0;
  opacity: 1;
  display: inline-block;
  font-size: 60px;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.black};
  overflow: hidden;
  white-space: nowrap;

  animation: ${typing} 5s steps(15, end) infinite;
`;

const CircleContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 29rem;
  height: 25.75rem;
  background: #00bcd4;
  border-radius: 12px;
  overflow: hidden;
`;

const Circle = styled.div`
  position: absolute;
  width: ${({ size }) => size}px;
  height: ${({ size }) => size}px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  animation: ${pulse} 2s infinite ease-in-out;
`;

const ScoreText = styled.p`
  font-size: ${({ theme }) => theme.fontSize.text.m};
  font-weight: 400;
  color: ${({ theme }) => theme.colors.pink.light};
`;

const ResultPoster = ({ score }) => {
  return (
    <FlexBox height="34.25rem" dir="col" row="between" col="center">
      <ResultTitle>누군가 당신의 좋알람을 울렸습니다.</ResultTitle>
      <CircleContainer>
        <Circle size={320} />
        <Circle size={240} />
        <Circle size={160} />

        <FlexBox dir="col" col="center">
          <ScoreText>{score}점</ScoreText>
          <Img width="76px" height="76px" src={HeartImg} />
        </FlexBox>
      </CircleContainer>
    </FlexBox>
  );
};

export default ResultPoster;
