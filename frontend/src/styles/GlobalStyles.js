import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Dongle", sans-serif;
  }

  button {
    background: none;
    border: none;
    cursor: pointer;
  }

  .dongle-light {
    font-family: "Dongle", sans-serif;
    font-weight: 300;
    font-style: normal;
}

  .dongle-regular {
    font-family: "Dongle", sans-serif;
    font-weight: 400;
    font-style: normal;
  }

  .dongle-bold {
    font-family: "Dongle", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
`;

export default GlobalStyles;
