import React from 'react';
import styled from 'styled-components';
import FlexBox from '../../styles/common/FlexStyle';

const StyledContainer = styled(FlexBox)`
  width: 48rem;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.pink.light};
`;

const Container = ({ children, row = 'between', ...props }) => {
  return (
    <StyledContainer dir="col" row={row} col="center" {...props}>
      {children}
    </StyledContainer>
  );
};

export default Container;
