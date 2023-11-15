import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSummarizeClick = async () => {
    setIsLoading(true);
    setError('');
    try {
      const response = await fetch('http://127.0.0.1:5000/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (response.ok) {
        const jsonResponse = await response.json();
        setSummary(jsonResponse.summary);
      } else {
        setError('Failed to get the summary.');
      }
    } catch (error) {
      setError('An error occurred while summarizing.');
      console.error('Summarization error:', error);
    }
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Summarize it for me</h1>
        <input
          value={inputText}
          className="input-field"  // Add this line
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter article to summarize"
        />
        <button className='summarize-button' onClick={handleSummarizeClick} disabled={isLoading}>
          {isLoading ? 'Summarizing...' : 'Summarize it'}
        </button>
        {error && <p className="error">{error}</p>}
        {summary && <div className="summary-box">{summary}</div>}
      </header>
    </div>
  );
}

export default App;
