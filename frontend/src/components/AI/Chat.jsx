import React, {useState, useEffect, useRef} from 'react'
import TypingAnimation from './TypingAnimation'
import { GiHollowCat } from "react-icons/gi";
import SelectDatasetToTrain from './SelectDatasetToTrain';

const Chat = () => {
    const [inputValue, setInputValue] = useState('')
    const [chatLog, setChatLog] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [isGetting, setIsGetting] = useState(true)
    const chatContainerRef = useRef(null);

    const handleSubmit = (event) => {
        event.preventDefault();
    
        setChatLog((prevChatLog) => [...prevChatLog, { type: 'user', message: inputValue }])
    
        sendMessage(inputValue);
        
        setInputValue('');
    }

    const getHistoricalMessage = async() => {
        const url = "http://localhost:8000/chatbot"
        const response = await fetch(url)
        const data = await response.json()  
        return data
    }

    useEffect(() => {
        const fetchData = async () => {
            const data = await getHistoricalMessage();
            console.log(data)
            const formattedData = data.map(msg => ({ type: msg.role, message: msg.content }));
            setChatLog(formattedData);
            setIsGetting(false)
        };
    
        fetchData();
      }, []);

    const sendMessage = async (inputValue) => {
        const url = "http://localhost:8000/chatbot"
        setIsLoading(true)

        try{
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: inputValue})
                }
            )

            const data = await response.json()
            console.log(data)

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            setChatLog((prevChatLog) => [...prevChatLog, { type: 'AI', message: data}])
            setIsLoading(false)
        }
        catch (error) {
            setIsLoading(false)
            console.error('There was a problem with the fetch operation:', error);
        }
    }

  return (
    <>
    <div className="container mx-auto max-w">
      <div className="flex flex-col h-screen">
        <h1 className="bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text text-center py-3 font-bold text-6xl">TTGPT</h1>
        <div className="flex-grow p-6 overflow-auto" ref={chatContainerRef}>
            {isGetting ? 
            (
                <h2>Loading...</h2>
            ):(
                <div className="flex flex-col space-y-4">
                    {
                    chatLog.map((message, index) => (
                        <div key={index} className={`flex ${
                        message.type === 'user' ? 'justify-end' : 'justify-start'
                        }`}>
                            {message.type === 'AI' && <GiHollowCat className="mr-2 w-8 h-8 text-black bg-white rounded-full" />}
                            <div className={`${
                            message.type === 'user' ? 'bg-purple-500' : 'bg-gray-800'
                            } rounded-lg p-4 text-white max-w-sm`}>
                                {message.message}
                            </div>
                        </div>
                    ))
                    }
                    {
                    isLoading &&
                    <div key={chatLog.length} className="flex justify-start">   
                        <div className="bg-gray-800 rounded-lg p-4 text-white max-w-sm">
                            <TypingAnimation />
                        </div>
                    </div>
                    }       
                </div>
                )
            }             
        </div>
        <form className="flex-none p-6" onSubmit={handleSubmit}>
            <div className="flex justify-center rounded-lg border border-gray-700 bg-gray-200">  
                <SelectDatasetToTrain className={"text-3xl pl-2 pt-2"}/>
                <input type="text" className="flex-grow px-4 py-2 bg-transparent text-black focus:outline-none" placeholder="Type your message..." value={inputValue} onChange={(e) => setInputValue(e.target.value)}/>
                <button type="submit" className="bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg px-4 py-2 text-white font-semibold focus:outline-none hover:from-blue-600 hover:to-purple-600 transition-colors duration-300">Send</button>
            </div>
        </form>
        </div>
    </div>
    </>
  )
}

export default Chat