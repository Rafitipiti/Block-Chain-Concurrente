import React from 'react';
import './myButton.scss';

type Color = 'white' | 'blue' | 'red';

type buttonProps = {
  text: string;
  color: Color;
  onClick: React.MouseEventHandler<HTMLButtonElement>;
};

const MyButton = (props: buttonProps) => {
  const { text, color, onClick } = props;

  const className = `button button--${color}`;

  return (
    <button type='button' className={className} onClick={onClick}>
      {text}
    </button>
  );
};

export default MyButton;
