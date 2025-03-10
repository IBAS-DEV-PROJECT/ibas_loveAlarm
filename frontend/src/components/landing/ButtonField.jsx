import React from 'react';
import { useNavigate } from 'react-router-dom';

// components
import Button from '../common/Button';

// styles
import FlexBox from '../../styles/common/FlexStyle';
import { Hastag } from '../../styles/common/TextStyle';

const ButtonField = () => {
  const navigate = useNavigate();

  return (
    <FlexBox dir="col" row="between" col="center" height="14.5rem" padding="0 0 7rem 0">
      <FlexBox width="22.75rem" row="between">
        <Hastag>#여사친 / 남사친</Hastag>
        <Hastag>#CC</Hastag>
        <Hastag>#로맨틱</Hastag>
        <Hastag>#성공적</Hastag>
      </FlexBox>
      <Button type="start" onClick={() => navigate('/test')}>
        나랑 가까운 사람 찾으러 가기
      </Button>
    </FlexBox>
  );
};

export default ButtonField;
