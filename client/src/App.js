import { useState } from "react";
import "./App.css";
import Dashboard from "./components/Dashboard";
import StockContext from "./context/StockContext";
import ThemeContext from "./context/ThemeContext";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [stockSymbol, setStockSymbol] = useState("MSFT");

  return (
    <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
      <StockContext.Provider value={{ stockSymbol, setStockSymbol }}>
        <Router>

          <Dashboard />
        </Router>
      </StockContext.Provider>
    </ThemeContext.Provider>
  );
}

export default App;