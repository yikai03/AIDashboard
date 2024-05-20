import React, { useState, useEffect } from 'react'
import Connections from '../components/DataIntegration/Connections'
import ConnectToDatabase from '../components/DataIntegration/ConnectToDatabase'

const DataIntegration = () => {
  const [connections, setConnections] = useState([])


  return (
    <div className="flex items-center ">
      <div className='container flex flex-col items-center border border-black p-4'>
        <h1 className='text-3xl font-bold'>Data Integration</h1>
        <ConnectToDatabase />
        {/* <h1>{connections.UniqueUserID}</h1> */}
        <Connections />
      </div>
    </div>
  )
}

export default DataIntegration