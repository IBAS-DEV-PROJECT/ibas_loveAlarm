import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AnswersProvider } from './context/AnswersContext.jsx';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AnswersProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AnswersProvider>
  </StrictMode>
);
