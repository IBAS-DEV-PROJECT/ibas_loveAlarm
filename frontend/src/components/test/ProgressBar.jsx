import React from 'react';
import styled from 'styled-components';

const ProgressContainer = styled.div`
  width: 26rem;
  height: 0.75rem;
  background: ${({ theme }) => theme.colors.white};
  border-radius: 20px;
  margin: 10px 0;
`;

const ProgressFill = styled.div`
  width: ${({ width }) => width}%;
  height: 100%;
  background: ${({ theme }) => theme.colors.pink.dark};
  border-radius: 20px;
  transition: width 0.3s ease-in-out;
`;

const ProgressBar = ({ current, total }) => {
  const progressPercentage = ((current + 1) / total) * 100;

  return (
    <ProgressContainer id="progress-bar">
      <ProgressFill width={progressPercentage} />
    </ProgressContainer>
  );
};

export default ProgressBar;
