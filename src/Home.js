import Euclidean from "./Euclidean.png"
import { useNavigate } from "react-router-dom";

const Home = () => {
    const navigate = useNavigate();
    const handleClick = () => {
        navigate("/create", { replace: true });
    };
    return (  
        <div className = "Home">
            <div className="row">
                <div className="desc">
                    <h2 className="whatwedo">ABOUT EXPANDIFY</h2>
                    <div className="elements">
                        <div className="element1">
                            <h3>Song Recommendations</h3>
                            <p>We generate a playlist of 20 songs based on a submission of a target song.</p>
                        </div>
                        <div className="element2">
                            <h3>Song Vectorization</h3>
                            <p>We vectorize songs on Spotify by the Spotify API listed audio features.</p>
                        </div>
                        <div className="element3">
                            <h3>Euclidean Distance</h3>
                            <p>We then find the songs with the smallest vector distance to the target song.</p>
                        </div>
                        <div className="element 4">
                            <h3>Playlist Generation</h3>
                            <p>We build a playlist that factors in euclidean distance as well as genre similarity.</p>
                        </div>
                    </div>
                </div>
                <img src={Euclidean} className = "Euclidean" alt = "Vector Graph Based on Song Components"/>
            </div>
            <div className="content2">
                <button onClick = {handleClick}> Generate a New Playlist </button>
            </div>
        </div>
    );
}
 
export default Home;