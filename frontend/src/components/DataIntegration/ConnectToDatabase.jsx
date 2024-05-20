import React, {useState} from 'react'

const ConnectToDatabase = () => {
  const [driver, setDriver] = useState('')
  const [server, setServer] = useState('')
  const [database, setDatabase] = useState('')

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
      <h1 className="text-2xl pt-3">Connect to Database</h1>
      <div className="flex flex-col pl-4 pr-4 pb-4 mt-4">
        <label className="text-xl w-64">Driver</label>
        <input type="text" className="border border-black p-2" value={driver} onChange={(e) => setDriver(e.target.value)} />
        <label className="text-xl">Server</label>
        <input type="text" className="border border-black p-2" value={server} onChange={(e) => setServer(e.target.value)} />
        <label className="text-xl">Database</label>
        <input type="text" className="border border-black p-2" value={database} onChange={(e) => setDatabase(e.target.value)} />
        <button className="bg-blue-500 rounded text-white p-2 mt-2" onClick={connect}>Connect</button>
      </div>
    </div>
  )
}

export default ConnectToDatabase