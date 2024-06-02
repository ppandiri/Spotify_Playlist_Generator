import { Link } from 'react-router-dom';
import logo from './logo.png';

const Navbar = () => {
    return (  
        <nav className="navbar">
            <img src={logo} className="App-logo" alt="logo" />
            <div className="links">
                <Link to="/">HOME</Link>
                <Link to="/create">NEW PLAYLIST</Link>
            </div>
        </nav>
    );
}
 
export default Navbar;