import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import ReactGA from 'react-ga';
import Main from './app/views/Main';
import './index.css';
import * as serviceWorker from './serviceWorker';

ReactGA.initialize('UA-120460450-1');

if (process.env.NODE_ENV !== 'production') {
  ReactGA.set({ debug: true });
}

const logPageView = () => {
  ReactGA.set({ page: window.location.pathname });
  ReactGA.pageview(window.location.pathname);
};

axios.defaults.baseURL = `${process.env.REACT_APP_API_HOST}`;

ReactDOM.render(<Main onUpdate={logPageView} />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
