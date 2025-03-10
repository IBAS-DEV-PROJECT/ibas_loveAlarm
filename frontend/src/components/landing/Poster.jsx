import React from 'react';
import styled from 'styled-components';

// asssets
import HeartImg from '../../assets/images/heart.png';

// styles
import FlexBox from '../../styles/common/FlexStyle';
import { Img } from '../../styles/common/ImgStyle';
import { Body2 } from '../../styles/common/TextStyle';

const TargetWrapper = styled.div`
  position: relative;
  width: 248px;
  height: 248px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Circle = styled.div`
  position: absolute;
  border: 5px solid ${({ theme }) => theme.colors.pink.circle};
  border-radius: 50%;
`;

const InnerCircle = styled(Circle)`
  width: 112px;
  height: 112px;
`;

const MiddleCircle = styled(Circle)`
  width: 148px;
  height: 148px;
`;

const OuterCircle = styled(Circle)`
  width: 184px;
  height: 184px;
`;

const LargestCircle = styled(Circle)`
  width: 216px;
  height: 216px;
`;

const Poster = () => {
  return (
    <FlexBox dir="col" col="center">
      <TargetWrapper>
        <LargestCircle />
        <OuterCircle />
        <MiddleCircle />
        <InnerCircle />
        <Img src={HeartImg} width="64px" />
      </TargetWrapper>

      <Body2>당신의 데이터 속에 당신의 이상형이 있습니다.</Body2>
    </FlexBox>
  );
};

export default Poster;
