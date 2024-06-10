import React, { useState, useEffect } from 'react'
import Connections from '../components/DataIntegration/Connections'
import ConnectToDatabase from '../components/DataIntegration/ConnectToDatabase'

const DataIntegration = () => {
  return (
    <div className="flex items-center justify-center">
      <div className='container flex flex-col justify-center items-center p-4 h-screen'>
        <div className='overflow-scroll overflow-x-hidden flex-grow '>
          <div className='flex flex-col justify-center items-center'>
            <h1 className='text-3xl font-bold'>Data Integration</h1>
            <ConnectToDatabase />
            {/* <h1>{connections.UniqueUserID}</h1> */}
            <Connections />
          </div>
        </div>
      </div>
    </div>
  )
}

export default DataIntegration