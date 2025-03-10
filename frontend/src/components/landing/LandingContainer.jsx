import React from 'react';

// components
import Container from '../common/Container';
import Banner from '../common/Banner';
import MainContents from './MainContents';
import ButtonField from './ButtonField';

const LandingContainer = () => {
  return (
    <Container>
      <Banner />
      <MainContents />
      <ButtonField />
    </Container>
  );
};

export default LandingContainer;
