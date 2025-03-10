import React from 'react';

// assets
import BannerImg from '../../assets/images/banner.png';

// styles
import { Img } from '../../styles/common/ImgStyle';
import FlexBox from '../../styles/common/FlexStyle';

const Banner = () => {
  return (
    <FlexBox col="end" height="15.5rem">
      <Img
        src={BannerImg}
        width="100%"
        border="1px solid ${({ theme }) => theme.colors.gray.light}"
      />
    </FlexBox>
  );
};

export default Banner;
