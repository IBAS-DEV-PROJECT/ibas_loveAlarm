import React from 'react';
import styled from 'styled-components';

// components
import ProgressBar from './ProgressBar';

// styles
import FlexBox from '../../styles/common/FlexStyle';

const Question = styled.p`
  font-size: ${({ size, theme }) => {
    const [category, level] = size.split('.');
    return theme.fontSize?.[category]?.[level] || theme.fontSize.q.m;
  }};

  font-weight: 700;
  color: ${({ theme }) => theme.colors.black};
`;

const SelectContainer = styled.div`
  display: ${({ layout }) => (layout === 'grid' ? 'grid' : 'flex')};
  grid-template-columns: ${({ layout }) => (layout === 'grid' ? '1fr 1fr' : 'none')};
  flex-direction: ${({ layout }) => (layout === 'col' ? 'column' : 'row')};
  gap: 10px;
`;

const InputField = styled.input`
  width: 24.75rem;
  height: 3.5rem;
  padding: 10px;
  font-size: ${({ theme }) => theme.fontSize.text.m};
  border: 3px solid ${({ theme }) => theme.colors.gray.light};
  border-radius: 5px;
  outline: none;

  &:focus {
    border-color: ${({ theme }) => theme.colors.pink.next};
  }
`;

const OptionButton = styled.button`
  width: ${({ buttonWidth }) => buttonWidth};
  background: ${({ selected, theme }) => (selected ? theme.colors.pink.dark : theme.colors.white)};
  color: ${({ selected, theme }) => (selected ? theme.colors.white : theme.colors.black)};
  border: 2px solid
    ${({ selected, theme }) => (selected ? theme.colors.pink.light : theme.colors.gray.light)};
  padding: 10px 0 10px 0;
  margin: 5px;
  cursor: pointer;
  border-radius: 10px;

  font-size: ${({ fontSize, theme }) => {
    const [category, level] = fontSize.split('.');
    return theme.fontSize?.[category]?.[level] || theme.fontSize.q.m;
  }};

  transition: all 0.3s ease-in-out;

  &:hover {
    background: ${({ theme }) => theme.colors.pink.dark};
    color: white;
  }
`;

const TestField = ({ question, answer, setAnswer, currentIndex, setCurrentIndex, questions }) => {
  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    const filteredValue = inputValue.replace(/[^a-z0-9!@#$%^&*()_+=\-{}\[\]:;"'<>,.?/|\\`~]/g, '');
    setAnswer(filteredValue);

    console.log(answer);
  };

  return (
    <FlexBox height="100%" dir="col" row="between" col="center" padding="2.5rem 0 2.5rem 0">
      {/* Progress Bar */}
      <FlexBox dir="col" row="between" col="center">
        <ProgressBar current={currentIndex} total={questions.length} />
      </FlexBox>

      {/* Question Field */}
      <Question size={question.style.size}>{question.question}</Question>

      {/* Answer Field */}
      {question.type === 'text' ? (
        <InputField
          type="text"
          placeholder={question.placeholder}
          value={answer}
          onChange={handleInputChange}
        />
      ) : (
        <SelectContainer
          count={question.options.length}
          questionId={question.id}
          layout={question.style.layout}
        >
          {question.options.map((option) => (
            <OptionButton
              fontSize={question.style.fontSize}
              buttonWidth={question.style.buttonWidth}
              key={option.value}
              // selected={answer === option.value}
              selected={answer[questions[currentIndex].key] === option.value}
              onClick={() => setAnswer(option.value)}
            >
              {option.label}
            </OptionButton>
          ))}
        </SelectContainer>
      )}
    </FlexBox>
  );
};

export default TestField;
