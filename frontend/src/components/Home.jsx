import React, { useState } from "react";

const PhraseInputForm = () => {
  const [phrase, setPhrase] = useState("");
  const [sentiment, setSentiment] = useState("");

  const handleInputChange = (event) => {
    setPhrase(event.target.value);
  };

  const sendPhraseToServer = (phrase) => {
    // Send the phrase to the server using fetch or any other method you prefer
    fetch("http://localhost:5000/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phrase }),
    })
      .then((response) => response.json())
      .then((data) => {
        setSentiment(data.sentiment);
        console.log("Server response:", data);
      })
      .catch((error) => {
        console.error("Error sending phrase to server:", error);
      });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Send the phrase to the server
    sendPhraseToServer(phrase);
  };

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        className="p-5 mt-40 flex flex-col items-center bg-blue-950 rounded-2xl">
        <label className="font-mono text-lg text-gray-400">
          Enter a phrase :
          <input
            className="ml-4 bg-slate-500 rounded-lg md:w-96"
            type="text"
            value={phrase}
            onChange={handleInputChange}
          />
        </label>
        <button
          type="submit"
          className="font-mono mt-4 px-3 py-1 rounded-lg text-blue-400 bg-black hover:bg-slate-900 duration-150 hover:scale-105 w-fit">
          Submit
        </button>
        <div className="text-white pt-3 ">
          The phrase inputed is {sentiment}
        </div>
      </form>
    </div>
  );
};

const Home = () => {
  return (
    <div className="bg-slate-950 h-screen w-full flex flex-col items-center ">
      <h1 className="px-3 py-2 text-blue-400 cursor-pointer hover:text-blue-700 duration-200 font-mono rounded-lg mt-9">
        Positive or Negative? Get Instant Sentiment Analysis for Text
      </h1>

      <PhraseInputForm />
    </div>
  );
};

export default Home;
