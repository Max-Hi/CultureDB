'use client'
// pages/page.tsx
import React, { useState } from 'react';

interface SearchResult {
  location: string;
  datetime: string;
  webpage: string;
  title: string;
  price: string;
}

const Page = () => {
  const [formData, setFormData] = useState({
    where: '',
    when: '',
    priceRange: '',
    type: '',
    author: '',
    title: ''
  });

  const [results, setResults] = useState<SearchResult[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSearch = async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    const data = await response.json();
    console.log(data) //setResults(data);
  };

  const createCalendarLink = (event: any, type: string) => {
    const base = type === 'google' 
      ? 'https://www.google.com/calendar/render?action=TEMPLATE'
      : 'https://calendar.apple.com/?action=TEMPLATE';

    const params = new URLSearchParams({
      text: event.title,
      dates: event.datetime,
      location: event.location,
      details: event.webpage,
    });

    return `${base}&${params.toString()}`;
  };

  return (
    <div>
      <div>
        <label>
          Where?
          <input type="text" name="where" value={formData.where} onChange={handleChange} />
        </label>
        <label>
          When?
          <input type="text" name="when" value={formData.when} onChange={handleChange} />
        </label>
        <label>
          Price Range
          <input type="text" name="priceRange" value={formData.priceRange} onChange={handleChange} />
        </label>
        <label>
          Type
          <input type="text" name="type" value={formData.type} onChange={handleChange} />
        </label>
        <label>
          Author
          <input type="text" name="author" value={formData.author} onChange={handleChange} />
        </label>
        <label>
          Title
          <input type="text" name="title" value={formData.title} onChange={handleChange} />
        </label>
      </div>
      <button onClick={handleSearch}>Search</button>
      <div>
        {results.map((result, index) => (
          <div key={index}>
            <h3>{result.title}</h3>
            <p>Location: {result.location}</p>
            <p>Date and Time: {result.datetime}</p>
            <p>Price: {result.price}</p>
            <a href={result.webpage} target="_blank" rel="noopener noreferrer">Webpage</a>
            <br />
            <a href={createCalendarLink(result, 'google')} target="_blank" rel="noopener noreferrer">Add to Google Calendar</a>
            <br />
            <a href={createCalendarLink(result, 'apple')} target="_blank" rel="noopener noreferrer">Add to Apple Calendar</a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Page;
