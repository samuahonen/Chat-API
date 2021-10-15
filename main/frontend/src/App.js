import './App.css';
import axios from 'axios';
import React, { useState,useEffect, useCallback } from 'react';

function App() {
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/test").then((response) => {
      console.log(response.data)
    })
  },[])
  return (
    <div className="App">
      test
    </div>
  );
}

export default App;
