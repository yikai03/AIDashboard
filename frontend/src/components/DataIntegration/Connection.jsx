import React, {useEffect, useState} from 'react'
import {TfiReload} from "react-icons/tfi"
import { MdKeyboardArrowDown } from "react-icons/md";
import { LuSave } from "react-icons/lu";
import Table from './Table'
import {toast} from 'react-toastify'

const Connection = ({connection}) => {
    const [IsExpanded, setIsExpanded] = useState(false)
    const [IsReloaded, setIsReloaded] = useState(false)
    const [description, setDescription] = useState(connection.Description)
    const [sampleData, setSampleData] = useState([])

    const toggleExpand = () => {
        setIsExpanded(!IsExpanded)
        console.log("clicked")
    }

    useEffect(() => {
        toggleReload(connection.ConnectionID)
    }, [])

    const toggleReload = async(ConnectionID) => {
        // const url = `http://localhost:8000/sql-query-top?ID=${ConnectionID}`
        const url = "http://localhost:8000/sql-query-top"
        console.log(ConnectionID)
        // const info = {ID: ConnectionID}
        try{
            const response = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ID: ConnectionID})
            })
            if (!response.ok) {
                throw new Error('Network response was not ok');
              }
            
            const data = await response.json()
            console.log(data)
            setSampleData(data)
            setIsReloaded(!IsReloaded)
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const toggleSave = async(ConnectionID) => {
        const url = "http://localhost:8000/add-description"
        try{
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ID: ConnectionID, Description: description})
                }
            )
            const data = await response.json()
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            if(data.status == "success"){
                toast.success("Description saved successfully")       
                console.log("Description saved successfully")         
            }
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }

        console.log("saved")
    }


    //Await for desription

    //Await for passing SQL to get sample data

    //Await for connection status

    //Await for statistical analysis (if needed)

    //Await for manual select columns (if needed)

    return (
        <div className='w-3/4 drop-shadow-xl bg-white border border-black rounded mt-1 mb-2 '>

            <div className='flex flex-row align-middle justify-between'>        
                <div className='text-2xl ml-1 font-bold w-32'>{connection.Table}</div>
                <div className='text-2xl font-bold w-24'>{connection.ConnectionStatus}</div>

                <TfiReload className='text-2xl cursor-pointer self-center' onClick={() => toggleReload(connection.ConnectionID)}/>
                <MdKeyboardArrowDown className="text-2xl self-center cursor-pointer" onClick={toggleExpand} />
            </div>

            {IsExpanded && (
            <div className="p-2">
                    <label htmlFor="description" className='mr-2 text-1xl font-bold'>Description:</label>
                    <input className='border border-black rounded w-96' id="description" name="description" value={description} onChange={(e) => setDescription(e.target.value)}></input>
                    <LuSave className='cursor-pointer inline ml-2 text-2xl' onClick={() =>toggleSave(connection.ConnectionID)}/>
                    <Table sampleData={sampleData}/>

            </div>
            )}

        </div>
    )
}

export default Connection