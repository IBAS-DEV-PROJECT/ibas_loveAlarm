import React from 'react';
import { StartButton, ResultButton } from '../../styles/common/ButtonStyle';

const Button = ({ type, children, ...props }) => {
  const ButtonComponent =
    {
      start: StartButton,
      result: ResultButton,
    }[type] || StartButton; // 기본값은 StartButton

  return <ButtonComponent {...props}>{children}</ButtonComponent>;
};

export default Button;
