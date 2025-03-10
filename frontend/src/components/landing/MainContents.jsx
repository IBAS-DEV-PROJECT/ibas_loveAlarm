import React from 'react';

// components
import Poster from './Poster';

// styles
import FlexBox from '../../styles/common/FlexStyle';
import { Title } from '../../styles/common/TextStyle';

const MainContents = () => {
  return (
    <FlexBox width="100%" dir="col" col="center">
      <Title>좋아하면 울리는</Title>
      <Poster />
    </FlexBox>
  );
};

export default MainContents;
