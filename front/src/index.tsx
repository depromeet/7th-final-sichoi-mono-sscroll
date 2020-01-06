import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import Main from './app/views/Main';
import './index.css';
import * as serviceWorker from './serviceWorker';

if (process.env.NODE_ENV !== 'production') {
  axios.defaults.baseURL = `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_PORT}`;
} else {
  axios.defaults.baseURL =
    'http://ec2-15-164-215-195.ap-northeast-2.compute.amazonaws.com';
}

ReactDOM.render(<Main />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
