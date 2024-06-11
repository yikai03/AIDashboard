import React, {useState} from 'react'
import { MdKeyboardArrowRight, MdKeyboardArrowDown } from "react-icons/md";
import '../../design/text-animation.css'

const ConnectToDatabase = () => {
  const [driver, setDriver] = useState('')
  const [server, setServer] = useState('')
  const [database, setDatabase] = useState('')
  const [isExpanded, setIsExpanded] = useState(false)

  const connect = async() => {
    const url = "http://localhost:8000/sql-connection"
    try{
      const response = await fetch(url,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({Driver: driver, Server: server, Database: database})
        })
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json()
      console.log(data)
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }


  return (
    <div className="flex flex-col w-3/4 items-center pb-2">
      <button className=' hover:underline text-color-animation text-color-animation-hover' onClick={() => setIsExpanded(!isExpanded)}>

        <h1 className={`text-2xl pt-3 flex items-center ${isExpanded ? 'text-black':''}`}>
          {isExpanded ? <MdKeyboardArrowDown className='mt-1'/> : <MdKeyboardArrowRight className='mt-1' />}
          Connect to Database 
        </h1>
      </button>

      <div className={`overflow-hidden transition-all duration-[600ms] ease-in-out flex flex-col items-center ${isExpanded ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0' }`}>
        <div className="flex flex-col pb-4 mt-4">
          <label className="text-xl w-64">Driver</label>
          <input type="text" 
          className="border border-black p-2 text-black focus:ring focus:outline-none focus:border-blue-400 focus:ring-blue-400"
          placeholder='Example: SQL Server' 
          value={driver} 
          onChange={(e) => setDriver(e.target.value)} />

          <label className="text-xl">Server</label>
          <input type="text" 
          className="border border-black p-2 text-black focus:ring focus:outline-none focus:border-blue-400 focus:ring-blue-400" 
          placeholder='Example: DESKTOP-OP58T1G' 
          value={server} 
          onChange={(e) => setServer(e.target.value)} />

          <label className="text-xl">Database</label>
          <input type="text" 
          className="border border-black p-2 text-black focus:ring focus:outline-none focus:border-blue-400 focus:ring-blue-400" 
          placeholder='Example: Sales_DB' 
          value={database} 
          onChange={(e) => setDatabase(e.target.value)} />

          <button className="bg-blue-500 rounded text-white p-2 mt-2 hover:bg-blue-600" onClick={connect}>Connect</button>
        </div>
      </div>

    </div>
  )
}

export default ConnectToDatabase