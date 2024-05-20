import React, {useState, useEffect} from 'react'
import Connection from './Connection'

const Connections = () => {
  const [ConnectionsData, setConnections] = useState([])  

  //Take data from API
  useEffect(() => {
    const fetchConnections = async () => {
      const response = await fetch('http://localhost:8000/sql-connection')
      const data = await response.json()
      setConnections(data.Connection)
    }
    fetchConnections()
  },[])



  return (
    <>
    <h1 className='text-2xl'>Connected Table</h1>
    {ConnectionsData.map((connectionss) => (
      <Connection key={connectionss.ConnectionID} connection={connectionss}/>
    ))}
    </>
  )
}

export default Connections