import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import Theme from './styles/theme';
import GlobalStyles from './styles/GlobalStyles';
import { useAnswers } from './context/AnswersContext';

// import pages
import LandingPage from './pages/LandingPage';
import TestPage from './pages/TestPage';
import LoadingPage from './pages/LoadingPage';
import ResultPage from './pages/ResultPage';

function App() {
  const { loading } = useAnswers();

  return (
    <ThemeProvider theme={Theme}>
      <GlobalStyles />
      {loading && <LoadingPage />}

      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/test" element={<TestPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
