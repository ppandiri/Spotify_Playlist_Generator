import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import logo from './logo.png';
import Create from './Create';

function App() {
  return (
    <Router>
    <div className="App">
      <title>
      <img src={logo} alt="logo" />
      Expandify
      </title>
      <Navbar />
      <div className="content">
        <Routes>
          <Route path="/" element = {<Home />} />
          <Route path="/create" element = {<Create />} />
        </Routes>
      </div>
    </div>
    </Router>
  );
}

export default App;
