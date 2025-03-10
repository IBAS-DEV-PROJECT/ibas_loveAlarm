import React, { createContext, useContext, useState } from 'react';

const AnswersContext = createContext(null);

export const AnswersProvider = ({ children }) => {
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <AnswersContext.Provider
      value={{ answers, setAnswers, result, setResult, loading, setLoading }}
    >
      {children}
    </AnswersContext.Provider>
  );
};

export const useAnswers = () => {
  const context = useContext(AnswersContext);
  if (!context) {
    throw new Error('useAnswers must be used within an AnswersProvider');
  }
  return context;
};
