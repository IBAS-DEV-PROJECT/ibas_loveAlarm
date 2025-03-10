import styled from 'styled-components';

// 제목 (96px)
export const Title = styled.h1`
  font-size: ${({ theme }) => theme.fontSize.title};
  font-weight: 700;
  color: ${({ theme }) => theme.colors.black};
`;

// 본문 텍스트 (36px)
export const Body = styled.p`
  font-size: ${({ theme }) => theme.fontSize.text.m};
  font-weight: 400;
  color: ${({ theme }) => theme.colors.black};
`;

// 본문 텍스트 (32px)
export const Body2 = styled.p`
  font-size: ${({ theme }) => theme.fontSize.text.s};
  font-weight: 400;
  color: ${({ theme }) => theme.colors.black};
`;

// 해시태그 (24px)
export const Hastag = styled.p`
  font-size: ${({ theme }) => theme.fontSize.text.xs};
  font-weight: 400;
  color: ${({ theme }) => theme.colors.gray.light};
`;

// 부제목
export const SubTitle = styled.h2`
  font-size: ${({ theme }) => theme.fontSize.text.l};
  font-weight: 700;
  color: ${({ theme }) => theme.colors.black};
`;

export const Question = styled.p`
  font-size: ${({ theme }) => theme.fontSize.text.m};
  font-weight: 700;
  color: ${({ theme }) => theme.colors.black};
`;

// 작은 텍스트 (부가 설명 등)
export const Caption = styled.span`
  font-size: ${({ theme }) => theme.fontSize.text.xs};
  font-weight: 400;
  color: ${({ theme }) => theme.colors.gray.dark};
`;
