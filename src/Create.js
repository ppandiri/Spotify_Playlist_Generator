import { useState } from "react";

const Create = () => {
    const [isPending, setIsPending] = useState(false);
    const [title, setTitle] = useState('');
   const handleSubmit = (e) => {
        setIsPending(true)
        console.log('new song submitted')
        setIsPending(false);
   }
    return ( 
        <div className="create">
            <h2>Enter a song:</h2> 
            <form onSubmit = {handleSubmit}>
            <input 
                type="text"
                required
                value={title}
                onChange = {(e) => setTitle(e.target.value)}
            />
            {!isPending && <button>Submit Song</button>}
            {isPending && <button disabled>Submitting blog...</button>}
            </form>
        </div>
    );
}
 
export default Create;