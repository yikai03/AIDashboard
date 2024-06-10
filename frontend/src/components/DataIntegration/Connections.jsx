import React, {useState, useEffect} from 'react'
import Connection from './Connection'
import CircleLoader from '../CircleLoader'
import { MdRefresh } from "react-icons/md";

const Connections = () => {
  const [ConnectionsData, setConnections] = useState([])  
  const [loading, setLoading] = useState(true)

  //Take data from API
  useEffect(() => {
    const fetchConnections = async () => {
      setLoading(true)
      const response = await fetch('http://localhost:8000/sql-connection')
      const data = await response.json()
      setConnections(data.Connection)
      setLoading(false)
    }
    fetchConnections()
  },[])

  const handleRefresh = async() => {
    setLoading(true)
    const response = await fetch("http://localhost:8000/sql-refresh")
    const data = await response.json()
    setConnections(data.Connection)
    setLoading(false)
  }

  return (
    <div className='w-3/4'>
      <div className='flex justify-between mb-2'>
        <h1 className='text-2xl'>Connected Table</h1>
        <button className=' self-center text-2xl hover:bg-gray-300 hover:rounded-md hover:ease-in-out hover:transition hover:duration-[500ms]' onClick={handleRefresh}>
          <MdRefresh/>
        </button>
      </div>
      <div className='flex flex-row items-center justify-center text-center'>
        <CircleLoader loading={loading}/> 
      </div>
      {      ConnectionsData.map((connectionss) => (
        <Connection key={connectionss.ConnectionID} connection={connectionss} opacity={loading ? 'opacity-0':'opacity-100'}/>
      ))} 
    </div>
  )
}

export default Connections