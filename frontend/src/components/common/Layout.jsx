import styled from 'styled-components';

// components
import Header from '../common/Header';

// styles
import FlexBox from '../../styles/common/FlexStyle';

const StyledLayout = styled(FlexBox)`
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 0;
  background-color: ${({ theme }) => theme.colors.background};
`;

const Layout = ({ children, ...props }) => {
  return (
    <StyledLayout dir="col" row="center" col="center" {...props}>
      <Header />
      {children}
    </StyledLayout>
  );
};

export default Layout;
