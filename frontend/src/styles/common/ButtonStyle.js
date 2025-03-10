import styled from 'styled-components';

export const StartButton = styled.button`
  width: 24rem;
  height: 3.5rem;
  font-size: ${({ theme }) => theme.fontSize.text.s};
  font-weight: 600;
  background-color: ${({ theme }) => theme.colors.white};
  color: ${({ theme }) => theme.colors.black};
  border: 1px solid ${({ theme }) => theme.colors.black};
  border-radius: 10px;
  box-shadow: 4px 6px 4px rgba(0, 0, 0, 0.25);
`;

export const ResultButton = styled.button`
  width: 24rem;
  height: 4.5rem;
  font-size: ${({ theme }) => theme.fontSize.text.m};
  font-weight: 600;
  background-color: ${({ theme }) => theme.colors.pink.circle};
  color: ${({ theme }) => theme.colors.white};
  border: 1px solid ${({ theme }) => theme.colors.white};
  border-radius: 10px;
  box-shadow: 4px 6px 4px rgba(0, 0, 0, 0.25);
  filter: ${({ isClicked }) => (isClicked ? 'none' : 'blur(4px)')};
`;
