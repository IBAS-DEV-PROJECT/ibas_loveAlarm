import styled from 'styled-components';

export const Img = styled.img`
  width: ${({ width }) => width || 'fit-content'};
  height: ${({ height }) => height || 'fit-content'};

  border: ${({ border }) => border || 'none'};
`;
